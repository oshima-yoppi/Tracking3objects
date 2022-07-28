
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


def drawBoxTop(img, box_top):
    x, y, w, h = int(box_top[0]), int(box_top[1]), int(box_top[2]), int(box_top[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (0, 65, 255), 2)
def drawBoxBottom(img, box_bottom):
    x, y, w, h = int(box_bottom[0]), int(box_bottom[1]), int(box_bottom[2]), int(box_bottom[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 0), 2)
def detectTwo(frame, tracker_top, tracker_bottom):
    success_top, box_top = tracker_top.update(frame)
    success_bottom, box_bottom = tracker_bottom.update(frame)
    if success_top:
        drawBoxTop(frame, box_top)
    if success_bottom:
        drawBoxBottom(frame, box_bottom)
    
    # Frame rate per second
    # cv2.putText(frame, "fps" + str(int(fps)), (15, 30), font, 0.5, (255, 255, 255), 2)
    return frame

def main(video_path):
    cap = cv2.VideoCapture(video_path)
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 30.0
    size = (640, 480)
    
    writer = cv2.VideoWriter('detect_movie/detect3.mp4', fmt, fps, size)
    if not cap.isOpened():
        return


    i =0
    while True:
        ret, frame = cap.read()
        if i == 0:
            box_top = (244, 330, 51, 41) 
            box_bottom = (394, 329, 46, 43)
            # Create tracker
            tracker_top = cv2.TrackerMIL_create()
            tracker_bottom = cv2.TrackerMIL_create()
            tracker_top.init(frame, box_top)
            tracker_bottom.init(frame, box_bottom)
            i += 1
        if ret:
            _, masked_img, plot = rgb_red(frame)
            frame = detectTwo(frame, tracker_top, tracker_bottom) 


            # print(plot)
            if plot:
                cv2.rectangle(frame, plot[0], plot[1],(0,255,0), thickness=2)
            writer.write(frame)
        else:
            writer.release()
            return
if __name__ == "__main__":
    main("136.m4v")


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

