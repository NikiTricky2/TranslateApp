import json
from tkinter import *
import tkinter.font as tkFont
from urllib import request, parse
from tkinter.messagebox import showinfo

languages_f = open("./languages.json", "r")
languages = json.loads(languages_f.read())
languages_f.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Translate text")
        icon_photo = PhotoImage(file = "app_icon.png")
        self.root.iconphoto(False, icon_photo)
        width=510
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.ft = tkFont.Font(family='Sans-Serif',size=10)

        self.app_title=Label(root)
        self.app_title["font"] = tkFont.Font(family='Sans-Serif',size=38)
        self.app_title["fg"] = "#000000"
        self.app_title["justify"] = "left"
        self.app_title["text"] = "Translate text"
        self.app_title.place(x=10,y=10,width=320,height=44)

        self.translate_from_entry=Entry(root)
        self.translate_from_entry["bg"] = "#ffffff"
        self.translate_from_entry["borderwidth"] = "4px"
        self.translate_from_entry["font"] = self.ft
        self.translate_from_entry["fg"] = "#000000"
        self.translate_from_entry["justify"] = "left"
        self.translate_from_entry.place(x=10,y=100,width=179,height=30)

        self.translate_from_label=Label(root)
        self.translate_from_label["font"] = self.ft
        self.translate_from_label["fg"] = "#000000"
        self.translate_from_label["justify"] = "left"
        self.translate_from_label["text"] = "Translate from:"
        self.translate_from_label.place(x=10,y=70,width=98,height=30)

        self.translate_to_entry=Entry(root)
        self.translate_to_entry["bg"] = "#ffffff"
        self.translate_to_entry["borderwidth"] = "4px"
        self.translate_to_entry["font"] = self.ft
        self.translate_to_entry["fg"] = "#000000"
        self.translate_to_entry["justify"] = "left"
        self.translate_to_entry.place(x=240,y=100,width=175,height=30)

        self.translate_to_label=Label(root)
        self.translate_to_label["font"] = self.ft
        self.translate_to_label["fg"] = "#000000"
        self.translate_to_label["justify"] = "left"
        self.translate_to_label["text"] = "Translate to:"
        self.translate_to_label.place(x=240,y=70,width=70,height=25)

        self.translate_text=Text(root)
        self.translate_text["bg"] = "#ffffff"
        self.translate_text["borderwidth"] = "4px"
        self.translate_text["font"] = self.ft
        self.translate_text["fg"] = "#000000"
        self.translate_text.place(x=10,y=160,width=182,height=294)

        self.translated_text=Text(root)
        self.translated_text["bg"] = "#ffffff"
        self.translated_text["borderwidth"] = "4px"
        self.translated_text["font"] = self.ft
        self.translated_text["fg"] = "#000000"
        self.translated_text["state"] = "disabled"
        self.translated_text.place(x=240,y=160,width=173,height=295)
        
        self.translate_button=Button(root)
        self.translate_button["bg"] = "#efefef"
        self.translate_button["font"] = self.ft
        self.translate_button["fg"] = "#000000"
        self.translate_button["justify"] = "center"
        self.translate_button["text"] = "Translate!"
        self.translate_button.place(x=430,y=100,width=67,height=30)
        self.translate_button["command"] = self.translate_button_command
    
    def translate_button_command(self):
        if self.translate_from_entry.get() not in languages.keys():
            showinfo("Invalid language", f"{self.translate_from_entry.get()} is not a valid language")
            return
        if self.translate_to_entry.get() not in languages.keys():
            showinfo("Invalid language", f"{self.translate_to_entry.get()} is not a valid language")
            return

        language_from = languages[self.translate_from_entry.get()]
        language_to = languages[self.translate_to_entry.get()]
        translate_str = self.translate_text.get("1.0", END)

        try:
            json_output = request.urlopen(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={language_from}&tl={language_to}&dt=t&q={parse.quote_plus(translate_str)}").read().decode("utf8")
        except:
            showinfo("An error occurred", "An error occurred. Please try again later.")
        
        translated_text = ""
        
        for sentence in json.loads(json_output)[0]:
            translated_text += sentence[0]
            
        self.translated_text["state"] = "normal"
        self.translated_text.delete('1.0', END)
        self.translated_text.insert("1.0", translated_text)
        self.translated_text["state"] = "disabled"

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
