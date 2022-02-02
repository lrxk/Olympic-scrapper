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
    def createUrl(self):
        url=self.url_part1+self.city_host+'-'+self.year+self.url_part2
        return url
    
    
class OlympicException(Exception):
    def __init__(self,message) -> None:
        self.message=message



ol=olympicScrapper(year=2020)
