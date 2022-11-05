FROM ubuntu:20.04


RUN apt update
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple opencv-python
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple opencv-contrib-python
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple opencv-python-headless
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple opencv-contrib-python-headless
RUN apt install libgtk2.0-dev
RUN apt install x11-xserver-utils

# docker run -it --rm --device=/dev/video0 -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix <image_name>
