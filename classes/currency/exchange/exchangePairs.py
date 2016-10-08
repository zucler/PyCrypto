import time
import json
import settings
from jsonpath_rw import parse
from classes.currency.pairs import CurrencyPairs
from classes.dbHelper import DbHelper
from classes.currency.trades import Trades
import logging

logger = logging.getLogger(__name__)


class ExchangePairs(CurrencyPairs):
    """ Exchange pairs for a given currency pair """

    def __init__(self, db_cursor, currency_pair):
        CurrencyPairs.__init__(self, db_cursor)

        self.currency_pair = str(currency_pair)  # type: str

    def get_all(self):
        """
        Get all exchange pairs for a currency pair

        Returns:
            List of dictionaries
        """
        query = ""
        query += "SELECT *"
        query += " FROM `EXCHANGEPAIR` `EP`"
        query += " JOIN `EXCHANGE` `E` ON `EP`.`EXCHANGEID`=`E`.`ID` AND `EP`.`ENABLED`=1"
        query += " WHERE `EP`.`PAIRID` = " + self.currency_pair

        exchange_pairs = self.db.get_results_as_dictionary_list(query)

        return exchange_pairs

    @staticmethod
    def load_exchange_pair_rates(exchange_pair, api_json, process_id):
        """
        Retrieve a single page and report the url and contents

        Args:
            exchange_pair (dict)
            process_id (int)

        Returns:

        """
        db = DbHelper(settings.DATABASE["USER"], settings.DATABASE["PASSWORD"], settings.DATABASE["HOST"],
                      settings.DATABASE["PORT"], settings.DATABASE["SCHEMA"])

        trades = Trades(db)

        start_time = time.time()

        exchange_id = exchange_pair["EXCHANGEID"]
        pair_id = exchange_pair["PAIRID"]
        api_url = exchange_pair["APIURL"]
        sell_path = exchange_pair["SELLPATH"]
        buy_path = exchange_pair["BUYPATH"]
        sell_vol_path = exchange_pair["SELLVOLUMEPATH"]
        buy_vol_path = exchange_pair["BUYVOLUMEPATH"]

        json_sell_expr = parse(sell_path)
        json_sell_vol_expr = parse(sell_vol_path)

        json_buy_expr = parse(buy_path)
        json_buy_vol_expr = parse(buy_vol_path)

        logger.debug("process " + str(process_id) + " started: " + api_url)
        json_response = json.loads(api_json)

        sell_rates = [match.value for match in json_sell_expr.find(json_response)]
        sell_volumes = [match.value for match in json_sell_vol_expr.find(json_response)]

        buy_rates = [match.value for match in json_buy_expr.find(json_response)]
        buy_volumes = [match.value for match in json_buy_vol_expr.find(json_response)]

        sell = zip(sell_rates, sell_volumes)
        buy = zip(buy_rates, buy_volumes)

        logger.debug("process " + str(process_id) + " inserting: " + str(len(sell)) + "+" + str(len(buy)))
        trades.update_rate_models(buy, sell, exchange_id, pair_id)
        trades.find_trade(pair_id)

        logger.debug("process " + str(process_id) + " sleeping ")
        time.sleep(settings.SLEEP_TIMER)
        logger.debug("process " + str(process_id) + " finished in " + "{:.2}".format(time.time() - start_time))

        db.close()
