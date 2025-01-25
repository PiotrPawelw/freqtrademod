import os
import subprocess

# Ścieżka do folderu z strategiami
strategies_dir = "user_data/strategies/"

# Funkcja do uruchamiania backtestu dla każdej strategii
def backtest_all_strategies():
    # Iteracja po plikach w folderze strategii
    for strategy_file in os.listdir(strategies_dir):
        # Sprawdzenie, czy plik ma rozszerzenie .py (czyli jest to plik strategii)
        if strategy_file.endswith(".py"):
            # Pobranie nazwy strategii (bez rozszerzenia)
            strategy_name = strategy_file[:-3]

            print(f"Rozpoczynanie backtestu dla strategii: {strategy_name}")

            # Uruchomienie procesu backtestu za pomocą subprocess
            try:
                subprocess.run([
                    "freqtrade", "backtesting", 
                    "--strategy", strategy_name,  # Nazwa strategii
                    "--timerange", "20250101-",
                    "--freqaimodel", "CatboostRegressor",
		    "--config", "./config.json",  # Zakres czasowy (dostosuj do swoich potrzeb)             # Liczba epok (można dostosować, ale w backtestach to nie ma wpływu)
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Błąd podczas backtestu dla strategii {strategy_name}: {e}")

if __name__ == "__main__":
    backtest_all_strategies()
