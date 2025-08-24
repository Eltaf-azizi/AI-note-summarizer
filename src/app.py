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

    if request.method == "POST":
        length = request.form.get("length", "short")
        tone = request.form.get("tone", "neutral")
        backend = request.form.get("backend") or settings.backend
        source = request.form.get("text_source", "paste")
        try:
            if source == "paste":
                input_text = request.form.get("note", "").strip()
            else:
                uploaded = request.files.get("file")
                if not uploaded or uploaded.filename == "":
                    raise ValueError("No file selected")
                input_text = load_any(uploaded)
            if not input_text:
                raise ValueError("No text provided")

            params = SummaryParams(length=length, tone=tone, backend=backend)
            result = pipeline.summarize(input_text, params)
        except Exception as e:
            error = str(e)


