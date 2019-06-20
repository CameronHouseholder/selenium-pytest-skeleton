import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

driver = None

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome_headless")

@pytest.fixture(scope='class')
def driver_init(request):
    global driver
    browser = request.config.option.browser
    
    if browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path="resources/webdrivers/chromedriver.exe", options=chrome_options)
    elif browser == "chrome_headless":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path="resources/webdrivers/chromedriver.exe", options=chrome_options)
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
