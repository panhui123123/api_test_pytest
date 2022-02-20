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


if __name__ == '__main__':
    print(1)