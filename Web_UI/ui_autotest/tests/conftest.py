import pytest
from selenium import webdriver

from Web_UI.ui_autotest.DataSource.LoadData import LoadData
from Web_UI.ui_autotest.utils import BASE_DIR
from Web_UI.ui_autotest.utils.operation.file import get_case_id
from Web_UI.ui_autotest.utils.testing.assemble import build_test_data


def pytest_sessionstart(session):
    # 初始化加载测试数据
    LoadData.load_local()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", type=str, default="chrome", help="测试使用的浏览器类型")


def pytest_generate_tests(metafunc):
    """
    用例收集阶段钩子
    实现夹具参数化。根据当前测试用例调用的夹具，对夹具进行参数化
    :param metafunc: 帮助实现参数化的钩子默认参数
    :return: None
    """
    yaml_path = metafunc.module.__file__.replace('.py', '.yaml')
    case_path = metafunc.module.__name__.rsplit(".", 1)[-1]
    # fixtures = metafunc.fixturenames
    fixtures = metafunc.definition._fixtureinfo.argnames
    ids = get_case_id(yaml_path, case_path)

    # 夹具参数化
    for fixture in fixtures:
        if fixture in ('data',):  # 维护需要参数化的夹具
            metafunc.parametrize(fixture, ids, indirect=True)


@pytest.fixture(scope="session")
def driver(request):
    """
    根据配置返回需要的driver对象
    :param request:
    :return: driver
    """
    browser_type = request.config.getoption("browser")

    if browser_type == "chrome":
        # 浏览器后台运行模式
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(executable_path=rf"{BASE_DIR}/libs/chromedriver", options=chrome_options)
        yield driver

        # 关闭网页及浏览器
        driver.close()
        driver.quit()


@pytest.fixture()
def data(request):
    # 根据用例编号，生成测试数据
    return build_test_data(request)
