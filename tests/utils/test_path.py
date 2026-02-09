import os
import pytest
from internal.utils.path import valid_path, validate_file


def test_valid_path_is_absolute():
    p = valid_path("~")
    assert os.path.isabs(p)


def test_validate_file_raises_for_missing():
    with pytest.raises(Exception):
        validate_file("/definitely/not/existing/file.log")


def test_validate_file_ok_for_existing(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("ok", encoding="utf-8")
    assert validate_file(str(f)) == str(f)
