"""Lbank exchange subclass"""

import logging

from freqtrade.exchange import Exchange
from freqtrade.exchange.exchange_types import FtHas


logger = logging.getLogger(__name__)


class Lbank(Exchange):
    """
    Lbank exchange class. Contains adjustments needed for Freqtrade to work
    with this exchange.
    """

    _ft_has: FtHas = {
        # lower than the allowed 2000 to avoid current_candle issue
        "ohlcv_candle_limit": 1998,
        "trades_has_history": False,
    }
