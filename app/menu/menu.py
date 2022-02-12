from app.menu_script import generate_menu
from flask import Blueprint, render_template
from loguru import logger
import logging


menu = Blueprint('menu', __name__)


@menu.route('/')
@logger.catch
def main_menu():
    menu = generate_menu()
    return render_template('menu.html', menu=menu)