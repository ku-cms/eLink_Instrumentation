#!/usr/bin/python3
import shelve

cable = shelve.open("cable.txt")


cable["100"] = ["35", "1", "34G"]
cable["101"] = ["35", "1", "34G"]
cable["102"] = ["80", "1", "34G"]
cable["103"] = ["80", "1", "34G"]
cable["104"] = ["100", "1", "34G"]
cable["105"] = ["100", "1", "34G"]
cable["106"] = ["160", "1", "34G"]
cable["107"] = ["160", "1", "34G"]
cable["108"] = ["160", "1", "34G"]
cable["109"] = ["160", "1", "34G"]
cable["111"] = ["180", "1", "34G"]
cable["113"] = ["200", "1", "34G"]
cable["136"] = ["35", "1", "36G"]
cable["137"] = ["35", "1", "36G"]
cable["138"] = ["35", "1", "36G"]
cable["139"] = ["80", "1", "36G"]
cable["140"] = ["80", "1", "36G"]
cable["143"] = ["80", "1", "36G"]
cable["144"] = ["100", "1", "36G"]
cable["145"] = ["100", "1", "36G"]
cable["148"] = ["100", "1", "36G"]
cable["149"] = ["140", "1", "36G"]
cable["150"] = ["140", "1", "36G"]
cable["151"] = ["140", "1", "36G"]
cable["153"] = ["140", "1", "36G"]
cable["154"] = ["160", "1", "36G"]
cable["155"] = ["160", "1", "36G"]
cable["156"] = ["160", "1", "36G"]
cable["157"] = ["160", "1", "36G"]
cable["159"] = ["160", "1", "36G"]
cable["160"] = ["160", "1", "36G"]
cable["161"] = ["160", "1", "36G"]
cable["162"] = ["160", "1", "36G"]
cable["163"] = ["160", "1", "36G"]
cable["164"] = ["160", "1", "36G"]
cable["165"] = ["160", "1", "36G"]
cable["167"] = ["180", "1", "36G"]
cable["169"] = ["180", "1", "36G"]
cable["170"] = ["180", "1", "36G"]
cable["172"] = ["180", "1", "36G"]
cable["173"] = ["180", "1", "36G"]
cable["174"] = ["180", "1", "36G"]
cable["175"] = ["180", "1", "36G"]
cable["176"] = ["180", "1", "36G"]
cable["177"] = ["180", "1", "36G"]
cable["178"] = ["200", "1", "36G"]
cable["179"] = ["200", "1", "36G"]
cable["179"] = ["200", "1", "36G"]
cable["180"] = ["200", "1", "36G"]
cable["182"] = ["200", "1", "36G"]
cable["183"] = ["35", "2", "36G"]
cable["184"] = ["35", "2", "36G"]
cable["185"] = ["35", "2", "36G"]
cable["186"] = ["35", "2", "36G"]
cable["187"] = ["80", "2", "36G"]
cable["188"] = ["80", "2", "36G"]
cable["189"] = ["80", "2", "36G"]
cable["190"] = ["80", "2", "36G"]
cable["191"] = ["100", "2", "36G"]
cable["192"] = ["100", "2", "36G"]
cable["193"] = ["100", "2", "36G"]
cable["194"] = ["100", "2", "36G"]
cable["195"] = ["160", "2", "36G"]
cable["196"] = ["160", "2", "36G"]
cable["197"] = ["160", "2", "36G"]
cable["198"] = ["160", "2", "36G"]
cable["200"] = ["200", "2", "36G"]
cable["201"] = ["200", "2", "36G"]
cable["202"] = ["200", "2", "36G"]



from tkinter import *
from tkinter import ttk


class Cable_Info:

    def __init__(self, root):

        root.title("Add New Cable")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.number = StringVar()
        self.gauge = StringVar()
        self.type = StringVar()
        self.length = StringVar()

        number_entry = ttk.Entry(mainframe, width=7, textvariable=self.number)
        length_entry = ttk.Entry(mainframe, width=7, textvariable=self.length)
        type_entry = ttk.Entry(mainframe, width=7, textvariable=self.type)
        gauge_entry = ttk.Entry(mainframe, width=7, textvariable=self.gauge)

        number_entry.grid(column=2, row=1, sticky=(W, E))
        length_entry.grid(column=2, row=2, sticky=(W, E))
        type_entry.grid(column=2, row=3, sticky=(W, E))
        gauge_entry.grid(column=2, row=4, sticky=(W, E))

        ttk.Button(mainframe, text="Add", command=self.add).grid(column=1, row=5, columnspan=2, sticky=W+E)

        ttk.Label(mainframe, text="Cable Number: ").grid(column=1, row=1, sticky=(W, E))
        ttk.Label(mainframe, text="Cable Length: ").grid(column=1, row=2, sticky=(W, E))
        ttk.Label(mainframe, text="Cable Type: ").grid(column=1, row=3, sticky=(W, E))
        ttk.Label(mainframe, text="Gauge: ").grid(column=1, row=4, sticky=(W, E))

        number_entry.focus()
        length_entry.focus()
        type_entry.focus()
        gauge_entry.focus()

        root.bind("<Return>", self.add)

    def add(self, *args):
        cable.update({self.number.get(): [self.length.get(), self.type.get(), self.gauge.get()]})


root = Tk()
Cable_Info(root)
root.mainloop()

cable.close()


