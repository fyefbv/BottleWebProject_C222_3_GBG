import datetime
from bottle import template, post, get
from graph_operations.cycle_detector import CycleDetector
from graph_operations.graph_loader import get_adjacency_matrix, get_graph_json

@post('/cycle_detection')
def cycle_detection_handler():
    """
    Обработчик POST-запроса для поиска всех циклов в текущем графе.
    Извлекает матрицу смежности из полей request.forms без явного указания
    количества вершин. Поля должны быть названы в формате "cell-i-j".
    """
    year = datetime.datetime.now().year

    adjacency_matrix = get_adjacency_matrix()
    graph_json = get_graph_json(adjacency_matrix)

    detector = CycleDetector(adjacency_matrix)
    cycles = detector.find_cycles()

    # 7. Возвращаем шаблон с данными
    return template('cycle_detection',
                    title='Поиск циклов в графе',
                    year=year,
                    adjacency_matrix=adjacency_matrix,
                    graph_json=graph_json,
                    cycles=cycles)


@get('/cycle_detection')
def cycle_detection_get():
    """
    Обработчик GET-запроса: если пользователь сразу зашёл на страницу поиска циклов,
    без POST-данных, показываем шаблон с сообщением о том, что граф не построен.
    """
    year = datetime.datetime.now().year
    return template('cycle_detection',
                    title='Поиск циклов в графе',
                    year=year,
                    adjacency_matrix=None,
                    graph_json=None,
                    cycles=None)
