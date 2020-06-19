# -*- coding: utf-8 -*-

import tkinter as tk
import vue.select_all as select_all
import vue.Insertion as Insertion  

class Menu :
    def __init__(self , fenetre ):
        self.window = fenetre
        self.window.geometry("350x200")
        self.window.title(' Projet GLPOO')
        self.Create_Button()
        tk.Label(self.window, text=""" Projet : 
                 Visualisation de Donnée Meteo 
                 des differents aéroport des USA """).grid(row=0 , column=0)

    def Create_Button(self):
        tk.Button(self.window,text="   Table Principale ",
          command=self.Choix_Principal , fg='red').grid(row=2,column=1,sticky=tk.W,pady=4 )
        tk.Button(self.window,text="        Insertion     ", 
          command=self.Choix_Insertion).grid(row=4,column=1,sticky=tk.W,pady=4)
        tk.Button(self.window,text="           Plot       ", 
          command=self.Choix_Plot).grid(row=6,column=1,sticky=tk.W,pady=4)
        tk.Button(self.window,text="     Create BDD      ", 
          command=self.Choix_Make_DB).grid(row=8,column=1,sticky=tk.W,pady=4)
        
    def Choix_Principal(self):
        select_all.Principale(self.Create_AND_Destroy())
    def Choix_Insertion(self):
        Insertion.Insertion_Window( self.Create_AND_Destroy() )
    def Choix_Plot(self):
        import Ploter
    def Choix_Make_DB(self):
        import model.Make_DB
        select_all.Principale(self.Create_AND_Destroy())
    def Create_AND_Destroy(self):
        new_window = tk.Tk()
        self.window.destroy()
        return new_window

