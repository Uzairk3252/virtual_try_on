// Selecting DOM elements
const scannerBtn = document.getElementById('scanner-btn');
const tryNowBtn = document.getElementById('try-now-btn');
const scannerModal = document.getElementById('scanner-modal');
const closeScanner = document.getElementById('close-scanner');
const video = document.getElementById('scanner-video');

// Open the camera modal when 'Scan' or 'Try Now' is clicked
const openCamera = async () => {
  try {
    scannerModal.style.display = 'flex';

    // Access the user's camera
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    video.play();
  } catch (err) {
    alert('Unable to access camera. Please check your permissions.');
    console.error(err);
  }
};

// Close the camera modal
const closeCamera = () => {
  scannerModal.style.display = 'none';

  // Stop the camera stream
  const stream = video.srcObject;
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach((track) => track.stop());
  }
  video.srcObject = null;
};

// Event listeners
scannerBtn.addEventListener('click', openCamera);
tryNowBtn.addEventListener('click', openCamera);
closeScanner.addEventListener('click', closeCamera);
