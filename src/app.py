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

    return render_template(
        "index.html",
        result=result,
        error=error,
        input_preview=safe_truncate(input_text, 2000),
    )


@app.route("/download", methods=["POST"]) 
def download():
    content = request.form.get("content", "")
    filename = request.form.get("filename", "summary.txt")
    if not content:
        return redirect(url_for("index"))
    mem = io.BytesIO(content.encode("utf-8"))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name=filename, mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=False)

