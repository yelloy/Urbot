#import urx
import cv2
import numpy as np
import threading
import time

EXIT = False
cam = cv2.VideoCapture("output1.avi")


def return_coord(img):
    coord = []
    img_original = img
    img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    img_gray_copy = img_gray.copy()

    # КООРДИНАТЫ ЦИЛИНДРОВ
    coord_cylinder = []
    pegs = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=50, minRadius=0, maxRadius=0)

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
            and img_original[int(peg[1])][int(peg[0])][2] < 50:
                print("КООРДИНАТЫ ЦИЛИНДРА: ", int(peg[1]), int(peg[0]))
                print("ЦВЕТ ЦИЛИНДРА: ", img_original[int(peg[1])][int(peg[0])])
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
            print("ЦВЕТ ОТВЕРСТИЯ: ", img_original[int(peg[1])][int(peg[0])])
            if img_original[int(peg[1])][int(peg[0])][1] < 50 and img_original[int(peg[1])][int(peg[0])][2] > 50:
                coord_holes.append([int(peg[0]), int(peg[1])])
    else:
        print("ОТВЕРСТИЯ НЕ НАЙДЕНЫ")

    coord.append(coord_cylinder)
    coord.append(coord_holes)
    return coord


def find_cylinder(camera):
    proof = [[]]
    N = 20
    # n раз проверяем область и рассчитываем вероятность и координату положения цилиндра
    for i in range(N):
        ret, img = camera.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # КООРДИНАТЫ ЦИЛИНДРОВ
        coord_cylinder = []
        pegs = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=50, minRadius=0, maxRadius=0)

        if pegs is not None:
            # Запись координат
            for peg in pegs[0]:
                x = int(peg[1])
                y = int(peg[0])
                #print(img[x][y])
                if img[x][y][1] < 40 and img[x][y][0] < 50 and img[x][y][2] < 50:
                    for coord_raw_i in range(len(proof)):
                        for coord_i in proof[coord_raw_i]:
                            print("Wwwwwwwwwwwwwwwwwwwwwwwwww")
                            x_ = proof[coord_raw_i][coord_i][0]
                            y_ = proof[coord_raw_i][coord_i][1]
                            delta = ((x_ - x) ** 2 + (y_ - y) ** 2)**0.5
                            print("delta: ", delta)
                            if delta < 8 and delta != 0:
                                proof[coord_raw_i].append([x, y])
                    if len(proof) == 0:
                        proof[coord_raw_i].append([x, y])
        else:
            print("ЦИЛИНДРЫ НЕ НАЙДЕНЫ")

    print(proof)
# Получится использовать для экономии времени в случае, если будет понятно как отличать не вставленные цилиндры
def thread_find_cylinders(camera):
    while not EXIT:
        ret, img = camera.read()
        coord = return_coord(img)
        for i in coord[0]:
            cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 3)
        for i in coord[1]:
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
        cv2.imshow('robot gripper', img)
        time.sleep(0.04)
# threading.Thread(target=thread_find_cylinders, args=cam)


''' ПРОВЕРКА ФИЛЬТРОВ НА КАРТИНКАХ
img = cv2.imread("test_image7.jpg")
coord = return_coord(img)
print("CYLINDERS: ", coord[0])
print("HOLES: ", coord[1])

for i in coord[0]:
    cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 3)
for i in coord[1]:
    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('my webcam', img)
cv2.waitKey(0)
'''

# ЦИКЛ СО СМЕНОЙ НОМЕРА ЗОНЫ

for i in range(7):
    # ДВИЖЕНИЕ В ЗОНУ 1 до тех пор пока не найден первый цилиндр
    # (спустя 1,5 секунды после его нахождения, остановить движение манипулятора и хватать цилиндр)
    pass
    # Захват изображения с камеры
    find_cylinder(cam)
    # Передаем координаты пикселей функции, преобразующей их в глобальные
