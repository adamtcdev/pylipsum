from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import requests
import xml.etree.ElementTree as ET

root = Tk()
root.title('Lorem Ipsum')
root.geometry('420x420')

def get_lipsum(amount, what, start_with):
    query_str = f"amount={amount}&what={what}&start={start_with}"

    try:
        resp = requests.get("http://www.lipsum.com/feed/xml?" + query_str)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)

        lipsum = root.find(".//lipsum").text.strip()
        generated = root.find(".//generated").text.strip()

        return lipsum, generated

    except requests.RequestException as e:
        print("Error: ", e)
        return None, None

def clipboard():
    root.clipboard_append(ltext.get("1.0", "end"))

def generate_lipsum():
    amount = amount_var.get()
    what = what_var.get()
    start_with = start_var.get()
    try:
        lipsum, generated = get_lipsum(amount, what, start_with)
        if not lipsum:
            raise Exception("No lipsum found in the response.")
        ltext.delete(1.0, END)
        ltext.insert(END, lipsum)
        gedlabel.config(text=generated)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate lipsum: {e}")

m1, m2 = Frame(), Frame()
m1.pack(side='top', fill=X)
m2.pack(side='top', fill=X)

amount_var = IntVar(value=5)
what_var = StringVar(value='paras')
start_var = StringVar(value='no')

Label(m1, text='Generate:').pack(side=LEFT, padx=5)

abutton = Entry(m1, textvariable=amount_var, width=5)
abutton.pack(side=LEFT, padx=5)

wcbox = Combobox(m1, textvariable=what_var, values=["paras", "words", "bytes", "lists"])
wcbox.pack(side=LEFT, padx=5)

gbutton = Button(m1, text='Generate', command=generate_lipsum)
gbutton.pack(side=RIGHT, padx=5, pady=5)

scbutton = Checkbutton(m2, variable=start_var, onvalue="yes", offvalue="no")
scbutton.pack(side=LEFT, padx=5)

Label(m2, text="Start with 'Lorem ipsum dolor sit amet...'").pack(side=LEFT)

gbutton = Button(m2, text='Copy', command=clipboard)
gbutton.pack(side=RIGHT, padx=5)

gedlabel = Label(text='')
gedlabel.pack(side=BOTTOM, fill=X, padx=5)

ltext = Text(wrap=WORD)
ltext.pack(fill=BOTH, expand=1, padx=5, pady=5)

root.mainloop()
