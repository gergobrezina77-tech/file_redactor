import re


class EmailRedactor:
    """Redacts email addresses using a standard pattern."""

    _PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

    def redact(self, text: str) -> str:
        return self._PATTERN.sub("[REDACTED]", text)


class PhoneRedactor:
    """Redacts phone numbers by matching digit/separator sequences of 7–16 characters."""

    _PATTERN = re.compile(r"\+?[\d\s\-().]{7,15}\d")

    def redact(self, text: str) -> str:
        return self._PATTERN.sub("[REDACTED]", text)
