from app import create_app
from os import getenv

app = create_app(getenv("FLASK_ENV", "production"))
if __name__ == "__main__":
    app.run()