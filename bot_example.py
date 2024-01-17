import os
import time
from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


# Defina a pasta dentro do seu projeto onde os downloads devem ser salvos temporariamente
project_download_dir = os.path.join(os.path.dirname(__file__), 'downloads')
if not os.path.exists(project_download_dir):
    os.makedirs(project_download_dir)


class Scraper():
    def __init__(self, search:str, base_url:str="https://trends.google.com.br/trends/explore", date:str="now", time:int="207-d", country:str="BR") -> None:
        self.search = search
        self.date = date
        self.country = country
        self.time = time # Por padrão está 7 dias
        self.base_url = f'{base_url}?date={self.date}%{self.time}&geo={self.country}&q={self.search}&hl=pt-BR'
        
        # Essa url tem alguns padrões, você pode verificar os padrões e setar na url acima, vá alterando manualmente no site e verificando os padrões
        # que a empresa necessita que funcione e monte a url, mas que seja algo dinâmico.
        
        # EXEMPLOS PEGO SO SITE GOOGLE TRENDS:
        "https://trends.google.com.br/trends/explore?date=now%204-H&geo=BE&q=casa&hl=pt-BR" # Ultimas 4 horas
        "https://trends.google.com.br/trends/explore?date=now%201-d&geo=BE&q=casa&hl=pt-BR" # Ontem
        "https://trends.google.com.br/trends/explore?date=now%207-d&geo=BE&q=casa&hl=pt-BR" # 7 dias
        "https://trends.google.com.br/trends/explore?date=today%201-m&geo=BE&q=casa&hl=pt-BR" # Ultimos 30 dias
        "https://trends.google.com.br/trends/explore?date=today%203-m&geo=BE&q=casa&hl=pt-BR" # Ultimos 90 dias
        "https://trends.google.com.br/trends/explore?geo=BE&q=casa&hl=pt-BR" # Ultimos 12 meses
        "https://trends.google.com.br/trends/explore?date=today%205-y&geo=BE&q=casa&hl=pt-BR" # Ultimos 5 anos
        
        
    def bot_search(self) -> None:
        logger.info("Starting bot...")
        
        # Configurações do Chrome para rodar em modo headless
        options = Options()
       #options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # Esta opção é importante para o Docker
        options.add_argument("--disable-dev-shm-usage")  # Isto pode ajudar se você estiver enfrentando problemas de memória
        options.add_argument("--disable-gpu")  # Recomendado para o modo headless
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option('prefs', {
            'download.default_directory': project_download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False
        })

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 30)

        try:
            driver.get(self.base_url)
            try:
                # Tenta localizar o texto do erro 429 na página
                error_message = wait.until(EC.visibility_of_element_located((By.ID, 'af-error-container')))
                if error_message:
                    logger.warning('Error 429 detected, refreshing...')
                    time.sleep(5)
                    driver.refresh()
            # Tenha em mente que você deve ter um número máximo de tentativas para evitar um loop infinito.
            except TimeoutException:
                # Se o erro 429 não estiver presente, prossiga normalmente
                pass
                               
            btn_download = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]')))
            if btn_download:
                logger.success('Botao para download capturado')
                btn_download.click()
                time.sleep(2)
                return btn_download.text
            else:
                print("Botão não encontrado.")
                return ''
            
        finally:
            driver.quit()

if __name__ == "__main__":
    scraper = Scraper("casa")
    scraper.bot_search()
    time.sleep(10)