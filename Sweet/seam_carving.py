import numpy as np
import cv2
import time
from functools import wraps



class SeamCarving():
    def __init__(self):
        self.img = cv2.imread('./static/example/seam.jpeg')
        self.width = -1
        self.height = -1
    
    def getEnergyOut(self):
        
        img = self.img
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.int)
        shape = img_gray.shape
        width = shape[0]
        height = shape[1]
        self.width = width
        self.height = height
        x = cv2.Sobel(img,cv2.CV_16S,1,0)  
        y = cv2.Sobel(img,cv2.CV_16S,0,1)  
        absX = cv2.convertScaleAbs(x)   
        absY = cv2.convertScaleAbs(y)  
        energy_out = cv2.addWeighted(absX,0.5,absY,0.5,0)
        energy_out = cv2.cvtColor(energy_out, cv2.COLOR_BGR2GRAY).astype(np.int)
        return energy_out
#    
    def getSeam(self, energy_out):
        
        width = self.width
        height = self.height
        tmp = np.zeros((height,3))
        index = (np.zeros(width)+9999).astype(np.int)
        energy_out = np.insert(energy_out, 0, index, axis=1)
        energy_out = np.insert(energy_out, height, index, axis=1)
        tmp[...,0] = energy_out[0][0:height]
        tmp[...,1] = energy_out[0][1:height+1]
        tmp[...,2] = energy_out[0][2:height+2]
        for i in range(1,width):
            
            min_arr = tmp.min(1).astype(np.int)
            energy_out[i][1:height+1] = energy_out[i][1:height+1] + min_arr
            tmp = np.zeros((height,3))
            tmp[...,0] = energy_out[i][0:height]
            tmp[...,1] = energy_out[i][1:height+1]
            tmp[...,2] = energy_out[i][2:height+2]

        energy_out = np.delete(energy_out, 0, axis=1)
        energy_out = np.delete(energy_out, -1, axis=1)
        seam_sorted = energy_out[width-1]
        return seam_sorted,energy_out
    
    def updateSeamAndImage(self, size):
        
        energy_out = self.getEnergyOut()
        img = self.img
        img = img.tolist()
        width = self.width
        height = self.height
        for k in range(0,size):
            seam_sorted,seam_energy = self.getSeam(energy_out)
            mini,pos = self.getMiniPos(seam_sorted)
            img[width-1].remove(img[width-1][pos])
            for i in range(width-2,-1,-1):
                
                pos = self.findSeam(pos,height,seam_energy[i])      
                img[i].remove(img[i][pos])
            
            height = height-1
            self.height = self.height-1
            self.img = np.array(img).astype(np.uint8)
            energy_out = self.getEnergyOut()
        
    
    
    def seamCarving(self,width,height):
        self.updateSeamAndImage(width)
        self.img = np.rot90(self.img)  
        self.updateSeamAndImage(height)
        self.img = np.rot90(self.img)
        self.img = np.rot90(self.img)
        self.img = np.rot90(self.img)
        _time = str(int(time.time()))
        _str = './static/image/'+_time+'.jpeg'
        cv2.imwrite(_str,self.img)
        return _time        
        
    
        
    def findSeam(self, pos, height, seam_energy):
        
        if pos==0:
            new_pos = np.argmin(seam_energy[:pos+2])
        elif pos==height-1:
            new_pos = np.argmin(seam_energy[pos-1:])
        else:
            new_pos = np.argmin(seam_energy[pos-1:pos+2])
        return new_pos
            
    def getMiniPos(self, _arr):
        
        index = _arr
        index = np.array(index)
        _min = np.min(index)
        pos = np.where(index==np.min(index))
        return _min, pos[0][-1]



