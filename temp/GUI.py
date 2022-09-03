# from cx_Freeze import setup, Executable

# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget,QMessageBox,QFileDialog,QApplication)
# from PyQt5.QtGui import *
from PyQt5.QtCore import (QThread,pyqtSignal)

import sys
import os
from PIL import Image
import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import xml.etree.ElementTree as ET
import json
import cv2

from window import Ui_Form
import config
from labelme import utils

# class LabelThread(QThread):
#     _signal = pyqtSignal()
#     def __init__(self, mode):
#         super().__init__()
#         self.mode = mode
#     def run(self):
#         if self.mode == 'ME':
#             # self._signal.emit()
#             from labelImg import main
#             main()
#             self.close()
#         if self.mode == 'IMG':
#             pass

def loadimg(path):
    img = Image.open(path)
    channels = len(img.split())
    # print(channels)
    if channels in [3,4]:
        array = np.array(img)
        array[:, :, :3] = array[:, :, (2, 1, 0)]
    elif channels == 1:
        # img = img.convert('L')
        array = np.array(img)
    return array

class dfThread(QThread):
    _signal = pyqtSignal(int,int)
    def __init__(self, show_flag,finalfunc,total,mode):
        super().__init__()
        self.show_flag = show_flag
        self.finalfunc = finalfunc
        self.total = total
        self.mode = mode

    def run(self):
        if self.mode == 1:
            new_bndbox_list = []
            for root, sub_folders, files in os.walk(config.DATAAUGMENTATION["IMGset_Input_Path"]):
                # total = len(files)
                # self.progressBar.setMaximum(total)
                for l,name in enumerate(files):
                    bndbox = read_xml_annotation(config.DATAAUGMENTATION["XML_Input_Path"], name[:-4] + '.xml')

        #             for epoch in range(AUGLOOP):
                    seq = iaa.Sequential(self.finalfunc).to_deterministic()

                    # 读取图片
                    # img = ia.imageio.imread(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name))#np.asarray(Image.open(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name)))
                    # img = cv2.imread(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name),-1)
                    img = loadimg(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name))
                    new_box = []
                    # bndbox 坐标增强
                    for i in range(len(bndbox)):
                        bbs = ia.BoundingBoxesOnImage([
                            ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                        ], shape=img.shape)

                        image_aug,bbs_aug = seq(image=img,bounding_boxes=bbs)#seq_det.augment_bounding_boxes([bbs])[0]
                        new_box.append(bbs_aug)
                        # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                        n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                        n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                        n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                        n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                        # if n_x1 == 1 and n_x1 == n_x2:
                        #     n_x2 += 1
                        # if n_y1 == 1 and n_y2 == n_y1:
                        #     n_y2 += 1
                        # if n_x1 >= n_x2 or n_y1 >= n_y2:
                        #     print('error', name)
                        new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])
                    # 存储变化后的图片
                    path = os.path.join(config.DATAAUGMENTATION["Output_Path"],'img', config.DATAAUGMENTATION["Output_Init_Num"].zfill(6) + name[-4:])
                    
                    if self.show_flag:
                        image_after = image_aug
                        for k in new_box: 
                            try:
                                image_after = k.draw_on_image(image_after, size=3)
                            except Exception as reason:
                                QMessageBox.warning(self, 'Warning', str(reason))
                        cv2.imshow('augx',image_after)
                        # cv2.imshow('augx',cv2.cvtColor(image_after,cv2.COLOR_BGR2RGB))
                        cv2.waitKey(300)
                        # cv2.destroyWindow('augx')
                    cv2.imwrite(path,image_aug)
                    
                    # 存储变化后的XML
                    change_xml_list_annotation(config.DATAAUGMENTATION["XML_Input_Path"], name[:-4], new_bndbox_list, os.path.join(config.DATAAUGMENTATION["Output_Path"] , 'xml'),
                                            config.DATAAUGMENTATION["Output_Init_Num"].zfill(6),name[-4:])
                    config.DATAAUGMENTATION["Output_Init_Num"] = str(int(config.DATAAUGMENTATION["Output_Init_Num"])+1)
                    self._signal.emit(l+1,self.total)
                    new_bndbox_list = []
                if self.show_flag:
                    cv2.destroyWindow('augx')
                # QMessageBox.about(self,"","已完成")
                # self.exit(0)
        
        if self.mode == 2:
            for root, sub_folders, files in os.walk(config.DATAAUGMENTATION["IMGset_Input_Path"]):
                for l,name in enumerate(files):
                    file = open(os.path.join(config.DATAAUGMENTATION["XML_Input_Path"],name[:-4] + '.json'),'rb')
                    json_file = json.load(file)

        #             for epoch in range(AUGLOOP):
                    seq = iaa.Sequential(self.finalfunc).to_deterministic()

                    # 读取图片
                    # img = ia.imageio.imread(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name))#np.asarray(Image.open(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name)))
                    # img = cv2.imread(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name),-1)
                    img = loadimg(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name))
                    new_point = []
                    # bndbox 坐标增强
                    ii = 0
                    class_num = len(json_file['shapes'])
                    while ii < class_num:
                        temp = []
                        for j in json_file['shapes'][ii]['points']:
                            temp.append(ia.Keypoint(x=j[0],y=j[1]))
                        kps = ia.KeypointsOnImage(temp,shape=img.shape)
                        image_aug,kps_aug = seq(image=img,keypoints=kps)
                        jj = 0

                        for j in range(len(kps_aug)):
                            x,y = float(kps_aug[j].x),float(kps_aug[j].y)
                            if float(kps_aug[j].x) <= 0:
                                x = 1
                            elif float(kps_aug[j].x) > img.shape[1]:
                                x = img.shape[1]

                            if float(kps_aug[j].y) <= 0:
                                y = 1
                            elif float(kps_aug[j].y) > img.shape[0]:
                                y = img.shape[0]

                            if x == 1 or x == img.shape[1] or y==1 or y==img.shape[0]:
                                jj+=1
                            json_file['shapes'][ii]['points'][j] = [x,y]
                        if jj == len(kps_aug):
                            del json_file['shapes'][ii]
                            ii -= 1
                            class_num -= 1
                            
                        ii += 1
                        new_point.append(kps_aug)
                        
                    # 存储变化后的图片
                    path = os.path.join(config.DATAAUGMENTATION["Output_Path"],'img', config.DATAAUGMENTATION["Output_Init_Num"].zfill(6) + name[-4:])
                    
                    if self.show_flag:
                        image_after = image_aug
                        for k in new_point: 
                            image_after = k.draw_on_image(image_after, size=7)
                        cv2.imshow('augp',image_after)
                        # cv2.imshow('augp',cv2.cvtColor(image_after,cv2.COLOR_BGR2RGB))
                        cv2.waitKey(300)
                        # cv2.destroyWindow('augp')
                    cv2.imwrite(path,image_aug)
                    
                    # 存储变化后的json
                    with open(os.path.join(config.DATAAUGMENTATION["Output_Path"] , 'json' , config.DATAAUGMENTATION["Output_Init_Num"].zfill(6)+ '.json'),'w') as f:
                        json_file['imageData'] = str(utils.img_arr_to_b64(image_aug[...,(2,1,0)]),encoding='utf-8')
                        json_file['imageHeight'] = image_aug.shape[0]
                        json_file['imageWidth'] = image_aug.shape[1]
                        json_file['imagePath'] = path
                        json.dump(json_file,f,indent=2)
                    config.DATAAUGMENTATION["Output_Init_Num"] = str(int(config.DATAAUGMENTATION["Output_Init_Num"])+1)
                    self._signal.emit(l+1,self.total)
                    new_point = []
                if self.show_flag:
                    cv2.destroyWindow('augp')
            
        if self.mode == 3:
            for root, sub_folders, files in os.walk(config.DATAAUGMENTATION["IMGset_Input_Path"]):
                files.sort()
                print(files)
                for l,name in enumerate(files):
                    seq = iaa.Sequential(self.finalfunc).to_deterministic()
                    # 读取图片
                    # img = ia.imageio.imread(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name))
                    # img = cv2.imread(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name),-1)
                    img = loadimg(os.path.join(config.DATAAUGMENTATION["IMGset_Input_Path"], name))

                    # 存储变化后的图片
                    image_aug = seq.augment_images([img])[0]
        #             path = os.path.join(AUG_IMG_DIR, name[:-4] + '_' + str(epoch) + '.jpg')
                    path = os.path.join(config.DATAAUGMENTATION["Output_Path"],'img', config.DATAAUGMENTATION["Output_Init_Num"].zfill(6) + name[-4:])
                    # image_auged = bbs.draw_on_image(image_aug)
                    cv2.imwrite(path,image_aug)

                    config.DATAAUGMENTATION["Output_Init_Num"] = str(int(config.DATAAUGMENTATION["Output_Init_Num"])+1)
                    self._signal.emit(l+1,self.total)

        

