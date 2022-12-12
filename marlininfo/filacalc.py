#!/usr/bin/env python
from __future__ import print_function
import os
import shutil
import traceback
import math
import sys

if sys.version_info.major >= 3:
    # from tkinter import *
    import tkinter as tk
    # from io import StringIO
else:
    # python 2
    # from Tkinter import *
    import Tkinter as tk
    # from StringIO import StringIO



class FilaCalcTk(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("FilaCalc")
        self.minsize(300, 200)
        # ^ Prevent weird tkinter behavior creating a 1px wide window
        #   only as high as the title bar when fill=tk.BOTH, expand=True
        #   and there are no widgets.
        new_row_i = 0
        master = self

        gPerCCLabel = tk.Label(master, text="g/cc")
        gPerCCLabel.grid(row=new_row_i, column=0)
        self.gPerCCE = tk.Entry(master)
        self.gPerCCE.grid(row=new_row_i, column=1)
        self.gPerCCE.delete(0, tk.END)
        self.gPerCCE.insert(0, "1.27")
        new_row_i += 1

        diameterLabel = tk.Label(master, text="diameter (mm)")
        diameterLabel.grid(row=new_row_i, column=0)
        self.diameterE = tk.Entry(master)
        self.diameterE.grid(row=new_row_i, column=1)
        self.diameterE.delete(0, tk.END)
        self.diameterE.insert(0, "1.75")
        new_row_i += 1

        costPerKgLabel = tk.Label(master, text="cost per kg")
        costPerKgLabel.grid(row=new_row_i, column=0)
        self.costPerKgE = tk.Entry(master)
        self.costPerKgE.grid(row=new_row_i, column=1)
        self.costPerKgE.delete(0, tk.END)
        self.costPerKgE.insert(0, "40")
        new_row_i += 1

        kgB = tk.Button(master, text="Calculate Kg", command=self.show_kg_click)
        # kgB.pack()  # can't pack in grid
        kgB.grid(row=new_row_i, column=0)
        self.kgE = tk.Entry(master)
        self.kgE.grid(row=new_row_i, column=1)
        new_row_i += 1

        lengthB = tk.Button(master, text="Calculate m", command=self.show_length_click)
        lengthB.grid(row=new_row_i, column=0)
        self.lengthE = tk.Entry(master)
        self.lengthE.grid(row=new_row_i, column=1)
        self.lengthE.delete(0, tk.END)
        self.lengthE.insert(0, "120")
        new_row_i += 1

        self.outputE = tk.Entry(master)
        self.outputE.grid(row=new_row_i, column=0, columnspan=2, sticky=tk.W+tk.E)

    def show_message(self, msg, console_enable=False):
        self.outputE.delete(0, tk.END)
        self.outputE.insert(0, msg)
        if console_enable:
            print(msg)


    def get_float(self, s, name, unit):
        s = s.strip()
        r = None
        if len(s) < 1:
            msg = "You must specify"
            if name is not None:
                msg += " {}".format(name)
            else:
                msg += " a value"
            if unit is not None:
                msg += " in {}".format(unit)
            msg += "."
            self.show_message(msg)
            return None
        try:
            r = float(s)
        except ValueError:
            msg = "You must specify a length in meters (m). '{}'".format(s)
            if unit is not None:
                msg += " {}".format(unit)
            msg += " is not a number.".format(s)
            self.show_message(msg)
            return None
        return r


    def show_kg_click(self):
        self.show_message("")
        length = self.get_float(self.lengthE.get(), "length", "m")
        if length is None:
            return
        diameter = self.get_float(self.diameterE.get(), "diameter", "mm")
        if diameter is None:
            return
        gPerCC = self.get_float(self.gPerCCE.get(), "specific gravity", "g/cc")
        if gPerCC is None:
            return

        d_cm = diameter / 10  # mm to cm
        l_cm = length * 100  # m to cm
        r_cm = d_cm / 2
        totalCC = math.pi * r_cm**2 * l_cm  # volume formula
        g = totalCC * gPerCC
        kg = round(g / 1000, 3)
        self.kgE.delete(0, tk.END)
        self.kgE.insert(0, str(kg))
        self.show_message(
            "Total volume in cc (cm^3): {}".format(
                round(totalCC, 3)
            )
        )

    def show_length_click(self):
        self.show_message("")
        weightS = self.kgE.get().strip()
        if len(weightS) < 1:
            self.show_message("You must specify Kg.")
            return
        diameter = self.get_float(self.diameterE.get(), "diameter", "mm")
        if diameter is None:
            return
        gPerCC = self.get_float(self.gPerCCE.get(), "specific gravity", "g/cc")
        if gPerCC is None:
            return
        self.lengthE.delete(0, tk.END)
        self.lengthE.insert(0, "not yet implemented")


def main():
    app = FilaCalcTk()
    app.mainloop()  # tk.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
