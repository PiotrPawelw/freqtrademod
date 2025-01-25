#!/usr/bin/env python3

import os
import subprocess


# Ścieżka do folderu z strategiami
strategies_dir = "user_data/strategies/"

freqaimodels = [
    "ReinforcementLearner_multiproc",
    "CatboostClassifier",
    "CatboostClassifierMultiTarget",
    "CatboostRegressor",
    "CatboostRegressorMultiTarget",
    "LightGBMClassifier",
    "LightGBMClassifierMultiTarget",
    "PyTorchMLPClassifier",
    "PyTorchMLPRegressor",
    "PyTorchTransformerRegressor",
    "ReinforcementLearner",
    "SKLearnRandomForestClassifier",
    "XGBoostClassifier",
    "XGBoostRFClassifier",
    "XGBoostRFRegressor",
    "XGBoostRegressor",
    "XGBoostRegressorMultiTarget",
]

hyperopt_losses = [
    "ShortTradeDurHyperOptLoss",
    "ShortTradeDurHyperOptLoss",
    "SharpeHyperOptLoss",
    "SharpeHyperOptLossDaily",
    "SortinoHyperOptLoss",
    "SortinoHyperOptLossDaily",
    "CalmarHyperOptLoss",
    "MaxDrawDownHyperOptLoss",
    "MaxDrawDownRelativeHyperOptLoss",
    "ProfitDrawDownHyperOptLoss",
    "MultiMetricHyperOptLoss",
    "MultiMetricHyperOptLoss",
]

spaces_options = ["roi", "stoploss", "trailing", "trades", "buy", "sell", "trailing", "all"]


def list_strategies():
    """
    Pobierz listę dostępnych strategii w folderze.
    """
    strategies = [f[:-3] for f in os.listdir(strategies_dir) if f.endswith(".py")]
    return strategies


def select_option(options, prompt):
    """
    Wyświetl listę opcji i pozwól użytkownikowi wybrać jedną.
    """
    if not options:
        print("Brak dostępnych opcji.")
        return None

    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    while True:
        try:
            choice = int(input("Wybierz opcję (numer): ").strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Nieprawidłowy numer. Spróbuj ponownie.")
        except ValueError:
            print("Wprowadź poprawny numer.")


def optimize_strategy(strategy_name, freqaimodel, epochs, hyperopt_loss, spaces):
    """
    Uruchom hiperoptymalizację dla podanej strategii z wybranym modelem, liczbą epok, funkcją strat i przestrzenią.
    """
    print(f"Rozpoczynanie hiperoptymalizacji dla strategii: {strategy_name}")
    print(
        f"Model: {freqaimodel}, Liczba epok: {epochs}, Funkcja strat: {hyperopt_loss}, Przestrzeń: {spaces}"
    )

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
                spaces,
                "--config",
                "./config.json",
                "--freqaimodel",
                freqaimodel,
                "--hyperopt-loss",
                hyperopt_loss,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas hiperoptymalizacji dla strategii {strategy_name}: {e}")


if __name__ == "__main__":
    strategies = list_strategies()
    selected_strategy = select_option(strategies, "Dostępne strategie:")

    if selected_strategy:
        selected_freqaimodel = select_option(freqaimodels, "Dostępne modele FreqAI:")

        if selected_freqaimodel:
            selected_hyperopt_loss = select_option(hyperopt_losses, "Dostępne funkcje strat:")

            if selected_hyperopt_loss:
                selected_spaces = select_option(spaces_options, "Dostępne przestrzenie (spaces):")

                if selected_spaces:
                    while True:
                        try:
                            epochs = int(input("Podaj liczbę epok (np. 50): ").strip())
                            break
                        except ValueError:
                            print("Wprowadź poprawną liczbę.")

                    optimize_strategy(
                        selected_strategy,
                        selected_freqaimodel,
                        epochs,
                        selected_hyperopt_loss,
                        selected_spaces,
                    )
