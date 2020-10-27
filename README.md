# heartbeat-js: Video-based pulse rate monitoring in JavaScript
ORIGINAL VERSION: https://github.com/prouast/heartbeat 

This is a simple JavaScript implementation of rPPG, a way to measure the pulse rate without skin contact.
It uses a live feed of the face to analyse subtle changes in skin color.

Here's how it works:

  - The face is detected and continuously tracked
  - Signal series is obtained by determining the facial color in every frame
  - Heart rate is estimated using frequency analysis and filtering of the series

## Demo
Test the live demo directly in your browser: [Demo](https://aurielws.github.io/)
**Works best if there is no subject motion.**

## How you can deploy it on your own github.io static page
  - Go to your terminal and enter each line after the the $
  
        $ mkdir Your_github_username.github.io
        $ cd Your_github_username.github.io
        $ git clone git@github.com:Aurielws/aurielws.github.io.git
        $ git add --all
        $ git commit -m "Initial commit"
        $ git push -u origin master
      
      
  - Fire up a browser and go to https://Your_github_username.github.io to see your version of this demo!
  - Read more about github.io pages here(https://pages.github.com/)
