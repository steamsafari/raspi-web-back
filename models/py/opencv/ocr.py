# coding: utf-8
import cv2 as cv
import pytesseract
import re

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

last_ocr_frame = None
last_ocr_digits = ''

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.rectangle(frame, (100, 70), (220, 170), (0, 255, 0), 2)
    cv.imshow('frame', frame)
    # rows, columns
    roi_digit = frame[70:170, 100:220]
    roi_digit_gray = cv.cvtColor(roi_digit, cv.COLOR_BGR2GRAY)
    ret, roi_digit_thresh = cv.threshold(roi_digit_gray, 64, 255,
                                         cv.THRESH_BINARY)

    cv.imshow('roi', roi_digit_thresh)
    if cv.waitKey(1) == ord('q'):
        break

    # 检查和上一次做OCR帧的差异，检测到移动再做OCR
    moved = False
    if (last_ocr_frame is None):
        moved = True
    else:
        diff = cv.absdiff(last_ocr_frame, roi_digit_thresh)
        if diff.mean() > 36:  # 超过百分之16的点有变化
            moved = True

    if moved:
        last_ocr_frame = roi_digit_thresh
        # Our operations on the frame come here
        print('Start OCR')
        text = pytesseract.image_to_string(roi_digit_thresh, config='--psm 6')
        if len(text.strip()):
            digits = re.sub(r'\D', "", text)
            if (len(digits)):
                if digits != last_ocr_digits:
                    last_ocr_digits = digits
                    print(digits, flush=True)

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
