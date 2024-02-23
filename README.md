# funky_webcam

An attempt to do something funky with the webcam.
It all started when a friend showed me what they can do with the new Apple webcam gesture recognition.
I got jealous and I wanted to have some hand gestures and webcam interactions too!

I had a "conversation" with chatGPT about what I could do and this project is the implementation of those ideas.

This is what the program is doing:

- Open the video source and read the stream
- For each frame, find the hands, hightlight them
- Write the original image and the hands joints on the destination

## Install

If you want to give that project a go, you can follow along!

- Python 3 and pip

I'll suppose you have Python 3 installed.

- Virtual webcam

You need a virtual video source to point your software at.
To create that you need to install the package `v4l2loopback-dkms`. Then you need to load a module that will create your new virtual video source:

```bash
sudo modprobe v4l2loopback devices=1 video_nr=4 exclusive_caps=1 card_label="Virtual Webcam"
```

Note that here I'm creating a new device called "Virtual Webcam" and this device will be available in `/dev/video4` (the `video_nr` parameter.)

- Clone this repo:

```bash
git clone https://github.com/Kylir/funky-webcam.git
```

- Create (do that only the first time) and activate your virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

- Install the requirements

```bash
pip install -r requirements.txt
```

- Identify the webcam you want to use as your _source_ and also the webcam you want at your _destination_ (the virtual one) and change the script accordingly.

You will need to use `v4l2-ctl` (part of the `v4l-utils` package)

```bash
v4l2-ctl --list-devices
```

This command is giving me:

```
Dummy video device (0x0000) (platform:v4l2loopback-000):
	/dev/video4

USB 2.0 Camera: USB 2.0 Camera (usb-0000:00:14.0-4):
	/dev/video2
	/dev/video3
	/dev/media1

Integrated_Webcam_HD: Integrate (usb-0000:00:14.0-6):
	/dev/video0
	/dev/video1
	/dev/media0
```

I now have the choice between webcam index 0 and index 2 for my sources.
And the "Dummy video device" is the virtual one we will use for the destination.

This needs to be changed in the code. The following instruction tells OpenCV to use the second webcam:

```python
cap = cv2.VideoCapture(2)
```

- run the script

```bash
python funky_webcam.py
```
