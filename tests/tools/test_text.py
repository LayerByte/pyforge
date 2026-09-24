def test_text_statistics_summarizes_readable_content():
    from pyforge.tools.text.core import text_statistics

    result = text_statistics("Hello world.\n\nHello PyForge!")
    assert result["words"] == 4
    assert result["unique_words"] == 3
    assert result["sentences"] == 2
    assert result["paragraphs"] == 2
    assert result["average_word_length"] == 5.5


def test_word_count_handles_unicode_and_empty_input():
    from pyforge.tools.text.core import word_count

    assert word_count("Žlutý kůň runs") == 3 and word_count("") == 0


def test_line_count_handles_trailing_newline():
    from pyforge.tools.text.core import line_count

    assert line_count("a\nb\n") == 2 and line_count("") == 0


def test_character_count_can_exclude_whitespace():
    from pyforge.tools.text.core import character_count

    assert character_count("a β") == 3 and character_count("a β", False) == 2


def test_duplicate_lines_filters_unique_content():
    from pyforge.tools.text.core import duplicate_lines

    assert duplicate_lines("a\nb\na\n") == {"a": 2}


def test_text_difference_marks_additions():
    from pyforge.tools.text.core import text_difference

    diff = text_difference("a\n", "a\nb\n")
    assert "+b" in diff and "--- before" in diff


def test_whitespace_cleaner_trims_and_collapses():
    from pyforge.tools.text.core import clean_whitespace

    assert clean_whitespace("a  \n\n\n b\t\n") == "a\n\n b\n"


def test_case_converter_supports_developer_styles():
    from pyforge.tools.text.core import convert_case

    assert (
        convert_case("Hello world", "snake") == "hello_world" and convert_case("hello_world", "camel") == "helloWorld"
    )


def test_slugifier_normalizes_text_and_separator():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.text.core import slugify

    assert slugify("Žlutý kůň & PyForge!") == "zluty-kun-pyforge"
    assert slugify("Hello world", "_") == "hello_world"
    with pytest.raises(ValidationError):
        slugify("Hello", ".")


def test_text_sorter_can_deduplicate():
    from pyforge.tools.text.core import sort_text

    assert sort_text("b\nA\nb", unique=True) == "A\nb"


def test_text_search_returns_line_numbers():
    from pyforge.tools.text.core import search_text

    assert search_text("one\nTwo\nthree", "two") == [{"line": 2, "text": "Two"}]


def test_regex_tester_reports_groups_and_invalid_patterns():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.text.core import regex_test

    assert regex_test(r"(a+)", "baa")[0]["groups"] == ["aa"]
    with pytest.raises(ValidationError):
        regex_test("[", "x")
