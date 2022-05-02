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

        city_label=tk.Entry(root)
        city_label["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        city_label["font"] = ft
        city_label["fg"] = "#333333"
        city_label["justify"] = "center"
        city_label["text"] = "Enter City name"
        city_label.place(x=40,y=170,width=164,height=30)

        year_label=tk.Entry(root)
        year_label["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        year_label["font"] = ft
        year_label["fg"] = "#333333"
        year_label["justify"] = "center"
        year_label["text"] = "Enter Year"
        year_label.place(x=260,y=170,width=178,height=30)

        city_entry=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        city_entry["font"] = ft
        city_entry["fg"] = "#333333"
        city_entry["justify"] = "center"
        city_entry["text"] = "City"
        city_entry.place(x=80,y=140,width=70,height=25)

        year_entry=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        year_entry["font"] = ft
        year_entry["fg"] = "#333333"
        year_entry["justify"] = "center"
        year_entry["text"] = "Year"
        year_entry.place(x=310,y=140,width=70,height=25)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
