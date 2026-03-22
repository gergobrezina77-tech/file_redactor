import json
import pathlib

from pipeline.extractor import Extractor
from pipeline.strategies import regex, spacy as spacy_strategies

BUFFER_DIR = pathlib.Path(__file__).parent.parent / "buffer"

"""
A list of redaction strategies and their supported fields.
"""
_STRATEGIES = {
    "regex": {
        "Email":        regex.EmailRedactor(),
        "Phone number": regex.PhoneRedactor(),
    },
    "nlp": {
        "Name":         spacy_strategies.NameRedactor(),
        "Email":        spacy_strategies.EmailRedactor(),
        "Phone number": spacy_strategies.PhoneRedactor(),
    },
}


class Redactor:
    """
    The main redactor class.
    This class implements the logic using a strategy pattern, where the actual redaction logic is delegated to strategy classes.
    Reads data from the buffer, extracts text, applies strategy and deletes the input file.
    """
    def __init__(self, file_path: str):
        # Set file and meta paths
        file_path = pathlib.Path(file_path)
        meta_path = BUFFER_DIR / (file_path.name + ".json")

        # Read meta information
        with open(meta_path, "r", encoding="utf-8") as fp:
            meta = json.load(fp)

        self.strategy_name = meta["strategy"]
        self.selections = meta["selections"]

        # Check meta data validity
        if self.strategy_name not in _STRATEGIES:
            raise ValueError(f"Unknown strategy {self.strategy_name!r}. Must be one of {set(_STRATEGIES)}")
        for selection in self.selections:
            if selection not in _STRATEGIES[self.strategy_name]:
                raise ValueError(f"Unknown selection {selection!r} for strategy {self.strategy_name!r}.")

        # Based on the meta data, collect strategies and extract text
        # This is a list of strategy child class instances
        self._strategies = [_STRATEGIES[self.strategy_name][s] for s in self.selections]
        self._text = Extractor(file_path).extract()

        # Clean up the buffer
        meta_path.unlink()


    
    def redact(self) -> str:
        """Applies all selected strategies in sequence."""
        text = self._text
        for strategy in self._strategies:
            text = strategy.redact(text)
        return text
