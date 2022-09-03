# --- utf-8 ---
# --- function: 将Labeling标注的格式转化为Labelme标注格式，并读取imageData ---
 
import os
import xml.etree.ElementTree as ET
import json
from base64 import b64encode
 
 
 
def get(root, name):
    return root.findall(name)
 
 
# 检查读取xml文件是否出错
def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not fing %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars
 
 
 
def xml2json(img_map, json_path, xml_path, img_path):
    for img_file in img_map:
        json_filename = os.path.join(json_path , img_file + ".json")
        xml_filename = os.path.join(xml_path,img_file+".xml")
        img_filename = os.path.join(img_path,img_file+img_map[img_file])
        # 定义通过Labelme标注后生成的json文件
        json_dict = {"version": "4.6.0", "flags": {}, "shapes": [], "imagePath": "", "imageData": None,
                    "imageHeight": 0, "imageWidth": 0}
    
        json_dict["imagePath"] = img_filename
    
        tree = ET.parse(xml_filename)  # 读取xml文件
    
        root = tree.getroot()
    
        size = get_and_check(root, 'size', 1)  # 读取xml中<>size<>字段中的内容
    
        # 读取二进制图片，获得原始字节码
        with open(img_filename, 'rb') as jpg_file:
            byte_content = jpg_file.read()
    
        # 把原始字节码编码成base64字节码
        base64_bytes = b64encode(byte_content)
    
        # 把base64字节码解码成utf-8格式的字符串
        base64_string = base64_bytes.decode('utf-8')
    
        # 用字典的形式保存数据
        json_dict["imageData"] = base64_string
    
        # 获取图片的长宽信息
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
    
        json_dict["imageHeight"] = height
        json_dict["imageWidth"] = width
    
        # 当标注中有多个目标时全部读取出来
        for obj in get(root, 'object'):
            # 定义图片的标注信息
            img_mark_inf = {"label": "", "points": [], "group_id": None, "shape_type": "rectangle", "flags": {}}
    
            category = get_and_check(obj, 'name', 1).text  # 读取当前目标的类别
    
            img_mark_inf["label"] = category
    
            bndbox = get_and_check(obj, 'bndbox', 1)  # 获取标注宽信息
    
            xmin = float(get_and_check(bndbox, 'xmin', 1).text)
            ymin = float(get_and_check(bndbox, 'ymin', 1).text)
            xmax = float(get_and_check(bndbox, 'xmax', 1).text)
            ymax = float(get_and_check(bndbox, 'ymax', 1).text)
    
            img_mark_inf["points"].append([xmin, ymin])
            img_mark_inf["points"].append([xmin, ymax])
            img_mark_inf["points"].append([xmax, ymax])
            img_mark_inf["points"].append([xmax, ymin])
    
            json_dict["shapes"].append(img_mark_inf)
    
        save = json_filename  # json文件的路径地址
    
        json_fp = open(save, 'w')  #
        json_str = json.dumps(json_dict, indent=2)  # 缩进，不需要的可以将indent=4去掉
    
        json_fp.write(json_str)  # 保存
        json_fp.close()
 
 
 


json_path = "new/json/"
xml_path = "new/xml/"  
img_path = 'init/img/'

if not os.path.exists(json_path):
    os.makedirs(json_path)

img_map ={}
for file in os.listdir(img_path):
    prefix,surfix = os.path.splitext(file.strip())
    if surfix[1:].lower() in ['png', 'jpg', 'jpeg']:
        img_map[prefix] = surfix

xml2json(img_map, json_path, xml_path, img_path)