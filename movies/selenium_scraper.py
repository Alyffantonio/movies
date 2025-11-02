from django.conf import settings
import requests
import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    options = Options()
    if settings.SELENIUM_HEADLESS:
        options.add_argument('--headless')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    service = Service(executable_path=settings.SELENIUM_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_rotten_tomatoes(titulo):

    driver = None
    try:
        driver = setup_driver()
        query = quote(titulo)
        driver.get(f"https://www.rottentomatoes.com/search?search={query}")

        wait = WebDriverWait(driver, 10)

        search_results = wait.until(
            EC.presence_of_element_located((By.ID, 'search-results'))
        )

        first_result = search_results.find_element(By.TAG_NAME, 'search-page-media-row')

        score = first_result.get_attribute('tomatometer-score')

        if score:
            return f"{score}%"

        return "N/A"

    except Exception as e:
        print(f"erro ao buscar '{titulo}' no Rotten Tomatoes: {e}")
        return "N/A"
    finally:
        if driver:
            driver.quit()


def get_metacritic(titulo):

    driver = None
    try:
        driver = setup_driver()
        query = quote(titulo)
        driver.get(f"https://www.metacritic.com/search/{query}")

        wait = WebDriverWait(driver, 10)

        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
            print("Botão de cookies aceito.")
            time.sleep(1)
        except Exception:
            print(" Botão de cookies não encontrado.")

        first_result = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='search-result-item']"))
        )

        score_element = first_result.find_element(By.CSS_SELECTOR, "div[data-testid='product-metascore'] span")

        score = score_element.text

        if score:
            return score

        return "N/A"

    except Exception as e:
        print(f" Erro ao buscar '{titulo}' no Metacritic: {e}")
        return "N/A"
    finally:
        if driver:
            driver.quit()