# Design Document: unit-converter-cli

## Overview

`unit-converter-cli` is a pure-Python, zero-dependency command-line application that guides users through unit conversions interactively. The initial release supports temperature conversions (Celsius ↔ Fahrenheit). The architecture is deliberately layered so that new conversion categories can be added with minimal changes to existing code.

The application runs as a single Python script (`main.py`) and is invoked with:

```
python main.py
# or
python3 main.py
```

No virtual environment or third-party packages are required.

---

## Architecture

The application follows a three-layer design:

```
┌─────────────────────────────────────┐
│              CLI Layer              │  main.py / ui.py
│  (menus, prompts, input validation) │
└────────────────┬────────────────────┘
                 │ calls
┌────────────────▼────────────────────┐
│           Controller Layer          │  app.py
│  (session loop, routing, dispatch)  │
└────────────────┬────────────────────┘
                 │ calls
┌────────────────▼────────────────────┐
│          Converter Layer            │  converters/
│  (pure conversion functions)        │
└─────────────────────────────────────┘
```

### Key Design Decisions

- **No external dependencies** — only the Python standard library (`sys`, `math`, `decimal` or plain `float` arithmetic) is used.
- **Extensibility via a converter registry** — each converter registers itself with a shared dictionary; adding a new category requires only creating a new module and registering it.
- **Pure converter functions** — conversion logic is kept in stateless functions so it is trivially testable without any I/O.
- **Input validation at the boundary** — all user input is validated in the CLI layer before being passed to converters, keeping converter logic free of I/O concerns.

---

## Components and Interfaces

### `main.py` — Entry Point

Bootstraps the application and delegates to the controller.

```python
def main() -> None: ...
```

### `app.py` — Application Controller

Owns the top-level session loop.

```python
def run() -> None: ...
def show_category_menu(registry: dict) -> None: ...
def handle_category_choice(choice: str, registry: dict) -> bool: ...
```

Returns `False` from `handle_category_choice` when the user selects quit, terminating the loop.

### `ui.py` — CLI Utilities

Reusable helpers for prompting and displaying output.

```python
def prompt_menu(options: list[str]) -> str: ...
def prompt_float(prompt_text: str) -> float: ...
def display_result(input_val: float, from_unit: str,
                   result: float, to_unit: str) -> None: ...
def display_error(message: str) -> None: ...
def display_welcome() -> None: ...
def display_farewell() -> None: ...
```

`prompt_float` loops internally until the user enters a valid numeric value, displaying an error on each invalid attempt.

### `converters/` — Converter Package

#### `converters/__init__.py` — Registry

```python
# Maps category display name → converter module's run() function
REGISTRY: dict[str, callable] = {}

def register(name: str, handler: callable) -> None: ...
```

#### `converters/temperature.py` — Temperature Converter

```python
def celsius_to_fahrenheit(celsius: float) -> float: ...
def fahrenheit_to_celsius(fahrenheit: float) -> float: ...
def run() -> None: ...   # interactive direction-selection loop
```

`run()` presents the direction menu, collects input, calls the appropriate pure function, and displays the result. It loops until the user chooses "Back to main menu".

---

## Data Models

The application is stateless between conversions; there are no persistent data structures. The only in-memory state is:

| Name | Type | Description |
|------|------|-------------|
| `REGISTRY` | `dict[str, callable]` | Maps category name → handler function |
| `input_val` | `float` | Raw numeric value entered by the user |
| `result` | `float` | Rounded conversion result (2 d.p.) |

### Conversion Result Representation

Results are plain Python `float` values rounded with `round(value, 2)`. Display formatting uses an f-string: `f"{result:.2f}"`.

### Conversion Formulas

| Direction | Formula |
|-----------|---------|
| Celsius → Fahrenheit | `result = (c × 9/5) + 32` |
| Fahrenheit → Celsius | `result = (f − 32) × 5/9` |

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Celsius-to-Fahrenheit formula correctness

*For any* float value `c`, `celsius_to_fahrenheit(c)` shall equal `(c * 9/5) + 32` (before rounding).

**Validates: Requirements 5.1**

---

### Property 2: Fahrenheit-to-Celsius formula correctness

*For any* float value `f`, `fahrenheit_to_celsius(f)` shall equal `(f - 32) * 5/9` (before rounding).

**Validates: Requirements 5.2**

---

### Property 3: Conversion results are rounded to 2 decimal places

*For any* numeric input, the value returned by `celsius_to_fahrenheit` or `fahrenheit_to_celsius` shall satisfy `round(result, 2) == result` — i.e., the result already has at most 2 decimal places.

**Validates: Requirements 5.3**

---

### Property 4: Temperature conversion round-trip

*For any* float value `c`, converting from Celsius to Fahrenheit and then back to Celsius shall produce a value equal to `round(c, 2)` — i.e., `round(fahrenheit_to_celsius(celsius_to_fahrenheit(c)), 2) == round(c, 2)`.

