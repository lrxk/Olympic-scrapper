from calendar import c
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd
import re
import argparse
import matplotlib.pyplot as plt
import numpy as np


class olympicScrapper:
    url_part1 = 'https://olympics.com/en/olympic-games/'
    url_part2 = '/medals'

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description='Display command')
        parser.add_argument('-city', '--city_host',
                            help='name of the city', type=str, metavar='')
        parser.add_argument(
            '-y', '--year', help='Year of the olympic', type=int, metavar=0)
        parser.add_argument(
            '-csv', '--to_csv', help='Return result as a CSV file', type=bool, metavar=False)
        parser.add_argument(
            '-p', '--plot', help='Create a bar plot', type=bool, metavar=False)
        parser.add_argument(
            '-a', '--all', help='Get all the olympic', type=bool, metavar=False)
        parser.add_argument(
            '-as', '--allStats', help='Get the general stats of all olympics', type=bool, metavar=False)
        parser.add_argument(
            '-s', '--stats', help='Get the stats of a specified olympic', type=bool, metavar=False)
        args = parser.parse_args()
        if args.all:
            self.to_csvAllOlympic()
            return
        
        if args.city_host:
            city_host = str(args.city_host)
            self.city_host = city_host.lower()
        else:
            raise OlympicException('A city must be provided')
        if args.year:
            self.year = args.year
        else:
            raise OlympicException('A year must be provided')
        if args.city_host and args.year:
            if args.stats:
                self.__getGeneralOlympicStats() 
        if args.to_csv:
            filename = self.city_host+'-'+str(self.year)
            self.to_csv(filename=filename)
        if args.plot:
            filename = self.city_host+'-'+str(self.year)
            self.plot()

    def __createUrl(self):
        url = self.url_part1+self.city_host+'-'+str(self.year)+self.url_part2
        return url

    def __getAllOlympicsSoup(self):
        type_url = 'https://olympics.com/en/olympic-games/olympic-results'
        data = urlopen(type_url)
        type_html = data.read()
        data.close()
        page_soup = soup(type_html, 'html.parser')
        section_soup = page_soup.find('section', {
                                      'class': 'Gridstyles__GridContainer-sc-1p7u4tu-0 fLQzGx styles__TabContentNotPaginated-sc-z55d96-6 ezZekU'})
        return section_soup
    # should return the type of the olympics

    def __getAllOlympicsType(self):
        olympic_game = []
        olympic_type = []
        for node in self.__getAllOlympicsSoup().findAll('span', {}):
            olympic_type.append(''.join(node.findAll(text=True)))
        temp = []
        for i in range(len(olympic_type)):
            if olympic_type[i] != '':
                temp.append(olympic_type[i])
        olympic_type = temp
        for node in self.__getAllOlympicsSoup().findAll('p', {}):
            olympic_game.append(''.join(node.findAll(text=True)))
        olympic = {}

        for i in range(len(olympic_game)):
            olympic_host_city = re.sub(
                "\s[0-9][0-9][0-9][0-9]", " ", olympic_game[i]).strip()
            olympic_host_city = re.sub("[., ]", "-", olympic_host_city)
            olympic_host_city = olympic_host_city.lower()
            olympic_year = re.sub("[a-zA-Z-.']", "", olympic_game[i]).strip()
            data = str(olympic_host_city)+'-'+str(olympic_year)
            olympic.update({data: olympic_type[i]})
        return olympic

    def __getAllOlympics(self):
        olympic_game = []
        olympic_type = []
        for node in self.__getAllOlympicsSoup().findAll('span', {}):
            olympic_type.append(''.join(node.findAll(text=True)))
        temp = []
        for i in range(len(olympic_type)):
            if olympic_type[i] != '':
                temp.append(olympic_type[i])
        olympic_type = temp
        for node in self.__getAllOlympicsSoup().findAll('p', {}):
            olympic_game.append(''.join(node.findAll(text=True)))
        olympic = {}

        for i in range(len(olympic_game)):
            olympic_host_city = re.sub(
                "\s[0-9][0-9][0-9][0-9]", "", olympic_game[i]).strip()
            olympic_host_city = re.sub("[ ]", "-", olympic_host_city)
            olympic_host_city = re.sub("[.]", "", olympic_host_city)
            olympic_host_city = re.sub("[']", "-", olympic_host_city)
            olympic_host_city = olympic_host_city.lower()
            olympic_year = re.sub("[a-zA-Z-.']", "", olympic_game[i]).strip()
            olympic.update({olympic_host_city: olympic_year})
        return olympic

    def to_csvAllOlympic(self):
        olympics = self.__getAllOlympics()
        cities_host = list(olympics.keys())
        years = list(olympics.values())
        for i in range(len(cities_host)):
            self.city_host = cities_host[i]
            self.year = years[i]
            filename = str(cities_host[i])+'-'+str(years[i])
            self.to_csv(filename=filename)

    def olympicType(self):
        olympic = self.__getAllOlympicsType()
        user_input = self.city_host+'-'+str(self.year)
        return olympic.get(user_input)

    def __getPageSoup(self):
        olympic_url = self.__createUrl()
        olympic_data = urlopen(olympic_url)
        real_url = str(olympic_data.geturl())
        if real_url != olympic_url:
            # the result of the olympic is empty
            # the first editions were not so official
            empty_result_url = self.url_part1 + \
                self.city_host+'-'+str(self.year)+'/results'
            if real_url == empty_result_url:
                return None
            else:
                err = "Olympic does not exist:" + self.city_host+"-"+self.year
                raise OlympicException(err)
        olympic_html = olympic_data.read()
        olympic_data.close()
        page_soup = soup(olympic_html, 'html.parser')
        return page_soup

    def __getResult(self):
        result = []
        if self.__getPageSoup() == None:
            return result
        for node in self.__getPageSoup().findAll('div', {'data-cy': 'medal'}):
            result.append(''.join(node.findAll(text=True)))
        for i in range(0, len(result)):
            if result[i] == '-':
                result[i] = '0'
        return result

    def __getCountries(self):
        countries = []
        if self.__getPageSoup() == None:
            return countries
        for node in self.__getPageSoup().findAll('span', {'data-cy': 'country-name'}):
            countries.append(''.join(node.findAll(text=True)))
        return countries

    def __getMedals(self, medal_type: str):
        result = self.__getResult()
        medals = []
        if medal_type == 'gold':
            for i in range(0, len(result), 4):
                medals.append(result[i])
        elif medal_type == 'silver':
            for i in range(1, len(result), 4):
                medals.append(result[i])
        elif medal_type == 'bronze':
            for i in range(2, len(result), 4):
                medals.append(result[i])
        elif medal_type == 'total':
            for i in range(3, len(result), 4):
                medals.append(result[i])
        elif result == []:
            return medals
        else:
            raise OlympicException('Specify a medal type')
        return medals

    def to_csv(self, filename):
        filename += ".csv"
        df = self.__olympic_data()
        if self.olympicType() == 'Summer':
            filename = 'Summer_Olympics/'+filename
        else:
            filename = 'Winter_Olympics/'+filename
        df.to_csv(filename, index=False)
    def __getGeneralOlympicStats(self):
        olympic_url=self.url_part1+self.city_host+'-'+str(self.year)
        olympic_data=urlopen(olympic_url)
        olympic_html=olympic_data.read()
        olympic_data.close()
        page_soup = soup(olympic_html, 'html.parser')
        stats = []
        for node in page_soup.findAll('div', {'class': 'styles__FactItems-sc-1w4me2-2 daFleI'}):
            stats.append(''.join(node.findAll(text=True)))
        new_stats = []
        new_stats.append(stats[1].replace('Country', ''))
        new_stats.append(stats[2].replace('Athletes', ''))
        new_stats.append(stats[3].replace('Teams', ''))
        new_stats.append(stats[4].replace('Events', ''))
        print(self.city_host+" "+str(self.year),end="\n")
        print("Country :"+new_stats[0],end="\n")
        print("Number of Athletes :"+new_stats[1],end="\n")
        print("Number of teams :"+new_stats[2],end="\n")
        print("Number of events :"+new_stats[3],end="\n")
    def __getGeneralAllOlympicStats(self):
        olympic = self.__getAllOlympics()
        cities_host = list(olympic.keys)
        years = list(olympic.values)
        olympic_type = list(self.__getAllOlympicsType().values)
        olympic_stats={}
        for i in range(len(cities_host)):
            olympic_url=self.url_part1+cities_host[i]+'-'+str(years[i])
            olympic_data = urlopen(olympic_url)
            olympic_html = olympic_data.read()
            olympic_data.close()
            page_soup = soup(olympic_html, 'html.parser')
            stats = []
            for node in page_soup.findAll('div', {'class': 'styles__FactItems-sc-1w4me2-2 daFleI'}):
                stats.append(''.join(node.findAll(text=True)))
            new_stats = []
            new_stats.append(stats[1].replace('Country', ''))
            new_stats.append(stats[2].replace('Athletes', ''))
            new_stats.append(stats[3].replace('Teams', ''))
            new_stats.append(stats[4].replace('Events', ''))
            key=cities_host[i]+'-'+years[i]
            olympic_stats.update({key:new_stats})
        country=[]
        athletes_nb=[]
        team_nb=[]
        nb_event=[]
        for i in range(len(olympic_stats)):
            key=cities_host[i]+'-'+years[i]
            country.append(olympic_stats.get(key)[1])
            athletes_nb.append(olympic_stats.get(key)[2])
            team_nb.append(olympic_stats.get(key)[3])
            nb_event.append(olympic_stats.get(key)[4])
        data={
            "city_host":cities_host,
            "year":years,
            "Type":olympic_type,
            "number of athletes":athletes_nb,
            "number of team":team_nb,
            "number of event":nb_event
        }
        df=pd.DataFrame(data)
        return df

    def __olympic_data(self) -> pd.DataFrame:

        data = {
            'countries': self.__getCountries(),
            'gold_medals': self.__getMedals(medal_type='gold'),
            'silver_medals': self.__getMedals(medal_type='silver'),
            'bronze_medals': self.__getMedals(medal_type='bronze'),
            'total_medals': self.__getMedals(medal_type='total'),
        }
        df = pd.DataFrame(data)
        return df
    # Not working as pleased

    def plot(self):
        # TODO

        df = self.__olympic_data()
        df = df.astype({'gold_medals': 'int32', 'silver_medals': 'int32',
                       'bronze_medals': 'int32', 'total_medals': 'int32'})

        # print(df.dtypes)

        df = df.query('gold_medals > 10')
        df = df.query('silver_medals > 10')
        df = df.query('bronze_medals > 10')
        df = df.query('total_medals > 10')
        countries = df.countries.array
        gold_medals = df.gold_medals.array
        silver_medals = df.silver_medals.array
        bronze_medals = df.bronze_medals.array
        total_medals = df.total_medals.array
        x = np.arange(len(countries))
        width = 0.35
        fig, ax = plt.subplots()
        # plt.figure(figsize=(20, 20), dpi=80)
        rect1 = ax.barh(x-width/2, gold_medals, width)
        rect2 = ax.barh(x+width/2, silver_medals, width)
        rect3 = ax.barh(x, bronze_medals, width)
        ax.bar_label(rect1, countries)
        ax.bar_label(rect2, countries)
        ax.bar_label(rect3, countries)
        fig.set_size_inches(18.5, 10.5)
        # fig.tight_layout()
        plt.show()

# Exception class nothing special send a specific message about the error


class OlympicException(Exception):
    def __init__(self, message) -> None:
        self.message = message


if __name__ == '__main__':
    ol = olympicScrapper()
