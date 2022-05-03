from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd
import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("Olympic Scrapper")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.city_entry=tk.Entry(root)
        self.city_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.city_entry["font"] = ft
        self.city_entry["fg"] = "#333333"
        self.city_entry["justify"] = "center"
        self.city_entry["text"] = "Enter City name"
        self.city_entry.place(x=40,y=170,width=164,height=30)

        self.year_entry=tk.Entry(root)
        self.year_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.year_entry["font"] = ft
        self.year_entry["fg"] = "#333333"
        self.year_entry["justify"] = "center"
        self.year_entry["text"] = "Enter Year"
        self.year_entry.place(x=260,y=170,width=178,height=30)

        city_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        city_label["font"] = ft
        city_label["fg"] = "#333333"
        city_label["justify"] = "center"
        city_label["text"] = "City"
        city_label.place(x=80,y=140,width=70,height=25)

        #information label
        self.info_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.info_label["font"] = ft
        self.info_label["fg"] = "#333333"
        self.info_label["justify"] = "center"
        self.info_label["text"] = "SEX"
        self.info_label.place(x=210,y=350,width=70,height=25)


        year_label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        year_label["font"] = ft
        year_label["fg"] = "#333333"
        year_label["justify"] = "center"
        year_label["text"] = "Year"
        year_label.place(x=310,y=140,width=70,height=25)

        send_button=tk.Button(root)
        send_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        send_button["font"] = ft
        send_button["fg"] = "#000000"
        send_button["justify"] = "center"
        send_button["text"] = "Send"
        send_button.place(x=210,y=250,width=70,height=25)
        send_button["command"] = self.send_button_command

    def send_button_command(self):
        
        print("command")
class OlympicException(Exception):
    def __init__(self, message) -> None:
        self.message = message
class OlympicScrapper:
    url_part1 = 'https://olympics.com/en/olympic-games/'
    url_part2 = '/medals'
    def __init__(self,city_host,year) -> None:
        self.city_host=city_host
        self.year=year
        self.page_soup=self.getPageSoup()
        self.result=self.result
        pass
    def createUrl(self):
        url = self.url_part1+self.city_host+'-'+str(self.year)+self.url_part2
        return url
    
    # get the soup of a page
    def getPageSoup(self):
        olympic_url = self.createUrl()
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
    def getResult(self):
        result = []
        for node in self.page_soup.findAll('div', {'data-cy': 'medal'}):
            result.append(''.join(node.findAll(text=True)))
        for i in range(0, len(result)):
            if result[i] == '-':
                result[i] = '0'
        return result
    def getCountries(self):
        countries = []
        for node in self.page_soup.findAll('span', {'data-cy': 'country-name'}):
            countries.append(''.join(node.findAll(text=True)))
        return countries
    # get medals data based on the type
    def getMedals(self,medal_type:str):
        if medal_type=="Gold":
            gold_medals = []
            for i in range(0, len(self.result), 4):
                gold_medals.append(self.result[i])
            return gold_medals
            
        elif medal_type=="Silver":
            silver_medals = []
            for i in range(1, len(self.result), 4):
                silver_medals.append(self.result[i])
            return silver_medals
            
        elif medal_type=="Bronze":
            bronze_medals = []
            for i in range(2, len(self.result), 4):
                bronze_medals.append(self.result[i])
            return bronze_medals

        elif medal_type=="Total":
            total_medals = []
            for i in range(3, len(self.result), 4):
                total_medals.append(self.result[i])
            return total_medals
        else:
            raise OlympicException("Medal type not recognized")
        
    def olympic_data(self) -> pd.DataFrame:

        data = {
            'countries': self.getCountries(),
            'gold_medals': self.getMedals(medal_type='gold'),
            'silver_medals': self.getMedals(medal_type='silver'),
            'bronze_medals': self.getMedals(medal_type='bronze'),
            'total_medals': self.getMedals(medal_type='total'),
        }
        df = pd.DataFrame(data)
        return df
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
