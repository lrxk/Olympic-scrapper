from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from numpy import empty
import pandas as pd
import re

class olympicScrapper:
    url_part1 = 'https://olympics.com/en/olympic-games/'
    url_part2 = '/medals'
    
    def __init__(self, city_host='', year=0) -> None:
        if(city_host == '' and year == 0):
            raise OlympicException('City_host and a year needed')
        if((city_host == '' or year == 0)):
            raise OlympicException('city_host-year pair needed')
        if not isinstance(city_host, str):
            raise OlympicException('city_host must be a string')
        if not isinstance(year, int):
            raise OlympicException('Year must be an int')
        self.city_host = city_host.lower()
        self.year = year

    def __createUrl(self):
        url = self.url_part1+self.city_host+'-'+str(self.year)+self.url_part2
        return url
    def __getAllOlympicsSoup(self):
        type_url='https://olympics.com/en/olympic-games/olympic-results'
        data=urlopen(type_url)
        type_html=data.read()
        data.close()
        page_soup=soup(type_html,'html.parser')
        section_soup=page_soup.find('section',{'class':'Gridstyles__GridContainer-sc-1p7u4tu-0 fLQzGx styles__TabContentNotPaginated-sc-z55d96-6 ezZekU'})
        return section_soup
    #should return the type of the olympics
    def olympicType(self):
        olympic_game=[]
        olympic_type=[]
        for node in self.__getAllOlympicsSoup().findAll('span',{}):
            if node !='':
                olympic_type.append(''.join(node.findAll(text=True)))
        for node in self.__getAllOlympicsSoup.findAll('p',{}):
            olympic_game.append(''.join(node.findAll(text=True))) 
        olympic={}
        
        for i in range(len(olympic_game)):
            olympic_host_city=re.sub("\s[0-9][0-9][0-9][0-9]"," ",olympic_game[i]).strip()
            olympic_host_city=olympic_host_city.lower()
            olympic_year=re.sub("[a-zA-Z-.']","",olympic_game[i]).strip()
            data=str(olympic_host_city)+'-'+str(olympic_year)
            olympic.update({data:olympic_type[i]})
        user_input=self.city_host+'-'+str(self.year)
        return olympic.get(user_input)
    def __getPageSoup(self):
        olympic_url = self.__createUrl()
        olympic_data = urlopen(olympic_url)
        olympic_html = olympic_data.read()
        olympic_data.close()
        page_soup = soup(olympic_html, 'html.parser')
        return page_soup
    # repeated code , find a way to simplify it

    def __getResult(self):
        result = []
        for node in self.__getPageSoup().findAll('div', {'data-cy': 'medal'}):
            result.append(''.join(node.findAll(text=True)))
        for i in range(0, len(result)):
            if result[i] == '-':
                result[i] = '0'
        return result

    def __getCountries(self):
        countries = []
        for node in self.__getPageSoup().findAll('span', {'data-cy': 'country-name'}):
            countries.append(''.join(node.findAll(text=True)))
        return countries

    def __getGoldMedals(self):
        gold_medals = []
        result = self.__getResult()
        for i in range(0, len(result), 4):
            gold_medals.append(result[i])
        return gold_medals

    def __getSilverMedals(self):
        silver_medals = []
        result = self.__getResult()
        for i in range(1, len(result), 4):
            silver_medals.append(result[i])
        return silver_medals

    def __getBronzeMedals(self):
        bronze_medals = []
        result = self.__getResult()
        for i in range(2, len(result), 4):
            bronze_medals.append(result[i])
        return bronze_medals

    def __getTotalMedals(self):
        total_medals = []
        result = self.__getResult()
        for i in range(3, len(result), 4):
            total_medals.append(result[i])
        return total_medals

    def to_csv(self, filename):
        filename+=".csv"
        data = {
            'Country': self.__getCountries(),
            'gold_medals': self.__getGoldMedals(),
            'silver_medals': self.__getSilverMedals(),
            'bronze_medals': self.__getBronzeMedals(),
            'total_medals': self.__getTotalMedals()
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
class OlympicException(Exception):
    def __init__(self, message) -> None:
        self.message = message
ol = olympicScrapper(city_host='Tokyo',year=2020)
ol.to_csv("tokyo-2020")
