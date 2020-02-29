import urx
import cv2
import numpy as np
import time
import math
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

def initialisationSession():
    global observeTablePoses
    observeTablePoses.append([0.350, -0.680, 0.800])
    observeTablePoses.append([0.0, -0.680, 0.800])
    observeTablePoses.append([-0.270, -0.680, 0.800])
    observeTablePoses.append([-0.270, 0.0, 0.800])
    observeTablePoses.append([-0.270, 0.960, 0.800])
    observeTablePoses.append([0.0, 0.960, 0.800])
    observeTablePoses.append([0.350, 0.960, 0.800])
    observeTablePoses.append([0.350, 0.0, 0.800])

    global observeTableOrient
    observeTableOrient = [2.94, 1.157, 0.0]

def moveToPoseOrient(pose, orient):
    """
    This function moves gripper to position and orientation in world space.
    """
    #Get components:
    x = pose[0]
    y = pose[1]
    z = pose[2]
    rx = orient[0]
    ry = orient[1]
    rz = orient[2]
    acceleration = 0.1
    velocity = 0.1

    print(x, y, z, rx, ry, rz)

    #Make gripper movement in base frame:
    rob.movel((x, y, z, rz, ry, rz), acceleration, velocity, wait = True)

def getCylHoleWorldCoordinates():
    #Пока робот проезжает по всем ключевым точкам, задерживаясь на 5 секунд.
    for pose in observeTablePoses:
        moveToPoseOrient(pose, observeTableOrient)
        time.sleep(5)

def moveGripperToCameraCenterPose():
    # Получаем полное положение схвата в мире:
    poseOrient = rob.getl()
    xGrip = poseOrient[0]
    yGrip = poseOrient[1]
    zGrip = poseOrient[2]
    rx = poseOrient[3]
    ry = poseOrient[4]
    rz = poseOrient[5]

    # Получаем координаты точки, куда нужно поместить схват, чтобы он оказался там, где был цилиднр:
    xTarget = xGrip - 0.01
    yTarget = yGrip - 0.065

    # Движение, не меняя ориентации в нужное положение:
    moveToPoseOrient([xTarget, yTarget, zGrip], [rx, ry, rz])

    #Получаем текущее положение и ориентацию схвата в пространстве мира:
    poseOrient = rob.getl()
    return poseOrient

    #Теперь относительно этого положения схвата можно получить координаты точек изображения...

def getCylinderCoordinateWorldSpace(point):
    """
    Когда схват стоит в определенном положении, координаты цилиндра, которые мы получили из изображения с камеры,
    можно перевести в координаты мира.

    :param point: Пиксель на исходном изображении. СК слева сверху.
    :return: Точка [x, y, z], куда надо переместить схват.
    """
    #Расстояние между объективом камеры и верхней точкой цилиндра:
    ZCamSpace = 0.4

    #Получаем фокусное расстояние в пискелях и меняем систему координат изображения (смещаем в центр):
    focusLengthInPixels = 10
    xPixel = point[0] - 320
    yPixel = point[1] - 240

    #Получаем X и Y в пространстве камеры:
    XCamSpace = ZCamSpace * xPixel / focusLengthInPixels
    YCamSpace = ZCamSpace * yPixel / focusLengthInPixels

    #Получаем полное положение схвата в мире:
    poseOrient = rob.getl()
    xGrip = poseOrient[0]
    yGrip = poseOrient[1]
    zGrip = poseOrient[2]
    rx = poseOrient[3]
    ry = poseOrient[4]
    rz = poseOrient[5]

    #Получаем координаты точки, куда нужно поместить схват, чтобы взять цилиндр:
    xTarget = xGrip - XCamSpace - 0.01
    yTarget = yGrip + YCamSpace - 0.065
    zTarget = 0.15

    #Движение, не меняя ориентации в нужное положение над цилиндром:
    moveToPoseOrient([xTarget, yTarget, zTarget], [rx, ry, rz])

def openGripper():
    header = "def myProg():\n"
    end = "end\n"
    prog = header
    prog += 'set_tool_digital_out(0, False)\n'
    prog += 'set_tool_digital_out(1, True)\n'
    prog += 'sleep(0.7)\n'
    prog += end
    rob.send_program(prog)

def closeGripper():
    header = "def myProg():\n"
    end = "end\n"
    prog = header
    prog += 'set_tool_digital_out(0, True)\n'
    prog += 'set_tool_digital_out(1, False)\n'
    prog += 'sleep(0.7)\n'
    prog += end
    rob.send_program(prog)

#Connect to UR10e:
rob = urx.Robot("172.31.1.3")
print("Successfully connected to UR10E.")

#Set transform matrix from flange to gripper:
rob.set_tcp((0, 0, 0, 0, 0, 0))

#Вывод текущей конфигурации:
state = rob.getl()
print("State: ", state)

# #Initialise important constants:
observeTablePoses = []
observeTableOrient = 0
initialisationSession()

#getCylHoleWorldCoordinates()

#forces = rob.get_tcp_force()
#print(forces)

# closeGripper()
# time.sleep(1)
# openGripper()
# time.sleep(1)
# closeGripper()
# time.sleep(1)
# openGripper()
# time.sleep(1)

#(0.350, -0.680, 0.800, 2.94, 1.157, 0.0)
rob.movel((0.30, -0.680, 0.800, 2.94, 1.157, 0.0), 0.1, 0.1, wait = True)
while True:
    time.sleep(0.01)
    if not rob.is_program_running():
        break
rob.stopl()

rob.movel((0.400, -0.680, 0.800, 2.94, 1.157, 0.0), 0.1, 0.1, wait = True)
rob.stopl()

rob.close()