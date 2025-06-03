import datetime
from bottle import template, post
from graph_operations.cycle_detector import CycleDetector
from graph_operations.graph_loader import get_adjacency_matrix, get_graph_json

@post('/cycle_detection')
def cycle_detection_handler():

    year = datetime.datetime.now().year

    adjacency_matrix = get_adjacency_matrix()
    graph_json = get_graph_json(adjacency_matrix)

    detector = CycleDetector(adjacency_matrix)
    cycles = detector.find_cycles()

    # Возвращаем шаблон с данными
    return template('cycle_detection',
                    title='Поиск циклов в графе',
                    year=year,
                    adjacency_matrix=adjacency_matrix,
                    graph_json=graph_json,
                    cycles=cycles)
