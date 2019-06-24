import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options
from datetime import datetime

driver = None

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome_headless")
    parser.addoption("--os", action="store", default="windows")

@pytest.fixture(scope='class')
def driver_init(request):
    global driver
    browser = request.config.option.browser
    os = request.config.option.os

    executable_path_dict  = {
        "windows": {
            "chrome": "resources/webdrivers/windows/chromedriver.exe",
            "firefox": "resources/webdrivers/windows/geckodriver.exe",
            "ie": "resources/webdrivers/windows/IEDriverServer.exe"
        },
        "mac": {
            "chrome": "resources/webdrivers/mac/chromedriver",
            "firefox": "resources/webdrivers/mac/geckodriver"
        },
        "linux": {
            "chrome": "resources/webdrivers/linux/chromedriver",
            "firefox": "resources/webdrivers/linux/geckodriver"
        }
    }
    
    if browser == "chrome":
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path=executable_path_dict[os]["chrome"], options=options)
    elif browser == "chrome_headless":
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(executable_path=executable_path_dict[os]["chrome"], options=options)
    elif browser == "firefox":
        #TODO: Add a firefox specific profile or options for testing
        driver = webdriver.Firefox(executable_path=executable_path_dict[os]["firefox"])
        driver.maximize_window()
    elif browser == "ie":
        #TODO Add IE specific options for testing, programatically set the zoom level to 100%
        driver = webdriver.Ie(executable_path=executable_path_dict["windows"]["ie"])
        driver.maximize_window()
    else: 
        pass

    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.close()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # file_name = report.nodeid.replace("::", "_")+".png"
            timestamp = datetime.now().strftime('%H-%M-%S')
            file_name = 'test_output/screenshots/img' + timestamp + '.png'
            driver.save_screenshot(file_name)
            _file_name = file_name.replace("test_output/", "")
            if _file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % _file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
