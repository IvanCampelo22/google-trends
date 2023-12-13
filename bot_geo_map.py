import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
import re
import uuid
import csv
from models.graph_models import Graphic
from selenium.webdriver.common.keys import Keys
from database.conn import session

dir = '/home/ivan/Projects/Charisma/google-trends/files/'

def bot_geo_map(param) -> None:
    try:
        chrome_options = Options()
        file_path = os.path.join(dir, 'geoMap.csv')

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False
        })

        chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

        link = 'https://trends.google.com.br/trends/'

        driver.get(link)

        sleep(3)

        if os.path.exists(file_path):
            os.remove(file_path)

        wait = WebDriverWait(driver, 20)
        input_element = wait.until(EC.element_to_be_clickable((By.ID, 'i7')))
        input_element.clear()
        input_element.send_keys(param)
        sleep(10)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.UywwFc-LgbsSe')))
        button.click()
        sleep(20)

        # Aguarde até que a `div` com a classe "fe-geo-chart-generated fe-atoms-generic-container" esteja visível na página
        container_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.fe-geo-chart-generated.fe-atoms-generic-container')))

        # Localize o botão de exportação dentro da `div` container
        export_button = container_div.find_element(By.CSS_SELECTOR, 'button.widget-actions-item.export')

        # Clique no botão de exportação
        export_button.click()




        print("O botão foi clicado")

        sleep(10)
    
    except Exception as e:
        print(f"Erro {e}")