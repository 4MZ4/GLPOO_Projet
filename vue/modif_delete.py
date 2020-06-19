# -*- coding: utf-8 -*-

import tkinter.ttk as ttk
import tkinter as tk
import controller.DB as DB
import vue.select_all as select_all
class Modif :
    def __init__(self , fenetre , ID ):
        self.window = fenetre
        self.window.geometry("500x200")
        self.window.title(' Projet GLPOO')
        self.DB = DB.DATABASE()
        self.ID = ID
        self.info = self.DB.GET_data_by_ID(self.ID)[0]
        self.Tableau()
        self.Print_Ligne()
        self.Create_BOX_Delete()
        self.Create_box_modification()
    def DELETE(self):
        self.DB.Delete_by_index( self.ID )
        #tk.messagebox.showinfo(" Reussi ", " La Suppression est Reussit  ")
        self.CALL_Principal()
    def MODIFY(self):
        if DB.Validation_Date( self.StartTime.get() ) == 1 and DB.Validation_Date( self.EndTime.get() ) :
            ST = DB.Correction_Date( self.StartTime.get() )
            ET = DB.Correction_Date( self.EndTime.get() )
            query = " UPDATE Event_ SET StartTime = '"+str( ST )+"' , EndTime = '"+str( ET )+"' , SeverityID = '"+str(self.col_severity.current())+"' ,TypeID = '"+str(self.col_typ.current())+"' ,TimeZoneID = '"+str(self.col_tim.current())+"' ,AirportID  = '"+str(self.col_air.current())+"' where EventID = "+str(self.ID)+";"
            self.DB.Run_Query(query)
            self.CALL_Principal()
        else:
            tk.messagebox.showinfo(" Echec ", " La Date saisie est erronée ")

    def CALL_Principal(self):
        self.window.destroy()
        new_window = tk.Tk()
        select_all.Principale(new_window  )
    
    def Tableau(self):
        tk.Label(self.window, text="    Pour Modifier au Suprimer cette donnée    ").grid(row=0 , column=0)
        tk.Label(self.window, text="    StartTime   ").grid(row=1 , column=0)
        tk.Label(self.window, text="    EndTime     ").grid(row=2 , column=0)
        tk.Label(self.window, text="    TimeZone    ").grid(row=3 , column=0)
        tk.Label(self.window, text="    Severity    ").grid(row=4 , column=0)
        tk.Label(self.window, text="    Type        ").grid(row=5 , column=0)
        tk.Label(self.window, text="    AirportCode ").grid(row=6 , column=0)
        
        
    def Print_Ligne( self  ):
        for i in range( 0 , 6 ):
            tk.Label(self.window, text= str(self.info[i]) ).grid(row=i+1 , column=1)
    def Create_box_modification(self):
        sev = DB.Convert_Data( self.DB.GET_severity() )
        typ = DB.Convert_Data( self.DB.GET_type()     )
        tim = DB.Convert_Data( self.DB.GET_timezone() )
        air = DB.Convert_Data( self.DB.GET_airport()  )
        
        self.StartTime = tk.Entry(self.window)
        self.EndTime = tk.Entry(self.window)
        self.col_severity = ttk.Combobox(self.window, values = sev  )
        self.col_typ = ttk.Combobox(self.window, values = typ)
        self.col_tim = ttk.Combobox(self.window, values = tim)
        self.col_air = ttk.Combobox(self.window, values = air)
        
        
        
        self.StartTime.insert(0,str(self.info[0]))  
        self.EndTime.insert(0,str(self.info[1]))
        self.col_severity.current( int(self.info[6]) )
        self.col_typ.current( int(self.info[7]))
        self.col_tim.current( int(self.info[8]))
        self.col_air.current( int(self.info[9]) )
        
        
        
        self.StartTime.grid(row=1, column=2)
        self.EndTime.grid(row=2, column=2)
        self.col_tim.grid(row=3, column=2)
        self.col_severity.grid(row=4, column=2)
        self.col_typ.grid(row=5, column=2)
        self.col_air.grid(row=6, column=2)
        tk.Button(self.window,text='Modification',
          command=self.MODIFY).grid(row=8,column=1,sticky=tk.W,pady=4)
    def Create_BOX_Delete(self):
        tk.Button(self.window,text='Suppression',
          command=self.DELETE).grid(row=8,column=2,sticky=tk.W,pady=4)
        

# window = tk.Tk()
# Modif(window , 99999 )
# window.mainloop()