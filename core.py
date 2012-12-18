from settings import *
import abc
from bs4 import BeautifulSoup
from models import Model
import MySQLdb
import MySQLdb.cursors 

"""Simple base class for all models."""
class BaseModel(object):

    db = None

    def __init__(self):
        self.db = Db(
            host    = db_settings['host'], 
            user    = db_settings['user'], 
            passwd  = db_settings['passwd'], 
            db      = db_settings['db'], 
        )

"""Abstract class for all pages to be scraped"""
class BasePage(object):
    __metaclass__ = abc.ABCMeta

    model = None
    source = None

    def __init__(self):
        self.model = Model()

    @abc.abstractmethod
    def scrape(self, input):
        """Retrieve data from the input source and return a dictionary."""
        return
    
    def process(self):
        """Process the scraped data."""

        self.soup = BeautifulSoup(self.source)
        result = self.scrape()

        market_id = self.model.get_bookmaker_market_id(self.market_type)

        for competitor, odds in result.iteritems():

            competitor_id = None

            try:
                """Attempt to get the competitor""" 
                competitor_id = self.model.get_competitor_id(competitor)

                """Get or create a new bet opportunity"""
                try:
                    bet_opportunity_id = self.model.get_bet_opportunity_id(\
                        competitor_id, market_id)
                except:
                    bet_opportunity_id = self.model.insert_bet_opportunity(\
                        competitor_id, market_id)

                odds = self.model.fraction_to_decimal(odds)

                """
                Insert new entries or update the price if it has changed,
                if so update the timestamp.
                """
                if self.model.get_bet_odds(bet_opportunity_id): 

                    if not self.model.get_bet_odds(bet_opportunity_id, odds):
                        self.model.update_bet_odds(bet_opportunity_id, odds)
                else:
                    self.model.insert_bet_odds(bet_opportunity_id, odds)

            except:
                """
                The competitors that either do not exist on our side or 
                have different spellings, end up here.
                """
                pass 


"""Simple database abstraction class."""
class Db():

    def __init__(self, host="localhost", user="", passwd="", db=""):
        
        self.db=MySQLdb.connect(host=host, user=user, passwd=passwd, \
             db=db, cursorclass=MySQLdb.cursors.DictCursor)

    def fetch(self, sql, params):
        try:
            c = self.db.cursor()
            c.execute(sql, params)
            row = c.fetchone()
            c.close()
        except MySQLdb.Error, e:
           print "Error %d: %s" % (e.args[0], e.args[1])
        return row

    def save(self, sql, params):
        try:
            c = self.db.cursor()
            c.execute(sql, params)
            self.db.commit()
            lastrowid = c.lastrowid
        except MySQLdb.Error, e:
           lastrowid = None
           print "Error %d: %s" % (e.args[0], e.args[1]) 
        c.close()
        return lastrowid


