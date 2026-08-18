from arabic_dictionary.utils.normalizer import normalize, strip_diacritics


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


# --- strip_diacritics: removes only diacritics and tatweel, preserves letter forms ---


def test_strip_diacritics_removes_harakat() -> None:
    assert strip_diacritics("قَلَمٌ") == "قلم"


def test_strip_diacritics_removes_tatweel() -> None:
    assert strip_diacritics("كــتاب") == "كتاب"


def test_strip_diacritics_preserves_ta_marbuta() -> None:
    # normalize() changes ة→ه, but strip_diacritics() must not
    assert strip_diacritics("شجرة") == "شجرة"


def test_strip_diacritics_preserves_alef_variants() -> None:
    # normalize() changes أإآ→ا, but strip_diacritics() must not
    assert strip_diacritics("أَكَلَ") == "أكل"


def test_strip_diacritics_preserves_alef_maqsura() -> None:
    assert strip_diacritics("فَتَى") == "فتى"