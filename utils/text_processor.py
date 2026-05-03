import re
from typing import Any


class TextProcessor:
    def extract_digits(self, text: str | None) -> int:
        if not text: return 0
        digits = re.sub(r'[^\d]', '', text)
        return int(digits) if digits else 0

    def is_in_excluded_field(self, text: str, exclusion: list[Any]) -> bool:
        return text in exclusion
