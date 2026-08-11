from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Entry:
    """
    يمثل كلمة عربية داخل القاموس.
    """

    text: str
    word_type: Optional[str] = None
    meaning: Optional[str] = None
    root: Optional[str] = None

    plural: Optional[str] = None
    singular: Optional[str] = None

    masculine: Optional[str] = None
    feminine: Optional[str] = None

    synonyms: List[str] = field(default_factory=list)
    antonyms: List[str] = field(default_factory=list)

    examples: List[str] = field(default_factory=list)

    source: Optional[str] = None

    @property
    def letters_count(self) -> int:
        return len(self.text.replace(" ", ""))

    def to_dict(self):
        return self.__dict__
