class olympicScrapper:
    url_part1 = 'https://olympics.com/en/olympic-games/'
    url_part2 = '/results'
    def __init__(self,url='',city_host='',year=0) -> None:
        if(city_host=='' and year==0):
            raise OlympicException('City_host and a year needed')
        if((city_host=='' or year==0)):
            raise OlympicException('city_host-year pair needed')
        self.url=url
        self.city_host=city_host
        self.year=year
        
class OlympicException(Exception):
    def __init__(self,message) -> None:
        self.message=message



ol=olympicScrapper(year=2020)
