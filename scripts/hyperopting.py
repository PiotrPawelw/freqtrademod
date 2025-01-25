import os
import subprocess
from typing import List


def list_files_in_directory(directory: str, extension: str) -> List[str]:
    """
    Zwraca listę plików z określonym rozszerzeniem w podanym katalogu.
    :param directory: Ścieżka do katalogu.
    :param extension: Rozszerzenie plików (np. ".py").
    :return: Lista nazw plików (bez rozszerzeń).
    """
    return [file[: -len(extension)] for file in os.listdir(directory) if file.endswith(extension)]


def user_choice(options: List[str], prompt: str) -> str:
    """
    Wyświetla menu wyboru dla użytkownika i zwraca wybraną opcję.
    :param options: Lista opcji do wyboru.
    :param prompt: Tekst wyświetlany użytkownikowi.
    :return: Wybrana opcja.
    """
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input("Wybierz numer: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Nieprawidłowy numer, spróbuj ponownie.")
        except ValueError:
            print("Proszę podać numer.")


def optimize_strategy(strategy_name: str, freqaimodel: str, epochs: int, spaces: List[str]):
    """
    Uruchamia hiperoptymalizację dla podanej strategii.
    :param strategy_name: Nazwa strategii.
    :param freqaimodel: Wybrany model FreqAI.
    :param epochs: Liczba epok.
    :param spaces: Lista przestrzeni do optymalizacji.
    """
    print(f"Rozpoczynanie hiperoptymalizacji dla strategii: {strategy_name}")
    try:
        subprocess.run(
            [
                "freqtrade",
                "hyperopt",
                "--strategy",
                strategy_name,
                "--epochs",
                str(epochs),
                "--spaces",
                *spaces,
                "--config",
                "./config.json",
                "--freqaimodel",
                freqaimodel,
                "--hyperopt-loss",
                "ShortTradeDurHyperOptLoss",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas hiperoptymalizacji dla strategii {strategy_name}: {e}")


if __name__ == "__main__":
    # Ścieżki do katalogów
    strategies_dir = "user_data/strategies/"
    freqai_models_dir = "freqtrade/freqai/prediction_models/"

    # Pobranie dostępnych strategii i modeli
    strategies = list_files_in_directory(strategies_dir, ".py")
    freqai_models = list_files_in_directory(freqai_models_dir, ".py")

    # Wybor użytkownika
    selected_strategy = user_choice(strategies, "Wybierz strategię:")
    selected_model = user_choice(freqai_models, "Wybierz model FreqAI:")

    # Pobranie liczby epok
    while True:
        try:
            selected_epochs = int(input("Podaj liczbę epok: "))
            if selected_epochs > 0:
                break
            else:
                print("Liczba epok musi być większa od zera.")
        except ValueError:
            print("Proszę podać liczbę całkowitą.")

    # Wybór przestrzeni optymalizacyjnych
    spaces = ["roi", "stoploss", "trailing"]
    selected_spaces = []
    print("Wybierz przestrzenie optymalizacyjne (wpisz numery oddzielone przecinkami, np. 1,2):")
    for idx, space in enumerate(spaces, start=1):
        print(f"{idx}. {space}")
    while True:
        try:
            choices = input("Twoje wybory: ").split(",")
            selected_spaces = [
                spaces[int(choice) - 1] for choice in choices if 1 <= int(choice) <= len(spaces)
            ]
            if selected_spaces:
                break
            else:
                print("Musisz wybrać co najmniej jedną przestrzeń.")
        except (ValueError, IndexError):
            print("Nieprawidłowy wybór, spróbuj ponownie.")

    # Uruchomienie hiperoptymalizacji
    optimize_strategy(selected_strategy, selected_model, selected_epochs, selected_spaces)
