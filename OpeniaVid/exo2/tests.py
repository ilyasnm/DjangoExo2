from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os


class UploadVideoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_video')
        self.video_file = SimpleUploadedFile('video.mp4', b'mock video content', content_type='video/mp4')

    def tearDown(self):
        # Supprimer le fichier de vidéo temporaire
        if os.path.exists('video_temp.mp4'):
            os.remove('video_temp.mp4')
        # Supprimer le fichier de transcription temporaire
        if os.path.exists('transcription.txt'):
            os.remove('transcription.txt')

    def test_upload_video_success(self):
        response = self.client.post(self.upload_url, {'video': self.video_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Video telechargee et audio analyse avec succes.')

    def test_upload_video_invalid_format(self):
        invalid_video_file = SimpleUploadedFile('video.txt', b'mock video content', content_type='text/plain')
        response = self.client.post(self.upload_url, {'video': invalid_video_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Invalid video format.')

    def test_upload_video_exceeds_size_limit(self):
        large_video_file = SimpleUploadedFile('large_video.mp4', b'mock video content' * 1024 * 1024, content_type='video/mp4')
        response = self.client.post(self.upload_url, {'video': large_video_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Video file size exceeds the limit.')

    def test_upload_video_analyze_failure(self):
        # Faux contenu vidéo pour provoquer une erreur lors de l'analyse
        invalid_video_file = SimpleUploadedFile('invalid_video.mp4', b'invalid video content', content_type='video/mp4')
        response = self.client.post(self.upload_url, {'video': invalid_video_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Impossible analyser le son de la video.')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

