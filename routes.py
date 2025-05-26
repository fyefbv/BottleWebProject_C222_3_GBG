"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='Об авторах проекта',
        message='Гаврилов Р.А, Баранов К.И, Гаджиев М.М',
        year=datetime.now().year
    )
