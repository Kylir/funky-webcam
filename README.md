# funky_webcam

An attempt to do something funky with the webcam.
It all started when a friend showed me what they can do with the new Apple webcam gesture recognition.
I got jealous and I wanted to have some webcam interaction too!

I had a conversation with chatGPT about what I could do and this is project is the implementation of those ideas.

## Install

If you want to give that project a go, you can follow along!

I'll suppose you have Python 3 installed.

- Clone this repo

- Create and activate your virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

- Install the requirements

```bash
pip install -r requirements.txt
```

- Identify the webcam you want to use and change the script

You will need to use `v4l2-ctl` (part of the `v4l-utils` package)

```bash
v4l2-ctl --list-devices

USB 2.0 Camera: USB 2.0 Camera (usb-0000:00:14.0-4):
	/dev/video2
	/dev/video3
	/dev/media1

Integrated_Webcam_HD: Integrate (usb-0000:00:14.0-6):
	/dev/video0
	/dev/video1
	/dev/media0
```

I now have the choice between webcam index 0 and index 2.
This needs to be changed in the code. The following instruction tells OpenCV to use the second webcam:

```python
cap = cv2.VideoCapture(2)
```

- run the script

```bash
python funky_webcam.py
```
