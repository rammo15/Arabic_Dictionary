from arabic_dictionary.utils.normalizer import normalize


def test_remove_diacritics():
    assert normalize("أَكَلَ") == "اكل"


def test_alef():
    assert normalize("إسلام") == "اسلام"


def test_tatweel():
    assert normalize("كــتاب") == "كتاب"


def test_alef_madda():
    assert normalize("آثار") == "اثار"


def test_yaa():
    assert normalize("فتى") == "فتي"


def test_ta_marbuta():
    assert normalize("مدرسة") == "مدرسه"