import requests
import selenium
import time
import undetected_chromedriver as uc
from selenium import webdriver
import re, requests, json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--lang=en_US')
options.add_argument('--disable-dev-shm-usage')


class nocap:
    def __init__(self, uid: str, apikey: str):
        self.uid = uid
        self.apikey = apikey
        self.api_url = 'https://solve.shimul.me/api/solve'
    def solve(self, site_url: str, method: str):
        if site_url == "":
            site_url = "https://shimuldn.github.io/hCaptchaSolverApi/demo_data/demo_sites/2/"
        if method == "browser":
            driver = uc.Chrome(options=options, use_subprocess=True)
            driver.get(site_url)
            time.sleep(1)
            WebDriverWait(driver, 2, ignored_exceptions=ElementNotVisibleException).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, "//iframe[contains(@title,'checkbox')]")
                )
            )
            
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "checkbox"))).click()
            driver.switch_to.default_content()
            HOOK_CHALLENGE = "//iframe[contains(@title,'content')]"
            WebDriverWait(driver, 15, ignored_exceptions=ElementNotVisibleException).until(
                    EC.frame_to_be_available_and_switch_to_it((By.XPATH, HOOK_CHALLENGE))
                )
            time.sleep(1)

            def solve_hcaptcha(driver, EC):
                print("Solving hcaptcha")
                _obj = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                    EC.presence_of_element_located((By.XPATH, "//h2[@class='prompt-text']"))
                )
                time.sleep(1)
                target=re.split(r"containing a", _obj.text)[-1][1:].strip()
                print(f'hcaptcha target {target}')

                WebDriverWait(driver, 10, ignored_exceptions=ElementNotVisibleException).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='task-image']"))
                )
                images_div = driver.find_elements(By.XPATH, "//div[@class='task-image']")

                image_data={}

                # Getting the data for api server format
                for item in images_div:
                    name=item.get_attribute("aria-label")
                    number=int(name.replace("Challenge Image ", ""))-1
                    image_style = item.find_element(By.CLASS_NAME, "image").get_attribute("style")
                    url = re.split(r'[(")]', image_style)[2]
                    image_data[number]=url

                # Doing final formating for api by adding mandatory target data_type site_key site and images 
                data_to_send={}
                data_to_send['target']=target
                data_to_send['data_type']="url"
                data_to_send['site_key']="dasds"
                data_to_send['site']="jj"
                data_to_send['images']=image_data
                
                full_url=self.api_url
                

                # Sending the request to api server
                # print(json.dumps(image_data))   # uncomment this to see the request data
                print("Sending request to api server")
                r = requests.post(url = full_url, headers={'Content-Type': 'application/json', 'uid': self.uid,
                'apikey': self.apikey}, data = json.dumps(data_to_send))

                # printing the response from api server
                # print(f'Response received from api server {r.text}')
                try:


                    if r.json()['status'] == "new":
                        time.sleep(2)
                        status=requests.get(r.json()['url'])
                        # print(status.json())
                        if status.json()['status'] == "solved":
                            # for item in images_div:
                            #     name=item.get_attribute("aria-label")
                            #     nn=int(name.replace("Challenge Image ", ""))-1
                                # print(status.json()['solution'][0])
                                # if status.json()['solution'][nn]:
                                #     time.sleep(0.05)
                                #     item.click()
                                # for res in status.json()['solution']:
                                #     print(status.json()['solution'][res])
                            sol=status.json()['solution']
                            # r=[]
                            # for i in sol:
                            #     if sol[i] == "True":
                            #         print(sol[i])
                            #         r.append(int(i))
                            print(sol)
                            # for ii in sol:
                            #     print(ii, type(ii))
                                # time.sleep(10)
                            for item in images_div:
                                name=item.get_attribute("aria-label")
                                nn=int(name.replace("Challenge Image ", ""))-1
                                # print(nn)
                                if nn in sol:
                                    item.click()

                            ## clicking the button
                            WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, "//div[@class='button-submit button']"))
                                ).click()

                            

                    else:
                        print(r.json())
                except Exception as e:
                    raise Exception(f'Error in api server response {e}')


                
                time.sleep(20)
                # Clicking the images to solve the captcha
                try:

                    if r.json()['success']:
                        for item in images_div:
                            name=item.get_attribute("aria-label")
                            nn=int(name.replace("Challenge Image ", ""))-1
                            if r.json()['solution'][str(nn)]:
                                time.sleep(0.05)
                                item.click()


                        time.sleep(20)
                        WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@class='button-submit button']"))
                        ).click()
                except Exception as e:
                    raise Exception(f'Error in api server response {e}')

                try:
                    error_txt=WebDriverWait(driver, 1, 0.1).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@class='error-text']"))
                    )
                    print(f'error found {error_txt}')
                except:
                    pass


                for i in range(5):
                    try:
                        WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='task-image']"))
                        )
                        solve_hcaptcha(driver, EC)
                    except:
                        print("hcaptcha Solved successfully")
                        break



            def is_challenge_image_clickable(driver):
                try:
                    WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='task-image']"))
                    )
                    return True
                except TimeoutException:
                    return False
                

            solve_hcaptcha(driver, EC)

        elif method == "requests":
            session = requests.Session()
            res = session.get(site_url)
            print(res.status_code)
        else:
            print("Invalid method available methods: browser, requests")
            return False
            
