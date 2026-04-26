from unittest.mock import patch, MagicMock
import pytest

import app


def make_registry(*names):
    return {name: MagicMock() for name in names}


# --- show_category_menu ---

def test_show_category_menu_returns_choice(capsys):
    registry = make_registry("Temperature")
    with patch("builtins.input", return_value="1"):
        result = app.show_category_menu(registry)
    assert result == "1"


def test_show_category_menu_includes_quit(capsys):
    registry = make_registry("Temperature")
    with patch("builtins.input", return_value="2"):
        app.show_category_menu(registry)
    out = capsys.readouterr().out
    assert "Quit" in out


def test_show_category_menu_lists_all_categories(capsys):
    registry = make_registry("Temperature", "Length")
    with patch("builtins.input", return_value="1"):
        app.show_category_menu(registry)
    out = capsys.readouterr().out
    assert "Temperature" in out
    assert "Length" in out


# --- handle_category_choice ---

def test_handle_category_choice_valid_calls_handler():
    handler = MagicMock()
    registry = {"Temperature": handler}
    result = app.handle_category_choice("1", registry)
    handler.assert_called_once()
    assert result is True


def test_handle_category_choice_quit_returns_false():
    registry = make_registry("Temperature")
    result = app.handle_category_choice("2", registry)
    assert result is False


def test_handle_category_choice_non_integer_returns_true(capsys):
    registry = make_registry("Temperature")
    result = app.handle_category_choice("abc", registry)
    assert result is True
    out = capsys.readouterr().out
    assert "Invalid choice" in out


def test_handle_category_choice_out_of_range_returns_true(capsys):
    registry = make_registry("Temperature")
    result = app.handle_category_choice("99", registry)
    assert result is True
    out = capsys.readouterr().out
    assert "Invalid choice" in out


def test_handle_category_choice_zero_is_invalid(capsys):
    registry = make_registry("Temperature")
    result = app.handle_category_choice("0", registry)
    assert result is True
    out = capsys.readouterr().out
    assert "Invalid choice" in out


def test_handle_category_choice_dispatches_correct_handler():
    h1, h2 = MagicMock(), MagicMock()
    registry = {"Temperature": h1, "Length": h2}
    app.handle_category_choice("2", registry)
    h2.assert_called_once()
    h1.assert_not_called()


# --- run ---

def test_run_displays_welcome_and_farewell(capsys):
    with patch("converters.REGISTRY", {"Temperature": MagicMock()}):
        with patch("app.show_category_menu", return_value="2"):
            app.run()
    out = capsys.readouterr().out
    assert "Welcome" in out
    assert "Goodbye" in out


def test_run_exits_on_quit():
    calls = []
    def fake_show(registry):
        calls.append(1)
        return "2"  # quit (index 2 = quit for 1-item registry)

    with patch("converters.REGISTRY", {"Temperature": MagicMock()}):
        with patch("app.show_category_menu", side_effect=fake_show):
            app.run()
    assert len(calls) == 1


def test_run_keyboard_interrupt_shows_farewell(capsys):
    with patch("converters.REGISTRY", {"Temperature": MagicMock()}):
        with patch("app.show_category_menu", side_effect=KeyboardInterrupt):
            app.run()
    out = capsys.readouterr().out
    assert "Goodbye" in out
