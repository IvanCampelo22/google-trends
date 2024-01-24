from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

import re
import os
import uuid
import csv
from time import sleep
from loguru import logger
from datetime import datetime

from database.conn import session
from models.graph_models import Graphic
from models.geo_map_models import GeoMap
from bot.bot_func import BotsFunctions, dir
from models.related_queries_models import RelatedQueriesTop, RelatedQueriesRising
from models.related_entities_models import RelatedEntitiesTop, RelatedEntitiesRising


class Scrapping():

    def gooole_trends(param, country: None, period: None, initial_date: None, end_date: None) -> None:
        logger.info("Iniciando bot")

        try:
            chrome_options = Options()

            file_path_multi_time_line = os.path.join(dir, 'multiTimeline.csv')
            file_path_geo_map = os.path.join(dir, 'geoMap.csv')
            file_path_related_entities = os.path.join(dir, f'relatedEntities.csv')
            file_path_related_queries = os.path.join(dir, f'relatedQueries.csv')

            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
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

            BotsFunctions.click_button_multi_timeline(wait)
                    

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

                        new_uuid = uuid.uuid4()

                        data_graphic_trends = Graphic(
                                uuid = new_uuid,
                                name=param,
                                date=data,
                                hour=hora,
                                value=str(valor)
                            )          
                        
                        try:
                            logger.success("Salvando no banco de dados Interesse ao Longo do Tempo")
                            with session.begin_nested():
                                existing_record = session.query(Graphic).filter_by(
                                    name=param,
                                    date=data,
                                    hour=hora,
                                    value=str(valor)
                                ).one_or_none()

                            if existing_record:
                                existing_record.value = str(valor)
                                existing_record.date = data 
                                existing_record.hour = hora
                            else:
                                session.merge(data_graphic_trends)

                            session.commit()
                        except Exception as e:
                            session.rollback()
                            logger.error(f"Erro ao inserir/atualizar registro: {str(e)}")          

                logger.success("Dados processados com sucesso.")
            

            sleep(10)

            BotsFunctions.click_button_geo_map(wait)

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

                    new_uuid = uuid.uuid4()

                    geo_map_trends = GeoMap(
                            uuid = new_uuid,
                            param=param,
                            initial_date=data_inicio,
                            end_date=data_fim,
                            region=region,
                            value=str(value_region)
                        )          
                    
                    try:
                        logger.info("Salvando no banco de dados Sub-Região")
                        with session.begin_nested():
                            existing_record = session.query(GeoMap).filter_by(
                                param=param,
                                initial_date=data_inicio,
                                end_date=data_fim,
                                region=region,
                                value=str(value_region)
                            ).one_or_none()

                        if existing_record:
                            existing_record.initial_date = data_inicio
                            existing_record.end_date = data_fim
                            existing_record.region = region 
                            existing_record.value = str(value_region)
                        else:
                            session.merge(geo_map_trends)

                        session.commit()
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Erro ao inserir/atualizar registro de Sub-Região: {str(e)}")

            
            sleep(10)

            BotsFunctions.scroll(driver)
            
            try:

                BotsFunctions.click_button_related_entities(wait)

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

                        new_uuid = uuid.uuid4()

                        related_entities = RelatedEntitiesTop(
                                uuid = new_uuid,
                                param=param,
                                region=country,
                                initial_date=data_inicio,
                                end_date=data_fim,
                                entities=entities,
                                value=str(value_related_entities)
                            )          
                        
                        try:
                            logger.info("Salvando no banco de dados Assuntos Relacionados TOP")
                            with session.begin_nested():
                                existing_record = session.query(RelatedEntitiesTop).filter_by(
                                    param=param,
                                    region=country,
                                    initial_date=data_inicio,
                                    end_date=data_fim,
                                    entities=entities,
                                    value=str(value_related_entities)
                                ).one_or_none()

                            if existing_record:
                                existing_record.region = country 
                                existing_record.initial_date = data_inicio
                                existing_record.end_date = data_fim
                                existing_record.entities = entities
                                existing_record.value = value_related_entities
                            else:
                                session.merge(related_entities)

                            session.commit()
                        except Exception as e:
                            session.rollback()
                            logger.error(f"Erro ao inserir/atualizar registro na tabela de Assuntos Relacionados Top {str(e)}")
            
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

                        
                            new_uuid = uuid.uuid4()

                            related_entities_rising = RelatedEntitiesRising(
                                    uuid = new_uuid,
                                    param=param,
                                    region=country,
                                    initial_date=data_inicio,
                                    end_date=data_fim,
                                    entities=entity,
                                    value=str(value)
                                )          
                            
                            try:
                                logger.info("Salvando no banco de dados Assuntos Relacionados RISING")
                                with session.begin_nested():
                                    existing_record = session.query(RelatedEntitiesRising).filter_by(
                                        param=param,
                                        region=country,
                                        initial_date=data_inicio,
                                        end_date=data_fim,
                                        entities=entity,
                                        value=str(value)
                                    ).one_or_none()

                                if existing_record:
                                    existing_record.region = country 
                                    existing_record.initial_date = data_inicio
                                    existing_record.end_date = data_fim
                                    existing_record.entities = entity
                                    existing_record.value = str(value)
                                else:
                                    session.merge(related_entities_rising)

                                session.commit()
                            except Exception as e:
                                session.rollback()
                                logger.error(f"Erro ao inserir/atualizar registro Assuntos Relacionados RISING: {str(e)}")
            
            except Exception as e:
                logger.error(e)
            
            finally:
                pass
                        
            sleep(10)


            try:
                
                BotsFunctions.click_button_related_queries(wait)

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

                        new_uuid = uuid.uuid4()

                        related_queries = RelatedQueriesTop(
                                uuid = new_uuid,
                                param=param,
                                region=country,
                                initial_date=data_inicio,
                                end_date=data_fim,
                                queries=entities,
                                value=str(value_related_entities)
                            )          
                        
                        try:
                            logger.info("Salvando no banco de dados Pesquisas Relacionadas TOP")
                            with session.begin_nested():
                                existing_record = session.query(RelatedQueriesTop).filter_by(
                                    param=param,
                                    region=country,
                                    initial_date=data_inicio,
                                    end_date=data_fim,
                                    queries=entities,
                                    value=str(value_related_queries)
                                ).one_or_none()

                            if existing_record:
                                existing_record.region = country
                                existing_record.initial_date = data_inicio
                                existing_record.end_date = data_fim
                                existing_record.queries = entities
                                existing_record.value = str(value_related_queries)
                            else:
                                session.merge(related_queries)

                            session.commit()
                        except Exception as e:
                            session.rollback()
                            logger.error(f"Erro ao inserir/atualizar registro na tabela de Pesquisas Relacionadas Top {str(e)}")
                

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

                        
                            new_uuid = uuid.uuid4()

                            related_queries_rising = RelatedQueriesRising(
                                    uuid = new_uuid,
                                    param=param,
                                    region=country,
                                    initial_date=data_inicio,
                                    end_date=data_fim,
                                    queries=entity,
                                    value=str(value)
                                )          
                            
                            try:
                                logger.info("Tentando inserir/atualizar registro Pesquisas Relacionadas RISING")
                                
                                with session.begin_nested():
                                    existing_record = session.query(RelatedQueriesRising).filter_by(
                                        uuid=new_uuid,
                                        param=param,
                                        region=country,
                                        initial_date=data_inicio,
                                        end_date=data_fim,
                                        queries=entity,
                                        value=str(value)
                                    ).one_or_none()

                                if existing_record:
                                    existing_record.region = country
                                    existing_record.initial_date = data_inicio
                                    existing_record.end_date = data_fim
                                    existing_record.queries = entity
                                    existing_record.value = str(value)
                                else:
                                    session.merge(related_queries_rising)

                                session.commit()
                            except Exception as e:
                                session.rollback()
                                logger.error(f"Erro ao inserir/atualizar registro Pesquisas Relacionadas RISING: {str(e)}")


            except IndexError:
                pass

            finally:
                pass
        
        except Exception as e: 
            session.rollback()
            logger.error(f"Erro:{e}")

        finally:
            session.close()
            driver.quit()
        


            