import cv2
import numpy as np
import os
import random
import time
def lightness(img, a):

    res = np.uint8(np.clip(img*(a/10.0), 0, 255))
    return res

def contrast(img, a):

    res = img.copy()
    row,col = img.shape[:2]
    b_arr = res[:,:,0].reshape(row*col)
    g_arr = res[:,:,1].reshape(row*col)
    r_arr = res[:,:,2].reshape(row*col)
    b_arr.sort()
    g_arr.sort()
    r_arr.sort()
    mid_b = b_arr[int(row*col/2)]
    mid_g = g_arr[int(row*col/2)]
    mid_r = r_arr[int(row*col/2)]
    per_all = (mid_b+mid_g+mid_r)/3
    a=a/100
    print(a)
    res = np.uint8(np.clip(img+(img-per_all)*(a-1), 0, 255))
    return res

def Saturation(img, a):

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float)
    hsv_img[:,:,1] = hsv_img[:,:,1]+float(a-100)
    hsv_img[hsv_img > 255] = 255
    hsv_img[hsv_img < 0] = 0
    res = cv2.cvtColor(np.round(hsv_img).astype(np.uint8), cv2.COLOR_HSV2BGR)

    return res

def change(br_value,sat_value,co_value):
    img=cv2.imread('./static/example/new.jpeg')
    img = np.array(img)
    res = lightness(img, br_value)
    res = contrast(res, co_value)
    res = Saturation(res, sat_value)
    _time = str(int(time.time()))
    _str = './static/image/'+_time+'.jpeg'
    cv2.imwrite(_str,res)
    return _time

