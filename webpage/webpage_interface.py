import pathlib
from flask import Flask, request, redirect, url_for, render_template, flash

STORAGE_DIR = pathlib.Path(__file__).parent.parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}

app = Flask(__name__, template_folder="../webpage")


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file or file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if not _allowed(file.filename):
        flash(f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
        return redirect(url_for("index"))

    dest = STORAGE_DIR / file.filename
    file.save(dest)
    flash(f"Uploaded '{file.filename}' successfully.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = "dev-secret"
    app.run(debug=True, host="127.0.0.1", port=5000)
