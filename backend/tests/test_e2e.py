import subprocess
import time
import unittest

from django.core.management import call_command
from django.test import LiveServerTestCase, override_settings
from selenium import webdriver

from app.settings import BASE_DIR
from user.controllers import create_user
from utils.jwt import encrypt_password

DRIVER_PATH = 'drivers/chromedriver.exe'
FRONTEND_PATH = str(BASE_DIR.parent) + '/frontend'
# cli = sys.modules['flask.cli']
# cli.show_server_banner = lambda *x: None
#
#
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


@override_settings(
    CORS_ORIGIN_ALLOW_ALL=True,
    CORS_ALLOW_CREDENTIALS=True,
    CORS_ORIGIN_WHITELIST=['*']
)
class SeleniumTestCase(LiveServerTestCase):
    port = 8000  # 服务器端口，默认为随机分配一个空闲端口

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # start Chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # You need to change this to your actual binary path.
        # options.binary_location = "C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
        # You need to change this to your actual web driver path.
        cls.webclient = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
        # delete all data in the database
        call_command('flush', '--noinput')
        create_user(username="test_thss", password=encrypt_password(str("test_thss")), nickname="test_thss", url="https://baidu.com", mobile="+86.123456789012", magic_number=0)

        # start the frontend server in a process
        # You need to change this to your actual frontend path.
        frontend_path = FRONTEND_PATH
        cls.frontend_process = subprocess.Popen(
            "npm run startwithoutbrowser", shell=True, cwd=frontend_path)

        # give the server 15 seconds to ensure it is up
        time.sleep(15)

    @classmethod
    def tearDownClass(cls):
        cls.webclient.close()
        cls.webclient.quit()
        cls.frontend_process.terminate()
        cls.frontend_process.kill()
        call_command('flush', '--noinput')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_web(self):
        """
        EXAMPLE: 使用测试用户进行登录
        """
        self.webclient.get('http://127.0.0.1:3001')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/a").click()
        time.sleep(1)
        self.webclient.find_element_by_id('username').send_keys('test_thss')
        time.sleep(1)
        self.webclient.find_element_by_id('password').send_keys('test_thss')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            '//*[@id="root"]/div/div[3]/div/button').click()
        time.sleep(3)

        """
        TODO: 登录后发帖，发帖标题为：Hello World，发帖内容为：你好！
        """
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[1]/div/a").click()
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[1]/div/input").send_keys('Hello World')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]/div[2]/section[1]/textarea").send_keys('你好！')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[3]/button").click()
        time.sleep(3)

        """
        TODO: 更新帖子标题为：Hello World！，帖子内容为：你好。
        """
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[2]/div[2]/span[2]/span/a[1]").click()
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[1]/div/input").send_keys('！')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]/div[2]/section[1]/textarea").clear()
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]/div[2]/section[1]/textarea").send_keys('你好。')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[3]/button").click()
        time.sleep(3)

        """
        TODO: 回复刚才的帖子，回复内容为：你好！
        """
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[2]/div[2]/span[2]/span/a[2]").click()
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]/div[2]/section[1]/textarea").send_keys('你好！')
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[3]/button").click()
        time.sleep(3)

        """
        TODO: 退出登录
        """
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/header/div/span/a").click()
        time.sleep(1)
        self.webclient.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[6]/button").click()
        time.sleep(3)


if __name__ == '__main__':
    unittest.main()
