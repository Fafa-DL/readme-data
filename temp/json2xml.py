import os
import numpy as np
import codecs
import json
from glob import glob
import cv2
import random
seed = np.random.randint(2**31)
random.seed(seed)
np.random.seed(seed)

def json2xml(img_map, json_path, xml_path, img_path):
    for img_file in img_map:
        json_filename = os.path.join(json_path , img_file + ".json")
        xml_filename = os.path.join(xml_path,img_file+".xml")
        img_filename = os.path.join(img_path,img_file+img_map[img_file])
        json_file = json.load(open(json_filename,"r",encoding="utf-8"))
        height, width, channels = cv2.imread(img_filename).shape
        with codecs.open(xml_filename,"w","utf-8") as xml:
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + 'img' + '</folder>\n')
            xml.write('\t<filename>' + img_file+img_map[img_file] + '</filename>\n')
            xml.write('\t<path>' + img_filename + '</path>\n')
            xml.write('\t<source>\n')
            xml.write('\t\t<database>Unknown</database>\n')
            # xml.write('\t\t<annotation>UAV AutoLanding</annotation>\n')
            # xml.write('\t\t<image>flickr</image>\n')
            # xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t</source>\n')
            # xml.write('\t<owner>\n')
            # xml.write('\t\t<flickrid>NULL</flickrid>\n')
            # xml.write('\t\t<name>ChaojieZhu</name>\n')
            # xml.write('\t</owner>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>'+ str(width) + '</width>\n')
            xml.write('\t\t<height>'+ str(height) + '</height>\n')
            xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
            xml.write('\t</size>\n')
            xml.write('\t\t<segmented>0</segmented>\n')
            for multi in json_file["shapes"]:
                points = np.array(multi["points"])
                xmin = int(min(points[:,0]))
                xmax = int(max(points[:,0]))
                ymin = int(min(points[:,1]))
                ymax = int(max(points[:,1]))
                label = multi["label"]
                if xmax <= xmin:
                    pass
                elif ymax <= ymin:
                    pass
                else:
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>'+label+'</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    xml.write('\t\t<truncated>0</truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
            xml.write('</annotation>')


json_path = "init/json/"
xml_path = "new/xml/"  
img_path = 'init/img/'

if not os.path.exists(xml_path):
    os.makedirs(xml_path)

img_map ={}
for file in os.listdir(img_path):
    prefix,surfix = os.path.splitext(file.strip())
    if surfix[1:].lower() in ['png', 'jpg', 'jpeg']:
        img_map[prefix] = surfix

json2xml(img_map,json_path,xml_path,img_path)