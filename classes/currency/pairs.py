from classes.dbHelper import DbHelper

class CurrencyPairs:
    """ Currency pairs on the market """

    def __init__(self, db):
        """

        Args:
            db (DbHelper):
        """
        self.db = db  # type: DbHelper

    def get_all(self):
        """
        Get all known currency pairs

        Returns:
            Dict of currency pairs
        """
        query = "SELECT * FROM `PAIR`"

        pairs = self.db.get_results_as_dictionary_list(query)

        return pairs

    def get_by_id(self, pair_id):
        query = "SELECT * FROM `PAIR` WHERE `ID` = " + str(pair_id)

        pair = self.db.get_first_row_as_dictionary(query)

        return pair
