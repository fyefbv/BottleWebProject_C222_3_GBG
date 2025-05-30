"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Отображает главную страницу"""
    return dict(
        title='Главная страница',
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
def about():
    """Отображает страницу определения свойств графа"""
    return dict(
        title='Определение свойств графа',
        year=datetime.now().year
    )

@route('/cycle_detection')
@view('cycle_detection')
def about():
    """Отображает страницу поиска циклов в графе"""
    return dict(
        title='Поиск циклов в графе',
        year=datetime.now().year
    )

@route('/max_flow')
@view('max_flow')
def about():
    """Отображает страницу поиска максимального потока"""
    return dict(
        title='Поиск максимального потока',
        year=datetime.now().year
    )