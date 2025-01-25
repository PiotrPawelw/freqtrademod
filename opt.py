#!/usr/bin/env python
import os
import subprocess


# Ścieżka do folderu z strategiami
strategies_dir = "user_data/strategies/"


# Funkcja do uruchamiania hyperoptymalizacji dla każdej strategii
def optimize_all_strategies():
    # Iteracja po plikach w folderze strategii
    for strategy_file in os.listdir(strategies_dir):
        # Sprawdzenie, czy plik ma rozszerzenie .py (czyli jest to plik strategii)
        if strategy_file.endswith(".py"):
            # Pobranie nazwy strategii (bez rozszerzenia)
            strategy_name = strategy_file[:-3]

            print(f"Rozpoczynanie hiperoptymalizacji dla strategii: {strategy_name}")

            # Uruchomienie procesu hiperoptymalizacji za pomocą subprocess
            try:
                subprocess.run(
                    [
                        "freqtrade",
                        "hyperopt",
                        "--strategy",
                        strategy_name,  # Nazwa strategii
                        "--epochs",
                        "50",
                        "--spaces",
                        "roi",
                        "stoploss",
                        "--config",
                        "./1.json",
                        "--freqaimodel",
                        "ReinforcementLearner_multiproc",
                        "--hyperopt-loss",
                        "ShortTradeDurHyperOptLoss",
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Błąd podczas hiperoptymalizacji dla strategii {strategy_name}: {e}")


if __name__ == "__main__":
    optimize_all_strategies()
