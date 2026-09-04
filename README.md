# Raspberry-Pi-4

A collection of Raspberry Pi 4 projects: a GPIO LED that blinks SOS in Morse code, a shell
one-liner for grabbing a still from the Pi Camera, and a TensorFlow Lite object detector that
runs live on the camera feed. Everything here is Python and shell, meant to be run directly on
the Pi.

## Projects

### blink_led

`blink_led/sos_led.py` blinks an LED in a repeating SOS pattern using `gpiozero`. The LED is
declared as `LED(17)`, so the anode goes to BCM GPIO 17 through a resistor and the cathode to
ground. Timing constants at the top of the file control the dot, dash, letter, and word pauses.
Note that as written `DOT_PAUSE` (0.5s) is longer than `LINE_PAUSE` (0.2s), so dots are held
longer than dashes.

The loop runs forever; stop it with Ctrl-C.

```
python3 blink_led/sos_led.py
```

Wiring photo and circuit diagram:

![circuit led](images/Circuit%20-%20LED%20.png)

![picture led](images/Picture%20-%20LED.jpg)

### camera

`camera/screenshot.sh` is a single `raspistill` call that saves one image to `test.jpg`,
flipped both vertically and horizontally:

```
sh camera/screenshot.sh
```

`camera/image_classifier.ipynb` is a short scratch notebook. It has a stub function that builds
the same `raspistill` command string, and a cell that shells out to the object detection script
in `object_detection/`. It is exploratory, not a finished tool.

### object_detection

Real-time object detection on the camera feed, adapted from the TensorFlow Lite Raspberry Pi
example (Apache 2.0 headers are kept in `detect.py` and `utils.py`). `detect.py` opens the
camera with OpenCV, runs an EfficientDet-Lite TFLite model on each frame, draws boxes with
`utils.visualize`, and computes FPS. In this copy the `cv2.imshow` call is commented out and
the script prints the detection result to stdout instead, so it works without a monitor.

Hardware: Raspberry Pi with a Pi Camera or a USB camera. A Coral USB Accelerator is optional.

Install and download the models:

```
cd object_detection
sh setup.sh
```

Run it:

```
python3 detect.py --model efficientdet_lite0.tflite
```

With a Coral USB Accelerator:

```
python3 detect.py --enableEdgeTPU --model efficientdet_lite0_edgetpu.tflite
```

Flags: `--model`, `--cameraId` (default 0), `--frameWidth` (640), `--frameHeight` (480),
`--numThreads` (4), `--enableEdgeTPU`. `object_detection/README.md` has the longer upstream
walkthrough, and `test_data/` holds a sample image and its expected results CSV.

### chicken_ai

The start of a chicken-watching camera. `chicken_ai/detect.py`, `utils.py`, and the
EfficientDet-Lite model are byte-identical copies of the ones in `object_detection/`, and
`detect.sh` runs them:

```
cd chicken_ai
sh detect.sh
```

`chicken_ai/image_classifier.py` sketches the intended pipeline but every function is empty:
`read_image_from_camera`, `label_objects_in_image`, `objects_of_interest`, `save_to_sqlite`,
`visualize_data`. So the detection half works and the filtering, storage, and charting half is
not written yet.

## Requirements

- Raspberry Pi 4 running Raspberry Pi OS
- Python 3
- `gpiozero` and an LED plus resistor for the blink project
- Pi Camera (or USB camera) for the camera and detection projects
- For object detection, from `object_detection/requirements.txt`: `argparse`, `numpy>=1.20.0`,
  `opencv-python~=4.5.3.56`, `tflite-support>=0.4.2`, `protobuf>=3.18.0,<4`
- Optional: Coral USB Accelerator for Edge TPU inference

## Setup

```
git clone https://github.com/espin086/Raspberry-Pi-4.git
cd Raspberry-Pi-4
cd object_detection && sh setup.sh
```

`setup.sh` upgrades pip, installs the requirements, and curls both TFLite models if they are
not already present. The blink and camera projects need no setup beyond `gpiozero` and a
configured camera.

## License

There is no LICENSE file in this repo. `object_detection/detect.py` and `utils.py` (and their
copies in `chicken_ai/`) carry Apache 2.0 headers from the TensorFlow Authors.
