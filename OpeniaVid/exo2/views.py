from django.shortcuts import render
import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from .models import Video, VideoAnalysis
import openai
from django.utils import timezone
import subprocess
import os
from django.http import HttpResponseBadRequest, JsonResponse
import datetime


MAX_VIDEO_SIZE = 4 * 1024 * 1024  # 4 MB
openai.api_key = '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'


def analyze_video(video_content):
    # Étape 1: Enregistrer le contenu du fichier vidéo dans un fichier temporaire
    with open("video_temp.mp4", "wb") as file:
        file.write(video_content)

    # Étape 2: Vérifier le format du fichier vidéo
    allowed_formats = [".mp4", ".mpeg", ".m4a", ".webm"]
    file_extension = os.path.splitext("video_temp.mp4")[1]
    if file_extension.lower() not in allowed_formats:
        os.remove("video_temp.mp4")
        return HttpResponseBadRequest("Le format de fichier vidéo n'est pas pris en charge.")

    # Étape 3: Vérifier la taille du fichier vidéo
    file_size = os.path.getsize("video_temp.mp4")
    if file_size > MAX_VIDEO_SIZE:
        os.remove("video_temp.mp4")
        return HttpResponseBadRequest("La taille du fichier vidéo dépasse la limite autorisée.")

    # Étape 4: Extraire l'audio de la vidéo
    audio_filename = "audio_temp.wav"
    extract_audio_command = f'ffmpeg -i video_temp.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_filename}'
    os.system(extract_audio_command)

    # Étape 5: Appeler l'API Whisper pour transcrire l'audio
    with open(audio_filename, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)

    # Étape 6: Supprimer les fichiers temporaires
    os.remove("video_temp.mp4")
    os.remove(audio_filename)

    return response


@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        content_type = video_file.content_type
        file_size = video_file.size
        if not video_file:
            return JsonResponse({'message': 'Le fichier video est manquant.'}, status=400)
       
        # Vérifier le format du fichier vidéo
        valid_formats = ['video/mp4', 'video/mpeg', 'audio/mp4', 'video/webm']
        if content_type not in valid_formats:
           return JsonResponse({'message': 'Invalid video format.', 'content_type': content_type}, status=400)

        # Vérifier la taille du fichier vidéo
        if file_size > MAX_VIDEO_SIZE:
           return JsonResponse({'message': 'Video file size exceeds the limit.'}, status=400)
        
        # Traiter le fichier vidéo ici et extraire l'audio
        video_content = video_file.read()

        # Appeler la méthode analyze_video pour effectuer l'analyse de l'audio
        response = analyze_video(video_content)

        if "text" in response:
            
            # Récupérer la transcription de l'audio
            transcription = response["text"]
            
            # Enregistrer la transcription dans la base de données
            video = Video.objects.create(
                title=video_file.name,
                content=video_content,
                analysis_date=timezone.now(),
            )

            VideoAnalysis.objects.create(
                video=video,
                timestamp=timezone.now(),
                transcription=transcription,
            )
            
            output_file_path = 'transcription.txt'
            output_file_path_base = os.path.splitext(output_file_path)[0]  # Nom de base sans extension
            output_file_path_ext = os.path.splitext(output_file_path)[1]  # Extension du fichier
            
            #Vérifier si le fichier existe déjà
            if os.path.exists(output_file_path):
            # Trouver un nom de fichier disponible en ajoutant un suffixe numérique
              suffix_num = 1
            while os.path.exists(output_file_path):
             output_file_path = f"{output_file_path_base}_{suffix_num}{output_file_path_ext}"
             suffix_num += 1


           # Enregistrer la transcription dans un fichier texte
            with open(output_file_path, 'w') as output_file:
             output_file.write(transcription)

            return JsonResponse({'message': 'Video telechargee et audio analyse avec succes.'})
        else:
            return JsonResponse({'message': 'Impossible analyser le son de la video.'}, status=400)
    else:
        return JsonResponse({'message': 'Methode de requête invalide.'}, status=405)
