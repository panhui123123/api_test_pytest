import pytest
from base.base_assertion import Assertion
from base.base_doExcel import DoExcel
from pprint import pprint
import allure

test_data_path = DoExcel('demo.xlsx', 'webtest')
test_demo_data = test_data_path.read_data()


@allure.feature('demo测试')
class TestDemo:
    @pytest.mark.parametrize('test_dict', test_demo_data)
    def test_demo(self, test_dict):
        my_assertion = Assertion(test_dict, test_data_path)
        res = my_assertion.send_request()
        my_assertion.assert_result(res)


if __name__ == '__main__':
    pytest.main(['-q', 'test_demo.py'])