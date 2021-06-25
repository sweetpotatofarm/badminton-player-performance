# badminton-player-performance
in this project, top player means the player near the camera, and bottom player means the player far from the camera.

## Introduction
The project would read a csv file, and generate four types of images and four types of videos.
- images
  - new_image(number)_top.jpg: images when the top player hits the ball, and use a red rectangle to tell the top player's position.
  - cut_image(number)_top.jpg: images same as new_image(number)_top.jpg, but only focus on the top player.
  - new_image(number)_bot.jpg: images when the bottom player hits the ball, and use a red rectangle to tell the bottom player's position.
  - cut_image(number)_bot.jpg: images same as new_image(number)_bot.jpg, but only focus on the bottom plaer.
- videos
  - video(number)_top.avi: one second video capturing the moment the top player hits the ball.
  - video(number)_cut_top.avi: video same as video(number)_top.avi, but only focus on the top player.
  - video(number)_bot.avi: one second video capturing the moment the bottom player hits the ball.
  - video(number)_cut_bot.avi: video same as video(number)_bot.avi, but only focus on the bottom player.

## Settings
The csv file's column would be:
  1. frame number
  2. visibility
  3. ball position(X)
  4. ball position(Y)
  5. Hit player
  6. player's position when hitting(X)
  7. player's position when hitting(Y)
  8. top player's position after homography(X)
  9. top player's position after homography(Y)
  10. bottom player's position after homography(X)
  11. bottom player's position after homography(Y)
  12. top player's bounding box position(left top)
  13. top player's bounding box position(right bottom)
  14. bottom player's bounding box position(left top)
  15. bottom player's bounding box position(right bottom)

make sure csv file is in the same directory as media.py

## Python module install
```sh
pip3 install numpy
pip3 install python-csv
pip3 install opencv-python
pip3 install moviepy
```

## Execute
```sh
python3 media.py  
```
```sh
csv file name?
```
enter csv file name, ex:
```sh
demo.csv
```
```sh
video name?
```
enter video name, ex:
```sh
demo.mp4
```
