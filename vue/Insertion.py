# -*- coding: utf-8 -*-

import tkinter.ttk as ttk
import tkinter as tk
from vue.modif_delete import Modif
import controller.DB as DB
        
class Insertion_Window :
    def __init__(self , fenetre ):
        self.window = fenetre
        self.window.geometry("400x200")
        self.window.title(' Projet GLPOO')
        self.DB = DB.DATABASE()
        self.Create_Label()
        self.Create_Box()
        self.Select()
        self.GRID()
        tk.Button(self.window,text='Insertion', 
          command=self.Insertion_DB).grid(row=8,column=1,sticky=tk.W,pady=4)

    def Insertion_DB(self):
        if DB.Validation_Date( self.StartTime.get() ) == 1 and DB.Validation_Date( self.EndTime.get() ) :
            ST = DB.Correction_Date( self.StartTime.get() )
            ET = DB.Correction_Date( self.EndTime.get() )
            new_id = self.DB.GET_new_index_event()
            query = "INSERT INTO Event_(EventID , StartTime ,  EndTime , SeverityID , TypeID ,TimeZoneID ,AirportID ) VALUES ("+str(new_id)+", '"+str( ST )+"', '"+str( ET )+"', '"+str(self.col_severity.current())+"', '"+str(self.col_typ.current())+"','"+str(self.col_tim.current())+"','"+str(self.col_air.current())+"');"
            self.DB.Run_Query(query)
            self.window.destroy()
            new_window = tk.Tk()
            Modif(new_window , new_id )
        else:
            tk.messagebox.showinfo(" Echec", " La Date saisie est erronée ")
    def Create_Label(self):
        tk.Label(self.window, text=" Insertion dans la base de Donnée  ").grid(row=1)
        tk.Label(self.window, text=" Start Time ").grid(row=2)
        tk.Label(self.window, text=" End Time   ").grid(row=3)
        tk.Label(self.window, text=" Severity   ").grid(row=4)
        tk.Label(self.window, text=" Type       ").grid(row=5)
        tk.Label(self.window, text=" TimeZone   ").grid(row=6)
        tk.Label(self.window, text=" AirPort    ").grid(row=7)
    def Create_Box( self ):
        # Import Data Categorie
        sev = DB.Convert_Data( self.DB.GET_severity() )
        typ = DB.Convert_Data( self.DB.GET_type()     )
        tim = DB.Convert_Data( self.DB.GET_timezone() )
        air = DB.Convert_Data( self.DB.GET_airport()  )
        # Create Boxes
        self.StartTime = tk.Entry(self.window)
        self.EndTime = tk.Entry(self.window)
        self.col_severity = ttk.Combobox(self.window, values = sev  )
        self.col_typ = ttk.Combobox(self.window, values = typ)
        self.col_tim = ttk.Combobox(self.window, values = tim)
        self.col_air = ttk.Combobox(self.window, values = air)
    def Select(self):
        self.StartTime.insert(0,"YYYY-MM-DD")
        self.EndTime.insert(0,"YYYY-MM-DD")
        self.col_severity.current(0)
        self.col_typ.current(0)
        self.col_tim.current(0)
        self.col_air.current(0)
    def GRID(self):
        self.StartTime.grid(row=2, column=2)
        self.EndTime.grid(row=3, column=2)
        self.col_severity.grid(row=4, column=2)
        self.col_typ.grid(row=5, column=2)
        self.col_tim.grid(row=6, column=2)
        self.col_air.grid(row=7, column=2)
                