def read_xml_annotation(root, image_id):
    bndboxlist = []
    try:
        in_file = open(os.path.join(root, image_id),encoding='utf-8')
    except:
        return bndboxlist
    tree = ET.parse(in_file)
    root = tree.getroot()


    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(float(bndbox.find('xmin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymin = int(float(bndbox.find('ymin').text))
        ymax = int(float(bndbox.find('ymax').text))

        bndboxlist.append([xmin, ymin, xmax, ymax])

    return bndboxlist


def change_xml_annotation(root, image_id, new_target):
    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    in_file = open(os.path.join(root, str(image_id) + '.xml'),encoding='utf-8')  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str("%06d" % str(id) + '.xml')))


def change_xml_list_annotation(root, image_id, new_target, saveroot, _id, surfix):
    try:
        in_file = open(os.path.join(root, str(image_id) + '.xml'),encoding='utf-8')  # 这里root分别由两个意思
    except:
        return 
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    if tree.find('filename') is not None:
        elem = tree.find('filename')
        elem.text = _id + surfix
    else:
        element = ET.Element(
            'filename')
        element.text = _id + surfix
        # tree.getroot().append(element)
        # elem = element.set(_id + surfix)
        # elem.text = _id + surfix
        xmlroot.insert(0,element)
    index = 0

    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        if new_target[index][0] == 1 and new_target[index][0] == new_target[index][2]:
            xmlroot.remove(object)
            continue
        if new_target[index][1] == 1 and new_target[index][1] == new_target[index][3]:
            xmlroot.remove(object)
            continue
        if new_target[index][0] >= new_target[index][2] or new_target[index][1] >= new_target[index][3]:
            xmlroot.remove(object)
            # print('error',image_id)
            continue
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, _id + '.xml'))


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False

