"""
Unit / example-based tests for the temperature converter.

Covers:
  - Known conversion values (Req 5.1, 5.2, 5.3)
  - Interactive flows via converters.temperature.run() (Req 3.1, 3.4, 4.1, 6.3, 7.1, 7.2)
"""

from unittest.mock import patch
import pytest

from converters.temperature import celsius_to_fahrenheit, fahrenheit_to_celsius
import converters.temperature as temp_module


# ---------------------------------------------------------------------------
# 8.1 — Known conversion values
# ---------------------------------------------------------------------------

def test_zero_celsius_to_fahrenheit():
    """0°C → 32.00°F  (Req 5.1, 5.3)"""
    assert celsius_to_fahrenheit(0) == 32.00


def test_boiling_celsius_to_fahrenheit():
    """100°C → 212.00°F  (Req 5.1, 5.3)"""
    assert celsius_to_fahrenheit(100) == 212.00


def test_freezing_fahrenheit_to_celsius():
    """32°F → 0.00°C  (Req 5.2, 5.3)"""
    assert fahrenheit_to_celsius(32) == 0.00


def test_boiling_fahrenheit_to_celsius():
    """212°F → 100.00°C  (Req 5.2, 5.3)"""
    assert fahrenheit_to_celsius(212) == 100.00


def test_results_are_rounded_to_two_decimal_places():
    """Results must have at most 2 decimal places  (Req 5.3)"""
    for val in [0, 1, 37, 100, -40, 98.6]:
        r = celsius_to_fahrenheit(val)
        assert round(r, 2) == r
        r2 = fahrenheit_to_celsius(val)
        assert round(r2, 2) == r2


# ---------------------------------------------------------------------------
# 8.2 — Interactive flow tests for converters.temperature.run()
# ---------------------------------------------------------------------------

def test_direction_menu_shows_three_options(capsys):
    """Direction menu presents 3 numbered options  (Req 3.1)"""
    # "3" → Back to main menu (exits the loop)
    with patch("builtins.input", return_value="3"):
        temp_module.run()
    out = capsys.readouterr().out
    assert "1." in out
    assert "2." in out
    assert "3." in out


def test_back_returns_to_category_menu(capsys):
    """Selecting option 3 exits run() without performing a conversion  (Req 3.4)"""
    with patch("builtins.input", return_value="3"):
        temp_module.run()
    out = capsys.readouterr().out
    # No conversion result should have been printed
    assert "=" not in out


def test_numeric_prompt_appears_after_direction_selection():
    """After choosing direction 1, input() is called with a temperature prompt  (Req 4.1)"""
    # direction "1" → C→F, then value "0", then "3" → back
    inputs = iter(["1", "0", "3"])
    with patch("builtins.input", side_effect=inputs) as mock_input:
        temp_module.run()
    # Collect all prompt strings passed to input()
    prompts = [str(call.args[0]) if call.args else "" for call in mock_input.call_args_list]
    assert any("temperature" in p.lower() or "celsius" in p.lower() or "fahrenheit" in p.lower()
               for p in prompts)


def test_post_result_prompt_loops_back_to_direction_menu(capsys):
    """After displaying a result the direction menu is shown again  (Req 6.3)"""
    # First pass: direction 1, value 0 → result shown, loop back
    # Second pass: direction 3 → exit
    inputs = iter(["1", "0", "3"])
    with patch("builtins.input", side_effect=inputs):
        temp_module.run()
    out = capsys.readouterr().out
    # Direction menu must appear at least twice (once before conversion, once after)
    assert out.count("Celsius to Fahrenheit") >= 2


def test_successive_conversions_both_display_results(capsys):
    """Two conversions in one session both show results  (Req 7.1)"""
    # C→F 0°C, then F→C 212°F, then back
    inputs = iter(["1", "0", "2", "212", "3"])
    with patch("builtins.input", side_effect=inputs):
        temp_module.run()
    out = capsys.readouterr().out
    assert "32.00" in out   # 0°C → 32.00°F
    assert "100.00" in out  # 212°F → 100.00°C


def test_conversion_returns_to_direction_menu(capsys):
    """After a conversion the direction menu is re-presented  (Req 7.2)"""
    inputs = iter(["1", "100", "3"])
    with patch("builtins.input", side_effect=inputs):
        temp_module.run()
    out = capsys.readouterr().out
    # Direction menu header appears before and after the conversion
    assert out.count("Celsius to Fahrenheit") >= 2
