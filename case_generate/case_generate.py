import requests
import os
from common.operation_excel import Write_excel  # 写入excel模块
from common.logger import Log  # 打印日志模块
from common.processing_json import write_data  # 写入json文件模块
# from common.difference import diff_excel, diff_json
# from common import read_config


excel_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data_new' + '\\demo_api.xlsx'

json_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\data_new' + '\\CMAPI_data.json'

class AnalysisJson:
    '''swagger自动生成测试用例'''


    def __init__(self,url_json):
        self.url_json = url_json
        r = requests.get(self.url_json + '/swagger/v1/swagger.json').json()
        self.title = r['info']['title']
        write_data(r,'{}.json'.format(self.title)) #创建文件
        self.interface_params = {}
        self.row = 2 #写入Excel起始行数
        self.num = 1 #case id
        global title_list,json_path
        if self.check_data(r):
            self.json_path = os.path.abspath(
                os.path.dirname(
                    os.path.dirname(__file__))) + '\\data_new' + '\\{}_data.json'.format(
                self.title)  # json file path，执行多个url的情况，区分生成的json文件
            self.data = r['paths']  # paths中的数据是有用的
        self.data = r['paths']

    def check_data(self,r):
        '''检查返回的数据是否是字典'''
        if not isinstance(r,dict):
            self.log.info('swagger return json error')
            return False
        else:
            return True

    def retrieve_data(self):
        '''主函数'''
        global body_name,method
        for k,v in self.data.items():
            method_list = []
            for _k,_v in v.items():
                interface = {}
                #if not _v['deprecated']:#接口是否被弃用
                method_list.append(_k)
                api = k #api地址
                if len(method_list) > 1: #api地址下请求方法不止一个的情况
                    for i in range(len(method_list)):
                        body_name = api.replace('/','_') + '_' * i #json文件对应参数名陈，excel中的body名称
                        method = method_list[-1] #请求方法
                else:
                    body_name = api.replace('/','_')
                    method = _k

                self.interface_params = self.retrieve_excel(_v,interface,api)
                #else:
                 #   break
        if self.interface_params:
            write_data(self.interface_params,self.json_path)

    def retrieve_excel(self,_v,interface,api):
        '''解析参数，拼接为字典--准备完成写入Excel的数据'''
        parameters = _v.get('parameters') #获取parameters字段
        if not parameters: #确保参数字典存在
            parameters = {}
        case_name = _v.get('summary','No') #接口作用
        tags = _v['tags'][0] #接口标签
        params_dict = self.retrieve_params(parameters) #处理接口参数，拼成dict形式
        if params_dict and parameters != {}: #单个或多个参数
            interface['row_num'] = self.row #写入Excel时的所在行
            interface['id'] = 'test_' + str(self.num)  #case id
            interface['tags'] = tags  #标签名称
            interface['name'] = case_name
            _type = 'json' #参数获取方式
            interface['method'] = method #请求方式
            interface['url'] = self.url_json + api # 拼接完成接口url
            interface['headers'] = 'yes' #是否传header
            interface['body'] = body_name
            interface['type'] = _type
            self.num += 1
            self.row += 1
            self.interface_params[body_name] = params_dict
            self.write_excel(interface,excel_path) #参数写入Excel
        else: #没有参数
            _type = 'data_old'
            interface['name'] = case_name
            interface['row_num'] = self.row
            interface['id'] = 'test_' + str(self.num)
            interface['tags'] = tags
            interface['method'] = method
            interface['url'] = self.url_json + api
            interface['headers'] = 'yes'
            interface['body'] = ''
            interface['type'] = _type
            self.num += 1
            self.row += 1
            self.interface_params[body_name] = params_dict
            self.write_excel(interface, excel_path)
        return self.interface_params


    def retrieve_params(self,parameters):
        '''处理参数，转为dict'''
        params = ''
        _in = ''
        for each in parameters:
            _in += each.get('in') + '\n' #参数传递位置
            params += each.get('name') + '\n' #参数
        _in = _in.strip('\n')
        _in_list = _in.split('\n')
        params = params.strip('\n')
        params_list = params.split('\n')
        del_list = params_list.copy()
        for i in range(len(_in_list)):
            if _in_list[i] == 'header':
                params_list.remove(del_list[i]) #只保存在body传的参数
        test_list = params_list.copy()
        params_dict = dict(zip(params_list,test_list)) #把list转为dict
        return params_dict

    def write_excel(self,interface,filename):
        '''把字典中的值写入对应的Excel行中'''
        wt = Write_excel(filename)
        try:
            wt.write(interface['row_num'],1,interface['id'])
            wt.write(interface['row_num'], 2, interface['tags'])
            wt.write(interface['row_num'], 3, interface['name'])
            wt.write(interface['row_num'], 4, interface['method'])
            wt.write(interface['row_num'], 5, interface['url'])
            wt.write(interface['row_num'], 7, interface['headers'])
            wt.write(interface['row_num'], 8, interface['body'])
            wt.write(interface['row_num'], 10, interface['type'])
        except Exception as e:
            return

if __name__ == '__main__':
    url = 'http://172.16.0.205:10023'
    AnalysisJson(url).retrieve_data()



