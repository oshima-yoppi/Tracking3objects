import cv2
import os

def save_all_frames(video_path, dir_path, basename, ext='png'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        print(ret, frame)
        print(n)
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return
video_path = "136.m4v"
dir_path = "frame"
# save_all_frames(video_path, dir_path, 'img')
# cap = cv2.VideoCapture(video_path)
# print(cap.get(cv2.CAP_PROP_FPS))
