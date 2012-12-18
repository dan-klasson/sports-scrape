from core import BasePage
from models import Model

"""Base class for all page objects that scrape from betvictor.com"""
class BetVictor(object):

    def scrape(self, content):

        competitors = []
        odds = []

        for item in content:
            
            try: 
                odds.append(item.a.string)
            except: 
                pass

            try:
                if item.find(text=True) != "\n":
                    competitors.append(item.find(text=True))
            except:
                pass

        if len(odds) != len(competitors):
            raise Exception("Scrape mismatch. Please manually review the \
                    scraping script as the source might have been changed")

        return dict(zip(competitors, odds))


class GrandPrix(BetVictor, BasePage):

    market_type = "Grand Prix"
    source = open("pages/f1.html")
 
    def scrape(self):
        content = self.soup.find_all('td')
        return super(GrandPrix, self).scrape(content)

class Constructors(BetVictor, BasePage):

    market_type = "Constructors Championship"
    source = open("pages/f2.html")

    def scrape(self):
        table = self.soup.find_all('table')[1]
        cols = table.find_all('td')

        return super(Constructors, self).scrape(cols)

class Drivers(BetVictor, BasePage):

    market_type = "Drivers Championship"
    source = open("pages/f2.html")

    def scrape(self):

        table = self.soup.find('table')
        cols = table.find_all('td')

        return super(Drivers, self).scrape(cols)