**Validates: Requirements 5.4**

---

### Property 5: Result display contains all required fields and correct formatting

*For any* combination of `input_val` (float), `from_unit` (str), `result` (float), and `to_unit` (str), the string produced by `display_result` shall contain the string representation of `input_val`, the `from_unit` label, a value formatted to exactly 2 decimal places, and the `to_unit` label.

**Validates: Requirements 6.1, 6.2**

---

### Property 6: Invalid menu input produces an error and does not navigate away

*For any* string that is not a valid menu option (not a recognised integer index for the current menu), the menu handler shall display an error message and re-present the same menu without advancing to a sub-workflow.

**Validates: Requirements 2.3, 3.5**

---

### Property 7: Non-numeric temperature input is rejected

*For any* string that cannot be parsed as a Python `float`, `prompt_float` shall display an error message and prompt again rather than returning a value.

**Validates: Requirements 4.3**

---

### Property 8: Valid category index dispatches to the correct handler

*For any* valid integer index into the converter registry, selecting that index shall invoke exactly the handler registered under that category name and no other handler.

**Validates: Requirements 2.2**

---

## Error Handling

| Scenario | Behaviour |
|----------|-----------|
| User enters a non-integer at the category menu | Display `"Invalid choice. Please enter a number from the menu."` and re-present the menu. |
| User enters an out-of-range integer at the category menu | Same error message and re-present. |
| User enters a non-integer at the direction menu | Display `"Invalid choice. Please enter 1, 2, or 3."` and re-present the direction menu. |
| User enters a non-numeric value at the temperature prompt | Display `"Invalid input. Please enter a numeric value."` and re-prompt. |
| `KeyboardInterrupt` (Ctrl-C) | Catch at the top-level loop, display a farewell message, and exit cleanly. |

All error messages are written to `stdout` (not `stderr`) to keep the interactive experience consistent. No exceptions propagate to the user.

---

## Testing Strategy

### Approach

The feature uses a **dual testing approach**:

- **Unit / example-based tests** — verify specific behaviours, navigation flows, and edge cases using concrete inputs.
- **Property-based tests** — verify universal correctness properties across a wide range of generated inputs.

The property-based testing library used is **[Hypothesis](https://hypothesis.readthedocs.io/)** (Python). Each property test is configured to run a minimum of **100 iterations**.

> Note: Hypothesis is a test-time dependency only and does not affect the zero-dependency runtime requirement.

### Unit Tests

Located in `tests/test_temperature.py` and `tests/test_ui.py`.

| Test | What it verifies |
|------|-----------------|
| `test_welcome_message` | Startup displays a welcome message (Req 1.2) |
| `test_category_menu_displayed` | Category menu lists all registered categories (Req 2.1) |
| `test_quit_exits_with_farewell` | Quit option exits cleanly with farewell (Req 2.4) |
| `test_direction_menu_displayed` | Temperature direction menu shows 3 options (Req 3.1) |
| `test_back_returns_to_category_menu` | Option 3 returns to category menu (Req 3.4) |
| `test_numeric_prompt_appears` | Numeric prompt appears after direction selection (Req 4.1) |
| `test_post_result_prompt` | Post-result prompt appears after conversion (Req 6.3) |
| `test_successive_conversions` | Two conversions in one session both display results (Req 7.1) |
| `test_conversion_returns_to_menu` | App returns to a menu after conversion (Req 7.2) |
| `test_quit_terminates_session` | Session terminates on quit (Req 7.3) |
| `test_known_celsius_to_fahrenheit` | 0°C → 32.00°F, 100°C → 212.00°F |
| `test_known_fahrenheit_to_celsius` | 32°F → 0.00°C, 212°F → 100.00°C |

### Property-Based Tests

Located in `tests/test_properties.py`. Each test references its design property via a comment tag.

```
# Feature: unit-converter-cli, Property N: <property_text>
```

| Test | Property | Hypothesis strategy |
|------|----------|---------------------|
| `test_c_to_f_formula` | Property 1 | `floats(allow_nan=False, allow_infinity=False)` |
| `test_f_to_c_formula` | Property 2 | `floats(allow_nan=False, allow_infinity=False)` |
| `test_results_rounded` | Property 3 | `floats(allow_nan=False, allow_infinity=False)` |
| `test_round_trip` | Property 4 | `floats(allow_nan=False, allow_infinity=False)` |
| `test_display_result_fields` | Property 5 | `floats` × `text` × `floats` × `text` |
| `test_invalid_menu_input_error` | Property 6 | `text()` filtered to exclude valid option strings |
| `test_non_numeric_rejected` | Property 7 | `text()` filtered to exclude float-parseable strings |
| `test_valid_index_dispatches` | Property 8 | `integers` bounded to registry size |

Each property test uses `@settings(max_examples=100)` (Hypothesis default is 100; set explicitly for clarity).
