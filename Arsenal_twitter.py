# %%
 
import yfinance as yf
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import os
import pandas as pd
import numpy as np
import glob
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import sys
import time


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

st.title("Interactions download app Created by NLP Dream Team")

dirname = st.text_input('Folder download',"")
dirname=dirname.replace("/","\\")
st.write('Folder download', dirname)



route_chromedriver = st.text_input('Chromedriver path',"")
route_chromedriver=route_chromedriver.replace("/","\\")
st.write('Current chromedriver path', route_chromedriver)
#print(route_chromedriver)


d = st.date_input(
     "Day to download",
     datetime.date(2021, 8, 11))
st.write('Selected date is:', d.strftime("%m/%d/%Y"))

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
     dataframe = pd.read_csv(uploaded_file)
     #st.write(dataframe)

def filter_df_bydate(d, dataframe):

    d=d.strftime("%m/%d/%Y")
    dataframe["Date2"]=pd.to_datetime(dataframe['Date'])
    dataframe["Date2"]=dataframe["Date2"].apply(lambda x: x.strftime("%m/%d/%Y"))
    dataframe=dataframe[dataframe["Date2"]==d]
    Call_day_download=dataframe[["Conversation ID","Date2"]]

    return Call_day_download

new_df=filter_df_bydate(d, dataframe)

st.write(new_df)

st.write("We are going to download interactions of day",d.strftime("%m/%d/%Y"))


#Download
def setting_selenium_options(download_file_path:str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    
    prefs = {
        "download.default_directory":download_file_path
        #"download.prompt_for_download": False,
        #"download.directory_upgrade": True
        }

    options.add_experimental_option('prefs', prefs)
    return options

options = setting_selenium_options(download_file_path = dirname)

def delete_selenium_log():
    if os.path.exists('selenium.log'):
        os.remove('selenium.log')


def show_selenium_log():
    if os.path.exists('selenium.log'):
        with open('selenium.log') as f:
            content = f.read()
            st.code(content)

def get_chromedriver_path():
    results = glob.glob('/**/chromedriver', recursive=True)  # workaround on streamlit sharing
    which = results[0]
    return which
            
            
      
# %%
#LogIn
def Login():
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        driver.get('https://signin.vivint.com/app/vivintinc_genesyspurecloud_1/exk4bop5qmPYkzu632p7/sso/saml?SAMLRequest=PHNhbWxwOkF1dGhuUmVxdWVzdCB4bWxuczpzYW1scD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOnByb3RvY29sIiB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBJRD0iSEs1RWpqS1ZRWmhFaUVvR0RLQ2xEZ0s1TGkwWWdraWl0b3EzTTJOdHlmSSIgVmVyc2lvbj0iMi4wIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iaHR0cHM6Ly9sb2dpbi51c3cyLnB1cmUuY2xvdWQvc2FtbCIgSXNzdWVJbnN0YW50PSIyMDIxLTA4LTI3VDE3OjAyOjUyWiIgRGVzdGluYXRpb249Imh0dHBzOi8vc2lnbmluLnZpdmludC5jb20vYXBwL3ZpdmludGluY19nZW5lc3lzcHVyZWNsb3VkXzEvZXhrNGJvcDVxbVBZa3p1NjMycDcvc3NvL3NhbWwiPjxzYW1sOklzc3Vlcj5odHRwOi8vd3d3Lm9rdGEuY29tL2V4azRib3A1cW1QWWt6dTYzMnA3PC9zYW1sOklzc3Vlcj48c2FtbHA6TmFtZUlEUG9saWN5IEFsbG93Q3JlYXRlPSJ0cnVlIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OnRyYW5zaWVudCIvPjwvc2FtbHA6QXV0aG5SZXF1ZXN0Pg%3D%3D')
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[id="okta-signin-username"]'))).send_keys("oscar.fernandez")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[id="okta-signin-submit"]'))).click()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[name="password"]'))).send_keys("TPteamNLP2021")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button.button-primary'))).click()


        time.sleep(10)

        driver.get("https://apps.usw2.pure.cloud/directory")
    






#driver = webdriver.Chrome(route_chromedriver, options=options)

st.write(dirname)






min = st.text_input('Min',"")
min=int(min)
max = st.text_input('Max',"")
max=int(max)
def download_audio(new_df,dirname,min, max):
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:

        for index,row in new_df[min:max].iterrows():

            driver.get(f'https://apps.usw2.pure.cloud/directory/#/engage/admin/interactions/{row[0]}/details')
            #time.sleep(10)
            try: 
                #Frame_reference=driver.find_element_by_xpath('//*[@id="ember1896"]/iframe')
                #driver.switch_to.frame(Frame_reference)
                #WebDriverWait(driver, 120).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="ember926"]/iframe')))
                WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@class="main-iframe visible ember-view"]/iframe')))

            except:
                pass

            try:
                #time.sleep(15)

                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="btn btn-link"]'))).click()
                #time.sleep(10)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="btn btn-default recording-download-button"]'))).click()

                #time.sleep(30)
                descargando = True
                while descargando == True:
                    carpeta_Download = os.listdir(dirname)
                    #carpeta_Download = os.listdir(r"C:\Users\fernandeztovar.7\Downloads")
                    if f"Call1-{row[0]}.WAV.crdownload" in carpeta_Download:
                        descargando = False      
                st.write(f"Downloaded interaction ID {index}: {row[0]}")

            except:

                st.write(f"Can't download interaction ID {index}: {row[0]}")


if __name__ == "__main__":
        
    delete_selenium_log()
    # executable_path = get_chromedriver_path()
    executable_path = "notset"
    # st.info(f'Chromedriver Path: {str(executable_path)}')
    st.balloons()
    if st.button('Start Selenium run'):
        
        st.info('Selenium is running, please wait...')
        Login()
        download_audio(new_df,dirname, min, max)

        show_selenium_log()
    


# %%



