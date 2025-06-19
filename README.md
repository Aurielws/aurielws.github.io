# heartbeat-js: Video-based pulse rate monitoring in JavaScript

This is a simple JavaScript implementation of rPPG, a way to measure the pulse rate without skin contact.
It uses a live feed of the face to analyse subtle changes in skin color.

Here's how it works:

  - The face is detected and continuously tracked
  - Signal series is obtained by determining the facial color in every frame
  - Heart rate is estimated using frequency analysis and filtering of the series

## Demo
Test the live demo directly in your browser: [Demo](https://aurielws.github.io/)
**Works best if there is no subject motion.**

