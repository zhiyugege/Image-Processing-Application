import cv2
import numpy as np
import time

def minifilter(img):
    index = img
    shape = img.shape
    height = shape[0]
    width = shape[1]
    for i in range(0,2):
        top_pixel = index[[0]+[i for i in range(height-1)],:]
        bottom_pixel = index[[i for i in range(1,height)]+[height-1],:]
        left_pixel = index[:,[0]+[i for i in range(width-1)]]
        right_pixel = index[:,[i for i in range(1,width)]+[width-1]]
        res = np.minimum(index,top_pixel)
        res = np.minimum(res,bottom_pixel)
        res = np.minimum(res,left_pixel)
        res = np.minimum(res,right_pixel)
        index = res
    return res

def guidedfilter(I,P,r=81,eps=0.001):
    
    m_I = cv2.boxFilter(I, -1, (r,r))  
    m_p = cv2.boxFilter(P, -1, (r,r))  
    m_Ip = cv2.boxFilter(I*P, -1, (r,r))  
    cov_Ip = m_Ip-m_I*m_p  
    m_II = cv2.boxFilter(I*I, -1, (r,r))  
    var_I = m_II-m_I*m_I  
    a = cov_Ip/(var_I+eps)  
    b = m_p-a*m_I  
    m_a = cv2.boxFilter(a, -1, (r,r))  
    m_b = cv2.boxFilter(b, -1, (r,r))  
    return m_a*I+m_b  

def getA(img, guided_res):
    
    guided_res_pre = guided_res.copy()
    size = guided_res.size
    max_size = size-int(size*0.001)
    guided_res_br = guided_res.reshape(size)
    guided_res_br.sort()
    _max = guided_res_br[max_size]
    A = np.min(img,2)[guided_res_pre>_max].max()
    t = 1-0.95*guided_res_pre/A
    t = np.maximum(t,0.1)
    return t,A

def main():
    
    img = cv2.imread('./static/example/hanse.png')
    pre = (img/255.0).astype(np.float)
    img = np.min(img,2)
    img = (img/255.0).astype(np.float)

    res = minifilter(img)
    guided_res = guidedfilter(img,res)
    guided = guided_res.copy()
    pre_img = pre.copy()
    t, A = getA(pre_img,guided)
    clear = np.zeros(pre.shape)
    for i in range(0,3):
        clear[:,:,i] = (pre[:,:,i]-A)/t+A
    clear = np.clip(clear, 0,1)
    final_img = (clear*255).astype(np.uint8)
    _time = str(int(time.time()))
    _str = './static/image/'+_time+'.png'
    cv2.imwrite(_str,final_img)
    return _time





