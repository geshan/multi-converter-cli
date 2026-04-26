def display_welcome() -> None:
    print("Welcome to Unit Converter CLI!")


def display_farewell() -> None:
    print("Goodbye!")


def display_error(message: str) -> None:
    print(message)


def prompt_menu(options: list) -> str:
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    return input("> ")


def prompt_float(prompt_text: str) -> float:
    while True:
        raw = input(prompt_text)
        try:
            return float(raw)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def display_result(input_val: float, from_unit: str, result: float, to_unit: str) -> None:
    print(f"{input_val} {from_unit} = {result:.2f} {to_unit}")
