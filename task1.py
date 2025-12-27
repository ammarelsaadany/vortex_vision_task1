import cv2
import numpy as np
import datetime


cap = cv2.VideoCapture(0)

recording = False
video_writer = None
mode = 'Z'

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to connect to camera")
        break

    processed_frame = frame.copy()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    display_img = frame

    if mode == 'G':
        display_img = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    elif mode == 'H':
        display_img = hsv_frame
    elif mode == 'R':
        display_img = rotated_frame
    elif mode == 'X':
        height, width = frame.shape[:2]
        small_size = (int(width / 2), int(height / 2))

        orig_s = cv2.resize(frame, small_size)
        gray_s = cv2.resize(cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR), small_size)
        hsv_s = cv2.resize(hsv_frame, small_size)
        rot_s = cv2.resize(rotated_frame, small_size)

        top_row = np.hstack((orig_s, gray_s))
        bottom_row = np.hstack((hsv_s, rot_s))
        display_img = np.vstack((top_row, bottom_row))

    cv2.imshow('reasult', display_img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('z'):
        mode = 'Z'
    elif key == ord('g'):
        mode = 'G'
    elif key == ord('h'):
        mode = 'H'
    elif key == ord('r'):
        mode = 'R'
    elif key == ord('x'):
        mode = 'X'
    elif key == ord('c'):
        timestamp = datetime.datetime.now().strftime("s")
        filename = f"assets/output_results/capture_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f" image saved {filename}")
    elif key == ord('s'):
        if not recording:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"assets/output_results/video_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            recording = True
            print("start recording")
        else:
            recording = False
            video_writer.release()
            print(" stop recording")

    if recording and video_writer is not None:
        video_writer.write(frame)

cap.release()
if video_writer is not None:
    video_writer.release()
