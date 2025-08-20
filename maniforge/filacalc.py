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
        # self.columnconfigure(tuple(range(60)), weight=1)
        # self.rowconfigure(tuple(range(30)), weight=1)
        tk.Grid.columnconfigure(master, 1, weight=1)

        gPerCCLabel = tk.Label(master, text="g/cc")
        gPerCCLabel.grid(row=new_row_i, column=0, sticky=tk.W+tk.E)
        self.gPerCCE = tk.Entry(master)
        self.gPerCCE.grid(row=new_row_i, column=1, sticky=tk.W+tk.E)
        self.gPerCCE.delete(0, tk.END)
        self.gPerCCE.insert(0, "1.27")
        new_row_i += 1

        diameterLabel = tk.Label(master, text="diameter (mm)")
        diameterLabel.grid(row=new_row_i, column=0, sticky=tk.W+tk.E)
        self.diameterE = tk.Entry(master)
        self.diameterE.grid(row=new_row_i, column=1, sticky=tk.W+tk.E)
        self.diameterE.delete(0, tk.END)
        self.diameterE.insert(0, "1.75")
        new_row_i += 1

        costPerKgLabel = tk.Label(master, text="cost per kg")
        costPerKgLabel.grid(row=new_row_i, column=0, sticky=tk.W+tk.E)
        self.costPerKgE = tk.Entry(master)
        self.costPerKgE.grid(row=new_row_i, column=1, sticky=tk.W+tk.E)
        self.costPerKgE.delete(0, tk.END)
        self.costPerKgE.insert(0, "40")
        new_row_i += 1

        kgB = tk.Button(master, text="Calculate Kg", command=self.calculate_kg_click)
        # kgB.pack()  # can't pack in grid
        kgB.grid(row=new_row_i, column=0, sticky=tk.W+tk.E)
        self.kgE = tk.Entry(master)
        self.kgE.grid(row=new_row_i, column=1, sticky=tk.W+tk.E)
        new_row_i += 1

        lengthB = tk.Button(master, text="Calculate m", command=self.calculate_length_click)
        lengthB.grid(row=new_row_i, column=0, sticky=tk.W+tk.E)
        self.lengthE = tk.Entry(master)
        self.lengthE.grid(row=new_row_i, column=1, sticky=tk.W+tk.E)
        self.lengthE.delete(0, tk.END)
        self.lengthE.insert(0, "120")
        new_row_i += 1

        self.outputE = tk.Text(master, height=2)
        grid = self.outputE.grid(row=new_row_i, column=0,
                                 columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk.Grid.rowconfigure(master, new_row_i, weight=1)

    def show_message(self, msg, console_enable=False):
        type_name = type(self.outputE).__name__
        if type_name == "Entry":
            self.outputE.delete(0, tk.END)
            self.outputE.insert(0, msg)
        elif type_name == "Text":
            self.outputE.delete(1.0, tk.END)
            self.outputE.insert(1.0, msg)
        else:
            raise NotImplementedError(type_name)
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

    def calculate_kg_click(self):
        '''
        Calculate weight from length, diameter, and density.
        '''
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
        kg = g / 1000
        # kg = round(kg, 3)
        self.kgE.delete(0, tk.END)
        self.kgE.insert(0, str(kg))
        msg = (
            "Total volume in cc (cm\u00B3): {}".format(
                round(totalCC, 3)
            )
        )
        costPerKgS = self.costPerKgE.get().strip()
        if len(costPerKgS) > 0:
            costPerKg = self.get_float(costPerKgS, "costPerKg", "$")
            totalCost = costPerKg * kg
            cost_line = "{}m Estimated Cost: ${}".format(
                length,
                math.ceil(totalCost*100) / 100,
                # ^ keep your own fractions; but not others', penny thief!
            )
            msg += "\n" + cost_line
        self.show_message(msg)

    def calculate_length_click(self):
        '''
        Calculate length from volume.
        '''
        self.show_message("")
        kgS = self.kgE.get().strip()
        if len(kgS) < 1:
            self.show_message("You must specify Kg.")
            return
        diameter = self.get_float(self.diameterE.get(), "diameter", "mm")
        if diameter is None:
            return
        gPerCC = self.get_float(self.gPerCCE.get(), "specific gravity", "g/cc")
        if gPerCC is None:
            return
        kg = float(kgS)
        g = kg * 1000.0
        # g = round(g, 3)
        length = ""
        d_cm = diameter / 10  # mm to cm
        r_cm = d_cm / 2

        # Calculate volume from weight and density (g/cc)
        totalCC = g / gPerCC

        # Calculate length from volume
        l_cm = totalCC / (math.pi * r_cm**2)

        length = l_cm / 100  # cm to m

        self.lengthE.delete(0, tk.END)
        self.lengthE.insert(0, length)
        volume_line = "Total volume in cc (cm\u00B3): {}".format(
            round(totalCC, 3)
        )
        msg = volume_line
        costPerKgS = self.costPerKgE.get().strip()
        if len(costPerKgS) > 0:
            costPerKg = self.get_float(costPerKgS, "costPerKg", "$")
            totalCost = costPerKg * kg
            cost_line = "{}m Estimated Cost: ${}".format(
                length,
                math.ceil(totalCost*100) / 100,
                # ^ keep your own fractions; but not others', penny thief!
            )
            msg += "\n" + cost_line
        self.show_message(msg)


def main():
    app = FilaCalcTk()
    app.mainloop()  # tk.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
