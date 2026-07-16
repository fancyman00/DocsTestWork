import os

from dotenv import load_dotenv
from flask import Flask

from docs.api import DocumentApi
from tools.database import Database

load_dotenv()

app = Flask(__name__)
database = Database(
    os.getenv("DB_USER", "postgres"),
    os.getenv("DB_PASSWORD", ""),
    os.getenv("DB_HOST", "127.0.0.1"),
    os.getenv("DB_PORT", "5432"),
)

DocumentApi(app, "/document", database)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="localhost", port=8081, threaded=True)
