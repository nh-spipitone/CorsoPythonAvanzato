import pytest

# NB: implementa in Utils/sanitization.py
from Utils.sanitization import normalize_text


def test_basic_normalization_crlf_tabs_bom_and_blanklines():
    raw = (
        "\ufeff\tdef foo():\r\n"
        "\t\tprint('x')  \r\n"
        "\r\n"
        "\r\n"
        "    \treturn 1\r\n"
    )
    expected = "def foo():\n" "    print('x')\n" "\n" "    return 1\n"
    out = normalize_text(raw, tabsize=4, collapse_blank=True)
    assert out == expected


def test_leading_and_trailing_blank_lines_are_trimmed():
    raw = "\n\n    a = 1\n\n\n"
    expected = "a = 1\n"
    assert normalize_text(raw) == expected


def test_only_leading_tabs_are_expanded_not_inside_strings():
    raw = "\tprint('\\tinside')\n\t\tvalue = '\\t'\n"
    # aspettativa: i tab in testa si trasformano in spazi, quelli nel contenuto restano
    expected = "    print('\\tinside')\n        value = '\\t'\n"
    assert normalize_text(raw, tabsize=4) == expected


def test_trailing_spaces_removed_and_newline_at_eof_added():
    raw = "x = 1    "  # nessun \n finale, spazi a fine riga
    expected = "x = 1\n"
    assert normalize_text(raw) == expected


def test_dedent_common_indent_but_preserve_relative_structure():
    raw = "        if True:\n" "            x = 1\n" "        y = 2\n"
    expected = "if True:\n" "    x = 1\n" "y = 2\n"
    assert normalize_text(raw) == expected


def test_idempotent_second_pass_no_change():
    s = "def a():\n    pass\n\n"
    assert normalize_text(normalize_text(s)) == normalize_text(s)
