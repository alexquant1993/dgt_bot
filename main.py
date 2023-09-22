import json
import time
import random
import ctypes
import logging
import constants
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException, NoSuchElementException, TimeoutException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from latest_user_agents import get_latest_user_agents
import httpagentparser
from selenium_recaptcha_solver import RecaptchaSolver
from twocaptcha import TwoCaptcha


class DGTBot:
    """
    Bot to check for availability of appointments at the DGT.
    """
    
    def __init__(self, office, type_procedure, country = None) -> None:
        # API Keys
        self.TWO_CAPTCHA_API_KEY = constants.TWO_CAPTCHA_API_KEY
        self.SITE_KEY_V2 = constants.SITE_KEY_V2
        self.SITE_KEY_V3 = constants.SITE_KEY_V3

        # Parameters for the exponential backoff algorithm
        self.MAX_RETRIES = 5
        self.INITIAL_BACKOFF = 60
        self.MAX_BACKOFF = 8 * 60

        # Parameters for the random sleep interval
        self.MIN_SLEEP_INTERVAL = 1
        self.MAX_SLEEP_INTERVAL = 3
        
        # Default parameters for the search
        self.base_url = "https://sedeclave.dgt.gob.es/WEB_NCIT_CONSULTA/solicitarCita.faces"
        self.iteration = 0
        self.office_id = 'publicacionesForm:oficina'
        self.type_procedure_id = 'publicacionesForm:tipoTramite'
        self.country_id = 'publicacionesForm:pais'
        
        # Parameters for the search
        self.office = office
        self.type_procedure = type_procedure
        self.country = country
        logging.basicConfig(format='%(asctime)s %(message)s', filename='dgt_bot.log', level=logging.INFO)

    def get_random_sleep_interval(self):
        """
        Generate a random sleep interval to add between requests
        Returns:
            A random sleep interval in seconds
        """
        return random.uniform(self.MIN_SLEEP_INTERVAL, self.MAX_SLEEP_INTERVAL)

    def get_erratic_sleep_interval(self):
        """
        Generate a more erratic sleep interval to mimic human behavior
        Returns:
            A random sleep interval in seconds
        """
        return random.triangular(self.MIN_SLEEP_INTERVAL, self.MAX_SLEEP_INTERVAL, self.MAX_SLEEP_INTERVAL / 2) * 0.2
    
    def exponential_backoff_with_jitter(self, retry_count):
        wait_time = min(self.INITIAL_BACKOFF * (2**retry_count), self.MAX_BACKOFF)
        jitter = random.uniform(0.5, 1.5)
        return wait_time * jitter

    def scroll_page(self):
        """
        Scrolls the page randomly to mimic human behavior.
        """
        scroll_by = random.randint(0, 500) - 250  # Scrolls up or down by a random amount
        self.driver.execute_script(f"window.scrollBy(0,{scroll_by});")
    
    def random_mouse_movements(self):
        """
        Simulates random mouse movements on the page.
        """
        action = ActionChains(self.driver)
        x_offset = random.randint(0, 200) - 100  # Moves left or right by a random amount
        y_offset = random.randint(0, 200) - 100  # Moves up or down by a random amount
        action.move_by_offset(x_offset, y_offset).perform()

    def click_random_element(self):
        """
        Clicks on a random benign element on the page.
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div, p, a, span")
        random.choice(elements).click()

    def get_status_code(self):
        for entry in self.driver.get_log('performance'):
            for k, v in entry.items():
                if k == 'message' and 'status' in v:
                    msg = json.loads(v)['message']['params']
                    for mk, mv in msg.items():
                        if mk == 'response':
                            response_url = mv['url']
                            response_status = mv['status']
                            if response_url == self.base_url:
                                return response_status

    def driver_setup(self):
        """
        Setup the Selenium driver.
        """
        logging.info("Setting up the driver...")
        options = Options()
        options.add_argument(f'--user-agent={self.get_chrome_header()}')
        # Set random browser window size
        width = random.randint(1000, 1920)
        height = random.randint(700, 1080)
        options.add_argument(f"--window-size={width},{height}")
        capabilities = DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        driver = \
            webdriver.Chrome(
                options=options,
                desired_capabilities=capabilities,
                service=ChromeService(ChromeDriverManager().install())
            )
        driver.get(self.base_url)
        time.sleep(self.get_erratic_sleep_interval())
        self.driver = driver

    def get_chrome_header(self) -> str:
        """
        Get Chrome header from the latest user agents: Windows + Chrome.
        """
        latest_user_agents = get_latest_user_agents()
        agents_dict = {}
        for user_agent in latest_user_agents:
            parsed_agent = httpagentparser.detect(user_agent)
            os = parsed_agent["platform"]["name"]
            browser = parsed_agent["browser"]["name"]
            agents_dict[f"{os}-{browser}"] = user_agent

        return agents_dict["Windows-Chrome"]
    
    def fill_field(self, field_id, value):
        """
        Fill a field in the form.
        Args:
            driver: Selenium driver.
            field_id (str): ID of the field to fill.
            value (str): Value to fill the field with.
        """
        logging.info(f"Filling field {field_id}...")
        el = self.driver.find_element(By.ID, field_id)
        el.click()
        time.sleep(self.get_random_sleep_interval())
        el.send_keys(value + Keys.ENTER)
        time.sleep(self.get_random_sleep_interval())    
        
    def solve_captcha(self):
        """
        Solve the CAPTCHA.
        """
        logging.info("Solving CAPTCHA...")
        # # Solve the CAPTCHA
        # solver_config = {
        #     'apiKey': self.TWO_CAPTCHA_API_KEY,
        #     'defaultTimeout': 120,
        #     'recaptchaTimeout': 600,
        #     'pollingInterval': 10,
        # }
        # solver = TwoCaptcha(**solver_config)
        # response = solver.recaptcha(sitekey=self.SITE_KEY_V2, url=self.base_url)
        # code = response['code']

        # # Input the response into the textarea
        # recaptcha_response_element = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea#g-recaptcha-response'))
        # )            
        # self.driver.execute_script("arguments[0].style.display = 'block';", recaptcha_response_element)
        # self.driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)        
        
        # Solve reCAPTCHA v2
        solver = RecaptchaSolver(self.driver)
        recaptcha_iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        
        # Solve reCAPTCHA v3
        # solver_config = {
        #     'apiKey': self.TWO_CAPTCHA_API_KEY,
        #     'defaultTimeout': 120,
        #     'recaptchaTimeout': 600,
        #     'pollingInterval': 10,
        # }
        # solver = TwoCaptcha(**solver_config)
        # response = solver.recaptcha(
        #     sitekey=self.SITE_KEY_V3,
        #     url=self.base_url,
        #     version='v3',
        #     score = 0.7,
        #     action = 'solicitarCita'
        # )
        # token = response['code']
        # self.driver.execute_script(f'''
        #     console.log('{token}');
        #     document.getElementById("publicacionesForm:responseV3").value = '{token}';
        # ''')
        
        # Simulate human behavior   
        time.sleep(self.get_random_sleep_interval())
        self.random_mouse_movements()
        self.scroll_page()    
    
    def submit_form(self):
        """
        Submit the form.
        """
        logging.info("Submitting form...")
        self.driver.find_element(By.CLASS_NAME, 'botonSINimgen').click()

    def make_request(self):
        logging.info("Making request...")
        try:
            self.driver_setup()
            status_code = self.get_status_code()
            if status_code != 200:
                raise ValueError(f'Invalid status code: {status_code}')
        except (ValueError, WebDriverException) as e:
            logging.error(f"Error initializing the driver: {str(e)}")
            self.driver.quit()
            return 'retry_setting_up_driver'
            
        # Populate the form fields
        self.fill_field(self.office_id, self.office)
        self.fill_field(self.type_procedure_id, self.type_procedure)
        if self.country:
            self.fill_field(self.country_id, self.country)
        
        # Solve the CAPTCHA
        try:
            self.solve_captcha()
        except Exception as e:
            logging.error(f"Error solving the CAPTCHA: {str(e)}")
            self.driver.quit()
            return 'retry_failed_captcha'
        
        # Submit the form
        self.submit_form()
        time.sleep(self.get_random_sleep_interval())

        # Check if the website did not go to HTTP status 500 after submitting the form
        # If the office is not available, the website will go to HTTP status 500
        try:
            self.driver.find_element(By.ID, self.office_id)
        except NoSuchElementException:
            logging.info("Website went to HTTP status 500 after submitting the form")
            self.driver.quit()
            return 'retry_setting_up_driver'

        # Check the status of the request
        try:
            check_error = self.driver.find_element(By.CLASS_NAME, 'msgError')
            msg = check_error.text
            if 'Estamos recibiendo un número muy elevado de accesos' in msg:
                response = 'retry_too_many_requests'
            elif 'No hay citas disponibles para la búsqueda realizada' in msg:
                response = 'retry_no_appointments'
            elif 'Verifique que no es un robot' in msg:
                response = 'retry_failed_captcha'
            else:
                response = 'retry_unknown_error'
        except NoSuchElementException:
            response = 'appointment_available'
            
        self.driver.quit()
        return response

    def make_request_with_retries(self, freq = 5):
        """
        Make a request to the website with retries.
        """
        self.iteration += 1
        logging.info(f"Making request with retries... (iteration {self.iteration})")
        retry_count = 0
        while retry_count < self.MAX_RETRIES:
            try:
                response = self.make_request()
                if response == 'appointment_available':
                    return response
                elif response == 'retry_setting_up_driver' or \
                    response == 'retry_failed_captcha':
                    logging.info(f"Retrying... ({retry_count}) - ({response})")
                    time.sleep(self.exponential_backoff_with_jitter(retry_count))
                    retry_count += 1
                else:
                    time.sleep(freq * 60 + random.uniform(0, 60))
            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                time.sleep(self.exponential_backoff_with_jitter(retry_count))
                retry_count += 1
        
        return response


if __name__ == "__main__":
    dgt_bot = DGTBot(office='Madrid', type_procedure='Canje de permiso de conducción', country='Perú')
    response = dgt_bot.make_request_with_retries()
    if response == 'appointment_available':
        title = 'ALERT'
        text = 'Appointment available'
        ctypes.windll.user32.MessageBoxW(0, text, title, 0x00001000)

