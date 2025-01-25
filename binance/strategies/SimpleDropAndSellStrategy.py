from pandas import DataFrame

from freqtrade.strategy.interface import IStrategy


class SimpleDropAndSellStrategy(IStrategy):
    # Interwał czasowy (np. 5-minutowe świece)
    timeframe = "5m"

    # Take profit i stop loss jako procenty
    minimal_roi = {"0": 0.0005}  # 0.05% zysk
    stoploss = -0.005  # -0.5% strata

    # Ta strategia nie wymaga trailing stop
    trailing_stop = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Dodajemy wskaźniki, jeśli są potrzebne.
        W tej strategii nie używamy dodatkowych wskaźników.
        """
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Definiujemy warunki zakupu.
        Kupujemy, gdy cena spadła o 0.5% w porównaniu z poprzednią świecą.
        """
        dataframe.loc[
            (dataframe["close"] < dataframe["close"].shift(1) * 0.995),  # Cena spadła o 0.5%
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Definiujemy warunki sprzedaży.
        Sprzedajemy, gdy cena wzrośnie o 0.05% w porównaniu z ceną zakupu.
        """
        dataframe.loc[
            (dataframe["close"] > dataframe["close"].shift(1) * 1.0005),  # Cena wzrosła o 0.05%
            "sell",
        ] = 1
        return dataframe
