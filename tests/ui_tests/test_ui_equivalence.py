import json
import time
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class EquivalenceUITest:
    BASE_URL = "http://localhost:8080"
    TEMPLATES_FILE = os.path.abspath("static/data/templates.json")    
    TEST_TEMPLATE = "Граф (15 вершин)"  # Шаблон для тестирования
    
    
    def __init__(self, logger):
        self.logger = logger
        
        # Настройка Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Максимизируем окно
        self.driver_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.driver_service, options=chrome_options)
        self.driver.implicitly_wait(10)
        self.logger.info("Браузер Chrome инициализирован")

    def load_template(self):
        """Загрузка шаблона матрицы из JSON-файла"""
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

    def enter_matrix_data(self, matrix):
        """Ввод матрицы смежности на главной странице"""
        try:
            # Установка количества вершин
            vertex_count = self.driver.find_element(By.ID, "vertex-count")
            vertex_count.clear()
            vertex_count.send_keys(str(len(matrix)))
            time.sleep(0.5)
            
            # Ввод значений матрицы
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    cell = self.driver.find_element(By.NAME, f"cell-{i}-{j}")
                    cell.clear()
                    cell.send_keys(str(matrix[i][j]))
            
            self.logger.info("Матрица смежности успешно заполнена")
        except Exception as e:
            self.logger.error(f"Ошибка ввода данных: {str(e)}")
            raise

    def test_full_equivalence_flow(self):
        """Полный тест: от ввода данных до получения результатов эквивалентности"""
        try:
            self.logger.info("Запуск тестирования страницы эквивалентности...")
            
            # 1. Переход на главную страницу
            self.logger.info(f"Открытие главной страницы: {self.BASE_URL}")
            self.driver.get(self.BASE_URL)
            
            # 2. Загрузка тестовых данных
            matrix = self.load_template()
            self.logger.info(f"Используется шаблон: {self.TEST_TEMPLATE}")
            
            # 3. Ввод матрицы
            self.logger.info("Ввод матрицы смежности...")
            self.enter_matrix_data(matrix)
            
            # 4. Построение графа
            self.logger.info("Построение графа...")
            build_btn = self.driver.find_element(By.ID, "build-graph")
            build_btn.click()
            
            # 5. Ожидание построения графа
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#graph-area svg"))
            )
            self.logger.info("Граф успешно построен")
            
            # 6. Переход на страницу эквивалентности
            self.logger.info("Переход на страницу эквивалентности...")
            # Используем JavaScript для навигации, так как прямой URL проще
            self.driver.get(self.BASE_URL + "/equivalence")
            
            # 7. Ожидание загрузки страницы эквивалентности
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Эквивалентность')]"))
            )
            self.logger.info("Страница эквивалентности загружена")
            
            # 8. Проверка результатов
            # - Визуализация графа
            graph = self.driver.find_element(By.ID, "d3-graph")
            if not graph.is_displayed():
                raise ValueError("Граф не отображается")
            self.logger.info("Граф отображается корректно")
            
            # - Проверка свойств отношения
            reflexive_result = self.driver.find_element(
                By.XPATH, "//h3[contains(text(), 'Рефлексивность')]/following-sibling::div[contains(@class, 'property-result')]/span"
            )
            symmetric_result = self.driver.find_element(
                By.XPATH, "//h3[contains(text(), 'Симметричность')]/following-sibling::div[contains(@class, 'property-result')]/span"
            )
            transitive_result = self.driver.find_element(
                By.XPATH, "//h3[contains(text(), 'Транзитивность')]/following-sibling::div[contains(@class, 'property-result')]/span"
            )
            
            self.logger.info(f"Рефлексивность: {reflexive_result.text}")
            self.logger.info(f"Симметричность: {symmetric_result.text}")
            self.logger.info(f"Транзитивность: {transitive_result.text}")
            
            # Проверяем, что все свойства определены (не прочерки)
            if reflexive_result.text == "–" or symmetric_result.text == "–" or transitive_result.text == "–":
                raise ValueError("Не все свойства отношения определены")
            
            # - Проверка замыканий
            closures = self.driver.find_elements(By.CSS_SELECTOR, ".closure-section .matrix-container pre")
            if len(closures) < 3:
                raise ValueError("Не все замыкания отображаются")
                
            self.logger.info(f"Рефлексивное замыкание:\n{closures[0].text}")
            self.logger.info(f"Симметричное замыкание:\n{closures[1].text}")
            self.logger.info(f"Транзитивное замыкание:\n{closures[2].text}")
            
            self.logger.info("Тест успешно завершен!")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}", exc_info=True)
            return False
            
        finally:
            # Всегда закрываем браузер
            self.driver.quit()
            self.logger.info("Браузер закрыт")

def setup_logger():
    """Настройка системы логирования только для консоли"""
    # Настройка логгера
    logger = logging.getLogger("UITestLogger")
    logger.setLevel(logging.INFO)
    
    # Форматтер для сообщений
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
    # Настройка логирования
    logger = setup_logger()
    
    logger.info("="*50)
    logger.info("Тестирование страницы эквивалентности")
    logger.info("="*50)
    
    try:
        tester = EquivalenceUITest(logger)
        success = tester.test_full_equivalence_flow()
        
        result = "УСПЕХ" if success else "НЕУДАЧА"
        logger.info("\nРезультат тестирования: %s", result)
    except Exception as e:
        logger.exception("Критическая ошибка при выполнении теста: %s", str(e))
        success = False
    
    logger.info("="*50)
    exit(0 if success else 1)