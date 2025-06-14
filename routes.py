"""
Routes and views for the bottle application.
"""

from bottle import route, view, get
from datetime import datetime
from graph_operations.graph_loader import get_adjacency_matrix, get_graph_json
from handlers.handler_index import index_handler
from handlers.handler_cycle_detection import cycle_detection_handler
from handlers.handler_equivalence import equivalence_handler

from handlers.handler_max_flow import generate_graph
from handlers.handler_max_flow import build_graph_handler    




@get('/')
@get('/home')
@view('index')
def home():
    """Отображает главную страницу"""
    return dict(
        title='Главная страница',
        graph_json = '',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Отображает страницу «О нас»"""
    return dict(
        title='Об авторах проекта',
        year=datetime.now().year
    )


@route('/equivalence')
def equivalence():
    return equivalence_handler()

@get('/cycle_detection')
@view('cycle_detection')
def cycle_detection():
    return dict(
        title='Поиск циклов в графе',
        year=datetime.now().year,
        adjacency_matrix=None,
        graph_json=None,
        cycles=None
    )

@route('/max_flow')
@view('max_flow')
def max_flow():
    """Отображает страницу поиска максимального потока"""
    return dict(
        title='Поиск максимального потока',
        year=datetime.now().year,
        graph_json = '',
        adjacency_matrix=None,
        max_flow_value=None,
        flow=None
    )