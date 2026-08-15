from abc import ABC

from arabic_dictionary.repository import DictionaryRepository


def test_repository_is_abstract():
    assert issubclass(DictionaryRepository, ABC)
