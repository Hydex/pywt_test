#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
对于各种频率的子带宽都显示出来 
文字区域应该在以下三种 : LH, HL, HH 
'''
import cv2
import os,sys
from PIL import Image  # PIL
import numpy
import pylab
from pywt import WaveletPacket2D

'''
im = Image.open("data/na.png").convert('L')
arr = numpy.fromstring(im.tostring(), numpy.uint8)
arr.shape = (im.size[1], im.size[0])
'''

arr = cv2.imread("data/font.png")
arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

#WaveletPacket2D 只能处理灰度 图片所以arr应该先转换
wp2 = WaveletPacket2D(arr, 'db2', 'sym', maxlevel=2)


pylab.imshow(arr, interpolation="nearest", cmap=pylab.cm.gray)

path = ['d', 'v', 'h', 'a']

#mod = lambda x: x
#mod = lambda x: abs(x)
mod = lambda x: numpy.sqrt(abs(x))


'''
pylab.figure()
for i, p2 in enumerate(path):
    pylab.subplot(2, 2, i + 1)
    p1p2 = p2
    pylab.imshow(mod(wp2[p1p2].data), origin='image', interpolation="nearest",
        cmap=pylab.cm.gray)
    pylab.title(p1p2)

for p1 in path:
    pylab.figure()
    for i, p2 in enumerate(path):
        pylab.subplot(2, 2, i + 1)
        p1p2 = p1 + p2
        pylab.imshow(mod(wp2[p1p2].data), origin='image',
            interpolation="nearest", cmap=pylab.cm.gray)
        pylab.title(p1p2)
'''

pylab.figure()
i = 1
#最大也只有两层2
for row in wp2.get_level(2, 'freq'):
    for node in row:
        
        #只找出与文字相似的高频图 LH, HL, HH 
        tuples = (node.path,) + wp2.expand_2d_path(node.path) # ('av', 'lh', 'll')
        if 'll' not in tuples:
            pylab.subplot(len(row), len(row), i)
            pylab.title(":::%s=(%s row, %s col)" % ((node.path,) + wp2.expand_2d_path(node.path)))
            
            pylab.imshow(mod(node.data), 
                         origin='image', 
                         interpolation="nearest",
                         cmap=pylab.cm.gray)
            i += 1

pylab.show()
