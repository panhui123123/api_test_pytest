import requests
import json
from base.base_readYaml import ReadYaml


def get_user_by_login():
    # 获取用户ID，用户token方法
    test_user = ReadYaml().read_yaml_data('test_user.yaml')
    test_user_phone = test_user['test_user'][0]
    test_user_password = test_user['test_user'][1]
    res = requests.post(url='http://api.kr-cell.net/login-register/login-by-phone', headers={'Content-Type':'application/json'},
                        data=json.dumps({'phone': test_user_phone, 'password': test_user_password}))
    return res.json()['userID'], res.json()['userKey']


if __name__ == '__main__':
    print(1)
    