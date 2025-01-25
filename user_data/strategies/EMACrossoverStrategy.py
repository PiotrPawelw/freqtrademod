from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import time


class EMACrossoverStrategy(IStrategy):
    """
    Strategia oparta na przecięciu dwóch wskaźników EMA: krótkoterminowego i długoterminowego.
    """

    # Definicja interwału czasowego
    timeframe = "5m"  # Możesz zmienić na 1m, 15m, 1h itp.

    # Stop-loss i take-profit
    stoploss = -0.2  # 2% straty maksymalnie
    trailing_stop = True  # Aktywacja trailing stop-loss
    trailing_stop_positive = 0.01  # Trailing stop aktywuje się przy zysku 1%
    trailing_stop_positive_offset = 0.02  # Ustawia trailing stop na 2%

    # Parametry optymalizacyjne dla EMA
    ema_short_period = IntParameter(5, 25, default=50, space="buy")  # EMA krótkoterminowa
    ema_long_period = IntParameter(30, 100, default=50, space="buy")  # EMA długoterminowa

    # Warunki minimalne dla handlu
    minimal_roi = {
        "0": 0.001,  # Minimalny zysk 1% (po osiągnięciu tego, pozycja może być zamknięta)
    }

    # Buforowanie cen likwidacji
    liquidation_prices = {}
    last_update_time = 0  # Ostatnia aktualizacja bufora

    def get_liquidation_price(self, trade):
        """
        Zwraca cenę likwidacji z bufora lub oblicza ją, jeśli jej tam nie ma.
        Odświeża bufor co 5 minut.
        """
        current_time = time.time()
        # Czyści bufor co 5 minut
        if current_time - self.last_update_time > 300:
            self.liquidation_prices = {}
            self.last_update_time = current_time

        # Jeśli cena likwidacji nie jest w buforze, oblicz ją
        if trade["trade_id"] not in self.liquidation_prices:
            self.liquidation_prices[trade["trade_id"]] = self.calculate_liquidation_price(
                amount=trade["amount"],
                entry_price=trade["price"],
                leverage=trade["leverage"],
                side=trade["side"],
                initial_margin=trade["initial_margin"],
            )
        return self.liquidation_prices[trade["trade_id"]]

    def calculate_liquidation_price(self, amount, entry_price, leverage, side, initial_margin):
        """
        Uproszczona funkcja do obliczania ceny likwidacji.
        """
        if side == "long":
            return entry_price * (1 - (initial_margin / (amount * leverage)))
        elif side == "short":
            return entry_price * (1 + (initial_margin / (amount * leverage)))
        else:
            return None

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Oblicz wskaźniki EMA i dodaj je do dataframe'u.
        """
        dataframe["ema_short"] = ta.EMA(dataframe, timeperiod=self.ema_short_period.value)
        dataframe["ema_long"] = ta.EMA(dataframe, timeperiod=self.ema_long_period.value)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Określ warunki wejścia w pozycję (kupno).
        """
        dataframe.loc[
            (
                dataframe["ema_short"] > dataframe["ema_long"]
            ),  # EMA krótkoterminowa powyżej długoterminowej
            "buy",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Określ warunki wyjścia z pozycji (sprzedaż).
        """
        dataframe.loc[
            (
                dataframe["ema_short"] < dataframe["ema_long"]
            ),  # EMA krótkoterminowa poniżej długoterminowej
            "sell",
        ] = 1
        return dataframe
