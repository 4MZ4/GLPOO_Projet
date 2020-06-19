# -*- coding: utf-8 -*-
import tkinter as tk
from controller.DB import DATABASE
from vue.modif_delete import Modif

class Principale :
    def __init__(self , fenetre ):
        self.window = fenetre
        self.window.geometry("790x200")
        self.window.title(' Projet GLPOO')
        self.DB = DATABASE()
        self.nb_ligne = 1
        self.Tableau()
        self.Print_ALL()
    def Redirection( self , ID ):
        new_window = tk.Tk()
        self.window.destroy()
        Modif(new_window , ID )
    def Tableau(self):
        tk.Label(self.window, text="    StartTime   |").grid(row=0 , column=0)
        tk.Label(self.window, text="    EndTime     |").grid(row=0 , column=1)
        tk.Label(self.window, text="    Severity    |").grid(row=0 , column=2)
        tk.Label(self.window, text="    TimeZone    |").grid(row=0 , column=3)
        tk.Label(self.window, text="    Type        |").grid(row=0 , column=4)
        tk.Label(self.window, text="    AirportCode |").grid(row=0 , column=5)
        tk.Label(self.window, text="    City        |").grid(row=0 , column=6)
        tk.Label(self.window, text="    County      |").grid(row=0 , column=7)
        tk.Label(self.window, text="    State       |").grid(row=0 , column=8)
    def Print_Ligne( self , info ):
        for i in range( 1 , 10 ):
            tk.Label(self.window, text= str(info[i]) ).grid(row=self.nb_ligne , column=i-1)
        tk.Button(self.window,text='Modif/Supr',command= lambda ID=info[0] : self.Redirection( ID )).grid(row=self.nb_ligne,column=10,sticky=tk.W,pady=4)
        self.nb_ligne += 1
    def Print_ALL(self):
        for i in self.DB.GET_principale():
            self.Print_Ligne( i )
