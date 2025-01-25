import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import IntParameter, IStrategy


class EMACrossoverStrategy(IStrategy):
    """
    Strategia oparta na przecięciu dwóch wskaźników EMA: krótkoterminowego i długoterminowego.
    """

    # Definicja interwału czasowego
    timeframe = "5m"  # Możesz zmienić na 1m, 15m, 1h itp.

    # Stop-loss i take-profit
    stoploss = -0.02  # 2% straty maksymalnie
    trailing_stop = True  # Aktywacja trailing stop-loss
    trailing_stop_positive = 0.01  # Trailing stop aktywuje się przy zysku 1%
    trailing_stop_positive_offset = 0.02  # Ustawia trailing stop na 2%

    # Parametry optymalizacyjne dla EMA
    ema_short_period = IntParameter(5, 25, default=10, space="buy")  # EMA krótkoterminowa
    ema_long_period = IntParameter(30, 100, default=50, space="buy")  # EMA długoterminowa

    # Warunki minimalne dla handlu
    minimal_roi = {
        # Minimalny zysk 1% (po osiągnięciu tego, pozycja może być zamknięta)
        "0": 0.01,
    }

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
