from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

import re
import os
import csv
from time import sleep
from loguru import logger
from datetime import datetime

from database.conn import session
from bot.db_func import DatabaseFunctions
from bot.bot_func import BotsFunctions, dir


class Scrapping():

    def gooole_trends(param, country: None, period: None, initial_date: None, end_date: None, 
                    interest_over_time: bool,
                    interest_by_subregion: bool,
                    related_issues: bool,
                    related_searches: bool
    ) -> None:
        logger.info("Iniciando bot")

        try:
            chrome_options = Options()

            file_path_multi_time_line = os.path.join(dir, 'multiTimeline.csv')
            file_path_geo_map = os.path.join(dir, 'geoMap.csv')
            file_path_related_entities = os.path.join(dir, f'relatedEntities.csv')
            file_path_related_queries = os.path.join(dir, f'relatedQueries.csv')

            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--headless")
            chrome_options.add_experimental_option('prefs', {
                'download.default_directory': dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': False
            })

            driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
            wait = WebDriverWait(driver, 30)

            link = 'https://trends.google.com.br/trends/'
            driver.get(link)

            logger.success("O site do Google Trends foi aberto com sucesso!")

            sleep(3)

            if os.path.exists(file_path_multi_time_line):
                os.remove(file_path_multi_time_line)

            if os.path.exists(file_path_geo_map):
                os.remove(file_path_geo_map)

            if os.path.exists(file_path_related_entities):
                os.remove(file_path_related_entities)

            if os.path.exists(file_path_related_queries):
                os.remove(file_path_related_queries)

            wait = WebDriverWait(driver, 20)
            input_element = wait.until(EC.element_to_be_clickable((By.ID, 'i7')))
            input_element.clear()
            input_element.send_keys(param)

            sleep(10)

            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.UywwFc-LgbsSe')))
            button.click()

            sleep(20)

            logger.success("Login realizado com sucesso no Google Trends!")
        

            if country:
                BotsFunctions.by_region(driver, wait, country)

                        
            if period:
                BotsFunctions.filter_date(driver, wait, period)

                
            if initial_date and end_date:
                BotsFunctions.filter_date_person(driver, initial_date, end_date, wait)
            
            sleep(20)

            try:
                driver.find_element(By.XPATH, '//*[@id="cookieBar"]/div/span[2]/a[2]').click()
            except:
                pass

            print(f"Valor de interest_over_time: {interest_over_time}")
            
            if interest_over_time:

                present_graph = BotsFunctions.click_button_multi_timeline(driver, wait)                    

                if present_graph: 
                    logger.info("Iniciando processo de scrapping do Interesse ao Longo do Tempo")

                    with open(file_path_multi_time_line, "r", encoding="utf-8") as csv_file:
                        csv_reader = csv.reader(csv_file)
                        
                        for _ in range(6): 
                            next(csv_reader)

                        for row in csv_reader:
                            tempo = row[0]

                            logger.info("Tratando dados")
                            match = re.search(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2})?(?:[-+]\d{2}:\d{2})?', tempo)

                            if match:
                                tempo_formatado = match.group(0)

                                data_hora = datetime.strptime(tempo_formatado, '%Y-%m-%dT%H:%M:%S%z') if 'T' in tempo_formatado else datetime.strptime(tempo_formatado, '%Y-%m-%d')

                                data = data_hora.strftime('%Y-%m-%d')
                                hora = data_hora.strftime('%H:%M:%S')

                                valor_str = row[1].replace("<", "").strip()

                                numeros = re.findall(r'\d+', valor_str)

                                valor = int(numeros[0]) if numeros else None

                                print(f"Parâmetro de pesquisa: {param}")
                                print(f"Data: {data}, Hora: {hora}, Valor: {valor}")

                                DatabaseFunctions.save_multi_timeline(param, data, hora, valor)

                        logger.success("Dados processados com sucesso.")
                    
                    sleep(10)
                
                else: 
                    logger.info("Indo para o próximo gráfico")
                    pass

            if interest_by_subregion:
                present_graph = BotsFunctions.click_button_geo_map(driver, wait)

                if present_graph:
                    logger.info("Iniciando processo de scrapping do Sub-Região")
                    with open(file_path_geo_map, "r", encoding="utf-8") as csv_file:
                        csv_reader = csv.reader(csv_file)

                        for _ in range(2): 
                            next(csv_reader)

                        for row in csv_reader:
                            region = row[0]
                            valor_str = row[1].replace("<", "").strip()
                            numeros = re.findall(r'\d+', valor_str)

                            value_region = int(numeros[0]) if numeros else None

                            if re.search(r'\(\d{2}/\d{2}/\d{4}, \d{2}:\d{2} – \d{2}/\d{2}/\d{4}, \d{2}:\d{2}\)', row[1]):
                                data_hora_str = re.search(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) – (\d{2}/\d{2}/\d{4}, \d{2}:\d{2})', row[1])
                                data_inicio = data_hora_str.group(1)
                                data_fim = data_hora_str.group(2)
                            
                            print(f"Região: {region}, valor: {value_region}")
                            print(f"Data Inicial: {data_inicio}, Data Final: {data_fim}")

                            DatabaseFunctions.save_region(param, data_inicio, data_fim, region, value_region)
                    
                    sleep(10)
                
                else: 
                    logger.info("Indo para o próximo gráfico")
                    pass

            BotsFunctions.scroll(driver)

            if related_issues: 
                try:

                    present_graph = BotsFunctions.click_button_related_entities(driver, wait)

                    if present_graph:
                        logger.info("Iniciando processo de scrapping de Assuntos Relacionados TOP")
                        with open(file_path_related_entities, "r", encoding="utf-8") as csv_file:
                            csv_reader = csv.reader(csv_file)

                            for _ in range(4):
                                next(csv_reader)

                            for row in csv_reader:
                                entities = row[0]
                                value_str = row[1].replace("<", "").strip()
                                numeros = re.findall(r'\d+', value_str)

                                value_related_entities = int(numeros[0]) if numeros else None

                                DatabaseFunctions.save_related_entities_top(param, country, data_inicio, data_fim, entities=entities, value_related_entities=value_related_entities)
                    
                                logger.info("Iniciando processo de scrapping de Assuntos Relacionados RISING")
                                rising_data = []
                                with open(file_path_related_entities, "r", encoding="utf-8") as file:
                                    current_section = None
                                    for line in file:
                                        line = line.strip()
                                        
                                        if line == "RISING":
                                            current_section = rising_data
                                        elif current_section is not None and line:
                                            parts = line.split(",")
                                            if len(parts) == 2:
                                                entity, value = [part.strip() for part in parts]
                                                current_section.append((entity, value))

                                for entity, value in rising_data:
                                    print(f"Entidade: {entity}")
                                    print(f"Valor: {value}")
                                    print() 

                                    DatabaseFunctions.save_related_entities_rising(param, country, data_inicio, data_fim, entity, value)

                except Exception as e:
                    logger.error(e)
                
                        
                sleep(10)

            else:
                logger.info("Indo para o próximo gráfico")
                pass

            
            if related_searches:
                try:
                    present_graph = BotsFunctions.click_button_related_queries(driver, wait)

                    if present_graph:
                        logger.info("Iniciando processo de scrapping de Pesquisas Relacionados TOP")
                        with open(file_path_related_queries, "r", encoding="utf-8") as csv_file:
                            csv_reader = csv.reader(csv_file)

                            for _ in range(4):
                                next(csv_reader)

                            for row in csv_reader:
                                entities = row[0]
                                value_str = row[1].replace("<", "").strip()
                                numeros = re.findall(r'\d+', value_str)

                                value_related_queries = int(numeros[0]) if numeros else None

                                DatabaseFunctions.save_related_queries_top(param, country, data_inicio, data_fim, entities,value_related_entities, value_related_queries)
                        
                                logger.info("Iniciando processo de scrapping de Pesquisas Relacionadas RISING")
                                rising_data = []
                                with open(file_path_related_queries, "r", encoding="utf-8") as file:
                                    current_section = None
                                    for line in file:
                                        line = line.strip()
                                        
                                        if line == "RISING":
                                            current_section = rising_data
                                        elif current_section is not None and line:
                                            parts = line.split(",")
                                            if len(parts) == 2:
                                                entity, value = [part.strip() for part in parts]
                                                current_section.append((entity, value))

                                for entity, value in rising_data:
                                    print(f"Entidade: {entity}")
                                    print(f"Valor: {value}")
                                    print()

                                    DatabaseFunctions.save_related_queries_rising(param, country, data_inicio, data_fim, entity, value)
        
                except IndexError:
                    pass

                finally:
                    pass
            
            else:
                logger.info("Indo para o próximo gráfico")
                pass
        
        except Exception as e: 
            session.rollback()
            logger.error(f"Erro:{e}")

        finally:
            session.close()
            driver.quit()