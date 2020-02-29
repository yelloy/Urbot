import cv2
import numpy as np


def return_coord(img):
    coord = []
    img_original = img
    img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    img_gray_copy = img_gray.copy()

    # КООРДИНАТЫ ЦИЛИНДРОВ
    coord_cylinder = []
    pegs = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=80, param2=50, minRadius=0, maxRadius=0)

    if pegs is not None:
        # Чисто подсветка
        circles = np.uint16(np.around(pegs))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img_gray,(i[0],i[1]),i[2],(255,255,255),2)
            # draw the center of the circle
            cv2.circle(img_gray,(i[0],i[1]),2,(255,255,255),3)

        #cv2.imshow('detected cylindres',img_gray)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        ########################
        # Запись координат
        for peg in pegs[0]:
            if img_original[int(peg[1])][int(peg[0])][1] < 40 and img_original[int(peg[1])][int(peg[0])][0] < 50\
                and img_original[int(peg[1])][int(peg[0])][2] < 50 and img_original[int(peg[1]) + 30][int(peg[0])][0] > 70 \
                    and img_original[int(peg[1]) - 30][int(peg[0])][0] > 70:
                print("КООРДИНАТЫ ЦИЛИНДРА: ", int(peg[1]), int(peg[0]))
                print("ЦВЕТ ЦИЛИНДРА: ", img_original[int(peg[1])][int(peg[0])])
                print("ЦВЕТ БЕЛЫЙ ВОКРУГ ОТВЕРСТИЯ: ", img_original[int(peg[1]) + 30][int(peg[0])])
                print("ЦВЕТ БЕЛЫЙ ВОКРУГ ОТВЕРСТИЯ: ", img_original[int(peg[1]) - 30][int(peg[0])])
                coord_cylinder.append([int(peg[0]), int(peg[1])])
    else:
        print("ЦИЛИНДРЫ НЕ НАЙДЕНЫ")

    # КООРДИНАТЫ ОТВЕРСТИЙ
    coord_holes = []
    pegs = cv2.HoughCircles(img_gray_copy, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=60, minRadius=0, maxRadius=0)

    if pegs is not None:
        # Чисто подсветка
        circles = np.uint16(np.around(pegs))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img_gray_copy,(i[0],i[1]),i[2],(255,255,255),2)
            # draw the center of the circle
            cv2.circle(img_gray_copy,(i[0],i[1]),2,(255,255,255),3)

        #cv2.imshow('detected holes', img_gray_copy)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        ########################
        # Запись координат
        for peg in pegs[0]:
            print("КООРДИНАТЫ ОТВЕРСТИЯ: ", int(peg[1]), int(peg[0]))
            print("РАДИУС ОТВЕРСТИЯ: ", peg[2])
            print("ЦВЕТ ОТВЕРСТИЯ: ", img_original[int(peg[1])][int(peg[0])])
            if img_original[int(peg[1])][int(peg[0])][1] < 50 and img_original[int(peg[1])][int(peg[0])][2] > 50:
                print("ЦВЕТ ЖЕЛТЫЙ ВОКРУГ ОТВЕРСТИЯ: ", img_original[int(peg[1]) + 30][int(peg[0])])
                print("ЦВЕТ ЖЕЛТЫЙ ВОКРУГ ОТВЕРСТИЯ: ", img_original[int(peg[1]) - 30][int(peg[0])])
                coord_holes.append([int(peg[0]), int(peg[1])])
    else:
        print("ОТВЕРСТИЯ НЕ НАЙДЕНЫ")

    coord.append(coord_cylinder)
    coord.append(coord_holes)
    return coord


cap = cv2.VideoCapture("output3.avi")
ret, frame = cap.read()
cv2.imwrite("FOCUS.jpg", frame)
while True:
    ret, frame = cap.read()
    coord = return_coord(frame)
    for i in coord[0]:
        cv2.circle(frame, (i[0], i[1]), 2, (255, 255, 255), 3)
    for i in coord[1]:
        cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow('1', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(coord)