class MainWin(QWidget, Ui_Form):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.finalfunc = []
        self.show()
      
    #     # load button
        self.pushButton.clicked.connect(lambda: self.load("IMG_Path"))
        self.pushButton_2.clicked.connect(lambda: self.load("B_IMG_Path"))
        self.pushButton_3.clicked.connect(lambda: self.load("B_XML_Path"))
        self.pushButton_4.clicked.connect(lambda: self.load("Output_Path"))
        
    #     # confirm button
        self.pushButton_5.clicked.connect(lambda: self.confirm("Data_aug"))
        
    #     # function button
        self.pushButton_6.clicked.connect(lambda: self.func("Single"))
        self.pushButton_7.clicked.connect(lambda: self.func("Batch"))
        #self.pushButton_8.clicked.connect(lambda: self.func("Labelme"))
        #self.pushButton_9.clicked.connect(lambda: self.func("Labelimg"))

    def progressinfo(self,value,num):
        self.progressBar.setValue(value)
        if value == num:
            self.progressBar.setValue(0)
            QMessageBox.about(self,"","已完成")
    
    # def Single(self):
    #     img = ia.imageio.imread(config.DATAAUGMENTATION["IMG_Path"])#np.asarray(Image.open(config.DATAAUGMENTATION["IMG_Path"]))
    #     seq = iaa.Sequential(self.finalfunc)
    #     img_aug = seq(image=img)
    #     ia.imshow(img_aug)
    #     self.finalfunc = []
    #     QMessageBox.about(self,"","已完成")
        
    # def Error(self):
    #     QMessageBox.critical(self,"错误","请勿同时勾选XML与JSON")
    #     return
    
    # def Batch_XML(self):
    #     mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'img'))
    #     mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'xml'))
    #     self.dfThread = dfThread(self.show_flag,self.finalfunc)
    #     self.dfThread._signal.connect(self.progressinfo)
    #     self.dfThread.start()
        
    #     # self.progressBar.setValue(0)
    #     self.finalfunc = []
    #     QMessageBox.about(self,"","已完成")

    def func(self,name):           
        if name == "Single":
            # img = cv2.imread(config.DATAAUGMENTATION["IMG_Path"],-1)#np.asarray(Image.open(config.DATAAUGMENTATION["IMG_Path"]))
            img = loadimg(config.DATAAUGMENTATION["IMG_Path"])
            seq = iaa.Sequential(self.finalfunc)
            img_aug = seq(image=img)
            cv2.imshow('show',img_aug)
            self.finalfunc = []
            QMessageBox.about(self,"","已完成")
            return
            
        if name == "Batch" and self.xml_batch and self.json_batch:
            QMessageBox.critical(self,"错误","请勿同时勾选XML与JSON")
            return
        if name == "Batch" and self.img_only and (self.json_batch or self.xml_batch):
            QMessageBox.critical(self,"错误","请确认批量操作方式")
            return
        if name == "Batch" and not self.img_only and len(config.DATAAUGMENTATION["XML_Input_Path"]) == 0:
            QMessageBox.critical(self,"错误","请选择标注路径")
            return
        if name == "Batch" and self.xml_batch and not self.img_only:
            mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'img'))
            mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'xml'))
            total = len(os.listdir(config.DATAAUGMENTATION["IMGset_Input_Path"]))
            self.progressBar.setMaximum(total)
            self.dfThread = dfThread(self.show_flag,self.finalfunc,total,1)
            self.dfThread._signal.connect(self.progressinfo)
            self.dfThread.start()
            
            # self.progressBar.setValue(0)
            self.finalfunc = []
            
            
        # 批量操作
        if name == "Batch" and self.json_batch and not self.img_only:
            mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'img'))
            mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'json'))
            total = len(os.listdir(config.DATAAUGMENTATION["IMGset_Input_Path"]))
            self.progressBar.setMaximum(total)
            self.dfThread = dfThread(self.show_flag,self.finalfunc,total,2)
            self.dfThread._signal.connect(self.progressinfo)
            self.dfThread.start()
            self.finalfunc = []
            
            
        if name == "Batch" and not self.xml_batch and not self.json_batch and self.img_only:
            mkdir(os.path.join(config.DATAAUGMENTATION["Output_Path"],'img'))
            total = len(os.listdir(config.DATAAUGMENTATION["IMGset_Input_Path"]))
            self.progressBar.setMaximum(total)
            self.dfThread = dfThread(self.show_flag,self.finalfunc,total,3)
            self.dfThread._signal.connect(self.progressinfo)
            self.dfThread.start()
            self.finalfunc = []
             
        
    def load(self,filename):
    
        if filename == "IMG_Path":
            config.DATAAUGMENTATION["IMG_Path"], _  = QFileDialog.getOpenFileName(self, 'Open file', './',"Image files (*.jpg *.png)")
            self.lineEdit.setText(config.DATAAUGMENTATION["IMG_Path"])
        
        if filename == "B_IMG_Path":
            config.DATAAUGMENTATION["IMGset_Input_Path"] = QFileDialog.getExistingDirectory(self, 'Open file', './')
            self.lineEdit_2.setText(config.DATAAUGMENTATION["IMGset_Input_Path"])    
            
        if filename == "B_XML_Path":
            config.DATAAUGMENTATION["XML_Input_Path"] = QFileDialog.getExistingDirectory(self, 'Open file', './')
            self.lineEdit_3.setText(config.DATAAUGMENTATION["XML_Input_Path"])
            
        if filename == "Output_Path":
            config.DATAAUGMENTATION["Output_Path"] = QFileDialog.getExistingDirectory(self, 'Open file', './')
            self.lineEdit_4.setText(config.DATAAUGMENTATION["Output_Path"])
            
    def confirm(self,function):
        if function == "Data_aug":
            self.augflag = [self.checkBox.isChecked(),self.checkBox_2.isChecked(),
                            self.checkBox_3.isChecked(),self.checkBox_4.isChecked(),
                            self.checkBox_5.isChecked(),self.checkBox_6.isChecked(),
                            self.checkBox_7.isChecked(),self.checkBox_8.isChecked(),
                            self.checkBox_9.isChecked(),self.checkBox_10.isChecked(),
                            self.checkBox_11.isChecked(),self.checkBox_12.isChecked(),
                            self.checkBox_13.isChecked(),self.checkBox_14.isChecked(),
                            self.checkBox_15.isChecked(),self.checkBox_16.isChecked(),
                            self.checkBox_17.isChecked(),self.checkBox_18.isChecked(),
                            self.checkBox_19.isChecked(),self.checkBox_20.isChecked(),
                            self.checkBox_21.isChecked(),self.checkBox_22.isChecked(),
                            self.checkBox_23.isChecked(),self.checkBox_24.isChecked(),]
            
            self.augfunc = [iaa.Add((-50,50)),
                            iaa.AdditiveGaussianNoise(scale=(0,0.2*255)), 
                            iaa.Cutout(nb_iterations=(1, 5),fill_mode="constant",cval=(0,255)), 
                            iaa.Dropout(p=(0,0.3)),
                            iaa.Salt(p=(0.1,0.5)),
                            iaa.Cartoon(),
                            iaa.BlendAlphaHorizontalLinearGradient(iaa.AveragePooling(11),start_at=(0.0,1.0),end_at=(0.0,1.0)),
                            iaa.GaussianBlur(sigma=(0.0,3.0)),
                            iaa.MotionBlur(k=(5,15),angle=[-45,45]),
                            iaa.ChangeColorTemperature((1100,10000)),
                            iaa.CLAHE(),
                            iaa.flip.HorizontalFlip(),
                            iaa.flip.VerticalFlip(),
                            iaa.Affine(scale=(0.5, 1.5)),
                            iaa.Affine(scale={"x": (0.5, 1.5), "y": (0.5, 1.5)}),
                            iaa.Affine(translate_px={"x": (-20, 20), "y": (-20, 20)}),
                            # iaa.Affine(translate_px={"x": -500, "y": (-20, 20)}),
                            iaa.WithColorspace(to_colorspace="HSV",from_colorspace="RGB",children=iaa.WithChannels(0,iaa.Add((0, 50)))),
                            iaa.PerspectiveTransform(scale=(0.01, 0.20)),
                            iaa.pillike.Autocontrast((10, 20), per_channel=True),
                            iaa.pillike.FilterEdgeEnhance(),
                            iaa.pillike.EnhanceBrightness(),
                            iaa.MaxPooling([2, 8]),
                            iaa.AveragePooling([2, 8]),
                            iaa.CropAndPad(percent=(-0.25, 0.25))]
            
            for i,j in enumerate(self.augflag):
                if j:
                    self.finalfunc.append(self.augfunc[i])
            if len(self.lineEdit_5.text()) != 0:
                config.DATAAUGMENTATION["Output_Init_Num"] = self.lineEdit_5.text()
            if len(self.lineEdit_5.text()) == 0:
                config.DATAAUGMENTATION["Output_Init_Num"] = '1'
            self.img_only = self.checkBox_25.isChecked()
            self.xml_batch = self.checkBox_26.isChecked()
            self.json_batch = self.checkBox_27.isChecked()
            self.show_flag = self.checkBox_28.isChecked()
                
            QMessageBox.about(self,"","您已确认")
                  
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWin()
    sys.exit(app.exec_())