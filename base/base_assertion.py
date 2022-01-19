from base.base_log import Log
from base.base_requests import HttpRequest
from base.base_doExcel import DoExcel
import json


# 断言封装
class Assertion:
    def __init__(self, test_dict, test_data_path, test_excel_data):
        self.test_dict = test_dict
        self.test_data_path = test_data_path
        self.test_excel_data = test_excel_data

    def is_json(self, my_json):
        try:
            json_object = json.loads(my_json)
        except ValueError as e:
            return False
        return True

    # 获取返回体内容，如果是json格式就返回json，不是就返回text
    def get_response_body(self, res):
        return res.json() if self.is_json(res.json()) else res.text

    def send_request(self):
        res = HttpRequest().http_request(url=self.test_dict['url'], method=self.test_dict['method'],
                                         headers=self.test_dict['headers'], data=self.test_dict['param'])
        self.test_data_path.write_data(int(self.test_dict['case_id']) + 1, 9, str(self.get_response_body(res)))
        return res

    def assert_result(self, res):
        test_result = 'UNKNOWN'
        try:
            assert res.status_code == 200
            assert eval(self.test_dict['expected_1'])
            assert eval(self.test_dict['expected_2'])
            test_result = 'PASS'
        except AssertionError as e:
            Log().error('执行用例{0}的时候报错:{1}'.format(self.test_dict["case_id"], e))
            Log().warning('预期结果是：{0}；实际请求结果是:{1}'.format(self.test_dict["expected_2"], self.get_response_body(self.send_request())))
            test_result = 'FAIL'
        finally:
            self.test_data_path.write_data(self.test_dict['case_id'] + 1, 10, test_result)


if __name__ == '__main__':
    data = DoExcel('demo.xlsx', 'webtest')
    print(data.read_data())


