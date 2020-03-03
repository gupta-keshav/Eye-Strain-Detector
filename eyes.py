import cv2
import numpy as np
import dlib
from math import hypot
import time
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def get_midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


font = cv2.FONT_HERSHEY_SIMPLEX

tick = time.time()
number_of_blinks = 0
strain_time = 0
late_blink_counter = 0
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        # x, y = face.left(), face.top()
        # x1, y1  = face.right(), face.bottom()
        # cv2.rectangle(frame, (x,y), (x1,y1), (0, 255, 0), 2)
        landmarks = predictor(gray, face)
        left_point = (landmarks.part(36).x, landmarks.part(36).y)
        right_point = (landmarks.part(39).x, landmarks.part(39).y)
        center_top = get_midpoint(landmarks.part(37), landmarks.part(38))
        center_bottom = get_midpoint(landmarks.part(41), landmarks  .part(40))

        hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

        ver_line_length = hypot(
            (center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        hor_line_length = hypot(
            (left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ratio = hor_line_length/(ver_line_length)
        if ratio > 6:
            cv2.putText(frame, "Blinking", (50, 150), font, 3, (0, 255, 0))
        tock = time.time()
        if(ratio > 6):
            if(tock - tick > 6):
                late_blink_counter += 1
            elif(tock-tick < 1):
                late_blink_counter += 0
            else:
                late_blink_counter -= 1
                if(late_blink_counter < 0):
                    late_blink_counter = 0
#             print(tock - tick)
#             print(late_blink_counter)
            if(late_blink_counter > 4):
                print("please bink eyes")
            tick = tock
    # print(tock-tick)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
