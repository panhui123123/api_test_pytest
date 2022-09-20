import pytest
import requests
import json
from base.base_readYaml import ReadYaml
from base.base_log import Log


@pytest.fixture(scope='class')
def login():
    # 获取用户ID，用户token方法
    test_user = ReadYaml().read_yaml_data('test_user.yaml')
    test_user_phone = test_user['test_user']['phone'][0]
    test_user_password = test_user['test_user']['phone'][1]
    try:
        res = requests.post(url='http://api.kr-cell.net/login-register/login-by-phone',
                            headers={'Content-Type': 'application/json'},
                            data=json.dumps({'phone': test_user_phone, 'password': test_user_password}))
        return res.json()['userID'], res.json()['userKey']
    except Exception as e:
        Log().error('{}、登陆获取用户ID、token时出错'.format(e))
        return 'NoUserId', 'NoUserKey'


# @pytest.fixture(scope='function')
# def replace_param(login, test_dict):
#     # 如果测试字典里面的param不为空，即param里面有数据，这里我会认定为post请求，开始数据替换
#     if test_dict['param'] is not None:
#         # 如果找到userID，则替换
#         if test_dict['param'].find('${userID}') != -1:
#             new_param = test_dict['param'].replace('${userID}', str(login[0]))
#             test_dict['param'] = new_param
#         # 如果找到userKey，则替换
#         if test_dict['param'].find('${userKey}') != -1:
#             new_param = test_dict['param'].replace('${userKey}', "'" + str(login[1]) + "'")
#             test_dict['param'] = new_param
#         # 遍历全局变量的key值，如果在param里面找到了key字符串，则用globals()[key]替换，完成所有的替换
#         if globals().keys():
#             # 遍历key值
#             for key in globals().keys():
#                 # 遍历出来需要做处理，因为参数化里面是${key}这种格式
#                 key_str = '${' + key + '}'
#                 # 查找替换
#                 if test_dict['param'].find(key_str) != -1:
#                     new_param = test_dict['param'].replace(key_str, str(globals()[key]))
#                     test_dict['param'] = new_param


if __name__ == '__main__':
    print(1)