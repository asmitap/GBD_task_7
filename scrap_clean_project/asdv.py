# from selenium import webdriver

# browser = webdriver.chrome(executable_path="/home/asmita/Desktop/webscrap/chromedriver")
# browser.get('https://www.google.com/search?q=shoes&client=ubuntu&hs=YUc&channel=fs&sxsrf=ALiCzsabge-ejkfBvWQBVeIzdjWsCkUDfQ%3A1657862814247&ei=nvrQYtLkDuztz7sPt4mX6Ao&ved=0ahUKEwjSq4ShlPr4AhXs9nMBHbfEBa0Q4dUDCA0&uact=5&oq=shoes&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywE6BwgAEEcQsAM6BwgAELADEEM6CggAEOQCELADGAE6BAgAEBM6BQgAEMQCOgQIABBDOgUIABCxAzoLCAAQgAQQsQMQgwE6BAgAEANKBQg8EgExSgQIQRgASgQIRhgBUPUGWJwSYM0UaAFwAXgAgAGuAYgBxAaSAQMwLjWYAQCgAQHIARHAAQHaAQYIARABGAk&sclient=gws-wiz')
# print('Title: %s' % browser.title)
# #time.sleep(10)
# browser.quit()
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(executable_path='/home/asmita/Desktop/webscrap/chromedriver')
driver.get("https://www.google.com/search?channel=fs&client=ubuntu&q=shoes")
time.sleep(30)

