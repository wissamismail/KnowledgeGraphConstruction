from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import json
import os

import chrome_handler
import helper_funcs
import sys

# current file path
current_file_path = os.path.dirname(os.path.realpath(__file__))
user_data_folder = current_file_path + "/chromedata"
chrome_profile = "Default"

def load_chrome():
    # service = Service(os.getcwd() + "/chromedriver")

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_folder}")
    options.add_argument(f'--profile-directory={chrome_profile}')

    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument("--headless")

    global helper_fn, driver

    driver = uc.Chrome(options=options)
    helper_fn = helper_funcs.HelperFn(driver)


def check_guildlines():
    guidlines_xpath = "//*[contains(text(), 'Tips for getting started')]"
    helper_fn.wait_for_element(guidlines_xpath)
    if helper_fn.is_element_present(guidlines_xpath):
        guidlines_close_xpath = "//*[contains(text(), 'Okay, let’s go')]"
        guidlines_close = helper_fn.find_element(guidlines_close_xpath)
        guidlines_close.click()
    else:
        print("No guidlines found")

def start_chat_gpt():
    load_chrome()
    driver.maximize_window()
    driver.get("https://chat.openai.com/chat")
    #if login page is present
    time.sleep(2)
    login_msg_xpath = "//*[contains(text(), 'Log in with your OpenAI account to continue')]"
    login_page = helper_fn.is_element_present(login_msg_xpath)
    if login_page:
        login_btn_xpath = "//*[@class='btn relative btn-primary']//*[contains(text(), 'Log in')]"
        helper_fn.wait_for_element(login_btn_xpath)
        login_button = helper_fn.find_element(login_btn_xpath)
        login_button.click()
        
        time.sleep(2)
        #google login
        google_btn_xpath = "//*[@data-provider='google']"
        helper_fn.wait_for_element(google_btn_xpath)
        google_btn = helper_fn.find_element(google_btn_xpath)
        google_btn.click()

        time.sleep(2)
        #select mail
        gmail_xpath = "//*[contains(text(), 'osgislover@gmail.com')]" ## change this to your google account name.
        helper_fn.wait_for_element(gmail_xpath)
        gmail = helper_fn.find_element(gmail_xpath)
        gmail.click()

    else:
        print("Already logged in")

    #check for guidlines
    check_guildlines()

def make_gpt_request(text):

    time.sleep(3)
    text_area_xpath = "//*[@id='prompt-textarea']"
    helper_fn.wait_for_element(text_area_xpath)
    if helper_fn.is_element_present(text_area_xpath):
        text_area = helper_fn.find_element(text_area_xpath)
        text_area.send_keys(text)

        #send button
        send_btn_xpath = "//*[@data-testid='send-button']"
        send_btn_xpath ="// *[ @ id = ""__next""] / div[1] / div / main / div[1] / div[2] / div[1] / div / form / div / div[2] / div / div / button"
        send_btn_xpath = "//*[@data-testid='fruitjuice-send-button']"

        helper_fn.wait_for_element(send_btn_xpath)
        send_btn = helper_fn.find_element(send_btn_xpath)
        time.sleep(2)
        send_btn.click()

    helper_fn.wait_for_x_seconds(5)
    #waiting for response
    response_xpath_light = "//*[@class='markdown prose w-full break-words dark:prose-invert light']" # for light mode
    response_xpath_dark = "//*[@class='markdown prose w-full break-words dark:prose-invert dark']" # for dark mode
    regenrate_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/form/div/div/div/button'
    helper_fn.wait_for_element(regenrate_xpath,120)

    response_xpath = response_xpath_dark if helper_fn.is_element_present(response_xpath_dark) else response_xpath_light # check for dark mode or light mode

    if helper_fn.is_element_present(response_xpath):
        helper_fn.wait_for_x_seconds(2)
        response = helper_fn.find_elements(response_xpath)[-1]
        # print(response.text)
        return response.text # will return all the texual information under that perticular xpath



def stop_chat_gpt():
    driver.close()
    driver.quit()

    # chrome_handler.kill_chrome()


categories = {
    "literature": "Lit",
    "medical-articles": "Med",
    "moviescripts": "Mov",
    "news-press-releases": "NPR",
}


def iterate_category(category_name, category_prefix, error_log_path):
    folder_path = f'E:/workspaces/PythonWS/Selenium-python/chatGPT/myDataset/{category_name}'
    files = sorted(os.listdir(folder_path))[51:100]
    all_data = {}
    errors = []
    output_json_temp = f'E:/workspaces/PythonWS/Selenium-python/chatGPT/myResult/Using_chatGPT/{category_name}.json'
    os.makedirs(os.path.dirname(output_json_temp), exist_ok=True)
    with open(output_json_temp, 'w', encoding='utf-8') as json_file:
        for idx, file_name in enumerate(files, start=1):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    req = text
                    time.sleep(10)
                    resp = make_gpt_request(req)
                    #print(resp)
                    svos = resp
                    if svos:
                        all_data[f"{category_prefix}-{idx}"] = {
                            "SVO_relationships": svos,
                            "total_SVOs": len(svos)
                        }
                    else:
                        errors.append(f"No SVOs found in file {file_name} ({category_prefix}-{idx})")
                    print(all_data)
                    json.dump(all_data, json_file, indent=4, ensure_ascii=False)
            except Exception as e:
                errors.append(f"Error processing file {file_name} ({category_prefix}-{idx}): {str(e)}")
    output_json_path = f'E:/workspaces/PythonWS/Selenium-python/chatGPT/myResult/Using_chatGPT/{category_name}.json'
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as json_file2:
        json.dump(all_data, json_file2, indent=4, ensure_ascii=False)
    print(f"SVOs for {category_name} saved to {output_json_path}")

    # Write errors to log file
    with open(error_log_path, 'a', encoding='utf-8') as log_file:
        for error in errors:
            log_file.write(error + '\n')
    print(f"Errors for {category_name} logged to {error_log_path}")

# Error log path
error_log_path = 'E:/workspaces/PythonWS/Selenium-python/chatGPT/myDataset/myResult/Using_chatGPT/error_log.txt'
os.makedirs(os.path.dirname(error_log_path), exist_ok=True)

if __name__ == "__main__":
    start_chat_gpt()

    try:
        while True:
            req = """
for every sentence(lit-x) that I will give you, I need to help me to return the SVO as Spacy do for this sentence, like this structure:
{
"lit-1": {
      "SVO_relationships": [
        {
          "subject": "the fake, country-wet freshness",
          "verb": "evaporated",
          "stem": "evaporate",
          "object": "like the tail end of a sweet dream"
        },
        {
          "subject": "the hot streets",
          "verb": "wavered",
          "stem": "waver",
          "object": "in the sun"
        },
        {
          "subject": "I",
          "verb": "kept hearing",
          "stem": "hear",
          "object": "about the Rosenbergs over the radio and at the office"
        },
        {
          "subject": "I",
          "verb": "couldn't get",
          "stem": "get",
          "object": "them out of my mind"
        }
      ],
      "total_SVOs": 4
  },

  "lit-2": {...
}
are you ready?
"""
            resp = make_gpt_request(req)

            # Process each category
            for category, prefix in categories.items():
                print(category)
                iterate_category(category, prefix, error_log_path)

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")
    finally:
        stop_chat_gpt()



