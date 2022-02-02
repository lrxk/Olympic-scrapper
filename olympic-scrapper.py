class olympicScrapper:
    def __init__(self,*args,**kwargs) -> None:
        self.url=kwargs.get('url')
        self.city_host=str(kwargs.get('city_host')).lower()
        self.year=int(kwargs.get('year'))


