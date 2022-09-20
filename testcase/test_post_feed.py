import pytest
from base.base_assertion import Assertion
from base.base_doExcel import DoExcel
from pprint import pprint
import allure

test_data_path = DoExcel('test_post_feed.xlsx', 'test_post_feed')
test_post_feed_data = test_data_path.read_data()


@allure.feature('日记测试')
class TestPostFeed:
    # pytest装饰器，将测试需要用的数据参数化，实现批量测试
    @pytest.mark.parametrize('test_dict', test_post_feed_data)
    def test_demo(self, login, test_dict):
        # 如果测试字典里面的param不为空，即param里面有数据，这里我会认定为post请求，开始数据替换
        if test_dict['param'] is not None:
            # 如果找到userID，则替换
            if test_dict['param'].find('${userID}') != -1:
                new_param = test_dict['param'].replace('${userID}', str(login[0]))
                test_dict['param'] = new_param
            # 如果找到userKey，则替换
            if test_dict['param'].find('${userKey}') != -1:
                new_param = test_dict['param'].replace('${userKey}', "'" + str(login[1]) + "'")
                test_dict['param'] = new_param
            # 遍历全局变量的key值，如果在param里面找到了key字符串，则用globals()[key]替换，完成所有的替换
            if globals().keys():
                # 遍历key值
                for key in globals().keys():
                    # 遍历出来需要做处理，因为参数化里面是${key}这种格式
                    key_str = '${' + key + '}'
                    # 查找替换
                    if test_dict['param'].find(key_str) != -1:
                        new_param = test_dict['param'].replace(key_str, str(globals()[key]))
                        test_dict['param'] = new_param
        my_assertion = Assertion(test_dict, test_data_path)
        res = my_assertion.send_request()
        # 如果excel里面rely字段不为空，则添加到全局变量globals里面
        if test_dict['rely'] is not None:
            rely_list = eval(test_dict['rely'])
            globals()[rely_list[0]] = rely_list[1]

        my_assertion.assert_result(res)


if __name__ == '__main__':
    pytest.main(['-s', 'test_post_feed.py'])


