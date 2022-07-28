import cv2
# import matplotlib.pyplot as plt
import numpy as np
class TemplateMatching():
    def __init__(self, template_path, color, th):
        self.template  = cv2.imread(template_path)
        self.h , self.w, _ = self.template.shape
        self.color = color
        self.th = th
        self.value = []

    def match(self, frame):
        """
        正規化相関係数を用いてテンプレートマッチングを行う
        """
        match = cv2.matchTemplate(frame, self.template, method=cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        self.plot = ()
        self.bool = False
        self.value.append(max_val)
        
        # 出力がある閾値self.thより大きい場合、マッチングしたとする。
        if max_val >= self.th:
            self.bool = True
            self.coodinate = max_loc
            self.plot = (self.coodinate[0]+self.w, self.coodinate[1]+self.h)
        return  

    def draw(self, frame):
        """
        frameに長方形を書き込む関数
        """
        if self.bool:
            cv2.rectangle(frame, self.coodinate, self.plot, self.color, 2)
        return frame


def detect_red(img):
    """
    赤色検知をする関数。
    二種類のマスクを用意してマスク処理を行う。
    """
    bgr_min = np.array([0,0,80])
    bgr_max = np.array([40, 40, 255])
    mask1 = cv2.inRange(img, bgr_min, bgr_max)

    bgr_min = np.array([0,0,60])
    bgr_max = np.array([15, 15, 255])
    mask2 = cv2.inRange(img, bgr_min, bgr_max)
    mask = mask1+ mask2
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    
    # 赤色検知した部分を囲む長方形を探索し、長方形の座標を算出
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


if __name__ == "__main__":
    cap = cv2.VideoCapture("136.m4v")
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 30.0
    size = (640, 480)
    writer = cv2.VideoWriter('detect_movie/template.mp4', fmt, fps, size)
    match_top = TemplateMatching('img/burger_top.png', (255, 0, 0), 0.92)
    match_bottom = TemplateMatching('img/burger_bottom.png', (0, 65, 255), 0.96)
    while True:
        ret, frame = cap.read()
        if ret:
            match_top.match(frame)
            match_bottom.match(frame)
            _, masked_img, coodinate = detect_red(frame)
            if coodinate:
                cv2.rectangle(frame, coodinate[0], coodinate[1],(0,255,0), thickness=2)
            frame = match_top.draw(frame)
            frame = match_bottom.draw(frame)
            writer.write(frame)
        else:
            writer.release()

