class olympicScrapper:
    url_part1 = 'https://olympics.com/en/olympic-games/'
    url_part2 = '/results'
    def __init__(self,*args,**kwargs) -> None:
        if args.count() == 0:
            raise OlympicException('No parameters given')            
        self.url=kwargs.get('url')
        self.city_host=str(kwargs.get('city_host')).lower()
        self.year=int(kwargs.get('year'))


class OlympicException(Exception):
    def __init__(self,message) -> None:
        self.message=message



