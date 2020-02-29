#import urx
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

#cam = cv2.VideoCapture(0)
#ret_val, img = cam.read()
#cv2.imshow('my webcam', img)
#cv2.waitKey(0)

'''
rob = urx.Robot("192.168.0.100")
rob.set_tcp((0, 0, 0.1, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
sleep(0.2)  #leave some time to robot to process the setup commands
rob.movej((1, 2, 3, 4, 5, 6), a, v)
rob.movel((x, y, z, rx, ry, rz), a, v)
print "Current tool pose is: ",  rob.getl()
rob.movel((0.1, 0, 0, 0, 0, 0), a, v, relative=true)  # move relative to current pose
rob.translate((0.1, 0, 0), a, v)  #move tool and keep orientation
rob.stopj(a)

robot.movel(x, y, z, rx, ry, rz), wait=False)
while True :
    sleep(0.1)  #sleep first since the robot may not have processed the command yet
    if robot.is_program_running():
        break

robot.movel(x, y, z, rx, ry, rz), wait=False)
while.robot.getForce() < 50:
    sleep(0.01)
    if not robot.is_program_running():
        break
robot.stopl()

try:
    robot.movel((0,0,0.1,0,0,0), relative=True)
except RobotError, ex:
    print("Robot could not execute move (emergency stop for example), do something", ex)'''