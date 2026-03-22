import pathlib
import pypdf
import docx


class Extractor:
    """A simple text extractor for txt, pdf, and docx files."""
    SUPPORTED_TYPES = {"txt", "pdf", "docx"}

    def __init__(self, file_path: str):
        self.file_path = pathlib.Path(file_path)
        self.file_type = self.file_path.suffix.lstrip(".").lower()
        if self.file_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"Unsupported file type: {self.file_type!r}. Must be one of {self.SUPPORTED_TYPES}")

    def extract(self) -> str:
        extractors = {
            "txt":  self._extract_txt,
            "pdf":  self._extract_pdf,
            "docx": self._extract_docx,
        }
        return extractors[self.file_type]()

    def _extract_txt(self) -> str:
        return self.file_path.read_text(encoding="utf-8")

    def _extract_pdf(self) -> str:
        reader = pypdf.PdfReader(self.file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _extract_docx(self) -> str:
        doc = docx.Document(self.file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
