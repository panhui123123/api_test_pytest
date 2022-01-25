import pytest
from base.base_assertion import Assertion
from base.base_doExcel import DoExcel
from pprint import pprint

test_data_path = DoExcel('test_post_feed.xlsx', 'test_post_feed')
test_post_feed_data = test_data_path.read_data()


class TestPostFeed:
    @pytest.mark.parametrize('test_dict', test_post_feed_data)
    def test_demo(self, test_dict):
        my_assertion = Assertion(test_dict, test_data_path, test_post_feed_data)
        res = my_assertion.send_request()
        my_assertion.assert_result(res)


if __name__ == '__main__':
    pytest.main(['-q', 'test_post_feed.py'])