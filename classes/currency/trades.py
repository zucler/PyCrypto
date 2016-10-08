import settings
import logging

from classes.dbHelper import DbHelper

logger = logging.getLogger(__name__)


class Trades:
    def __init__(self, db):
        self.db = db  # type: DbHelper

    def update_rate_models(self, buy, sell, exchange_id, pair_id):
        sorted(sell, key=self._get_key)
        sorted(sell, key=self._get_key, reverse=True)

        sell = sell[:5]
        buy = buy[:5]

        sell = [s + (exchange_id, pair_id) for s in sell]
        buy = [b + (exchange_id, pair_id) for b in buy]

        self._store_rates_details("sell", sell)
        self._store_rates_details("buy", buy)

    def find_trade(self, pair_id):
        """

        Args:
            pair_id (int)

        """
        query = "SELECT rate, exchangeid, volume, e.name as exchange_name"
        query += " FROM sell JOIN exchange e ON exchangeid=e.id AND pairid=" + str(pair_id)
        query += " WHERE CURRENT_TIMESTAMP()-DATE<" + str(settings.TRADE_WINDOW)
        query += " AND rate=(SELECT min(rate) FROM sell WHERE CURRENT_TIMESTAMP()-DATE<" + str(
            settings.TRADE_WINDOW) + ")"

        min_sell_trade = self.db.get_first_row_as_dictionary(query)
        min_sell = min_sell_trade["rate"]
        sell_exchange = min_sell_trade["exchange_name"]
        sell_volume = min_sell_trade["volume"]
        fromex = min_sell_trade["exchangeid"]

        query = "SELECT rate, exchangeid, volume, e.name as exchange_name"
        query += " FROM buy JOIN exchange e ON exchangeid=e.id AND pairid=" + str(pair_id)
        query += " WHERE CURRENT_TIMESTAMP()-DATE<" + str(settings.TRADE_WINDOW)
        query += " AND rate=(SELECT max(rate) FROM buy WHERE CURRENT_TIMESTAMP()-DATE<" + str(
            settings.TRADE_WINDOW) + ")"

        max_buy_trade = self.db.get_first_row_as_dictionary(query)
        max_buy = max_buy_trade["rate"]
        buy_exchange = max_buy_trade["exchange_name"]
        buy_volume = max_buy_trade["volume"]
        toex = max_buy_trade["exchangeid"]

        trade_volume = min(sell_volume, buy_volume)
        profit = max_buy - min_sell

        if profit > 0:
            last_trade_query = "SELECT fromex, toex, buyprice, sellprice, volume"
            last_trade_query += " FROM trade WHERE parid=" + str(pair_id)
            last_trade_query += " AND date=(SELECT max(date) FROM trade WHERE pairid=" + str(pair_id) + ")"

            old_from_ex, old_to_ex, old_sell, old_buy, old_volume = 0, 0, 0, 0, 0

            last_trade = self.db.get_first_row_as_dictionary(last_trade_query)
            if last_trade:
                old_sell = last_trade["sellprice"]
                old_buy = last_trade["buyprice"]
                old_volume = last_trade["volume"]

            if old_volume == trade_volume and old_sell == min_sell and old_buy == max_buy:
                logger.info("Previous trade still available")
            else:
                logger.info("Buying " + "{:10.8f}".format(trade_volume) + " for pair_id=" + str(pair_id) + " at " + str(
                    min_sell) + " in " + sell_exchange + " and selling at " + str(max_buy) + " in " + buy_exchange)
                logger.info("{:10.8f}".format(trade_volume * min_sell) + " spent for transaction")
                logger.info("Getting " + "{:10.8f}".format(profit * trade_volume) + " profit")
                insert_trade_query = "INSERT INTO trade (FROMEX, TOEX, BUYPRICE, SELLPRICE, VOLUME, PAIRID) VALUES (%s, %s, %s, %s, %s, %s)"
                trade = (fromex, toex, min_sell, max_buy, trade_volume, pair_id)

                self.db.insert(insert_trade_query, trade)
                logger.debug("inserted ")
        else:
            logger.info("Price difference: " + "{:10.8f}".format(profit))
            logger.info("Trade is not yet profitable for pair_id=" + str(pair_id))

    def _store_rates_details(self, trade_type, data):
        query = "INSERT INTO `" + trade_type + "` (RATE, VOLUME, EXCHANGEID, PAIRID) VALUES (%s, %s, %s, %s)"

        self.db.insert(query, data)

    @staticmethod
    def _get_key(item):
        a, b = item
        return a
