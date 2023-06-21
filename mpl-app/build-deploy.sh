sudo apt-get install python3-tk 
docker build -t matplotlib-container .
docker run -p 8888:8888 -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix matplotlib-container
