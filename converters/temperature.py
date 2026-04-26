from ui import prompt_float, display_result, prompt_menu, display_error


def celsius_to_fahrenheit(celsius: float) -> float:
    return round((celsius * 9 / 5) + 32, 2)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return round((fahrenheit - 32) * 5 / 9, 2)


def run() -> None:
    while True:
        choice = prompt_menu([
            "Celsius to Fahrenheit",
            "Fahrenheit to Celsius",
            "Back to main menu",
        ])

        if choice == "1":
            value = prompt_float("Enter temperature in Celsius: ")
            result = celsius_to_fahrenheit(value)
            display_result(value, "Celsius", result, "Fahrenheit")
        elif choice == "2":
            value = prompt_float("Enter temperature in Fahrenheit: ")
            result = fahrenheit_to_celsius(value)
            display_result(value, "Fahrenheit", result, "Celsius")
        elif choice == "3":
            break
        else:
            display_error("Invalid choice. Please enter 1, 2, or 3.")
