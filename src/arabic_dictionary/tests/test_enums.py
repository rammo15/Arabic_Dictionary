from arabic_dictionary.domain.enums import RelationType
from arabic_dictionary.domain.enums import WordType


def test_word_type_enum():

    assert WordType.NOUN.value == "noun"


def test_relation_enum():

    assert RelationType.SYNONYM.value == "synonym"
