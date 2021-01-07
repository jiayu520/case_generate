import json


def write_data(res,json_file):
    '''把处理后的参数写入json文件'''
    if isinstance(res,dict):
        with open(json_file,'w',encoding='utf-8') as f:
            json.dump(res,f,indent=4,ensure_ascii=False)