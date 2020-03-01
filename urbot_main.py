#import urx
import cv2
import numpy as np
import threading
import time

EXIT = False
cam = cv2.VideoCapture("output3.avi")


def sort_by_value(input_value):
    criteria = ((320-input_value[0])**2 + (240-input_value[1])**2)**0.5
    return criteria


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


def find_holes(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # КООРДИНАТЫ ОТВЕРСТИЙ
    coord_holes = []
    pegs = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=60, minRadius=0, maxRadius=0)

    if pegs is not None:
        # Запись координат
        for peg in pegs[0]:
            #print("КООРДИНАТЫ ОТВЕРСТИЯ: ", int(peg[1]), int(peg[0]))
            #print("ЦВЕТ ОТВЕРСТИЯ: ", img[int(peg[1])][int(peg[0])])
            if img[int(peg[1])][int(peg[0])][1] < 50 and img[int(peg[1])][int(peg[0])][2] > 50:
                coord_holes.append([int(peg[0]), int(peg[1])])
    else:
        pass
        #print("ОТВЕРСТИЯ НЕ НАЙДЕНЫ")
    coord_holes.sort(key=sort_by_value)
    return coord_holes


def find_cylinder(camera):
    proof = [[[0, 0]]]
    cylinder_coord = []
    N = 10
    # n раз проверяем область и рассчитываем вероятность и координату положения цилиндра
    for i in range(N):
        #img = cv2.imread("test_image7.jpg")
        ret, img = camera.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # КООРДИНАТЫ ЦИЛИНДРОВ
        coord_cylinder = []
        pegs = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=30, minRadius=30, maxRadius=70)
        #print(pegs)
        if pegs is not None:
            # Запись координат
            for peg in pegs[0]:
                shodstvo = False
                x, y = int(peg[0]), int(peg[1])
                radius = 40
                x_border1 = x + radius
                if x_border1 >= 640:
                    x_border1 = 639
                x_border2 = x - radius
                if x_border2 < 0:
                    x_border2 = 0
                y_border1 = y + radius
                if y_border1 >= 480:
                    y_border1 = 479
                y_border2 = y - radius
                if y_border2 < 0:
                    y_border2 = 0
                #print(x_border1, y_border1)
                border_point1 = img[y_border1][x_border1]
                border_point2 = img[y_border1][x_border2]
                border_point3 = img[y_border2][x_border1]
                border_point4 = img[y_border2][x_border2]
                border_condition = (border_point1[0] < 70 and border_point1[1] > 50) \
                                   or (border_point2[0] < 70 and border_point2[1] > 50) \
                                   or (border_point3[0] < 70 and border_point3[1] > 50) \
                                   or (border_point4[0] < 70 and border_point4[1] > 50)

                #print(img[x][y])
                if img[y][x][1] < 40 and img[y][x][0] < 50 and img[y][x][2] < 50 and not border_condition:
                    rg = len(proof)

                    #print(rg)
                    for coord_raw_i in range(rg):
                        last_element = len(proof[coord_raw_i])-1
                        x_ = proof[coord_raw_i][last_element][0]
                        y_ = proof[coord_raw_i][last_element][1]
                        delta = ((x_ - x) ** 2 + (y_ - y) ** 2)**0.5
                        if delta < 8:
                            proof[coord_raw_i].append([x, y])
                            shodstvo = True
                    if not shodstvo:
                        proof.append([[x, y]])
    for element in proof:
        #print(element)
        if len(element) > 6:
            mean_x = []
            mean_y = []
            for el in element:
                mean_x.append(el[0])
                mean_y.append(el[1])
            mean_x = int(np.mean(mean_x))
            mean_y = int(np.mean(mean_y))
            cylinder_coord.append([mean_x, mean_y])

    if not len(cylinder_coord):
        pass
        #print("ЦИЛИНДРЫ НЕ НАЙДЕНЫ")
    cylinder_coord.sort(key=sort_by_value)
    return cylinder_coord


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

'''
# ПРОВЕРКА ФИЛЬТРОВ НА КАРТИНКАХ
img = cv2.imread("test_image3.jpg")
coord = return_coord(img)
print("CYLINDERS: ", coord[0])
print("HOLES: ", coord[1])

for i in coord[0]:
    cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 3)
for i in coord[1]:
    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('my webcam', img)
cv2.waitKey(0)
#'''

# ЦИКЛ СО СМЕНОЙ НОМЕРА ЗОНЫ

while True:
    # ДВИЖЕНИЕ В ЗОНУ 1 до тех пор пока не найден первый цилиндр
    # (спустя 1,5 секунды после его нахождения, остановить движение манипулятора и хватать цилиндр)

    # Захват изображения с камеры
    ret, img = cam.read()
    cylinder_coord = find_cylinder(cam)
    hole_coord = find_holes(img)
    for i in cylinder_coord:
        cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 3)
    for i in hole_coord:
        print(hole_coord)
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Передаем координаты пикселей функции, преобразующей их в глобальные
