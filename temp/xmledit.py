import xml.etree.cElementTree as ET
import os
import glob
import json
import copy

def count_xml_num(indir):

    # 提取xml文件列表
    annotations = glob.glob(os.path.join(indir) + '*.xml')

    dict = {} # 新建字典，用于存放各类标签名及其对应的数目
    label_set = set()
    for i, file in enumerate(annotations): # 遍历xml文件
       
        # actual parsing
        in_file = open(file, encoding = 'utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()

        # 遍历文件的所有标签
        for obj in root.iter('object'):
            name = obj.find('name').text
            if(name in label_set): 
                dict[name] += 1 # 如果标签不是第一次出现，则+1
            else: 
                label_set.add(name)
                dict[name] = 1 # 如果标签是第一次出现，则将该标签名对应的value初始化为1

    # 保存结果
    file = open('xml_label_counts.txt', 'w',encoding='utf-8')
    for key in dict.keys(): 
        file.write(key + ': ' + str(dict[key]) + '\n')  
    file.close()

def count_json_num(indir):

    # 提取xml文件列表
    annotations = glob.glob(os.path.join(indir) + '*.json')

    dict = {} # 新建字典，用于存放各类标签名及其对应的数目
    label_set = set()
    for i, file in enumerate(annotations): # 遍历xml文件
       
        # actual parsing
        json_init = open(file,'r',encoding='utf-8')
        info = json.load(json_init)

        # 遍历文件的所有标签
        for i, label in enumerate(info['shapes']):
            name = info['shapes'][i]['label']
            if(name in label_set): 
                dict[name] += 1 # 如果标签不是第一次出现，则+1
            else: 
                label_set.add(name)
                dict[name] = 1 # 如果标签是第一次出现，则将该标签名对应的value初始化为1

    # 保存结果
    file = open('json_label_counts.txt', 'w',encoding='utf-8')
    for key in dict.keys(): 
        file.write(key + ': ' + str(dict[key]) + '\n')  
    file.close()        

def main(PARAM,mode='jsonreplace'):
    xml_input_dir = PARAM["XML_Input_Path"]
    xml_output_dir = PARAM["XML_Output_Path"]
    CLASSES = PARAM["New_Classes_for_Delete"]
    if not os.path.exists(xml_output_dir):
        os.makedirs(xml_output_dir)
    if mode == 'xmldelete':
        for filename in os.listdir(xml_input_dir):
            path_xml = os.path.join(xml_input_dir, filename)
            tree = ET.parse(path_xml)
            root = tree.getroot()
    
            for child in root.findall('object'):
                name = child.find('name').text
                if name in CLASSES:
                    root.remove(child)
    
            tree.write(os.path.join(xml_output_dir, filename))
            print(filename+' is done')
    elif mode == 'xmlreplace':
        for filename in os.listdir(xml_input_dir):
            path_xml = os.path.join(xml_input_dir, filename)
            tree = ET.parse(path_xml)
            root = tree.getroot()
    
            for child in root.findall('object'):
                name = child.find('name').text
                if name in PARAM["Original_Class_for_Replace"]:
                    idx = PARAM["Original_Class_for_Replace"].index(name)
                    child.find('name').text = PARAM["New_Class_for_Replace"][idx]
    
            tree.write(os.path.join(xml_output_dir, filename))
            print(filename+' is done')

    elif mode == 'jsondelete':
        for filename in os.listdir(xml_input_dir):
            json_init = open(os.path.join(xml_input_dir, filename),'r',encoding='utf-8')
            info = json.load(json_init)
            shapes = []
            for i, label in enumerate(info['shapes']):
                # print(filename,i,label)
                if info['shapes'][i]['label'] not in CLASSES:
                # 找到位置进行删除
                
                    shapes.append(info['shapes'][i])
        # 使用新字典替换修改后的字典
            info['shapes'] = shapes
            json_dict = info
    
            json_new = open((os.path.join(xml_output_dir, filename)),'w')
            json.dump(json_dict, json_new, indent=2)

    elif mode == 'jsonreplace':
        for filename in os.listdir(xml_input_dir):
            json_init = open(os.path.join(xml_input_dir, filename),'r',encoding='utf-8')
            info = json.load(json_init)
            for i, label in enumerate(info['shapes']):
                # print(filename,i,label)
                if info['shapes'][i]['label'] in PARAM["Original_Class_for_Replace"]:
                    idx = PARAM["Original_Class_for_Replace"].index(info['shapes'][i]['label'])
                    info['shapes'][i]['label'] = PARAM["New_Class_for_Replace"][idx]
        # 使用新字典替换修改后的字典
            json_dict = info
    
            json_new = open((os.path.join(xml_output_dir, filename)),'w')
            json.dump(json_dict, json_new, indent=2)

PARAM = dict(
    XML_Input_Path = 'init/xml/',
    XML_Output_Path = 'new/xml/',
    New_Classes_for_Delete = ['person'],
    Original_Class_for_Replace = ['car','person'],
    New_Class_for_Replace = ['bilibili','dog']

)

# xml_input_dir = 'init/xml/'
# xml_output_dir = 'new/xml/'
indir='init/json/'   # xml文件所在的目录
# main(PARAM,mode='xmldelete')
count_json_num(indir)