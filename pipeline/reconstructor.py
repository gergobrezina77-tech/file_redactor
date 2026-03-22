import pathlib

STORAGE_DIR = pathlib.Path(__file__).parent.parent / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


class Reconstructor:
    """Writes redacted text to a .txt file in storage/, named after the original file."""

    def __init__(self, original_filename: str):
        stem = pathlib.Path(original_filename).stem
        self._output_path = STORAGE_DIR / f"{stem}.txt"

    def reconstruct(self, text: str) -> pathlib.Path:
        """Write text to storage and return the output path."""
        self._output_path.write_text(text, encoding="utf-8")
        return self._output_path
