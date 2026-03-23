import json
import pathlib
from flask import Flask, request, redirect, url_for, render_template, flash

from pipeline.redactor import Redactor
from pipeline.reconstructor import Reconstructor, STORAGE_DIR

BUFFER_DIR = pathlib.Path(__file__).parent.parent / "buffer"
BUFFER_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"txt"}

app = Flask(__name__, template_folder="../webpage")


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    selections = request.form.getlist("selection")
    strategy = request.form.get("strategy")

    # In Case something not selected / Edge cases
    if not strategy:
        flash("Please select a strategy (Regex or NLP).")
        return redirect(url_for("index"))

    if strategy not in {"regex", "nlp"}:
        flash("Invalid strategy.")
        return redirect(url_for("index"))

    if not selections:
        flash("Please select at least one field to redact.")
        return redirect(url_for("index"))
    
    valid_fields = {"Name", "Email", "Phone number"}
    if not all(s in valid_fields for s in selections):
        flash("Invalid selection.")
        return redirect(url_for("index"))

    if strategy == "regex" and "Name" in selections:
        flash("Name redaction is not supported with Regex. Please choose NLP.")
        return redirect(url_for("index"))

    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if not _allowed(file.filename):
        flash(f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
        return redirect(url_for("index"))

    # Save the uploaded file and metadata for processing
    file.save(BUFFER_DIR / file.filename)

    # Save the strategy and selections into a .json
    with open(BUFFER_DIR / (file.filename + ".json"), "w", encoding="utf-8") as fp:
        json.dump({"strategy": strategy, "selections": selections}, fp)


    """
    Using the buffer file location and metadata, we can invoke the Redactor
    This class returns the redacted text in string format, based on the strategy and selections.
    """
    redacted = Redactor(BUFFER_DIR / file.filename).redact()

    """"
    The Reconstructor class takes the original filename and the redacted text, and saves the redacted text into a new file in the STORAGE_DIR.
    """
    output_path = Reconstructor(file.filename).reconstruct(redacted)

    return redirect(url_for("result", filename=output_path.name))


@app.route("/results")
def results():
    files = sorted(STORAGE_DIR.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
    return render_template("results.html", files=[f.name for f in files])


@app.route("/result/<filename>")
def result(filename: str):
    output_path = STORAGE_DIR / filename
    if not output_path.exists():
        flash("Result file not found.")
        return redirect(url_for("index"))
    content = output_path.read_text(encoding="utf-8")
    return render_template("result.html", filename=filename, content=content)


if __name__ == "__main__":
    app.secret_key = "dev-secret"
    app.run(debug=True, host="127.0.0.1", port=5000)
