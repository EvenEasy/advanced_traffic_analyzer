import pytest
from internal.anazyler import AdvancedTrafficAnalyzer


def test_read_row_ok():
    row = "1700000000 127.0.0.1 GET / 200 123\n"
    ts, ip, mtd, url, code, size = AdvancedTrafficAnalyzer._read_row(row)

    assert ts == 1700000000
    assert ip == "127.0.0.1"
    assert mtd == "GET"
    assert url == "/"
    assert code == 200
    assert size == 123


def test_read_row_invalid_parts_count():
    with pytest.raises(AssertionError):
        AdvancedTrafficAnalyzer._read_row("1700000000 127.0.0.1 GET /\n")


def test_read_row_invalid_method():
    with pytest.raises(AssertionError):
        AdvancedTrafficAnalyzer._read_row("1700000000 127.0.0.1 PATCH / 200 123\n")


def test_parse_log_respects_limit(tmp_path):
    p = tmp_path / "access.log"
    p.write_text(
        "\n".join([
            "1700000000 127.0.0.1 GET / 200 1",
            "1700000001 127.0.0.2 POST /a 201 2",
            "1700000002 127.0.0.3 GET /b 200 3",
        ]) + "\n",
        encoding="utf-8"
    )

    a = AdvancedTrafficAnalyzer()
    rows = list(a.parse_log(p, limit=2))
    assert len(rows) == 2
    assert rows[0][0] == 1700000000
    assert rows[1][0] == 1700000001
