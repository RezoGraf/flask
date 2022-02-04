from lib2to3.pgen2.pgen import generate_grammar
from app.menu_script import generate_menu
from flask import Blueprint, render_template


menu = Blueprint('menu', __name__)


@menu.route('/')
def main_menu():
    menu = generate_menu()
    return render_template('menu.html', menu=menu)