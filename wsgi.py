"""wsgi start for clear developer start"""
from app.main import app

if __name__ == "__main__":
    app.run(debug=False)
