import pandas as pd
from binance.client import Client


# Ustaw swoje klucze API Binance (opcjonalne dla publicznych danych)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# Inicjalizacja klienta Binance
client = Client(API_KEY, API_SECRET)


def get_spot_pairs():
    """
    Pobierz dane o parach spot z Binance.
    """
    try:
        # Pobierz wszystkie symbole z rynku spot
        exchange_info = client.get_exchange_info()
        symbols = exchange_info["symbols"]

        # Filtruj pary spot (status TRADING oznacza aktywne pary)
        spot_pairs = [symbol for symbol in symbols if symbol["status"] == "TRADING"]
        return spot_pairs
    except Exception as e:
        print(f"Error fetching spot pairs: {e}")
        return []


def get_24hr_ticker_data():
    """
    Pobierz dane z 24-godzinnego tickera dla wszystkich par.
    """
    try:
        tickers = client.get_ticker()
        return tickers
    except Exception as e:
        print(f"Error fetching 24hr ticker data: {e}")
        return []


def find_profitable_spot_pairs(base_pair):
    """
    Analizuje najbardziej opłacalne pary na rynku spot na podstawie procentowej zmiany i wolumenu.
    Filtruje tylko pary zawierające wybraną główną parę.
    """
    tickers = get_24hr_ticker_data()

    # Tworzenie DataFrame dla analizy
    df = pd.DataFrame(tickers)
    df["priceChangePercent"] = df["priceChangePercent"].astype(float)
    df["quoteVolume"] = df["quoteVolume"].astype(float)

    # Filtruj pary z wybraną główną parą (base_pair)
    df = df[df["symbol"].str.endswith(base_pair)]

    # Filtruj i sortuj na podstawie procentowej zmiany i wolumenu
    profitable_pairs = df.sort_values(
        by=["priceChangePercent", "quoteVolume"], ascending=False
    ).head(10)

    # Formatowanie symboli na postać BASE/QUOTE
    profitable_pairs["formattedSymbol"] = profitable_pairs["symbol"].apply(
        lambda x: f"{x[: -len(base_pair)]}/{base_pair}"
    )

    return profitable_pairs


if __name__ == "__main__":
    # Pytaj użytkownika o główną parę walutową
    base_pair = input("Podaj główną parę walutową (np. USDT, BTC, ETH): ").strip().upper()

    # Znajdź najbardziej opłacalne pary na rynku spot dla wybranej głównej pary
    profitable_pairs = find_profitable_spot_pairs(base_pair)

    if not profitable_pairs.empty:
        print("Najbardziej opłacalne pary spot na Binance dla ", base_pair, ":")
        print(profitable_pairs[["formattedSymbol", "priceChangePercent", "quoteVolume"]])
    else:
        print(f"Brak wyników dla podanej głównej pary: {base_pair}")
