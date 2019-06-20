from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class BasePage(object):
    # page variables
    timeout = 10

    # constructor
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.timeout)

    def get(self, url):
        """
        Force the web browser to navigate to the url

        Parameters
        ----------
        url: str
            The url the web browser navigates to
        """  
        self.driver.get(url)

    def find_all(self, locator):
        """
        Find all the elements that match the locator and return a list of the located web elements

        Parameters
        ----------
        locator: tuple
            The locator used to find all the elements

        Returns
        -------
        list
            a list of the located elements
        """  
        return self.driver.find_elements(*locator)

    def find(self, locator):
        """
        Find the element that matches the locator and returns the located element

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        WebElement
            the located element
        """  
        return self.driver.find_element(*locator)

    def click_elem_located(self, locator):
        """
        Find the element that matches the locator, wait until the element is visible and then click the element

        Parameters
        ----------
        locator: tuple
            The locator used to find the element
        """ 
        self.wait.until(EC.visibility_of_element_located(locator)).click()

    def set_elem_text(self, locator, text):
        """
        Find the element that matches the locator, wait until the element is visible, clear the element text and then set the text of the element

        Parameters
        ----------
        locator: tuple
            The locator used to find the element
        text: str
            The locator used to find the element
        """ 
        elem = self.find(locator)
        self.wait.until(EC.visibility_of(elem))
        elem.clear()
        elem.send_keys(text)

    def select_elem_option_by_value(self, locator, value):
        """
        Find the select element that matches the locator, wait until the select element is visible, and then select the option by value

        Parameters
        ----------
        locator: tuple
            The locator used to find the element
        value: str
            The value of the option to be selected
        """ 
        select = Select(self.wait.until(EC.visibility_of_element_located(locator)))
        select.select_by_value(value)

    def tab_elem(self, locator):
        """
        Find the element that matches the locator, wait until the element is visible, and then press the tab key

        Parameters
        ----------
        locator: tuple
            The locator used to find the element
        """ 
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(Keys.TAB)

    def get_elem_text(self, locator):
        """
        Find the element that matches the locator, wait until the element is visible, and then return the element text

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        str
            the text of the located element
        """  
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def get_elem_value(self, locator):
        """
        Find the element that matches the locator, wait until the element is visible, and then return the element value attribute

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        str
            the value attribute of the located element
        """  
        return self.wait.until(EC.visibility_of_element_located(locator)).get_attribute("value")

    def get_elem_option_by_value(self, locator):
        """
        Find the select element that matches the locator, wait until the select element is visible, and then return the select option value attribute

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        str
            the value attribute of the selected option
        """  
        select = Select(self.wait.until(EC.visibility_of_element_located(locator)))
        return select.first_selected_option.get_attribute("value")

    def elem_is_displayed(self, locator):
        """
        Try to find the element that matches the locator and then return a boolean based on if the element is displayed or not.

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        boolean
            true if the element is displayed, false if the element is not displayed
        """  
        try:
            is_displayed = self.driver.find_element(*locator).is_displayed()
        except:
            is_displayed = False
        return is_displayed

    def elem_is_selected(self, locator):
        """
        Find the element that matches the locator, wait till the element is visible, and then return a boolean based on if the element is selected or not.

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        boolean
            true if the element is selected, false if the element is not selected
        """  
        return self.wait.until(EC.visibility_of_element_located(locator)).is_selected()

    def elem_is_enabled(self, locator):
        """
        Find the element that matches the locator, wait till the element is visible, and then return a boolean based on if the element is enabled or not.

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        boolean
            true if the element is enabled, false if the element is not enabled
        """  
        return self.wait.until(EC.visibility_of_element_located(locator)).is_enabled()

    def get_elem_count(self, locator):
        """
        Find all the elements that match the locator and then return the element count.

        Parameters
        ----------
        locator: tuple
            The locator used to find the element

        Returns
        -------
        int
            an integer that represents the number of elements that match the locator
        """  
        return len(self.find_all(locator))

    def accept_alert(self):
        """
        Try to accept an alert if one is present, if not continue on

        """  
        try:
            self.driver.switch_to.alert.accept()
        except:
            pass

    def alert_is_displayed(self, text):
        """
        Try to switch to an alert, determine if the alert text is correct, and then return a boolean if the alert/correct alert is displayed or not

        Parameters
        ----------
        text: str
            The alert text used to determine if the correct alert is displayed

        Returns
        -------
        boolean
            true if the alert is displayed, false if the alert is not displayed
        """  
        is_displayed = False
        try:
            alert = self.driver.switch_to.alert
            if text in alert.text:
                is_displayed = True
            alert.accept()
        except:
            is_displayed = False
        return is_displayed
    
    def get_current_window(self):
        """
        Get and return the handle of the current window in the session

        Returns
        -------
        str
            the handle of the current window
        """  
        return self.driver.current_window_handle

    def get_windows(self):
        """
        Get and return the handles of all windows in the session

        Returns
        -------
        list
            a list of the handles of all windows
        """  
        return self.driver.window_handles

    def switch_to_window(self, window):
        """
        Switch to another window in the session

        Parameters
        ----------
        window: str
            The window handle of the window the session should switch to
        """  
        self.driver.switch_to.window(window)

    def switch_to_frame_by_name(self, name):
        """
        Switch to an iframe by the iframe name

        Parameters
        ----------
        name: str
            The name of the iframe the session should switch to
        """  
        self.driver.switch_to.frame(name)

    def get_page_title(self):
        """
        Get and return the page title

        Returns
        -------
        str
            the title of the page
        """  
        return self.driver.title

