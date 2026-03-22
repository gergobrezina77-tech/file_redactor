"""spaCy-based redaction strategies. Supports Name, Email, and Phone number fields.
Requires the 'en_core_web_sm' model (python -m spacy download en_core_web_sm).
The model is loaded lazily on first use.
"""
import spacy
from spacy.matcher import Matcher

_nlp = None


def _get_nlp():
    """Load and cache the spaCy model."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


class NameRedactor:
    """Redacts person names using spaCy's named entity recognition (PERSON label)."""

    def redact(self, text: str) -> str:
        nlp = _get_nlp()
        doc = nlp(text)
        tokens = [token.text_with_ws for token in doc]

        for ent in doc.ents:
            if ent.label_ == "PERSON":
            # Replace all tokens in the span, emit [REDACTED] only at start
                for j in range(ent.start, ent.end):
                    tokens[j] = "[REDACTED]" if j == ent.start else ""

        return "".join(tokens)


class EmailRedactor:
    """Redacts email addresses using spaCy's token.like_email heuristic."""

    def redact(self, text: str) -> str:
        nlp = _get_nlp()
        doc = nlp(text)
        tokens = [token.text_with_ws for token in doc]

        for i, token in enumerate(doc):
            if token.like_email:
                tokens[i] = "[REDACTED]"

        return "".join(tokens)


class PhoneRedactor:
    """Redacts phone numbers using spaCy's Matcher with a digit/separator shape pattern."""

    _PATTERN = [{"SHAPE": {"REGEX": r"[\d\+\-\(\)\s]{7,}"}}]

    def redact(self, text: str) -> str:
        nlp = _get_nlp()
        matcher = Matcher(nlp.vocab)
        matcher.add("PHONE", [self._PATTERN])
        doc = nlp(text)
        redacted = text
        for _, start, end in reversed(matcher(doc)):
            span = doc[start:end]
            redacted = redacted[: span.start_char] + "[REDACTED]" + redacted[span.end_char :]
        return redacted
