# !/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import json

#这里写你自己的存放照片和json文件的路径
json_dir = 'new/json/'
json_files = os.listdir(json_dir)
print(json_files)
#这里写你要删除的标签名
delete_name = "person"

for json_file in json_files:
    json_file_ext = os.path.splitext(json_file)

    if json_file_ext[1] == '.json':
    #判断是否为json文件
        jsonfile = json_dir + json_file
        print(jsonfile)

        with open(jsonfile,'r',encoding = 'utf-8') as jf:
            info = json.load(jf)
            print(1)
            
            for i,label in enumerate(info['shapes']):
                if info['shapes'][i]['label'] == delete_name:
                    del info['shapes'][i]
                    # 找到位置进行删除
            # 使用新字典替换修改后的字典
            json_dict = info
        
        # 将替换后的内容写入原文件 
        with open(jsonfile,'w') as new_jf:
            json.dump(json_dict,new_jf, indent=2)
        jf.close()
        new_jf.close()
    
print('delete label over!')
