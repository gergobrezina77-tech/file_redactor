import pathlib



class Extractor:
    """A simple text extractor for txt files."""
    SUPPORTED_TYPES = {"txt"}

    def __init__(self, file_path: str):
        self.file_path = pathlib.Path(file_path)
        self.file_type = self.file_path.suffix.lstrip(".").lower()
        if self.file_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"Unsupported file type: {self.file_type!r}. Must be one of {self.SUPPORTED_TYPES}")

    def extract(self) -> str:
        extractors = {
            "txt":  self._extract_txt,
        }
        try:
            text = extractors[self.file_type]()
        finally:
            self.file_path.unlink(missing_ok=True)
        return text

    def _extract_txt(self) -> str:
        return self.file_path.read_text(encoding="utf-8")
