import { Heartbeat } from './heartbeat.js';

const OPENCV_URI = 'https://docs.opencv.org/master/opencv.js';
const HAARCASCADE_URI = 'haarcascade_frontalface_alt.xml';

const startButton = document.getElementById('start-demo');
const statusText = document.getElementById('status-text');
const visualizer = document.getElementById('visualizer');

const demo = new Heartbeat('webcam', 'canvas', HAARCASCADE_URI, 30, 6, 250);

startButton.disabled = true;

async function loadOpenCv(uri) {
  return new Promise((resolve, reject) => {
    const tag = document.createElement('script');
    tag.src = uri;
    tag.async = true;
    tag.type = 'text/javascript';
    tag.onload = () => {
      if (typeof cv !== 'undefined' && cv.Mat) {
        resolve();
        return;
      }

      cv.onRuntimeInitialized = () => {
        resolve();
      };
    };
    tag.onerror = () => {
      reject(new URIError("opencv didn't load correctly."));
    };

    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
  });
}

const ready = loadOpenCv(OPENCV_URI)
  .then(() => {
    startButton.disabled = false;
    startButton.textContent = 'Start measurement';
    statusText.textContent = 'Ready when you are. Click start and allow webcam access to begin.';
  })
  .catch((error) => {
    console.error(error);
    statusText.textContent = 'We could not load the computer-vision tools. Refresh the page to try again.';
  });

startButton.addEventListener('click', async () => {
  startButton.disabled = true;
  startButton.textContent = 'Initializing…';
  statusText.textContent = 'Grant camera permission and keep your face steady in good light.';

  try {
    await ready;
    await demo.init();
    startButton.textContent = 'Measuring';
    startButton.classList.add('is-live');
    statusText.textContent = 'Measurement in progress. Keep your face centered for the most accurate reading.';
    visualizer.classList.add('visualizer--active');
  } catch (error) {
    console.error(error);
    startButton.disabled = false;
    startButton.textContent = 'Try again';
    statusText.textContent = 'Unable to access your webcam. Check browser permissions and try again.';
  }
});
