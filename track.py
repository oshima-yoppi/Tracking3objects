import cv2

def drawBoxTop(frame, box_top):
    print(box_top)
    x, y, w, h = int(box_top[0]), int(box_top[1]), int(box_top[2]), int(box_top[3])
    cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 65, 255), 2)
def drawBoxBottom(frame, box_bottom):
    x, y, w, h = int(box_bottom[0]), int(box_bottom[1]), int(box_bottom[2]), int(box_bottom[3])
    cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (255, 0, 0), 2)


file = "136.m4v"
cap = cv2.VideoCapture(file)  # 0 for Camera

# Create tracker
tracker_top = cv2.TrackerMIL_create()
tracker_bottom = cv2.TrackerMIL_create()

_, frame = cap.read()
box_top = (244, 330, 51, 41) 
box_bottom = (394, 329, 46, 43)
tracker_top.init(frame, box_top)
tracker_bottom.init(frame, box_bottom)


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
    

while True:
    _, frame = cap.read()
    frame = detectTwo(frame, tracker_top, tracker_bottom)
    # success_top, box_top = tracker_top.update(frame)
    # success_bottom, box_bottom = tracker_bottom.update(frame)
    # if success_top:
    #     drawBoxTop(frame, box_top)
    # if success_bottom:
    #     drawBoxBottom(frame, box_bottom)
    
    # Frame rate per second
    # cv2.putText(frame, "fps" + str(int(fps)), (15, 30), font, 0.5, (255, 255, 255), 2)
    cv2.imshow("tracking", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break