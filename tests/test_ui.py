from unittest.mock import patch
from io import StringIO
import pytest

import ui


def test_display_welcome(capsys):
    ui.display_welcome()
    out = capsys.readouterr().out
    assert len(out.strip()) > 0


def test_display_farewell(capsys):
    ui.display_farewell()
    out = capsys.readouterr().out
    assert len(out.strip()) > 0


def test_display_error(capsys):
    ui.display_error("Something went wrong")
    out = capsys.readouterr().out
    assert "Something went wrong" in out


def test_display_error_goes_to_stdout(capsys):
    ui.display_error("err msg")
    captured = capsys.readouterr()
    assert "err msg" in captured.out
    assert captured.err == ""


def test_prompt_menu_prints_numbered_options(capsys):
    with patch("builtins.input", return_value="1"):
        result = ui.prompt_menu(["Option A", "Option B", "Quit"])
    out = capsys.readouterr().out
    assert "1." in out and "Option A" in out
    assert "2." in out and "Option B" in out
    assert "3." in out and "Quit" in out
    assert result == "1"


def test_prompt_menu_returns_raw_input(capsys):
    with patch("builtins.input", return_value="abc"):
        result = ui.prompt_menu(["X"])
    assert result == "abc"


def test_prompt_float_valid_integer(capsys):
    with patch("builtins.input", return_value="42"):
        result = ui.prompt_float("Enter value: ")
    assert result == 42.0


def test_prompt_float_valid_decimal(capsys):
    with patch("builtins.input", return_value="3.14"):
        result = ui.prompt_float("Enter value: ")
    assert result == pytest.approx(3.14)


def test_prompt_float_retries_on_invalid(capsys):
    inputs = iter(["abc", "not_a_number", "7.5"])
    with patch("builtins.input", side_effect=inputs):
        result = ui.prompt_float("Enter value: ")
    out = capsys.readouterr().out
    assert result == pytest.approx(7.5)
    assert out.count("Invalid input. Please enter a numeric value.") == 2


def test_prompt_float_error_to_stdout(capsys):
    inputs = iter(["bad", "1.0"])
    with patch("builtins.input", side_effect=inputs):
        ui.prompt_float("Enter: ")
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a numeric value." in captured.out
    assert captured.err == ""


def test_display_result_format(capsys):
    ui.display_result(100.0, "Celsius", 212.0, "Fahrenheit")
    out = capsys.readouterr().out.strip()
    assert out == "100.0 Celsius = 212.00 Fahrenheit"


def test_display_result_two_decimal_places(capsys):
    ui.display_result(0.0, "C", 32.0, "F")
    out = capsys.readouterr().out.strip()
    assert "32.00" in out


def test_display_result_contains_all_fields(capsys):
    ui.display_result(37.5, "Celsius", 99.5, "Fahrenheit")
    out = capsys.readouterr().out
    assert "37.5" in out
    assert "Celsius" in out
    assert "99.50" in out
    assert "Fahrenheit" in out
