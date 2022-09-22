#!/usr/bin/env /python3

from __future__ import print_function
from __future__ import with_statement

import sys

print("TODO")
sys.exit(1)

# Alt: ffprobe (slower)
def with_opencv(filename):
    import cv2 # opencv-python
    video = cv2.VideoCapture(filename)

    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return duration, frame_count

    # image dimensions
    img = cv2.imread('my_image.jpg',0)
    height, width = img.shape[:2]

    # video dims etc
    vcap = cv2.VideoCapture('video.avi') # 0=camera
    assert vcap.isOpened()
    width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    fps = vcap.get(cv2.CAP_PROP_FPS)
