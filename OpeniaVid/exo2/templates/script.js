document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
  
    var formData = new FormData(this);
  
    var messageDiv = document.getElementById('message');
    messageDiv.innerHTML = 'Uploading video...';
  
    fetch('/upload/', {
      method: 'POST',
      body: formData
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      messageDiv.innerHTML = data.message;
    })
    .catch(function(error) {
      console.error(error);
      messageDiv.innerHTML = 'An error occurred.';
    });
  });
  