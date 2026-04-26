from ui import display_welcome, display_farewell, display_error, prompt_menu


def show_category_menu(registry: dict) -> str:
    options = list(registry.keys()) + ["Quit"]
    return prompt_menu(options)


def handle_category_choice(choice: str, registry: dict) -> bool:
    keys = list(registry.keys())
    quit_index = len(keys) + 1
    try:
        index = int(choice)
    except ValueError:
        display_error("Invalid choice. Please enter a number from the menu.")
        return True

    if index == quit_index:
        return False
    elif 1 <= index <= len(keys):
        registry[keys[index - 1]]()
        return True
    else:
        display_error("Invalid choice. Please enter a number from the menu.")
        return True


def run() -> None:
    from converters import REGISTRY

    display_welcome()
    try:
        while True:
            choice = show_category_menu(REGISTRY)
            if not handle_category_choice(choice, REGISTRY):
                break
    except KeyboardInterrupt:
        pass
    display_farewell()
