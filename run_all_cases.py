import pytest

if __name__ == '__main__':
    pytest.main(['-q', './testcase', '--alluredir=./report/allure-results'])