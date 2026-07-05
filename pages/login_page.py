
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE_CONTAINER = (By.CSS_SELECTOR, ".error-message-container")

    def __init__(self, driver):
        self.driver = driver
        # Initialize WebDriverWait with a reasonable timeout
        self.wait = WebDriverWait(driver, 10) 

    def enter_username(self, username):
        """
        Enters the provided username into the username input field.
        """
        username_element = self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        username_element.clear()
        username_element.send_keys(username)

    def enter_password(self, password):
        """
        Enters the provided password into the password input field.
        """
        password_element = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_element.clear()
        password_element.send_keys(password)

    def click_login(self):
        """
        Clicks the Login button.
        """
        login_button_element = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button_element.click()

    def login(self, username, password):
        """
        Performs the complete login action by entering username and password, then clicking login.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_login_page_displayed(self):
        """
        Verifies if the login page is displayed by checking for the visibility of the username field.
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD)) is not None
        except:
            return False

    def get_error_message(self):
        """
        Retrieves the text of the error message displayed on the login page, if any.
        Returns an empty string if no error message is found or visible.
        """
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE_CONTAINER))
            return error_element.text
        except:
            return "" # Return an empty string if the error message container is not found or visible
