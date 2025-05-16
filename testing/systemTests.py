import unittest
import multiprocessing
import os
import time

from Explorate import create_app
from Explorate.config import TestingConfig
from Explorate.models import db, User, Adventure, UserSelection, Recommendations, Ratings
from werkzeug.security import generate_password_hash

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

localHost = "http://127.0.0.1:5000/"

def run_flask_app():
    app = create_app(TestingConfig)
    app.run(use_reloader=False)

class SystemTests(unittest.TestCase):
    def setUp(self):
        self.app_ctx = create_app(TestingConfig).app_context()
        self.app_ctx.push()
        db.create_all()
        
        self.server_thread = multiprocessing.Process(target=run_flask_app)
        self.server_thread.start()
        
        time.sleep(2)
        
        # select browser
        browser_type = os.getenv("BROWSER", "edge").lower()
        
        if browser_type == "chrome":
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=options)
        elif browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(options=options)
        elif browser_type == "edge":
            options = webdriver.EdgeOptions()
            self.driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")
        
        self.driver.implicitly_wait(10)
        return super().setUp()
    
    def addUser(self, username, password):
        user = User(
            Username=username,
            email=f'{username}@example.com',
            password=generate_password_hash(password),
            country='Australia',
            dateofbirth='2000-1-1'
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def test_1_homepage_to_login(self): 
        self.driver.get(localHost)

        find_adventure_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.ID, "loginPage"))
        )
        find_adventure_button.click()
        
        # Now confirm redirect to login (optional)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.url_contains("/login")
        )
        
        time.sleep(3)
        self.assertIn("/login", self.driver.current_url)
        
    def test_2_loginSuccess(self):
        
        # add user
        user = self.addUser('testUser', 'plswork')
        
        self.test_1_homepage_to_login()
        
        try:
            #print all available element ids
            elements_with_id = self.driver.find_elements(By.XPATH, "//*[@id]")
            print(f"found {len(elements_with_id)} with element IDs:")
            for element in elements_with_id:
                print(f"Element with ID: {element.get_attribute('id')}")
        except Exception:
            pass
        
        # find elements
        user_id_field = self.driver.find_element(By.ID, "Username")
        password_field = self.driver.find_element(By.ID, "password3")
        login_btn = self.driver.find_element(By.ID, "login-btn")
        
        # send key
        user_id_field.send_keys("testUser")
        password_field.send_keys("plswork")
        
        login_btn.click()
        
        time.sleep(3)
        self.assertIn("/FindAdv", self.driver.current_url)
        
    def tearDown(self):
        self.driver.quit()
        self.server_thread.terminate()
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()