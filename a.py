import cv2

file = "136.m4v"
cap = cv2.VideoCapture(file)  # 0 for Camera

# Create tracker
tracker = cv2.TrackerMIL_create()
success, img = cap.read()
tracker_top = cv2.TrackerMIL_create()
tracker_bottom = cv2.TrackerMIL_create()


bbox = cv2.selectROI("tracking", img, False)
box_top = cv2.selectROI("tracking", img, False)
box_bottom = cv2.selectROI("tracking", img, False)
print(box_top, box_bottom)
tracker.init(img, bbox)
font = cv2.FONT_HERSHEY_SIMPLEX

def drawBox(img, bbox):
    # Box drawing function
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 0), 3, 1)
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 0), 3, 1)
    cv2.putText(img, "tracking", (15, 70), font, 0.5, (0, 0, 255), 2)



while True:
    timer = cv2.getTickCount()
    success, img = cap.read()
    success, bbox = tracker.update(img)
    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "tracking lost", (15, 70), font, 0.5, (0, 0, 255), 2)

    
    # Frame rate per second
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img, "fps" + str(int(fps)), (15, 30), font, 0.5, (255, 255, 255), 2)
    cv2.imshow("tracking", img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break