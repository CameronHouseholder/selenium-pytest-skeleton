import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
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

    chrome_options_dict = {
        "chrome": ["--start-maximized", "--ignore-certificate-errors", "--incognito"],
        "chrome_headless": ["--start-maximized", "--ignore-certificate-errors", "--incognito", "--headless", "--disable-gpu"]
    }
    
    if "chrome" in browser:
        options = Options()
        # adds different chrome options from a dictionary depending on if it should be ran headless or not
        chrome_options = chrome_options_dict[browser]
        for chrome_option in chrome_options:
            options.add_argument(chrome_option)
        driver = webdriver.Chrome(executable_path=executable_path_dict[os]["chrome"], options=options)
    elif "firefox" in browser:
        #TODO: Add a firefox specific profile or options for testing
        driver = webdriver.Firefox(executable_path=executable_path_dict[os]["firefox"])
        driver.maximize_window()
    elif "internet_explorer" in browser:
        capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
        capabilities["ignoreZoomSetting"] = True
        driver = webdriver.Ie(executable_path=executable_path_dict["windows"]["ie"], capabilities=capabilities)
        driver.maximize_window()
        """
        the ctrl + 0 key command only works if the default zoom level of IE is 100% 
        default zoom level is controlled by the default scaling option in the display settings on the machine running the IE browser
        if the default zoom level is greater or less than 100% the zoom level should be manually set
        """
        driver.find_element_by_tag_name("html").send_keys(Keys.CONTROL + "0")
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
