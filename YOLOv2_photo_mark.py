# -*- coding:utf-8 -*-
import os
import cv2
import numpy as np
import sys

path = sys.path[0] + os.sep

global ix ,iy, ox, oy, drawing, downFlag, drawed

drawing = False # 当鼠标按下时变为 True
drawed = False # 当绘制一个图形时变为True
ix, iy = -1, -1
ox, oy = -1, -1
# 创建回调函数
def draw_circle(event, x, y, flags, param):
    global ix, iy, ox, oy, drawing, downFlag, drawed
    # 当按下左键时返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x, y
    # 当鼠标左键按下并移动时绘制图形。 event 可以查看移动, flag 查看是否按下
    # elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
    #      if drawing == True:
    #             cv2.rectangle(image,(ix, iy), (x, y), (255, 0, 0), thickness=3)
    #             ox, oy = x, y
    # 当放开左键时，
    elif event == cv2.EVENT_LBUTTONUP:
        drawed = True
        cv2.rectangle(image, (ix, iy), (x, y), (255, 0, 0), thickness=1)
        ox, oy = x, y
    # 按下右键时，downFlag设为True，表示当前图片标记结束
    elif event == cv2.EVENT_RBUTTONDOWN:
        downFlag = True
        drawed = False
    return

number = 0
image_path = path + "images" + os.sep # 图片文件夹路径
f_wrect = open(path + 'images.txt', 'a') # 用来记录标记的图片
for fn in os.listdir(image_path):
    number += 1
    window_name = os.path.splitext(fn)[0]
    image = cv2.imread(image_path + fn)
    height = image.shape[0]
    width = image.shape[1]
    f_wrect.write(fn + '\n')
    print 'num: %d' % number, window_name, width, height
    label = open(path + 'labels' + os.sep + os.path.splitext(fn)[0] + '.txt', 'a')
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_circle)
    while(True):
        global downFlag, drawing, drawed
        downFlag = False #当点击鼠标右键时变为True，退出绘制，关闭当前图片
        cv2.imshow(window_name, image)
        cv2.waitKey(255)
        if drawed == True:
            dw = 1.0 / width
            dh = 1.0 / height
            x = (ix + ox) / 2.0
            y = (iy + oy) / 2.0    
            x = x * dw # center of box-x
            y = y * dh # center of box-y
            w = (ox - ix) * dw # width of box
            h = (oy - iy) * dh # height of box
            image_rect = '0 %s' % x + ' ' + '%s' % y + ' ' + '%s' % w + ' ' + '%s' % h + '\n' #此处0代表该类目标的序号
            label.write(image_rect)
            drawed = False
        #当downFlag为True时，表示当前图片标记结束
        if downFlag == True:
            break
    cv2.destroyWindow(window_name)
