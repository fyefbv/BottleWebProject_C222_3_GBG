import datetime
from bottle import template, get
from graph_operations.equivalence_analyzer import EquivalenceAnalyzer
from graph_operations.graph_loader import get_adjacency_matrix, get_graph_json

@get('/equivalence')
def equivalence_handler():
    """Обработчик GET-запросов для страницы анализа эквивалентности"""
    # Получение текущего года (для отображения в шаблоне)
    year = datetime.datetime.now().year
    
    # Загрузка матрицы смежности графа
    adjacency_matrix = get_adjacency_matrix()
    
    # Если матрица пуста - возвращаем шаблон с ошибкой
    if not adjacency_matrix:
        return template('equivalence',
                        title='Эквивалентность',
                        year=year,
                        results=None,
                        graph_json=None)
    
    # Преобразование матрицы в JSON для визуализации графа
    graph_json = get_graph_json(adjacency_matrix)
    
    # Анализ свойств матрицы
    try:
        analyzer = EquivalenceAnalyzer(adjacency_matrix)
        results = analyzer.analyze()
    except Exception as e:
        print(f"Ошибка анализа: {e}")
        results = None
    
    # Рендеринг шаблона с результатами
    return template('equivalence',
                    title='Эквивалентность',
                    year=year,
                    results=results,
                    graph_json=graph_json)