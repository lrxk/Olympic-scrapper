from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

class olympicScrapper:
    url_part1 = 'https://olympics.com/en/olympic-games/'
    url_part2 = '/results'
    def __init__(self,city_host='',year=0) -> None:
        if(city_host=='' and year==0):
            raise OlympicException('City_host and a year needed')
        if((city_host=='' or year==0)):
            raise OlympicException('city_host-year pair needed')
        if not isinstance(city_host,str):
            raise OlympicException('city_host must be a string')
        if not isinstance(year,int):
            raise OlympicException('Year must be an int')
        self.city_host=city_host.lower()
        self.year=year
    def __createUrl(self):
        url=self.url_part1+self.city_host+'-'+self.year+self.url_part2
        return url
    def __getPageSoup(self):
        olympic_url=self.__createUrl()
        olympic_data = urlopen(olympic_url)
        olympic_html = olympic_data.read()
        olympic_data.close()
        page_soup=soup(olympic_html,'html.parser')
        return page_soup
    def __getResult(self):
        result=[]
        for node in self.__getPageSoup().findAll('div',{'data-cy':'medal'}):
            result.append(''.join(node.findAll(text=True)))
        for i in range(0,len(result)):
            if result[i]=='-':
                result[i]='0'
        return result    
    def getCountries(self):
        countries=[]
        for node in self.getSoup().findAll('span',{'data-cy':'country-name'}):
            countries.append(''.join(node.findAll(text=True)))
        return countries
    def getGoldMedals(self):
        gold_medals=[]
        result=self.getResult()
        for i in range(0,len(result),4):
            gold_medals.append(result[i])
        return gold_medals
class OlympicException(Exception):
    def __init__(self,message) -> None:
        self.message=message



ol=olympicScrapper(year=2020)
