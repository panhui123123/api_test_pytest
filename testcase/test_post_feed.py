import pytest
from base.base_assertion import Assertion
from base.base_doExcel import DoExcel
from pprint import pprint

test_data_path = DoExcel('test_post_feed.xlsx', 'test_post_feed')
test_post_feed_data = test_data_path.read_data()


@pytest.mark.usefixtures('login')
class TestPostFeed:
    @pytest.mark.parametrize('test_dict', test_post_feed_data)
    def test_demo(self, login, test_dict):
        if test_dict['param'] is not None:
            if test_dict['param'].find('${userID}') != -1:
                new_param = test_dict['param'].replace('${userID}', str(login[0]))
                test_dict['param'] = new_param
            if test_dict['param'].find('${userKey}') != -1:
                new_param = test_dict['param'].replace('${userKey}', "'" + str(login[1]) + "'")
                test_dict['param'] = new_param
        else:
            pass
        my_assertion = Assertion(test_dict, test_data_path)
        res = my_assertion.send_request()
        my_assertion.assert_result(res)


if __name__ == '__main__':
    pytest.main(['-s', 'test_post_feed.py'])
