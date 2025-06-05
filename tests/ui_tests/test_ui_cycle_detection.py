import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

class UITestCycleDetection:
    BASE_URL = "http://localhost:8080"
    TEMPLATES_FILE = "static/data/templates.json" 
    TEST_TEMPLATE = "Граф (15 вершин)"
    
    def __init__(self, logger):
        self.logger = logger
        
        # Настройка Firefox WebDriver
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.implicitly_wait(10)

    # Загрузка шаблона матрицы из JSON-файла
    def load_template(self):
        try:
            with open(self.TEMPLATES_FILE, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                for template in templates:
                    if template["name"] == self.TEST_TEMPLATE:
                        self.logger.info(f"Шаблон '{self.TEST_TEMPLATE}' успешно загружен")
                        return template["adjacency_matrix"]
                raise ValueError(f"Шаблон '{self.TEST_TEMPLATE}' не найден")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки шаблона: {str(e)}")
            raise

    # Ввод матрицы смежности на главной странице
    def enter_matrix_data(self, matrix):
        try:
            # Установка количества вершин
            vertex_count = self.driver.find_element(By.ID, "vertex-count")
            vertex_count.clear()
            vertex_count.send_keys(str(len(matrix)))
            time.sleep(0.1)
            
            # Ввод значений матрицы
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    cell = self.driver.find_element(By.NAME, f"cell-{i}-{j}")
                    cell.clear()
                    cell.send_keys(str(matrix[i][j]))
                    time.sleep(0.05)
            
            self.logger.info("Матрица смежности успешно заполнена")
        except Exception as e:
            self.logger.error(f"Ошибка ввода данных: {str(e)}")
            raise

    # Полный тест: от ввода данных до получения результатов
    def test_full_cycle_detection_flow(self):
        try:
            self.logger.info("Запуск тестирования")
            
            # Переход на главную страницу
            self.logger.info(f"Открытие главной страницы: {self.BASE_URL}")
            self.driver.get(self.BASE_URL)
            
            # Загрузка тестовых данных
            matrix = self.load_template()
            
            # Ввод матрицы
            self.logger.info("Ввод матрицы смежности")
            self.enter_matrix_data(matrix)
            time.sleep(2)
            
            # Построение графа
            self.logger.info("Построение графа")
            build_btn = self.driver.find_element(By.ID, "build-graph")
            build_btn.click()
            
            # Ожидание построения графа
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#graph-area svg"))
            )
            self.logger.info("Граф успешно построен")
            time.sleep(4)
            
            # Переход на страницу поиска циклов
            self.logger.info("Переход на страницу поиска циклов")
            cycle_btn = self.driver.find_element(By.ID, "cycle-detection-btn")
            cycle_btn.click()
            
            # Ожидание загрузки страницы циклов
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "cycle-detected"))
            )
            self.logger.info("Страница поиска циклов загружена")
            time.sleep(2)
            
            # Вывод количества найденных циклов
            cycle_count = self.driver.find_element(By.ID, "cycle-detected").text
                
            self.logger.info(f"Найдено циклов: {cycle_count}")
            time.sleep(5)

            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}", exc_info=True)
            return False
            
        finally:
            self.driver.quit()
            self.logger.info("Браузер закрыт")

# Настройка логгера
def setup_logger():
    logger = logging.getLogger("UITestLogger")
    logger.setLevel(logging.INFO)
    
    # Формат сообщений
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(console_handler)
    
    return logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Тестирование страницы поиска циклов")
    
    tester = UITestCycleDetection(logger)
    success = tester.test_full_cycle_detection_flow()
        
    result = "Тест успешно пройден" if success else "Тест не пройден"
    logger.info(f"Результат тестирования: {result}")
    exit(0 if success else 1)