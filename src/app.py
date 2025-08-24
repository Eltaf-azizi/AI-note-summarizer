from flask import Flask, render_template, request, send_file, redirect, url_for
from .pipeline import Pipeline, SummaryParams
from .utils import load_any, safe_truncate
from .config import settings
import io

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = settings.max_upload_mb * 1024 * 1024

pipeline = Pipeline()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    input_text = ""
