# Requirements Document

## Introduction

A command-line interface (CLI) application written in Python with no external dependencies that guides users through unit conversions interactively. The first supported conversion type is temperature, enabling bidirectional conversion between Celsius and Fahrenheit with results rounded to 2 decimal places. The application is designed to be extensible so additional unit categories can be added in the future.

## Glossary

- **CLI**: Command-Line Interface — the text-based interface through which the user interacts with the application.
- **App**: The unit-converter-cli Python application.
- **Converter**: The component responsible for performing a specific unit conversion calculation.
- **Temperature_Converter**: The Converter specialised for temperature unit conversions.
- **User**: A person running the application from a terminal.
- **Conversion_Result**: The numeric output produced by the Converter, rounded to 2 decimal places.
- **Celsius**: A temperature scale where water freezes at 0° and boils at 100°.
- **Fahrenheit**: A temperature scale where water freezes at 32° and boils at 212°.

---

## Requirements

### Requirement 1: Application Entry Point

**User Story:** As a User, I want to launch the application from the command line, so that I can start performing unit conversions without any setup or external dependencies.

#### Acceptance Criteria

1. THE App SHALL be executable as a standard Python script using `python` or `python3` with no third-party packages installed.
2. WHEN the App starts, THE App SHALL display a welcome message and prompt the User to select a conversion category.

---

### Requirement 2: Conversion Category Selection

**User Story:** As a User, I want to choose a conversion category from a menu, so that I can navigate to the specific type of conversion I need.

#### Acceptance Criteria

1. WHEN the App starts, THE App SHALL present a numbered menu listing all available conversion categories.
2. WHEN the User enters a valid category number, THE App SHALL navigate to the corresponding conversion workflow.
3. IF the User enters a value that does not correspond to any listed category, THEN THE App SHALL display an error message and re-present the category menu.
4. WHEN the User selects the option to quit, THE App SHALL exit cleanly with a farewell message.

---

### Requirement 3: Temperature Conversion — Direction Selection

**User Story:** As a User, I want to choose the direction of temperature conversion, so that I can convert either from Celsius to Fahrenheit or from Fahrenheit to Celsius.

#### Acceptance Criteria

1. WHEN the temperature category is selected, THE App SHALL present a numbered menu with the following options: (1) Celsius to Fahrenheit, (2) Fahrenheit to Celsius, (3) Back to main menu.
2. WHEN the User selects option 1, THE Temperature_Converter SHALL accept a Celsius value as input and produce a Fahrenheit Conversion_Result.
3. WHEN the User selects option 2, THE Temperature_Converter SHALL accept a Fahrenheit value as input and produce a Celsius Conversion_Result.
4. WHEN the User selects option 3, THE App SHALL return to the conversion category menu.
5. IF the User enters a value that does not correspond to any listed option, THEN THE App SHALL display an error message and re-present the direction menu.

---

### Requirement 4: Temperature Value Input

**User Story:** As a User, I want to enter a numeric temperature value, so that the application can compute the converted result.

#### Acceptance Criteria

1. WHEN a conversion direction is selected, THE App SHALL prompt the User to enter a numeric temperature value.
2. WHEN the User enters a valid integer or decimal number, THE Temperature_Converter SHALL use that value as the input for conversion.
3. IF the User enters a non-numeric value, THEN THE App SHALL display an error message and re-prompt for a valid numeric value.

---

### Requirement 5: Temperature Conversion Calculation

**User Story:** As a User, I want the application to accurately convert temperature values, so that I receive a correct result.

#### Acceptance Criteria

1. WHEN converting from Celsius to Fahrenheit, THE Temperature_Converter SHALL apply the formula: result = (input × 9/5) + 32.
2. WHEN converting from Fahrenheit to Celsius, THE Temperature_Converter SHALL apply the formula: result = (input − 32) × 5/9.
3. THE Temperature_Converter SHALL round every Conversion_Result to exactly 2 decimal places.
4. FOR ALL numeric input values, converting from Celsius to Fahrenheit and then back to Celsius SHALL produce a value equal to the original input when both results are rounded to 2 decimal places (round-trip property).

---

### Requirement 6: Conversion Result Display

**User Story:** As a User, I want to see the conversion result clearly, so that I can read and use the output immediately.

#### Acceptance Criteria

1. WHEN a Conversion_Result is produced, THE App SHALL display the original input value, the source unit, the Conversion_Result, and the target unit on a single output line.
2. THE App SHALL format the Conversion_Result to exactly 2 decimal places in the displayed output.
3. WHEN a result is displayed, THE App SHALL prompt the User to perform another conversion or return to the main menu.

---

### Requirement 7: Continuous Operation

**User Story:** As a User, I want to perform multiple conversions in a single session, so that I do not have to restart the application between conversions.

#### Acceptance Criteria

1. WHILE the App is running, THE App SHALL allow the User to perform successive conversions without restarting.
2. WHEN a conversion is complete, THE App SHALL return the User to a menu (either the direction menu or the category menu, per the User's choice) rather than exiting.
3. WHEN the User chooses to quit from the main menu, THE App SHALL terminate the session.
