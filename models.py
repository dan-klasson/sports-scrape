from core import BaseModel

class Model(BaseModel):

    def get_competitor_id(self, name):
        sql = "SELECT competitor_id FROM competitor WHERE description = %s"
        row = self.db.fetch(sql, (name, ))
        return row['competitor_id']

    def get_bookmaker_market_id(self, name):
        sql = """
            SELECT bm.bookmaker_market_id FROM bookmaker_market AS bm 
            INNER JOIN market_type AS mt ON bm.market_type_id = mt.market_type_id 
            WHERE mt.description = %s
        """
        row = self.db.fetch(sql, (name, ))
        return row['bookmaker_market_id']
       
    def get_bet_opportunity_id(self, competitor_id, market_id):
        sql = """
            SELECT bet_opportunity_id FROM bet_opportunity 
            WHERE competitor_id = %s
            AND bookmaker_market_id = %s
        """
        row = self.db.fetch(sql, (competitor_id, market_id, ))
        return row['bet_opportunity_id']

    def insert_bet_opportunity(self, competitor_id, market_id):
        sql = """
            INSERT INTO bet_opportunity SET
            competitor_id = %s,
            bookmaker_market_id = %s;
        """
        return self.db.save(sql, (competitor_id, market_id, ))

    def get_bet_odds(self, bet_opportunity_id, odds=False):

        sql = """
            SELECT lay_price FROM bet_odds
            WHERE bet_opportunity_id = %s
        """

        params = (bet_opportunity_id, )

        if odds:
            sql += "AND lay_price = %s"
            params += (odds, )

        row = self.db.fetch(sql, params)
        return row

    def update_bet_odds(self, bet_opportunity_id, odds):
        sql = """
            UPDATE bet_odds SET 
            lay_price = %s, 
            last_update = NOW()
            WHERE bet_opportunity_id = %s
        """
        return self.db.save(sql, (odds, bet_opportunity_id, ))


    def insert_bet_odds(self, bet_opportunity_id, odds):
        sql = """
            INSERT INTO bet_odds SET
            bet_opportunity_id = %s,
            lay_price = %s,
            last_update = NOW()
        """

        return self.db.save(sql, (bet_opportunity_id, odds, ))

    def fraction_to_decimal(self, fraction):
        values = fraction.split("/")
        odds = float(values[0]) / float(values[1]) + 1
        return round(odds, 2)


