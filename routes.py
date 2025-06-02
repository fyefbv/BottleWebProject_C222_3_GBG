"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime
from graph_operations.graph_loader import get_adjacency_matrix, get_graph_json
from handlers.handler_index import build_graph_handler
from handlers.handler_cycle_detection import cycle_detection_handler

@route('/')
@route('/home')
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
@view('equivalence')
def equivalence():
    """Отображает страницу определения свойств графа"""
    return dict(
        title='Определение свойств графа',
        year=datetime.now().year
    )

# @route('/cycle_detection')
# @view('cycle_detection')
# def cycle_detection():
#     """Отображает страницу поиска циклов в графе"""
#     return dict(
#         title='Поиск циклов в графе',
#         graph_json = get_graph_json(),
#         adjacency_matrix = get_adjacency_matrix(),
#         year=datetime.now().year
#     )

@route('/max_flow')
@view('max_flow')
def max_flow():
    """Отображает страницу поиска максимального потока"""
    return dict(
        title='Поиск максимального потока',
        year=datetime.now().year
    )