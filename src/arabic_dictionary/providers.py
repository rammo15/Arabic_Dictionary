from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Entry


class Provider(ABC):
    """
    الواجهة الأساسية لأي مصدر بيانات.
    """

    name = "provider"

    @abstractmethod
    def lookup(self, word: str) -> Entry | None:
        """
        البحث عن كلمة.
        """
        raise NotImplementedError
