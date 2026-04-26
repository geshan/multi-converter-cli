# multi-converter-cli

A lightweight, interactive command-line tool for unit conversions written in pure Python with no external dependencies. Launch it, pick a conversion category from the menu, enter a value, and get an instant result rounded to 2 decimal places.

Currently supported conversions:
- **Temperature** — Celsius ↔ Fahrenheit (bidirectional)

The app is designed to be extensible — new unit categories (length, weight, etc.) can be added with minimal changes.

## Running the app

### Prerequisites

- Python 3.8 or higher
- No third-party packages required

### Start the CLI

```bash
python main.py
```

> If `python` does not run try `python3`.

You'll be greeted with a menu to select a conversion category. Follow the on-screen prompts to choose a direction, enter a value, and see the result. Press `Ctrl+C` or select **Quit** from the main menu to exit.

## Testing

### Prerequisites

Property-based tests use [Hypothesis](https://hypothesis.readthedocs.io/). Install it as a dev dependency:

```bash
pip install hypothesis
```

### Run all tests

```bash
python -m pytest tests/ -v
```

### Test breakdown

| File | What it covers |
|------|---------------|
| `tests/test_ui.py` | CLI utility functions (menus, prompts, display helpers) |
| `tests/test_app.py` | Application controller (routing, session loop, error handling) |
| `tests/test_temperature.py` | Known conversion values and interactive temperature flows |
| `tests/test_properties.py` | Property-based tests verifying formula correctness across generated inputs |
