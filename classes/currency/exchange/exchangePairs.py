from classes.currency.pairs import CurrencyPairs

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
