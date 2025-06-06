import json
import time
import logging
import requests
import subprocess
import signal
import os
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

class UITestEquivalenceAnalysis:
    BASE_URL = "http://localhost:8080"
    TEMPLATES_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "data", "templates.json"))

    def __init__(self, logger):
        self.logger = logger
        self.server_process = None

        # Запускаем локальный сервер
        self.start_server()

        # Настройка Chrome WebDriver
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.implicitly_wait(20)

    def start_server(self):
        try:
            self.logger.info("Запуск локального сервера (app.py)...")
            app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app.py"))
            self.server_process = subprocess.Popen(
                ["python", app_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            def read_output(proc):
                for line in proc.stdout:
                    self.logger.info(f"[app.py] {line.strip()}")

            threading.Thread(target=read_output, args=(self.server_process,), daemon=True).start()

        except Exception as e:
            self.logger.error(f"Ошибка запуска сервера: {str(e)}")
            raise

    def stop_server(self):
        if self.server_process:
            self.logger.info("Остановка сервера...")
            if os.name == 'nt':
                self.server_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                self.server_process.terminate()
            self.server_process.wait()
            self.logger.info("Сервер остановлен")

    def wait_for_server(self, timeout=30):
        self.logger.info(f"Ожидание доступности сервера {self.BASE_URL}...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(self.BASE_URL, timeout=5)
                if response.status_code == 200:
                    self.logger.info("Сервер доступен")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        raise RuntimeError(f"Сервер не стал доступен за {timeout} секунд")

    def load_template(self, test_template):
        try:
            with open(self.TEMPLATES_FILE, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                for template in templates:
                    if template["name"] == test_template:
                        self.logger.info(f"Шаблон '{test_template}' успешно загружен")
                        return template["adjacency_matrix"]
                raise ValueError(f"Шаблон '{test_template}' не найден")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки шаблона: {str(e)}")
            raise

    def enter_matrix_data(self, matrix):
        try:
            vertex_count = self.driver.find_element(By.ID, "vertex-count")
            self.scroll_to_element(vertex_count)
            vertex_count.clear()
            vertex_count.send_keys(str(len(matrix)))
            time.sleep(0.1)

            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    cell = self.driver.find_element(By.NAME, f"cell-{i}-{j}")
                    self.scroll_to_element(cell)
                    cell.clear()
                    cell.send_keys(str(matrix[i][j]))
                    time.sleep(0.02)

            self.logger.info("Матрица смежности успешно заполнена")
        except Exception as e:
            self.logger.error(f"Ошибка ввода данных: {str(e)}")
            raise

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
            element
        )
        time.sleep(0.02)

    def check_equivalence_results(self):
        try:
            reflexive_result = self.driver.find_element(
                By.CSS_SELECTOR, ".property-card:nth-child(1) .property-result span").text
            symmetric_result = self.driver.find_element(
                By.CSS_SELECTOR, ".property-card:nth-child(2) .property-result span").text
            transitive_result = self.driver.find_element(
                By.CSS_SELECTOR, ".property-card:nth-child(3) .property-result span").text

            self.logger.info(f"Результаты анализа: Рефлексивность={reflexive_result}, "
                             f"Симметричность={symmetric_result}, Транзитивность={transitive_result}")

            reflexive_closure = self.driver.find_element(
                By.CSS_SELECTOR, ".closures-grid > div:nth-child(1) pre").text
            symmetric_closure = self.driver.find_element(
                By.CSS_SELECTOR, ".closures-grid > div:nth-child(2) pre").text
            transitive_closure = self.driver.find_element(
                By.CSS_SELECTOR, ".closures-grid > div:nth-child(3) pre").text

            self.logger.info("Матрицы замыканий успешно получены")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка проверки результатов: {str(e)}")
            return False

    def test_full_equivalence_analysis_flow(self):
        try:
            self.logger.info("Запуск тестирования анализа эквивалентности")

            self.wait_for_server(timeout=30)

            # Первый тест — эквивалентное отношение
            self.driver.get(self.BASE_URL)
            matrix = self.load_template("Эквивалентное отношение (4 вершины)")
            self.enter_matrix_data(matrix)
            time.sleep(2)
            build_btn = self.driver.find_element(By.ID, "build-graph")
            self.scroll_to_element(build_btn)
            build_btn.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#graph-area svg"))
            )
            time.sleep(2)
            methods_section = self.driver.find_element(By.ID, "methods")
            self.scroll_to_element(methods_section)
            time.sleep(1)
            equivalence_btn = self.driver.find_element(
                By.XPATH, "//a[.//span[contains(text(), 'Анализ отношений эквивалентности')]]")
            equivalence_btn.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".result-section"))
            )
            self.check_equivalence_results()
            time.sleep(3)

            # Второй тест — неэквивалентное отношение
            self.driver.get(self.BASE_URL)
            matrix = self.load_template("Неэквивалентное отношение (4 вершины)")
            self.enter_matrix_data(matrix)
            time.sleep(2)
            build_btn = self.driver.find_element(By.ID, "build-graph")
            self.scroll_to_element(build_btn)
            build_btn.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#graph-area svg"))
            )
            time.sleep(2)
            methods_section = self.driver.find_element(By.ID, "methods")
            self.scroll_to_element(methods_section)
            time.sleep(1)
            equivalence_btn = self.driver.find_element(
                By.XPATH, "//a[.//span[contains(text(), 'Анализ отношений эквивалентности')]]")
            equivalence_btn.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".result-section"))
            )
            self.check_equivalence_results()
            time.sleep(3)

            return True

        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}", exc_info=True)
            return False

        finally:
            self.driver.quit()
            self.logger.info("Браузер закрыт")
            self.stop_server()

def setup_logger():
    logger = logging.getLogger("UITestLogger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Тестирование страницы анализа эквивалентности")

    tester = UITestEquivalenceAnalysis(logger)
    success = tester.test_full_equivalence_analysis_flow()

    result = "Тест успешно пройден" if success else "Тест не пройден"
    logger.info(f"Результат тестирования: {result}")
    exit(0 if success else 1)
