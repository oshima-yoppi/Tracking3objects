
import cv2
import numpy as np
# from torch import scatter_reduce


def rgb_red(img):
    bgr_min = np.array([0,0,80])
    bgr_max = np.array([40, 40, 255])
    mask1 = cv2.inRange(img, bgr_min, bgr_max)

    bgr_min = np.array([0,0,60])
    bgr_max = np.array([15, 15, 255])
    mask2 = cv2.inRange(img, bgr_min, bgr_max)
    mask = mask1+ mask2
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    
    # print(mask[:,0].size)
    # exit()
    plot = []
    if 255 in mask:
        for i in range(480):
            if 255 in mask[i,:] :
                ymin = i
                break
        for i in reversed(range(480)):
            if 255 in mask[i,:] :
                ymax = i
                break


        for i in range(640):
            if 255 in mask[:,i] :
                xmin = i
                break
        for i in reversed(range(640)):
            if 255 in mask[:,i] :
                xmax = i
                break
        plot = [(xmin, ymin), (xmax, ymax)]

    return mask, masked_img, plot


def save_detect(video_path):
    cap = cv2.VideoCapture(video_path)
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 30.0
    size = (640, 480)
    writer = cv2.VideoWriter('detect_movie/red.mp4', fmt, fps, size)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if ret:
            _, masked_img, plot = rgb_red(frame)
            # print(plot)
            if plot:
                cv2.rectangle(frame, plot[0], plot[1],(0,255,0), thickness=2)
            writer.write(frame)
        else:
            writer.release()
            return
if __name__ == "__main__":
    save_detect("136.m4v")


# i = 0
# while 1:
#     img = cv2.imread("frame/img_{}.png".format(str(i).zfill(4)))
#     height, width, channels = img.shape[:3]
#     print(height, width)
#     # red_mask, red_masked_img = detect_red_color(img)
#     red_mask, red_masked_img = rgb_red(img)
#     cv2.imshow("Image", red_masked_img)
#     cv2.waitKey()
#     i += 1

