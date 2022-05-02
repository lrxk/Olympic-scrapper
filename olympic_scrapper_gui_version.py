import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLineEdit_310=tk.Entry(root)
        GLineEdit_310["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_310["font"] = ft
        GLineEdit_310["fg"] = "#333333"
        GLineEdit_310["justify"] = "center"
        GLineEdit_310["text"] = "Enter City name"
        GLineEdit_310.place(x=40,y=170,width=164,height=30)

        GLineEdit_763=tk.Entry(root)
        GLineEdit_763["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_763["font"] = ft
        GLineEdit_763["fg"] = "#333333"
        GLineEdit_763["justify"] = "center"
        GLineEdit_763["text"] = "Enter Year"
        GLineEdit_763.place(x=260,y=170,width=178,height=30)

        GLabel_71=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_71["font"] = ft
        GLabel_71["fg"] = "#333333"
        GLabel_71["justify"] = "center"
        GLabel_71["text"] = "City"
        GLabel_71.place(x=80,y=140,width=70,height=25)

        GLabel_661=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_661["font"] = ft
        GLabel_661["fg"] = "#333333"
        GLabel_661["justify"] = "center"
        GLabel_661["text"] = "Year"
        GLabel_661.place(x=310,y=140,width=70,height=25)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
