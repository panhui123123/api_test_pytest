from base.base_log import Log
from base.base_requests import HttpRequest
from base.base_doExcel import DoExcel
import json


def is_json(my_json):
    try:
        json_object = json.loads(my_json)
    except ValueError as e:
        return False
    return True


# 如果是json格式就返回json，不是就返回text
def get_response_body(text):
    return json.loads(text) if is_json(text) else text


# 断言封装
class Assertion:
    # 初始化方法，传入测试的数据字典，测试数据的excel对象，测试数据列表
    def __init__(self, test_dict, test_data_path):
        self.test_dict = test_dict
        self.test_data_path = test_data_path

    def send_request(self):
        # 得到请求结果并写入excel
        res = HttpRequest().http_request(url=self.test_dict['url'], method=self.test_dict['method'],
                                         headers=self.test_dict['headers'], data=self.test_dict['param'])
        self.test_data_path.write_data(int(self.test_dict['case_id']) + 1, 9, str(get_response_body(res.text)))
        return res

    def assert_result(self, res):
        test_result = 'UNKNOWN'
        try:
            # 断言成功则pass
            assert res.status_code == 200
            assert eval(self.test_dict['expected_1'])
            assert eval(self.test_dict['expected_2'])
            test_result = 'PASS'
        except AssertionError as e:
            # 断言失败则打出log，并fail
            test_result = 'FAIL'
            Log().error('执行用例{0}的时候报错:{1}'.format(self.test_dict["case_id"], e))
            # 重点敲黑板，这个地方一定一定要raise！一定要raise！一定要raise！曾经没加这句话导致我控制台的AssertionError没有显示，导致我排查
            # 花了一下午，头发都掉了不少。raise是为了显示的引发异常，一定要加啊
            raise e
        finally:
            # 无论断言成功失败都将结果写入excel
            self.test_data_path.write_data(self.test_dict['case_id'] + 1, 10, test_result)


if __name__ == '__main__':
    data = DoExcel('demo.xlsx', 'webtest')
    print(data.read_data())




