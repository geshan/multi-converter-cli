# Implementation Plan: unit-converter-cli

## Overview

Implement a pure-Python, zero-dependency CLI unit converter in a layered architecture: a CLI layer (`ui.py`), a controller layer (`app.py`), and a converter layer (`converters/`). The entry point is `main.py`. Tests live in `tests/`.

## Tasks

- [x] 1. Set up project structure and core interfaces
  - Create the directory layout: `converters/`, `tests/`
  - Create empty `__init__.py` files for `converters/` and `tests/`
  - Create stub files: `main.py`, `app.py`, `ui.py`, `converters/temperature.py`
  - _Requirements: 1.1_

- [x] 2. Implement the CLI utilities layer (`ui.py`)
  - [x] 2.1 Implement `display_welcome`, `display_farewell`, and `display_error`
    - `display_welcome` prints a welcome message on startup
    - `display_farewell` prints a farewell message on quit
    - `display_error` prints the given error string to stdout
    - _Requirements: 1.2, 2.4_

  - [x] 2.2 Implement `prompt_menu`
    - Accepts a list of option strings, prints them as a numbered menu, and returns the raw input string
    - _Requirements: 2.1, 3.1_

  - [x] 2.3 Implement `prompt_float`
    - Loops until the user enters a value parseable as `float`; displays `"Invalid input. Please enter a numeric value."` on each bad attempt
    - Returns the parsed `float`
    - _Requirements: 4.1, 4.2, 4.3_

  - [ ]* 2.4 Write property test for `prompt_float` (Property 7)
    - **Property 7: Non-numeric temperature input is rejected**
    - Use `hypothesis` `text()` strategy filtered to exclude float-parseable strings; assert `prompt_float` never returns for those inputs (mock stdin)
    - **Validates: Requirements 4.3**

  - [x] 2.5 Implement `display_result`
    - Prints input value, source unit, result formatted to 2 d.p., and target unit on one line
    - _Requirements: 6.1, 6.2_

  - [ ]* 2.6 Write property test for `display_result` (Property 5)
    - **Property 5: Result display contains all required fields and correct formatting**
    - Use `floats` × `text` × `floats` × `text` strategies; assert output contains `input_val`, `from_unit`, a `:.2f`-formatted result, and `to_unit`
    - **Validates: Requirements 6.1, 6.2**

- [x] 3. Implement the temperature converter (`converters/temperature.py`)
  - [x] 3.1 Implement `celsius_to_fahrenheit` and `fahrenheit_to_celsius`
    - `celsius_to_fahrenheit(c)`: returns `round((c * 9/5) + 32, 2)`
    - `fahrenheit_to_celsius(f)`: returns `round((f - 32) * 5/9, 2)`
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 3.2 Write property test for formula correctness (Properties 1 & 2)
    - **Property 1: Celsius-to-Fahrenheit formula correctness**
    - **Property 2: Fahrenheit-to-Celsius formula correctness**
    - Use `floats(allow_nan=False, allow_infinity=False)`; assert each function matches its formula before rounding
    - **Validates: Requirements 5.1, 5.2**

  - [ ]* 3.3 Write property test for rounding (Property 3)
    - **Property 3: Conversion results are rounded to 2 decimal places**
    - Use `floats(allow_nan=False, allow_infinity=False)`; assert `round(result, 2) == result` for both functions
    - **Validates: Requirements 5.3**

  - [ ]* 3.4 Write property test for round-trip (Property 4)
    - **Property 4: Temperature conversion round-trip**
    - Use `floats(allow_nan=False, allow_infinity=False)`; assert `round(fahrenheit_to_celsius(celsius_to_fahrenheit(c)), 2) == round(c, 2)`
    - **Validates: Requirements 5.4**

  - [x] 3.5 Implement `run()` in `converters/temperature.py`
    - Present the direction menu (Celsius→Fahrenheit, Fahrenheit→Celsius, Back)
    - Collect numeric input via `prompt_float`, call the appropriate pure function, display result via `display_result`
    - Loop until the user selects "Back to main menu"
    - Display `"Invalid choice. Please enter 1, 2, or 3."` on bad direction input
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 6.3, 7.1, 7.2_

- [x] 4. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement the converter registry (`converters/__init__.py`)
  - Define `REGISTRY: dict[str, callable] = {}`
  - Implement `register(name, handler)` that adds an entry to `REGISTRY`
  - Register the temperature converter: `register("Temperature", temperature.run)`
  - _Requirements: 2.1, 2.2_

- [x] 6. Implement the application controller (`app.py`)
  - [x] 6.1 Implement `show_category_menu`
    - Builds the numbered list from `REGISTRY` keys plus a "Quit" option and calls `prompt_menu`
    - _Requirements: 2.1_

  - [x] 6.2 Implement `handle_category_choice`
    - Maps a valid integer string to the corresponding registry handler and calls it; returns `False` for the quit option
    - Displays `"Invalid choice. Please enter a number from the menu."` and returns `True` (keep looping) for any invalid input
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ]* 6.3 Write property test for valid index dispatch (Property 8)
    - **Property 8: Valid category index dispatches to the correct handler**
    - Use `integers` bounded to registry size; assert the correct handler mock is called and no other handler is invoked
    - **Validates: Requirements 2.2**

  - [ ]* 6.4 Write property test for invalid menu input (Property 6)
    - **Property 6: Invalid menu input produces an error and does not navigate away**
    - Use `text()` filtered to exclude valid option strings; assert `display_error` is called and no handler is invoked
    - **Validates: Requirements 2.3, 3.5**

  - [x] 6.5 Implement `run()`
    - Calls `display_welcome`, then loops calling `show_category_menu` / `handle_category_choice` until `False` is returned
    - Catches `KeyboardInterrupt` and calls `display_farewell` before exiting
    - _Requirements: 1.2, 2.1, 2.2, 2.3, 2.4, 7.1, 7.3_

- [x] 7. Implement the entry point (`main.py`)
  - Define `main()` that imports and calls `app.run()`
  - Add `if __name__ == "__main__": main()` guard
  - _Requirements: 1.1, 1.2_

- [x] 8. Write unit / example-based tests (`tests/test_temperature.py`, `tests/test_ui.py`)
  - [x] 8.1 Write unit tests for known temperature conversions
    - `0°C → 32.00°F`, `100°C → 212.00°F`, `32°F → 0.00°C`, `212°F → 100.00°C`
    - _Requirements: 5.1, 5.2, 5.3_

  - [x]* 8.2 Write unit tests for interactive flows (mocking stdin/stdout)
    - Welcome message on startup (Req 1.2)
    - Category menu lists registered categories (Req 2.1)
    - Quit exits with farewell (Req 2.4)
    - Direction menu shows 3 options (Req 3.1)
    - "Back" returns to category menu (Req 3.4)
    - Numeric prompt appears after direction selection (Req 4.1)
    - Post-result prompt appears after conversion (Req 6.3)
    - Two successive conversions both display results (Req 7.1)
    - App returns to a menu after conversion (Req 7.2)
    - Session terminates on quit (Req 7.3)
    - _Requirements: 1.2, 2.1, 2.4, 3.1, 3.4, 4.1, 6.3, 7.1, 7.2, 7.3_

- [x] 9. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Property-based tests use [Hypothesis](https://hypothesis.readthedocs.io/) (`pip install hypothesis`) — a test-time dependency only; the runtime remains zero-dependency
- Each property test should use `@settings(max_examples=100)` and include a comment tag `# Feature: unit-converter-cli, Property N: <property_text>`
- All error messages go to stdout (not stderr) to keep the interactive experience consistent
