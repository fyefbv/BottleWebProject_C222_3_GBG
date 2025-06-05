import json
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

class CycleDetectionUITest:
    BASE_URL = "http://localhost:8080"
    TEMPLATES_FILE = "static/data/templates.json" 
    TEST_TEMPLATE = "Граф (15 вершин)"  # Шаблон для тестирования
    
    def __init__(self, logger):
        self.logger = logger
        
        # Настройка Firefox WebDriver
        self.driver_service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=self.driver_service)
        self.driver.implicitly_wait(10)
        self.logger.info("Браузер Firefox инициализирован")

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

    def test_full_cycle_detection_flow(self):
        """Полный тест: от ввода данных до получения результатов"""
        try:
            self.logger.info("Запуск тестирования...")
            
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
            
            # 6. Переход на страницу поиска циклов
            self.logger.info("Переход на страницу поиска циклов...")
            cycle_btn = self.driver.find_element(By.ID, "cycle-detection-btn")
            cycle_btn.click()
            
            # 7. Ожидание загрузки страницы циклов
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "cycle-detected"))
            )
            self.logger.info("Страница поиска циклов загружена")
            
            # 8. Проверка результатов
            # - Количество циклов
            cycle_count = self.driver.find_element(By.ID, "cycle-detected").text
            if not cycle_count.isdigit():
                raise ValueError("Некорректное значение количества циклов")
                
            cycle_count = int(cycle_count)
            if cycle_count <= 0:
                raise ValueError("Циклы не обнаружены")
                
            self.logger.info(f"Найдено циклов: {cycle_count}")
            
            # - Список циклов
            cycle_list = self.driver.find_element(By.ID, "cycle-example").text
            if "Циклов не найдено" in cycle_list:
                raise ValueError("Список циклов пуст")
            self.logger.info("Список циклов отображается корректно")
            
            # - Визуализация графа
            graph = self.driver.find_element(By.ID, "d3-graph")
            if not graph.is_displayed():
                raise ValueError("Граф не отображается")
            self.logger.info("Граф отображается корректно")
            
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
    logger.info("Тестирование страницы поиска циклов")
    logger.info("="*50)
    
    try:
        tester = CycleDetectionUITest(logger)
        success = tester.test_full_cycle_detection_flow()
        
        result = "УСПЕХ" if success else "НЕУДАЧА"
        logger.info("\nРезультат тестирования: %s", result)
    except Exception as e:
        logger.exception("Критическая ошибка при выполнении теста: %s", str(e))
        success = False
    
    logger.info("="*50)
    exit(0 if success else 1)