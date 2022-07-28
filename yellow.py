
import cv2
import numpy as np


def detect_yellow(img):
    hsv_img= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array([38*180/360, 20*255/100, 55*255/100])
    hsv_max = np.array([45*180/360, 35*255/100, 70*255/100])
    # hsv_max = np.array([60*180/360, 50*255/100, 90*255/100])
    mask = cv2.inRange(hsv_img, hsv_min, hsv_max)
    mask = cv2.bitwise_not(mask)
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    
    
    # plot = []
    # if 255 in mask:
    #     for i in range(480):
    #         if 255 in mask[i,:] :
    #             ymin = i
    #             break
    #     for i in reversed(range(480)):
    #         if 255 in mask[i,:] :
    #             ymax = i
    #             break


    #     for i in range(640):
    #         if 255 in mask[:,i] :
    #             xmin = i
    #             break
    #     for i in reversed(range(640)):
    #         if 255 in mask[:,i] :
    #             xmax = i
    #             break
    #     plot = [(xmin, ymin), (xmax, ymax)]

    return mask, masked_img


def save_detect(video_path):
    cap = cv2.VideoCapture(video_path)
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 30.0
    size = (640, 480)
    writer = cv2.VideoWriter('detect_movie/yellow.mp4', fmt, fps, size)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if ret:
            mask, masked_img = detect_yellow(frame)
            # print(plot)
            # if plot:
            #     cv2.rectangle(frame, plot[0], plot[1],(0,255,0), thickness=2)
            writer.write(masked_img)
        else:
            writer.release()
            return

save_detect("136.m4v")
# i = 0
# while 1:
#     img = cv2.imread("frame/img_{}.png".format(str(i).zfill(4)))
#     # red_mask, red_masked_img = detect_red_color(img)
#     red_mask, red_masked_img = detect_yellow(img)
#     cv2.imshow("Image", red_masked_img)
#     cv2.waitKey()
#     i += 1

