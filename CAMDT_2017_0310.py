##Program: CAMDT (Climate Agriculture Modeling Decision Tool)
##  The CAMDT is a computer desktop tool designed to guide decision-makers
##  in adopting appropriate crop and water management practices
##  that can improve crop yields given a climate condition
##Author: Eunjin Han
##Institute: IRI-Columbia University, NY
##Revised: August, 2, 2016
##Date: February 17, 2016
##===================================================================

title = 'CAMDT User-Interface'

# Import Pmw from this directory tree.
import sys
sys.path[:0] = ['../../..']
from Tkinter import *
import Tkinter #Tkinter is the PYthon interface to Tk, the GUI toolkit ofr Tcl/Tk
import Pmw #Pmw(Python megawidgets) are composite widgets written entirely in Python using Tkinter widgets as base classes
       #Pmw provide a convinent ways to add functionality to an appilcation without the need to writ ea lot of code (e.g., Combobox) 
import datetime    #to convert date to doy or vice versa 
from tkFileDialog import *  # importing everything from tkFileDialog module for askopenfilename
 #Small addendum: tkFileDialog is renamed to tkinter.filedialog in Python 3  ?????
import subprocess  #to run executable
import shutil   #to remove a foler which is not empty
import os   #operating system
import numpy as np
import matplotlib.pyplot as plt  #to create plots
import fnmatch   # Unix filename pattern matching => to remove PILI0*.WTD
import os.path
from scipy.stats import rankdata #to make a rank to create yield exceedance curve

class CAMDT:     
    sf = frame = None  #initially, no frame
   
    def __init__(self, parent):  #initializing an instance
        global startyear2   #declare global variables to take user's inputs
        global endyear2
        global startyear3
        global endyear3
        global CheckVar, CheckVar21,CheckVar31,CheckVar32,CheckVar33,CheckVar51 #CheckVar22,
        global v_name
        global planting_date
        global Rbutton2,Rbutton3,cul_Rbutton,Fbutton1,IRbutton
        global group26,group35
        global floodVar1,floodVar2,floodVar3 #constant flooding depth or not :EJ(8/2/2016)
        
        # Create and pack a NoteBook.
        notebook = Pmw.NoteBook(parent)
        notebook.pack(fill = 'both', expand = 1, padx = 10, pady = 10)

#==========================First page "Simulation Setup"
        #Add a page to the notebook.
        page = notebook.add('Simulation setup')
        notebook.tab('Simulation setup').focus_set()
       # page.configure(background = 'white')
       # Create the "Simulation mode" contents of the page.
       # 1) ADD SCROLLED FRAME
        sf = Pmw.ScrolledFrame(page) #,usehullsize=1, hull_width=700, hull_height=220)
        sf.pack(padx=5, pady=3, fill='both', expand=YES)

        group = Pmw.Group(sf.interior(), tag_text = 'Simulation mode',tag_font = Pmw.logicalfont('Helvetica', 1))
        group.pack(fill = 'x',anchor=N, padx = 10, pady = 5)    
       
        CheckVar = Tkinter.IntVar()
        s_modelist=[('Hindcast', 0), ('Forecast', 1)]
        for text, value in s_modelist:
            Radiobutton(group.interior(), text=text, value=value, variable=CheckVar).pack(side=LEFT,expand=YES) #anchor=W)
        CheckVar.set(0)  #By default- hindcast mode

        # Create the "Simulation horizon" contents of the page.
        group2 = Pmw.Group(sf.interior(), tag_text = 'Simulation horizon(crop growing season)',tag_font = Pmw.logicalfont('Helvetica', 1))
        group2.pack(fill = 'x', expand = 1, padx = 10, pady = 5)
        #frame 1 within group2
        fm_gp21=Frame(group2.interior())
        startyear2 = Pmw.EntryField(fm_gp21, labelpos = 'w',
            label_text = 'Planting Year(4digit):',value = '2009',
            validate = {'validator': 'numeric', 'min' : 1950, 'max' : 2020, 'minstrict' : 0})
          #  modifiedcommand = self.changed)
        startyear2.pack(fill = 'x', padx = 10, pady = 5)

        mth_list = ("1","2","3","4","5","6","7","8","9","10","11","12") #,"-99")
        self.startmonth2 = Pmw.ComboBox(fm_gp21, label_text='Planting Month:', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=mth_list,
                        entryfield_entry_state=DISABLED)
        self.startmonth2.pack(fill = 'x', padx = 10, pady = 5)
        self.startmonth2.selectitem(mth_list[11])  #[12]=-99  # Display default item
        fm_gp21.pack(fill='x', expand=1,padx=10,side=LEFT)   

		#frame 2 within group2
        fm_gp22=Frame(group2.interior())
        #end year
        endyear2 = Pmw.EntryField(fm_gp22, labelpos = 'w',
            label_text = 'Harvesting Year(4digit):',value = '2010',
            validate = {'validator': 'numeric', 'min' : 1950, 'max' : 2020, 'minstrict' : 0})
        endyear2.pack(fill = 'x', padx = 10, pady = 5)
        
         #ending month
        self.endmonth2 = Pmw.ComboBox(fm_gp22, label_text='Harvesting Month:', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=mth_list,
                        entryfield_entry_state=DISABLED)
        self.endmonth2.pack(fill = 'x', padx = 10, pady = 5)
        # Display default item
        self.endmonth2.selectitem(mth_list[6])  #[12]=-99
        label10= Label(fm_gp22, text='*NOTE:Harvesting Month should be long enough \n(~3 months later than expected harvesting dates)') 
        label10.pack(side=TOP, anchor=N)
        fm_gp22.pack(fill='x', expand=1,padx=10,side=LEFT)         

# 3rd group: Create the "Predictionhorizon" contents of the page.
        group3 = Pmw.Group(sf.interior(), tag_text = 'Prediction horizon (seasonal climate forecast)',tag_font = Pmw.logicalfont('Helvetica', 1))
        group3.pack(fill = 'x', expand = 1, padx = 10, pady = 5)
        #frame 1 within group3
        fm_gp31=Frame(group3.interior())
        startyear3 = Pmw.EntryField(fm_gp31, labelpos = 'w',
            label_text = 'Forecast Start Year(4digit):',value = '2009',
            validate = {'validator': 'numeric', 'min' : 1950, 'max' : 2020, 'minstrict' : 0})
        startyear3.pack(fill = 'x', padx = 10, pady = 5)
         #starting month
        self.startmonth3 = Pmw.ComboBox(fm_gp31, label_text='Forecast Start Month:', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=mth_list,
                        entryfield_entry_state=DISABLED)
        self.startmonth3.pack(fill = 'x', padx = 10, pady = 5)
        # Display default item
        self.startmonth3.selectitem(mth_list[11]) #[12]=-99 [11]=12
        fm_gp31.pack(fill='x', expand=1,padx=10,side=LEFT)   

		#frame 2 within group3
        fm_gp32=Frame(group3.interior())       
        #end year
        endyear3 = Pmw.EntryField(fm_gp32, labelpos = 'w',
            label_text = 'Forecast End Year(4digit):',value = '2010',
            validate = {'validator': 'numeric', 'min' : 1950, 'max' : 2020, 'minstrict' : 0})
        endyear3.pack(fill = 'x', padx = 10, pady = 5)
         #ending month
        self.endmonth3 = Pmw.ComboBox(fm_gp32, label_text='Forecast End Month:', labelpos='wn',
                        listbox_width=10, dropdown=1,
                        scrolledlist_items=mth_list,
                        entryfield_entry_state=DISABLED)
        self.endmonth3.pack(fill = 'x', padx = 10, pady = 5)
        # Display default item
        self.endmonth3.selectitem(mth_list[1]) #[12]=-99 [1]=February
        fm_gp32.pack(fill='x', expand=1,padx=10,side=LEFT)
         
        #Planting date
        fm1=Frame(sf.interior()) #assign frame 1
        planting_date=Pmw.EntryField(fm1, labelpos='w',entry_width=5, 
            label_text='Planting date (DOY)',value = '349',  #doy349=Dec. 15th
            validate = {'validator': 'numeric', 'min' : 1, 'max' : 366, 'minstrict' : 0})
        planting_date.pack(side=LEFT) #, pady = 5)
        label11= Label(fm1, text='*NOTE:Planting date should be within the "Planting Month" of Sim horizon') 
        label11.pack(anchor=N)
        fm1.pack(fill='x', expand=1,padx=10,side=TOP)     

        # Create and pack the ButtonBox.
        buttonBox = Pmw.ButtonBox(sf.interior(),
                labelpos = 'w',
                label_text = 'Validate inputs ?',
                frame_borderwidth = 2,
                frame_relief = 'groove')
        buttonBox.pack()
        #self.buttonBox.pack(fill = 'both', expand = 1, padx = 10, pady = 10)

        # Add some buttons to the ButtonBox.
        buttonBox.add('Yes', command = self.validate_in)


#==========================Second page for "Seasonal Forecast"
        # Add two more empty pages.
        page2 = notebook.add('Temporal Downscaling')
        notebook.tab('Temporal Downscaling').focus_set()

       # 1) ADD SCROLLED FRAME
        sf_p2 = Pmw.ScrolledFrame(page2) #,usehullsize=1, hull_width=700, hull_height=220)
        sf_p2.pack(padx=5, pady=3, fill='both', expand=YES)
        
        fm1=Frame(sf_p2.interior()) #assign frame 1
        # Radio button to select "weather station"
        group20 = Pmw.Group(fm1, tag_text = 'Station with Historical Weather Data',tag_font = Pmw.logicalfont('Helvetica', 1))
        group20.pack(fill = 'both', side=TOP, padx = 10, pady = 5)  
        Wstation_list = ("PILI","LEGA")
        self.Wstation = Pmw.ComboBox(group20.interior(), label_text='Station Name:', labelpos='wn',
                        listbox_width=20, dropdown=1,
                        scrolledlist_items=Wstation_list,
                        entryfield_entry_state=DISABLED)
        self.Wstation.selectitem(Wstation_list[0])
        self.Wstation.pack(fill = 'x', side=LEFT,padx = 10, pady = 5)
        label20= Label(group20.interior(), text='*Make sure ####.WTD file should exist in workding directory') 
        label20.pack(anchor=N)

        # Radio button to select "Downscaling method"
        group21 = Pmw.Group(fm1, tag_text = 'Downscaling Method',tag_font = Pmw.logicalfont('Helvetica', 1))
        group21.pack(fill = 'both', side=TOP, padx = 10, pady = 5)    
        
        CheckVar21 = Tkinter.IntVar()
        down_method=[('FResampler', 0), ('Stochastic Disag', 1)]
        for text, value in down_method:
            Radiobutton(group21.interior(), text=text, command = self.empty_downscale_label, value=value, variable=CheckVar21).pack(side=LEFT,expand=YES)
        CheckVar21.set(1)  #By default- Stochastic Disag

        # Create button to launch the dialog 
        down_button=Tkinter.Button(fm1,
                text = 'Click to add more details for the selected method',
                command = self.getmoreinput,bg='gray70',font = ("weight bold",10)).pack(side=TOP,anchor=N)

        # Create the "Downscaling method" contents of the page.
        group22 = Pmw.Group(fm1, tag_text = 'FResampler',tag_font = Pmw.logicalfont('Helvetica', 0.7))
        group22.pack(fill = 'x', side=LEFT,anchor=N,expand=YES, padx = 10, pady = 5)
        #Label to fill user-input for downscaling details

        self.label11 = Label(group22.interior(), text='Num. of realization:', padx=5, pady=5)
        self.label11.grid(row=0,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label12 = Label(group22.interior(), text='Not added',relief='sunken',width=10, padx=5) #, pady=5)
        self.label12.grid(row=0,column=1, sticky=W) #rowspan=1,columnspan=1)
        self.label13 = Label(group22.interior(), text='*Must be multiples of 10,', padx=5) #, pady=5)
        self.label13.grid(row=1,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label14 = Label(group22.interior(), text='   preferably greater than 30', padx=5) #, pady=5)
        self.label14.grid(row=2,column=0, sticky=W) #rowspan=1,columnspan=1)

        #contents for Stochastic Disag      
        group23 = Pmw.Group(fm1, tag_text = 'Stochastic Disag.',tag_font = Pmw.logicalfont('Helvetica', 0.7))
       # group23.pack(fill = 'both', side=LEFT, padx = 10, pady = 5)
        group23.pack(fill = 'x', side=LEFT,anchor=N,expand=YES,padx = 10, pady = 5)
        self.label21 = Label(group23.interior(), text='Num. of realization:', padx=5, pady=5)
        self.label21.grid(row=0,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label22 = Label(group23.interior(), text='Not added',relief='sunken',padx=5, pady=5)
        self.label22.grid(row=0,column=1, sticky=W) #rowspan=1,columnspan=1)
        self.label23 = Label(group23.interior(), text='*Rainfall Target variable for *.MTH', padx=5, pady=5)
        self.label23.grid(row=1,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label24 = Label(group23.interior(), text='(1 indicates "chosen")', padx=5, pady=5)
        self.label24.grid(row=1,column=1, sticky=W) #rowspan=1,columnspan=1)
        self.label25 = Label(group23.interior(), text='Amount:', padx=5, pady=5)
        self.label25.grid(row=2,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label26 = Label(group23.interior(), text='Not added',relief='sunken', padx=5, pady=5)
        self.label26.grid(row=2,column=1, sticky=W) #rowspan=1,columnspan=1)
        self.label27 = Label(group23.interior(), text='Frequency:', padx=5, pady=5)
        self.label27.grid(row=3,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label28 = Label(group23.interior(), text='Not added',relief='sunken', padx=5, pady=5)
        self.label28.grid(row=3,column=1, sticky=W) #rowspan=1,columnspan=1)
        self.label29 = Label(group23.interior(), text='Intensity:', padx=5, pady=5)
        self.label29.grid(row=4,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label20 = Label(group23.interior(), text='Not added',relief='sunken', padx=5, pady=5)
        self.label20.grid(row=4,column=1, sticky=W) #rowspan=1,columnspan=1)
        fm1.pack(side=TOP)

##        #assign frame 2
##        fm2=Frame(sf_p2.interior())
##        # Radio button to select "How to get seasonal forecast"
##        group24 = Pmw.Group(fm2, tag_text = 'Tercile-baesd Seasonal Forecast',tag_font = Pmw.logicalfont('Helvetica', 2))
##        group24.pack(fill = BOTH, side=TOP, padx = 10, pady = 5)     

        #assign frame 2
        fm2=Frame(sf_p2.interior())
        group24 = Pmw.Group(fm2, tag_text = 'Tercile-baesd Seasonal Forecast',tag_font = Pmw.logicalfont('Helvetica', 1))
        group24.pack(fill = BOTH, side=TOP, padx = 10, pady = 5)     
        self.BN = Pmw.EntryField(group24.interior(), labelpos = 'w',
            label_text = 'Below Normal(%):', entry_width = 10,
            validate = {'validator': 'real', 'min' : 1, 'max' : 99, 'minstrict' : 0})
        self.BN.pack(fill = 'x', padx = 5, pady = 5,side=LEFT)
        self.AN = Pmw.EntryField(group24.interior(), labelpos = 'w',
            label_text = 'Above Normal(%):', entry_width = 10,
            validate = {'validator': 'real', 'min' : 1, 'max' : 99, 'minstrict' : 0})
        self.AN.pack(fill = 'x', padx = 5, pady = 5,side=LEFT)
        #-Near Normal
        NN=Label(group24.interior(), text='Near Normal(%):', padx=5, pady=5).pack(side=LEFT)
        NN_box = Label(group24.interior(), text='100-BN-AN',padx=5, pady=5).pack(side=LEFT)
        fm2.pack(fill = BOTH, side=TOP)
##        
##        CheckVar22 = Tkinter.IntVar()
##        SF_data=[('From CPT', 0), ('User-specified', 1)]
##        for text, value in SF_data:
##            Radiobutton(group24.interior(), text=text, command = self.empty_scf_label, value=value, variable=CheckVar22).pack(side=LEFT,expand=YES)
##        CheckVar22.set(1)  #By default- FResampler

##        # Create button to launch the dialog for cultivar
##        down_button22=Tkinter.Button(fm2,
##                text = 'Click to add more details for SF input',
##                command = self.getSFinput,bg='gray70').pack(side=TOP,anchor=N)
##
##        # Create the "Downscaling method" contents of the page.
##        group25 = Pmw.Group(fm2, tag_text = 'CPT input',tag_font = Pmw.logicalfont('Helvetica', 0.7))
##        group25.pack(fill = 'x', anchor=N,side=LEFT,expand=1, padx = 10, pady = 5)
##        #Label to fill user-input for downscaling details
##
##        self.label31 = Label(group25.interior(), text='CPT_file:', padx=5, pady=5)
##        self.label31.grid(row=0,column=0, sticky=W) #rowspan=1,columnspan=1)
##        self.label32 = Label(group25.interior(), text='Not added',relief='sunken', padx=5, pady=5)
##        self.label32.grid(row=0,column=1, sticky=W) #rowspan=1,columnspan=1)
##        self.label33 = Label(group25.interior(), text='Latitude:', padx=5, pady=5)
##        self.label33.grid(row=1,column=0, sticky=W) #rowspan=1,columnspan=1)
##        self.label34 = Label(group25.interior(), text='Not added',relief='sunken',width=10, padx=5, pady=5)
##        self.label34.grid(row=1,column=1, sticky=W) #rowspan=1,columnspan=1)
##        self.label35 = Label(group25.interior(), text='Longitude:', padx=5, pady=5)
##        self.label35.grid(row=2,column=0, sticky=W) #rowspan=1,columnspan=1)
##        self.label36 = Label(group25.interior(), text='Not added',relief='sunken',width=10, padx=5, pady=5)
##        self.label36.grid(row=2,column=1, sticky=W) #rowspan=1,columnspan=1)
##
##        #contents for Stochastic Disag      
##        group26 = Pmw.Group(fm2, tag_text = 'User-specified',tag_font = Pmw.logicalfont('Helvetica', 0.7))
##       # group23.pack(fill = 'both', side=LEFT, padx = 10, pady = 5)
##        group26.pack(fill = 'x', anchor=N,side=LEFT,expand=1, padx = 10, pady = 5)
##        self.label41 = Label(group26.interior(), text='Below Normal(%):', padx=5, pady=5)
##        self.label41.grid(row=0,column=0, sticky=W) #rowspan=1,columnspan=1)
##        self.label42 = Label(group26.interior(), text='Not added',relief='sunken',width=10, padx=5, pady=5)
##        self.label42.grid(row=0,column=1, sticky=W) #rowspan=1,columnspan=1)
##        self.label43 = Label(group26.interior(), text='Near Normal(%):', padx=5, pady=5)
##        self.label43.grid(row=1,column=0, sticky=W) #rowspan=1,columnspan=1)
##        self.label44 = Label(group26.interior(), text='Not added',relief='sunken',width=10, padx=5, pady=5)
##        self.label44.grid(row=1,column=1, sticky=W) #rowspan=1,columnspan=1)
##        self.label45 = Label(group26.interior(), text='Above Normal(%):', padx=5, pady=5)
##        self.label45.grid(row=2,column=0, sticky=W) #rowspan=1,columnspan=1)
##        self.label46 = Label(group26.interior(), text='Not added',relief='sunken',width=10, padx=5, pady=5)
##        self.label46.grid(row=2,column=1, sticky=W) #rowspan=1,columnspan=1)

#=========================Third page for "DSSAT baseline setup - I "
        page3 = notebook.add('DSSAT setup 1')
        notebook.tab('DSSAT setup 1').focus_set()
       # 1) ADD SCROLLED FRAME
        sf_p3 = Pmw.ScrolledFrame(page3) #,usehullsize=1, hull_width=700, hull_height=220)
        sf_p3.pack(padx=5, pady=3, fill='both', expand=YES)

        #Assign a group for planting method
        group32 = Pmw.Group(sf_p3.interior(), tag_text = 'Planting method',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group32.pack(fill='both', expand=1,side=TOP, padx = 10, pady = 2)  
        # Radio button to select "Planting method"
        Rbutton2 = Tkinter.IntVar()
        plt_option=[('Dry seed', 0), ('Transplanting', 1)]
        for text, value in plt_option:
            Radiobutton(group32.interior(), text=text, value=value, variable=Rbutton2).pack(side=LEFT,expand=YES)
        Rbutton2.set(1)  #By default- Transplanting

        # set up "Planting details"
        group33 = Pmw.Group(sf_p3.interior(), tag_text = 'Planting details',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group33.pack(fill = 'x', side=TOP, padx = 10, pady = 2)
        #-planting distribution
        pdist_list = ("Hills","Rows","Broadcast")
        self.plt_dist = Pmw.ComboBox(group33.interior(), label_text='Planting distribution:', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=pdist_list,
                        entryfield_entry_state=DISABLED)
        self.plt_dist.pack(fill = 'x', padx = 10, pady = 2)
        self.plt_dist.selectitem(pdist_list[1])
        #-planting population at seedling (plant/m2)
        self.ppop_seed=Pmw.EntryField(group33.interior(), labelpos='w', label_text='Plt population at seedling(plt/m2):',
            value = '75',validate = {'validator': 'real', 'min' : 1, 'max' : 100, 'minstrict' : 0})
        self.ppop_seed.pack(fill='x', side=TOP,expand=1,padx=10, pady = 0.5)
        self.ppop_emer=Pmw.EntryField(group33.interior(), labelpos='w', label_text='Plt population at emergence(plt/m2):',
            value = '25',validate = {'validator': 'real', 'min' : 1, 'max' : 80, 'minstrict' : 0})
        self.ppop_emer.pack(fill='x', side=TOP,expand=1,padx=10, pady = 0.5)
        self.row_space=Pmw.EntryField(group33.interior(), labelpos='w', label_text='Planting row spacing(cm):',
            value = '20',validate = {'validator': 'real', 'min' : 1, 'max' : 80, 'minstrict' : 0})
        self.row_space.pack(fill='x', side=TOP,expand=1,padx=10, pady = 0.5)
        self.row_dir=Pmw.EntryField(group33.interior(), labelpos='w', label_text='Row direction(deg from North):',
            value = '0',validate = {'validator': 'real', 'min' : 0, 'max' : 360, 'minstrict' : 0})
        self.row_dir.pack(fill='x', side=TOP,expand=1,padx=10, pady = 0.5)
        self.plt_depth=Pmw.EntryField(group33.interior(), labelpos='w', label_text='Planting depth(cm):',
            value = '2',validate = {'validator': 'real', 'min' : 1, 'max' : 50, 'minstrict' : 0})
        self.plt_depth.pack(fill='x', side=TOP,expand=1,padx=10, pady = 0.5)
        #aline labels
        entries = (self.plt_dist, self.ppop_seed, self.ppop_emer, self.row_space, self.row_dir, self.plt_depth)
        Pmw.alignlabels(entries)

        #assign frame 3
        fm33=Frame(sf_p3.interior())
        # group for soil set up
        group35 = Pmw.Group(fm33, tag_text = 'Soil',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group35.pack(fill = 'x', side=TOP, padx = 10, pady = 2)
        #-soil types
        soil_list = ("SCL(WI_ANPH007)","LoamySand(WI_ANPH008)","Clay(WI_VRPH021)","Clay(WI_VRPH043)","SCL2(WI_CMPH009)")
        self.soil_type = Pmw.ComboBox(group35.interior(), label_text='Soil type:', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=soil_list,
                        entryfield_entry_state=DISABLED)
        self.soil_type.pack(fill = 'x',side=LEFT, padx = 10, pady = 2)
        self.soil_type.selectitem(soil_list[0])
        #-rooting depth
        rdepth_list = ("deep","medium","shallow")
        self.rt_depth = Pmw.ComboBox(group35.interior(), label_text='Rooting depth:', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=rdepth_list,
                        entryfield_entry_state=DISABLED)
        self.rt_depth.pack(fill = 'x',side=LEFT, padx = 10, pady = 2)
        self.rt_depth.selectitem(rdepth_list[1])
        fm33.pack(fill = 'both', expand = 1,side=TOP)

        #assign frame 4
        fm34=Frame(sf_p3.interior())
        # set up "cultivar selection"
        group36 = Pmw.Group(fm34, tag_text = 'Cultivar selection',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group36.pack(fill = 'x', side=TOP, padx = 10, pady = 2)
        cul_Rbutton = Tkinter.IntVar()
        cul_option=[('Calibrated', 0), ('User-specified', 1)]
        for text, value in cul_option:
            Radiobutton(group36.interior(), text=text, value=value, variable=cul_Rbutton).pack(side=LEFT,expand=YES)
        cul_Rbutton.set(0)  #By default- calibrated

        # Create button to launch the dialog 
        cul_button=Tkinter.Button(fm34,
                text = 'Click to add more details for cultivar type',
                command = self.getCulinput,bg='gray70').pack(side=TOP,anchor=N)

        # Create the "cultivar" contents of the page.
        group361 = Pmw.Group(fm34, tag_text = 'Calibrated',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group361.pack(fill = 'x', side=LEFT,anchor=N,expand=YES, padx = 10, pady = 5)
        self.label361 = Label(group361.interior(), text='Cultivar ID:', padx=5, pady=5)
        self.label361.grid(row=0,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label362 = Label(group361.interior(), text='Not added',relief='sunken',width=10, padx=5, pady=5)
        self.label362.grid(row=0,column=1, sticky=W) #rowspan=1,columnspan=1)
        self.label363 = Label(group361.interior(), text='Cultivar name:', padx=5, pady=5)
        self.label363.grid(row=1,column=0, sticky=W) #rowspan=1,columnspan=1)
        self.label364 = Label(group361.interior(), text='Not added',relief='sunken',width=10,padx=5, pady=5)
        self.label364.grid(row=1,column=1, sticky=W) #rowspan=1,columnspan=1)

        #contents for user-specified cultivar    
        group362 = Pmw.Group(fm34, tag_text = 'User-specified cultivar',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group362.pack(fill = 'x', side=LEFT,anchor=N,expand=YES,padx = 10, pady = 2)
        self.label301 = Label(group362.interior(), text='Cultivar ID:') 
        self.label302 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label303 = Label(group362.interior(), text='Cultivar name:') 
        self.label304 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label305 = Label(group362.interior(), text='Ecotype code:') 
        self.label306 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label307 = Label(group362.interior(), text='P1:') 
        self.label308 = Label(group362.interior(), text='Not added',relief='sunken',width=10)
        self.label309= Label(group362.interior(), text='P2R:') 
        self.label310 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label311= Label(group362.interior(), text='P5:') 
        self.label312 = Label(group362.interior(), text='Not added',relief='sunken',width=10)  
        self.label313= Label(group362.interior(), text='P2O:') 
        self.label314 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label315= Label(group362.interior(), text='G1:') 
        self.label316 = Label(group362.interior(), text='Not added',relief='sunken',width=10)  
        self.label317= Label(group362.interior(), text='G2:') 
        self.label318 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label319= Label(group362.interior(), text='G3:') 
        self.label320 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        self.label321= Label(group362.interior(), text='G4:') 
        self.label322 = Label(group362.interior(), text='Not added',relief='sunken',width=10) 
        #aline lables names
        entries = (self.label301, self.label303, self.label305, self.label307, self.label309,
                self.label311,self.label313,self.label315,self.label317,self.label319,self.label321)
        i=0
        for entry in entries:
            entry.grid(row=i,column=0, sticky=W)
            i=i+1
        #aline  empty label
        entries = (self.label302, self.label304, self.label306, self.label308, self.label310,
                self.label312,self.label314,self.label316,self.label318,self.label320,self.label322)
        i=0
        for entry in entries:
            entry.grid(row=i,column=1) #, sticky=W) 
            i=i+1
        #aline lables names
        entries = (self.label313, self.label315, self.label317, self.label319, self.label321)
        i=1
        for entry in entries:
            entry.grid(row=i,column=2, sticky=W)
            i=i+1
        #aline  empty label
        entries = (self.label314, self.label316, self.label318, self.label320, self.label322)
        i=1
        for entry in entries:
            entry.grid(row=i,column=3) #, sticky=W) 
            i=i+1

        fm34.pack(fill = 'both', expand = 1,side=TOP)
#=========================4th page for "DSSAT baseline setup - II "
        page4 = notebook.add('DSSAT setup 2')
        notebook.tab('DSSAT setup 2').focus_set()
       # 1) ADD SCROLLED FRAME
        sf_p4 = Pmw.ScrolledFrame(page4) #,usehullsize=1, hull_width=700, hull_height=220)
        sf_p4.pack(padx=5, pady=3, fill='both', expand=YES)

        #assign frame 1
        fm41=Frame(sf_p4.interior())
        # Radio button to select "Irrigation method"
        group41 = Pmw.Group(fm41, tag_text = 'Fertilization application',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group41.pack(fill='both', expand=1, side=TOP, padx = 10, pady = 5)    
      
        Fbutton1 = Tkinter.IntVar()
        Frt_option=[('Fertilization', 0), ('No Fertilization', 1)]
        for text, value in Frt_option:
            Radiobutton(group41.interior(), text=text, command = self.empty_fert_label, value=value, variable=Fbutton1).pack(side=LEFT,expand=YES)
        Fbutton1.set(1)  #By default- no Fertilization
        # Create button to launch the dialog 
        frt_button=Tkinter.Button(fm41,
                text = 'Click to add more details for fertilizer',
                command = self.getFertInput,bg='gray70').pack(side=TOP,anchor=N)

        # Create the "fertilizer" contents of the page.
        group42 = Pmw.Group(fm41, tag_text = 'Fertilizer application',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group42.pack(fill = 'x', side=TOP,expand=1, padx = 2, pady = 5)
        self.nfertilizer = Pmw.EntryField(group42.interior(), labelpos = 'w',
            label_text = 'Number of fertilizer applications? ',
            validate = {'validator': 'numeric', 'min' : 1, 'max' : 3, 'minstrict' : 0})
        self.nfertilizer.pack( side=TOP, anchor=W,padx = 5, pady = 5)  
        frame_frt =Frame(group42.interior())
        label000 = Label(frame_frt, text='No. application', padx=5, pady=5)
        label001 = Label(frame_frt, text='Days after planting',padx=5, pady=5)
        label002 = Label(frame_frt, text='Amount (N, kg/ha)', padx=5, pady=5)
        label003 = Label(frame_frt, text='Fertilizer material',padx=5, pady=5)
        label004 = Label(frame_frt, text='Application method',padx=5, pady=5)
        self.label005 = Label(frame_frt, text='1st:',padx=5, pady=5)
        self.label006 = Label(frame_frt, text='Not added',relief='sunken',width=13)  
        self.label007 = Label(frame_frt, text='Not added',relief='sunken',width=15) 
        self.label008 = Label(frame_frt, text='Not added',relief='sunken',width=13) 
        self.label009 = Label(frame_frt, text='Not added',relief='sunken',width=25) 
        self.label010 = Label(frame_frt, text='2nd:',padx=5, pady=5) 
        self.label011 = Label(frame_frt, text='Not added',relief='sunken',width=13) 
        self.label012 = Label(frame_frt, text='Not added',relief='sunken',width=15) 
        self.label013 = Label(frame_frt, text='Not added',relief='sunken',width=13) 
        self.label014 = Label(frame_frt, text='Not added',relief='sunken',width=25)   
        self.label015 = Label(frame_frt, text='3rd:',padx=5, pady=5) 
        self.label016 = Label(frame_frt, text='Not added',relief='sunken',width=13) 
        self.label017 = Label(frame_frt, text='Not added',relief='sunken',width=15) 
        self.label018 = Label(frame_frt, text='Not added',relief='sunken',width=13) 
        self.label019 = Label(frame_frt, text='Not added',relief='sunken',width=25)  
        #aline  empty label
        entries = (label000, label001, label002, label003, label004)
        i=0
        for entry in entries:
            entry.grid(row=0,column=i) #, sticky=W) 
            i=i+1
        entries = (self.label005, self.label006, self.label007, self.label008, self.label009)
        i=0
        for entry in entries:
            entry.grid(row=1,column=i) #, sticky=W) 
            i=i+1
        entries = (self.label010, self.label011, self.label012, self.label013, self.label014)
        i=0
        for entry in entries:
            entry.grid(row=2,column=i) #, sticky=W) 
            i=i+1
        entries = (self.label015, self.label016, self.label017, self.label018, self.label019)
        i=0
        for entry in entries:
            entry.grid(row=3,column=i) #, sticky=W) 
            i=i+1
        frame_frt.pack(fill = 'x', expand = 1,side=TOP)
        fm41.pack(fill = 'both', expand = 1,side=TOP)
        #assign frame 2
        fm42=Frame(sf_p4.interior())
        # Radio button to select "Planting method"
        group43 = Pmw.Group(fm42, tag_text = 'Irrigation',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group43.pack(fill='x', expand=1,side=TOP, padx = 10, pady = 5)          

        IRbutton = Tkinter.IntVar()
        IR_option=[('Automatic when required', 0),('On Reported dates', 2),('No Irrigation', 3)]
        for text, value in IR_option:
            Radiobutton(group43.interior(), text=text, command = self.empty_irrig_label, value=value, variable=IRbutton).pack(side=LEFT,expand=YES)
        IRbutton.set(3)  #By default- no irrigation
        
        # Create button to launch the dialog 
        Irr_button=Tkinter.Button(fm42,
                text = 'Click to add more details for irrigation',
                command = self.getIrrInput,bg='gray70').pack(side=TOP,anchor=N)
        
        # Create the "Automatic irrigation" contents of the page.
        group44 = Pmw.Group(fm42, tag_text = 'Irrigation (Automatic)',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group44.pack(fill = 'x', side=TOP,expand=1, padx = 2, pady = 5)
        self.label401 = Label(group44.interior(), text='Management depth(cm):',anchor=W, padx=10)
        self.label401.grid(row=0,column=0, sticky=W)
        self.label402 = Label(group44.interior(), text='Not added',relief='sunken', padx=5)
        self.label402.grid(row=0,column=1, sticky=W)
        self.label403 = Label(group44.interior(), text='Threshold(% of max available):',anchor=W,padx=10)
        self.label403.grid(row=0,column=2, sticky=W)
        self.label404 = Label(group44.interior(), text='Not added',relief='sunken',padx=5)
        self.label404.grid(row=0,column=3, sticky=W)
##        self.label405 = Label(group44.interior(), text='End point(% of max available):',anchor=W, padx=10)
##        self.label405.grid(row=1,column=0, sticky=W)
##        self.label406 = Label(group44.interior(), text='Not added',relief='sunken',padx=5)
##        self.label406.grid(row=1,column=1, sticky=W)
        self.label407 = Label(group44.interior(), text='Efficiency fraction:',anchor=W,padx=10)
        self.label407.grid(row=1,column=0, sticky=W)
        self.label408 = Label(group44.interior(), text='Not added',relief='sunken',padx=5)
        self.label408.grid(row=1,column=1, sticky=W)

   # Create the "manual irrigation" contents of the page.
        group45 = Pmw.Group(fm42, tag_text = 'Irrigation (Reported)',tag_font = Pmw.logicalfont('Helvetica', 0.5))
        group45.pack(fill = 'x', side=TOP,expand=1, padx = 2, pady = 5)
        self.nirrigation = Pmw.EntryField(group45.interior(), labelpos = 'w',
            label_text = 'Number of irrigations? ',
            validate = {'validator': 'numeric', 'min' : 1, 'max' : 3, 'minstrict' : 0})
        self.nirrigation.pack( side=TOP, padx = 5, anchor=W, pady = 5)
        frame_in1 =Frame(group45.interior())
        self.label120 = Label(frame_in1, text='Puddling date(YYDOY):',padx=5)
        self.label120.grid(row=0,column=0, sticky=W)
        self.label121= Label(frame_in1, text='Not added',relief='sunken',width=13)  
        self.label121.grid(row=0,column=1, sticky=W)
##        self.label122 = Label(frame_in1, text='Puddling:',padx=5)
##        self.label122.grid(row=1,column=0, sticky=W)
##        self.label123= Label(frame_in1, text='Not added',relief='sunken',width=13) 
##        self.label123.grid(row=1,column=1, sticky=W)
        self.label124 = Label(frame_in1, text='Percolation rate(mm/day):',padx=5)
        self.label124.grid(row=2,column=0, sticky=W)
        self.label125= Label(frame_in1, text='Not added',relief='sunken',width=13)
        self.label125.grid(row=2,column=1, sticky=W) 
        frame_in1.pack(fill = 'x', expand = 1,side=TOP)

        frame_in2 =Frame(group45.interior())
        label100 = Label(frame_in2, text='No. irrigation', width=10, padx=5,pady=5)
        label101 = Label(frame_in2, text='Date(YYDOY)', width=13,padx=5,pady=5)
        label102 = Label(frame_in2, text='Bund height',width=15, padx=5,pady=5)
        label103 = Label(frame_in2, text='Flood depth', width=20, padx=5,pady=5)
        label1031 = Label(frame_in2, text='Constant depth?', width=20, padx=5,pady=5)
        self.label104 = Label(frame_in2, text='1st:',width=10,padx=5)
        self.label105 = Label(frame_in2, text='Not added',relief='sunken',width=13)  
        self.label106 = Label(frame_in2, text='Not added',relief='sunken',width=15) 
        self.label107 = Label(frame_in2, text='Not added',relief='sunken',width=20) 
        self.label1071 = Label(frame_in2, text='Not added',relief='sunken',width=20) 
        self.label108 = Label(frame_in2, text='2nd:',width=10,padx=5) 
        self.label109 = Label(frame_in2, text='Not added',relief='sunken',width=13) 
        self.label110 = Label(frame_in2, text='Not added',relief='sunken',width=15) 
        self.label111 = Label(frame_in2, text='Not added',relief='sunken',width=20)    
        self.label1111 = Label(frame_in2, text='Not added',relief='sunken',width=20) 
        self.label112 = Label(frame_in2, text='3rd:',width=10,padx=5) 
        self.label113 = Label(frame_in2, text='Not added',relief='sunken',width=13) 
        self.label114 = Label(frame_in2, text='Not added',relief='sunken',width=15) 
        self.label115 = Label(frame_in2, text='Not added',relief='sunken',width=20) 
        self.label1151 = Label(frame_in2, text='Not added',relief='sunken',width=20) 
        #aline  empty label
        entries = (label100, label101, label102, label103,label1031)
        i=0
        for entry in entries:
            entry.grid(row=0,column=i) #, sticky=W) 
            i=i+1
        entries = (self.label104, self.label105, self.label106, self.label107,self.label1071)
        i=0
        for entry in entries:
            entry.grid(row=1,column=i) #, sticky=W) 
            i=i+1
        entries = (self.label108, self.label109, self.label110, self.label111,self.label1111)
        i=0
        for entry in entries:
            entry.grid(row=2,column=i) #, sticky=W) 
            i=i+1
        entries = (self.label112, self.label113, self.label114, self.label115,self.label1151)
        i=0
        for entry in entries:
            entry.grid(row=3,column=i) #, sticky=W) 
            i=i+1
        frame_in2.pack(fill = 'x', expand = 1,side=TOP)      
     
        fm42.pack(fill = 'x', expand = 1,side=TOP)
     #   fm_in1=Frame(fm31)
#=========================5th  page for "DSSAT setup"
        page5 = notebook.add('*Scenarios setup')
        notebook.tab('*Scenarios setup').focus_set()

       # 1) ADD SCROLLED FRAME
        sf_p5 = Pmw.ScrolledFrame(page5) #,usehullsize=1, hull_width=700, hull_height=220)
        sf_p5.pack(padx=5, pady=3, fill='both', expand=YES)

        group51 = Pmw.Group(sf_p5.interior(), tag_text = 'Working directory')
        group51.pack(fill = 'x', expand = 1, anchor=N, padx = 10, pady = 5)     
        #Working directory
        fm51=Frame(group51.interior())
        self.WDir_label0=Label(fm51, text='Working directory:', padx=5, pady=5)
        self.WDir_label0.pack(fill = 'x', side=LEFT, anchor=W, padx = 10, pady = 5)
        self.WDir_label = Label(fm51, text='N/A',relief='sunken', padx=5, pady=5)
        self.WDir_label.pack(fill = 'x', side=LEFT, anchor=W, padx = 10, pady = 5)
        fm51.pack(side=TOP)
        fm52=Frame(group51.interior())
       # Create button to get file path
        self.file_button=Tkinter.Button(fm52,
                text = 'Click to select a working directory',
                command = self.getWdir,bg='gray70').pack(side=TOP,anchor=N)
        fm52.pack(side=TOP)
        WDir_label2=Label(fm52, text='*NOTE: Make sure all input files are in the chosen directory').pack(side=TOP,anchor=W)
        WDir_label3=Label(fm52, text='          Output files will be created under the chosen directory with new scenario names').pack(side=TOP, anchor=W)

        # 3rd group for threshold of water stress index"
        group53 = Pmw.Group(sf_p5.interior(), tag_text = 'Threshold for water stress index')
        group53.pack(fill = 'x', expand = 1,anchor=N, padx = 10, pady = 5)   
        self.wsi_threshold = Pmw.EntryField(group53.interior(), labelpos = 'w',
            label_text = 'Threshold water stress (0~1) to compute prob. of exceeding it? ', value = '0.5', #by default =0.5
            validate = {'validator': 'real', 'min' : 0.01, 'max' : 1, 'minstrict' : 0})
        self.wsi_threshold.pack( side=TOP, padx = 5, pady = 5) 

        # 2nd group for What-If Scenarios"
        group52 = Pmw.Group(sf_p5.interior(), tag_text = 'What-If scenarios')
        group52.pack(fill = 'x', expand = 1,anchor=N, padx = 10, pady = 5)   
##        self.nscenario = Pmw.EntryField(group52.interior(), labelpos = 'w',
##            label_text = 'How many scenarios? ',
##            validate = {'validator': 'numeric', 'min' : 1, 'max' : 5, 'minstrict' : 0})
##        self.nscenario.pack( side=TOP, padx = 5, pady = 5)      
        fm53=Frame(group52.interior())
        label51 = Label(fm53, text='Scenario Name').pack(side=TOP)
        label510 = Label(fm53, text='(4char) ').pack(side=TOP)
        self.name1 = Pmw.EntryField(fm53, labelpos = 'w',entry_width=10,
            label_text = '1:',
            validate = {'validator': 'alphanumeric', 'min' : 1, 'max' : 10, 'minstrict' : 0})
        self.name1.pack( side=TOP, padx = 5, pady = 5) 
        self.name2 = Pmw.EntryField(fm53, labelpos = 'w',entry_width=10,
            label_text = '2:',
            validate = {'validator': 'alphanumeric', 'min' : 1, 'max' : 10, 'minstrict' : 0})
        self.name2.pack( side=TOP, padx = 5, pady = 5) 
        self.name3 = Pmw.EntryField(fm53, labelpos = 'w',entry_width=10,
            label_text = '3:',
            validate = {'validator': 'alphanumeric', 'min' : 1, 'max' : 10, 'minstrict' : 0})
        self.name3.pack( side=TOP, padx = 5, pady = 5) 
        self.name4 = Pmw.EntryField(fm53, labelpos = 'w',entry_width=10,
            label_text = '4:',
            validate = {'validator': 'alphanumeric', 'min' : 1, 'max' : 10, 'minstrict' : 0})
        self.name4.pack( side=TOP, padx = 5, pady = 5) 
        self.name5 = Pmw.EntryField(fm53, labelpos = 'w',entry_width=10,
            label_text = '5:',
            validate = {'validator': 'alphanumeric', 'min' : 1, 'max' : 10, 'minstrict' : 0})
        self.name5.pack( side=TOP, padx = 5, pady = 5) 
        fm53.pack(side=LEFT)

         #-2nd frame
        fm54=Frame(group52.interior())
        label52 = Label(fm54, text='     ').pack(side=TOP)
        label520 = Label(fm54, text='     ').pack(side=TOP)
       # Create button to get file path
        self.param_button1=Tkinter.Button(fm54,
                text = 'Click to write param1.txt',
                command = self.writeParam1,bg='gray70').pack(side=TOP,anchor=N, padx = 5, pady = 2)
        self.param_button2=Tkinter.Button(fm54,
                text = 'Click to write param2.txt',
                command = self.writeParam2,bg='gray70').pack(side=TOP,anchor=N, padx = 5, pady = 2)
        self.param_button3=Tkinter.Button(fm54,
                text = 'Click to write param3.txt',
                command = self.writeParam3,bg='gray70').pack(side=TOP,anchor=N, padx = 5, pady = 2)
        self.param_button4=Tkinter.Button(fm54,
                text = 'Click to write param4.txt',
                command = self.writeParam4,bg='gray70').pack(side=TOP,anchor=N, padx = 5, pady = 2)
        self.param_button5=Tkinter.Button(fm54,
                text = 'Click to write param5.txt',
                command = self.writeParam5,bg='gray70').pack(side=TOP,anchor=N, padx = 5, pady = 2)
        fm54.pack(side=LEFT)
         #-3rd frame
        fm55=Frame(group52.interior())
        label53 = Label(fm55, text='  ').pack(side=TOP)
        label530 = Label(fm55, text='Crop').pack(side=TOP) 
        self.label54 = Label(fm55, text='N/A',relief='sunken')
        self.label54.pack( side=TOP,padx = 5, pady = 5) 
        self.label55 = Label(fm55, text='N/A',relief='sunken')
        self.label55.pack( side=TOP,padx = 5, pady = 5) 
        self.label56 = Label(fm55, text='N/A',relief='sunken')
        self.label56.pack( side=TOP,padx = 5, pady = 5) 
        self.label57 = Label(fm55, text='N/A',relief='sunken')
        self.label57.pack( side=TOP,padx = 5, pady = 5) 
        self.label58 = Label(fm55, text='N/A',relief='sunken')
        self.label58.pack( side=TOP,padx = 5, pady = 5) 
        fm55.pack(side=LEFT)

         #-4th frame - price
        fm56=Frame(group52.interior())
        label54 = Label(fm56, text='Crop price').pack(side=TOP)
        label540 = Label(fm56, text='(PHP/ton)').pack(side=TOP) 
        self.price1 = Pmw.EntryField(fm56, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.price1.pack( side=TOP, padx = 5, pady = 5) 
        self.price2 = Pmw.EntryField(fm56, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.price2.pack( side=TOP, padx = 5, pady = 5) 
        self.price3 = Pmw.EntryField(fm56, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.price3.pack( side=TOP, padx = 5, pady = 5) 
        self.price4 = Pmw.EntryField(fm56, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.price4.pack( side=TOP, padx = 5, pady = 5) 
        self.price5 = Pmw.EntryField(fm56, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.price5.pack( side=TOP, padx = 5, pady = 5)  
        fm56.pack(side=LEFT)
         #-5th frame - Price of N fertilizer
        fm57=Frame(group52.interior())
        label55 = Label(fm57, text='Cost of N fert.').pack(side=TOP)
        label550 = Label(fm57, text='(PHP/kg N)').pack(side=TOP)
        self.costN1 = Pmw.EntryField(fm57, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0.1, 'minstrict' : 0})
        self.costN1.pack( side=TOP, padx = 5, pady = 5) 
        self.costN2 = Pmw.EntryField(fm57, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0.1,'minstrict' : 0})
        self.costN2.pack( side=TOP, padx = 5, pady = 5) 
        self.costN3 = Pmw.EntryField(fm57, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0.1,'minstrict' : 0})
        self.costN3.pack( side=TOP, padx = 5, pady = 5) 
        self.costN4 = Pmw.EntryField(fm57, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0.1, 'minstrict' : 0})
        self.costN4.pack( side=TOP, padx = 5, pady = 5) 
        self.costN5 = Pmw.EntryField(fm57, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0.1, 'minstrict' : 0})
        self.costN5.pack( side=TOP, padx = 5, pady = 5)  
        fm57.pack(side=LEFT)
 
        #-6th frame - Cost of irrigation
        fm58=Frame(group52.interior())
        label56 = Label(fm58, text='Cost of irrig.').pack(side=TOP)
        label560 = Label(fm58, text='(PHP/mm)').pack(side=TOP)
        self.costI1 = Pmw.EntryField(fm58, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costI1.pack( side=TOP, padx = 5,pady = 5) 
        self.costI2 = Pmw.EntryField(fm58, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costI2.pack( side=TOP, padx = 5,pady = 5) 
        self.costI3 = Pmw.EntryField(fm58, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costI3.pack( side=TOP, padx = 5,pady = 5) 
        self.costI4 = Pmw.EntryField(fm58, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costI4.pack( side=TOP, padx = 5,pady = 5) 
        self.costI5 = Pmw.EntryField(fm58, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costI5.pack( side=TOP, padx = 5,pady = 5)  
        fm58.pack(side=LEFT)

        #-7th frame - General Cost
        fm59=Frame(group52.interior())
        label57 = Label(fm59, text='General Cost').pack(side=TOP)
        label570 = Label(fm59, text='(PHP/ha)').pack(side=TOP)
        self.costG1 = Pmw.EntryField(fm59, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costG1.pack( side=TOP, padx = 5, pady = 5) 
        self.costG2 = Pmw.EntryField(fm59, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costG2.pack( side=TOP, padx = 5, pady = 5) 
        self.costG3 = Pmw.EntryField(fm59, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costG3.pack( side=TOP, padx = 5, pady = 5) 
        self.costG4 = Pmw.EntryField(fm59, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costG4.pack( side=TOP, padx = 5, pady = 5) 
        self.costG5 = Pmw.EntryField(fm59, labelpos = 'w',entry_width=10,
                    validate = {'validator': 'real', 'min' : 0, 'minstrict' : 0})
        self.costG5.pack( side=TOP, padx = 5, pady = 5)  
        fm59.pack(side=LEFT)       

        #-8th frame for comments
        fm591=Frame(group52.interior())
        label47 = Label(fm591, text=' ').pack(side=TOP)
        label370 = Label(fm591, text='comments').pack(side=TOP)
        self.comment1 = Pmw.EntryField(fm591, labelpos = 'w')
        self.comment1.pack( side=TOP, padx = 5, pady = 5) 
        self.comment2 = Pmw.EntryField(fm591, labelpos = 'w')
        self.comment2.pack( side=TOP, padx = 5, pady = 5) 
        self.comment3 = Pmw.EntryField(fm591, labelpos = 'w')
        self.comment3.pack( side=TOP, padx = 5, pady = 5) 
        self.comment4 = Pmw.EntryField(fm591, labelpos = 'w')
        self.comment4.pack( side=TOP, padx = 5, pady = 5) 
        self.comment5 = Pmw.EntryField(fm591, labelpos = 'w')
        self.comment5.pack( side=TOP, padx = 5, pady = 5)  
        fm591.pack(side=LEFT)
        
        group54 = Pmw.Group(sf_p5.interior(), tag_text = 'Run DSSAT & Display Outputs')
        group54.pack(fill = 'x', expand = 1,anchor=N, padx = 10, pady = 5)

        #2. Run CAMDT
        button52=Tkinter.Button(group54.interior(), text = 'Run DSSAT for N weather realizations',
                command = self.RunCAMDT,bg='green').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
        fm592=Frame(group54.interior())
        #Create button to execute graphs (1)yield boxplot
        button53=Tkinter.Button(fm592,text = 'I. Display Yield Estimation (Boxplot)',
                command = self.Yield_Analysis,bg='peachpuff1').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
        # Create button to execute graphs (2) water stress index
        button55=Tkinter.Button(fm592, text = 'III. Display Average Water Stress (WS)',
                command = self.WSI_Analysis,bg='peachpuff1').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
        # Create button to execute graphs (3) gross margin
        button57=Tkinter.Button(fm592, text = 'V. Display Gross Margin (Boxplot)',  
                command = self.Economic_Analysis,bg='peachpuff1').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
        fm592.pack(fill = 'x', expand = 1,side=LEFT)

        fm593=Frame(group54.interior())
        # Create button to execute graphs (2) yield exceedance curve
        button54=Tkinter.Button(fm593, text = 'II. Display Yield Estimation (Exceedance Curve)',
                command = self.Yield_exceedance,bg='peachpuff1').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
       # Create button to execute graphs (3)prob of exceeding X% water stress
        button56=Tkinter.Button(fm593, text = 'IV. Display Risk of Exceeding X% WS',
                command = self.Risk_Analysis,bg='peachpuff1').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
        # Create button to execute graphs (4) gross margin exceedance curve
        button58=Tkinter.Button(fm593, text = 'VI. Display Gross Margin (Exceedance Curve)',
                command = self.Margin_exceedance,bg='peachpuff1').pack(fill = 'x', expand = 1,side=TOP,anchor=N, padx = 10, pady = 5)
        fm593.pack(fill = 'x', expand = 1,side=LEFT)

#=========================6th  page for "Credit"
        page6 = notebook.add('*CREDIT')
        notebook.tab('*CREDIT').focus_set()

       # 1) ADD SCROLLED FRAME
        sf_p6 = Pmw.ScrolledFrame(page6) #,usehullsize=1, hull_width=700, hull_height=220)
        sf_p6.pack(padx=5, pady=3, fill='both', expand=YES)

        group61 = Pmw.Group(sf_p6.interior(), tag_text = 'Authors:')
        group61.pack(fill = 'x',anchor=N, padx = 10, pady = 5)

        self.authrs1=Label(group61.interior(), text='Eunjin Han, Ph.D. at IRI', padx=5, pady=5)
        self.authrs1.pack(side=TOP, anchor=W, expand=YES)
        self.authrs2=Label(group61.interior(), text='Amor Ines, Ph.D. at Michigan State Univ. and IRI', padx=5, pady=5)
        self.authrs2.pack(side=TOP, anchor=W, expand=YES)

        group62 = Pmw.Group(sf_p6.interior(), tag_text = 'Other Contributions:')
        group62.pack(fill = 'x',anchor=N, padx = 10, pady = 5)     

        self.cont1=Label(group62.interior(), text='James Hansen, Ph.D. at IRI', padx=5, pady=5)
        self.cont1.pack(side=TOP, anchor=W, expand=YES)
        self.cont2=Label(group62.interior(), text='Kiyoshi Honda, Ph.D. at Chubu Univ. in Japan', padx=5, pady=5)
        self.cont2.pack(side=TOP, anchor=W, expand=YES)
        self.cont3=Label(group62.interior(), text='Walter Baethgen, Ph.D. at IRI', padx=5, pady=5)
        self.cont3.pack(side=TOP, anchor=W, expand=YES)

        notebook.setnaturalsize()
#======End of creatign pages================================

     ###button original

        #Create error message
        self.val_dialog1 = Pmw.MessageDialog(parent, title = 'Error in input',
                   defaultbutton = 0,
                   message_text = 'Sim Horizon: End-year should be >= Start-year!')
        self.val_dialog1.iconname('Error in inputs')
        self.val_dialog1.withdraw()
        
        self.val_dialog2 = Pmw.MessageDialog(parent, title = 'Error in input',
                   defaultbutton = 0,
                   message_text = 'Sim Horizon: End-Month should be > Start-Month!')
        self.val_dialog2.withdraw()
        
        self.val_dialog3 = Pmw.MessageDialog(parent, title = 'Error in input',
                   defaultbutton = 0,
                   message_text = 'Sim Horizon: Simulation period is too long! (over 2 years)')
        self.val_dialog3.withdraw()

        self.val_dialog4 = Pmw.MessageDialog(parent, title = 'Error in input',
                   defaultbutton = 0,
                   message_text = 'Pred Horizon: End-year should be >= Start-year!')
        self.val_dialog4.withdraw()

        self.val_dialog5 = Pmw.MessageDialog(parent, title = 'Validating Simulation Inputs',
                   defaultbutton = 0,
                   message_text = 'Pred Horizon: End-Month should be > Start-Month!')
        self.val_dialog5.withdraw()

        self.val_dialog6 = Pmw.MessageDialog(parent, title = 'Validating Simulation Inputs',
                   defaultbutton = 0,
                   message_text = 'Pred Horizon: End-year is too far!(over 2 years)')
        self.val_dialog6.withdraw()

        self.val_dialog7 = Pmw.MessageDialog(parent, title = 'Validating Simulation Inputs',
                   defaultbutton = 0,
                   message_text = 'Pred Year should be >= Sim Year!')
        self.val_dialog7.withdraw()

        self.val_dialog8 = Pmw.MessageDialog(parent, title = 'Validating Simulation Inputs',
                   defaultbutton = 0,
                   message_text = 'Pred Month should be >= Sim Month!')
        self.val_dialog8.withdraw()

        self.val_dialog9 = Pmw.MessageDialog(parent, title = 'Validating Simulation Inputs',
                   defaultbutton = 0,
                   message_text = 'Change End-Month so that pred horizon < 3 months!')
        self.val_dialog9.withdraw()

        self.val_dialog10 = Pmw.MessageDialog(parent, title = 'Validating Simulation Inputs',
                   defaultbutton = 0,
                   message_text = 'Good Job! - No issues found!')
        self.val_dialog10.withdraw()

        self.val_dialog11 = Pmw.MessageDialog(parent, title = 'Validating Planting date',
                   defaultbutton = 0,
                   message_text = 'Planting date should be later than simulation starting date!')
        self.val_dialog11.withdraw()

        self.val_dialog12 = Pmw.MessageDialog(parent, title = 'Checking missing inputs',
                   defaultbutton = 0,
                   message_text = 'Month input is missing!')
        self.val_dialog12.withdraw()
      
        #error message when there is no scenario name
        self.writeparam_err = Pmw.MessageDialog(parent, title = 'Error message in writing param.txt',
                   defaultbutton = 0,
                   message_text = 'No scenario name available!')
        self.writeparam_err.withdraw()

        #error message when fertilizer info is missing
        self.fertilizer_err = Pmw.MessageDialog(parent, title = 'Error in Fertilizer Input',
                   defaultbutton = 0,
                   message_text = 'No Fertilizer input! Please click the Button for more detiled input on DSSAT setup2 page.')
        self.fertilizer_err.withdraw()
        #error message when cultivar info is missing
        self.cultivar_err = Pmw.MessageDialog(parent, title = 'Error in Cultivar Input',
                   defaultbutton = 0,
                   message_text = 'No Cultivar input! Please click the Button for more detiled input on DSSAT setup1 page.')
        self.cultivar_err.withdraw()
        #error message when irrigation info is missing
        self.irrigation_err = Pmw.MessageDialog(parent, title = 'Error in Irrigation Input',
                   defaultbutton = 0,
                   message_text = 'No Irrigaiotn input! Please click the Button for more detiled input on DSSAT setup2 page.')
        self.irrigation_err.withdraw()
        
        #error message when there is no number of fertilizer applications
        self.nfert_err_dialog = Pmw.MessageDialog(parent, title = 'Error in fertilizer input',
                   defaultbutton = 0,
                   message_text = 'Number of fertilizer applications should be provided in "DSSAT setup 2" tab!')
        self.nfert_err_dialog .iconname('Error in fertilizer input')
        self.nfert_err_dialog .withdraw()

        #error message when there is no number of irrigation (for only irr option=on reported dates)
        self.nirr_err_dialog = Pmw.MessageDialog(parent, title = 'Error in fertilizer input',
                   defaultbutton = 0,
                   message_text = 'Number of irrigations should be provided if "On Reported dates" is chosen in "DSSAT setup 2" tab!')
        self.nirr_err_dialog .iconname('Error in irrigation input')
        self.nirr_err_dialog .withdraw()

        #to add more specification for FResampler
        #contents for FResampler
        self.FRdialog = Pmw.Dialog(parent, title='FResampler details')
        self.SampFactor = Pmw.EntryField(self.FRdialog.interior(), labelpos = 'w',
            label_text = 'Num. of realization ( > 30):',
            validate = {'validator': 'real', 'min' : 30, 'max' : 500, 'minstrict' : 0})
        self.SampFactor.pack(fill = 'x', padx = 10, pady = 5)
        self.FRdialog.withdraw()

        #to add more specification for Stochastic Disag.
        #contents for Stochastic Disag.
        self.DisaggDialog = Pmw.Dialog(parent, title='Stochastic Downscaling details')
        #-number of realization
        self.nRealz = Pmw.EntryField(self.DisaggDialog.interior(), labelpos = 'w',
            label_text = 'Num. of realization ( > 30):',
            validate = {'validator': 'numeric', 'min' : 30, 'max' : 500, 'minstrict' : 0})
        self.nRealz.pack(fill = 'x',side=TOP,anchor=W,padx = 10, pady = 5)  
        #-checkbutton for target values to create *.MTH for DisAg.exe
        label=Tkinter.Label(self.DisaggDialog.interior(), text="*Choose target to translate SF to monthly values \n *NOTE: Chose only one or two combinations)",wraplength=300,relief=SUNKEN )
        label.pack(side=TOP,anchor=W)   
        CheckVar31 = Tkinter.IntVar()   
        CheckVar32 = Tkinter.IntVar() 
        CheckVar33 = Tkinter.IntVar()   
        b1 = Tkinter.Checkbutton(self.DisaggDialog.interior(), text = 'Rain amount',\
                                 variable = CheckVar31,onvalue = 1, offvalue = 0).pack(side=TOP,anchor=W)
        b2 = Tkinter.Checkbutton(self.DisaggDialog.interior(), text = 'Rain frequency',
                                 variable = CheckVar32,onvalue = 1, offvalue = 0).pack(side=TOP,anchor=W)   
        b3 = Tkinter.Checkbutton(self.DisaggDialog.interior(), text = 'Rain intensity',\
                                 variable = CheckVar33,onvalue = 1, offvalue = 0).pack(side=TOP,anchor=W)
        self.DisaggDialog.withdraw()
        
        #to add more specification for calibrated cultivar.
        self.cul_dialog1 = Pmw.Dialog(parent, title='Cultivar information')
        cul_list = ("PHPS01 PSB Rc82","PHME01 Mestiso 20","IB0012 IR 58","IB0014 IR 54","IB0015 IR 64")
        self.calib_cul = Pmw.ComboBox(self.cul_dialog1.interior(), label_text='Cultivar name', labelpos='wn',
                        listbox_width=15, dropdown=1,
                        #selectioncommand = self.save_culname,
                        scrolledlist_items=cul_list,
                        entryfield_entry_state=DISABLED)
        self.calib_cul.pack(fill = 'x', padx = 10, pady = 2)
        self.calib_cul.selectitem(cul_list[0])
        self.cul_dialog1.withdraw()
        
        #to add more specification for user-specified cultivar.
        self.cul_dialog2 = Pmw.Dialog(parent, title='Cultivar information')
        self.var_ID = Pmw.EntryField(self.cul_dialog2.interior(), labelpos = 'w',
            label_text = 'Cultivar ID:',validate = {'validator': 'alphanumeric', 'min' : 6, 'max' : 6, 'minstrict' : 0})
        self.var_ID.pack(fill='x', expand=1, padx=10, pady=5)
        fm_cul1=Frame(self.cul_dialog2.interior()) #,width=290)
        #-cultivar name
        Label(fm_cul1, text="Cultivar name:").pack(side=LEFT, padx=5, pady=10)
        v_name = StringVar()
        self.var_name=Entry(fm_cul1, textvariable=v_name).pack(side=LEFT)
        fm_cul1.pack(side=TOP)
        fm_cul2=Frame(self.cul_dialog2.interior()) #,width=290)
         #-ecotype code
        self.eco_code = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'Ecotype code:',validate = {'validator': 'alphanumeric', 'min' : 6, 'max' : 6, 'minstrict' : 0})
         #- P1 
        self.P1 = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'P1:', validate = {'validator': 'real', 'min' : 2, 'max' : 990, 'minstrict' : 0})
         #-P2R
        self.P2R = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'P2R:', validate = {'validator': 'real', 'min' : 2, 'max' : 990, 'minstrict' : 0})
         #- P5 
        self.P5 = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'P5:', validate = {'validator': 'real', 'min' : 2, 'max' : 990, 'minstrict' : 0})
         #-P20
        self.P2O = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'P2O:', validate = {'validator': 'real', 'min' : 2, 'max' : 20, 'minstrict' : 0})
         #- G1
        self.G1 = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'G1:',
            validate = {'validator': 'real', 'min' : 2, 'max' : 99, 'minstrict' : 0})
         #- G2
        self.G2 = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'G2:',
            validate = {'validator': 'real', 'min' : 0.01, 'max' : 0.5, 'minstrict' : 0})
         #- G3
        self.G3 = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'G3:',
            validate = {'validator': 'real', 'min' : 0.5, 'max' : 2, 'minstrict' : 0})
         #- G4
        self.G4 = Pmw.EntryField(fm_cul2, labelpos = 'w',
            label_text = 'G4:',
            validate = {'validator': 'real', 'min' : 0.5, 'max' : 2, 'minstrict' : 0})
        #aline labels
        entries = (self.eco_code, self.P1, self.P2R, self.P5, self.P2O, self.G1, self.G2, self.G3, self.G4)
        for entry in entries:
            entry.pack(fill='x', expand=1, padx=10, pady=5)
        Pmw.alignlabels(entries)
        fm_cul2.pack(side=TOP)
        self.cul_dialog2.withdraw()

        #error message when there is no scenario name
        self.Eanalysis_err = Pmw.MessageDialog(parent, title = 'Error in Economical Analysis',
                   defaultbutton = 0,
                   message_text = 'No cost/price info added!')
        self.Eanalysis_err.withdraw()
        
 #============to add more specification for fertilization information
        self.fert_dialog = Pmw.Dialog(parent, title='Fertilization Application')
        self.frt_group1 = Pmw.Group(self.fert_dialog.interior(), tag_text = '1st application')
        self.frt_group1.pack(fill = 'both',side=TOP, expand = 1, padx = 10, pady = 5)  
        self.day1 = Pmw.EntryField(self.frt_group1.interior(), labelpos = 'w',
            label_text = 'Days after planting:',
            validate = {'validator': 'numeric', 'min' : 1, 'max' : 200, 'minstrict' : 0})
        self.amount1 = Pmw.EntryField(self.frt_group1.interior(), labelpos = 'w',
            label_text = 'Amount (N, kg/ha):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 100, 'minstrict' : 0})
        #-fertilizer material
        material_list = ("FE005(Urea)","FE001(Ammonium nitrate)","None")
        self.fert_mat1 = Pmw.ComboBox(self.frt_group1.interior(),label_text='fertilizer material:',labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=material_list,
                        entryfield_entry_state=DISABLED)
        first =material_list[2]
        self.fert_mat1.selectitem(first)
        #-fertilizer application method
        apply_list = ("AP012(Broadcast on flooded/saturated soil, 15% in soil)","AP013(Broadcast on flooded/saturated soil, 30% in soil)","None")
        self.fert_app1 = Pmw.ComboBox(self.frt_group1.interior(),label_text='application method:',labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=apply_list,
                        entryfield_entry_state=DISABLED)
        first =apply_list[2]
        self.fert_app1.selectitem(first)
        #aline labels
        entries = (self.day1, self.amount1, self.fert_mat1, self.fert_app1)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)
        #2nd fertilizer application
        self.frt_group2 = Pmw.Group(self.fert_dialog.interior(), tag_text = '2nd application')
        self.frt_group2.pack(fill = 'both', side=TOP, expand = 1, padx = 10, pady = 5)  
        self.day2 = Pmw.EntryField(self.frt_group2.interior(), labelpos = 'w',
            label_text = 'Days after planting:',
            validate = {'validator': 'numeric', 'min' : 1, 'max' : 200, 'minstrict' : 0})
        self.amount2 = Pmw.EntryField(self.frt_group2.interior(), labelpos = 'w',
            label_text = 'Amount(N, kg/ha):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 100, 'minstrict' : 0})
        #-fertilizer material
        self.fert_mat2 = Pmw.ComboBox(self.frt_group2.interior(),label_text='fertilizer material:',labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=material_list,
                        entryfield_entry_state=DISABLED)
        first =material_list[2]
        self.fert_mat2.selectitem(first)
        #-fertilizer application method
        self.fert_app2 = Pmw.ComboBox(self.frt_group2.interior(),label_text='application method:',labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=apply_list,
                        entryfield_entry_state=DISABLED)
        first =apply_list[2]
        self.fert_app2.selectitem(first)
        #aline labels
        entries = (self.day2, self.amount2, self.fert_mat2, self.fert_app2)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)
        #3rd fertilizer application
        self.frt_group3 = Pmw.Group(self.fert_dialog.interior(), tag_text = '3rd application')
        self.frt_group3.pack(fill = 'both',  side=TOP, expand = 1, padx = 10, pady = 5)  
        self.day3 = Pmw.EntryField(self.frt_group3.interior(), labelpos = 'w',
            label_text = 'Days after planting:',
            validate = {'validator': 'numeric', 'min' : 1, 'max' : 200, 'minstrict' : 0})
        self.amount3 = Pmw.EntryField(self.frt_group3.interior(), labelpos = 'w',
            label_text = 'Amount(N, kg/ha):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 100, 'minstrict' : 0})
        #-fertilizer material
        self.fert_mat3 = Pmw.ComboBox(self.frt_group3.interior(),label_text='fertilizer material:',labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=material_list,
                        entryfield_entry_state=DISABLED)
        first =material_list[2]
        self.fert_mat3.selectitem(first)
        #-fertilizer application method
        self.fert_app3 = Pmw.ComboBox(self.frt_group3.interior(),label_text='application method:',labelpos='wn',
                        listbox_width=15, dropdown=1,
                        scrolledlist_items=apply_list,
                        entryfield_entry_state=DISABLED)
        first =apply_list[2]
        self.fert_app3.selectitem(first)
        #aline labels
        entries = (self.day3, self.amount3, self.fert_mat3, self.fert_app3)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)
        self.fert_dialog.withdraw()

 #============to add more specification for automatic irrigation(auto when required)
        self.AutoIrrDialog = Pmw.Dialog(parent, title='Automatic irrigation when required')
        self.irr_depth = Pmw.EntryField(self.AutoIrrDialog.interior(), labelpos = 'w',
            label_text = 'Management depth(cm):',validate = {'validator': 'real', 'min' : 1, 'max' : 200, 'minstrict' : 0},
            value = '30')
        #-threshold
        self.irr_thresh = Pmw.EntryField(self.AutoIrrDialog.interior(), labelpos = 'w',
            label_text = 'Threshold(% of maximum available water triggering irrigation ):', validate = {'validator': 'real', 'min' : 1, 'max' : 100, 'minstrict' : 0},
            value = '50')
         #- Efficiency fraction 
        self.eff_fraction = Pmw.EntryField(self.AutoIrrDialog.interior(), labelpos = 'w',
            label_text = 'Efficiency fraction:', validate = {'validator': 'real', 'min' : 0, 'max' : 1, 'minstrict' : 0},
            value = '1')
        #aline labels
        entries = (self.irr_depth, self.irr_thresh, self.eff_fraction)
        for entry in entries:
            entry.pack(fill='x', expand=1, padx=10, pady=5)
        Pmw.alignlabels(entries)
        self.AutoIrrDialog.withdraw()
 #============to add more specification for automatic irrigation(Fixed amount automatic)
        self.AutoIrrDialog2 = Pmw.Dialog(parent, title='Fixed amount automatic')
        self.irr_depth2 = Pmw.EntryField(self.AutoIrrDialog2.interior(), labelpos = 'w',
            label_text = 'Management depth(cm):',validate = {'validator': 'real', 'min' : 1, 'max' : 200, 'minstrict' : 0},
            value = '30')
        #-threshold
        self.irr_thresh2 = Pmw.EntryField(self.AutoIrrDialog2.interior(), labelpos = 'w',
            label_text = 'Threshold(% of max available):', validate = {'validator': 'real', 'min' : 1, 'max' : 100, 'minstrict' : 0},
            value = '50')
         #- Efficiency fraction 
        self.eff_fraction2 = Pmw.EntryField(self.AutoIrrDialog2.interior(), labelpos = 'w',
            label_text = 'Efficiency fraction:', validate = {'validator': 'real', 'min' : 0, 'max' : 1, 'minstrict' : 0},
            value = '1')
         #-amount
        self.irr_amount = Pmw.EntryField(self.AutoIrrDialog2.interior(), labelpos = 'w',
            label_text = 'Amount (mm):', validate = {'validator': 'real', 'min' : 1, 'max' : 500, 'minstrict' : 0})
 #aline labels
        entries = (self.irr_depth2, self.irr_thresh2, self.eff_fraction2, self.irr_amount)
        for entry in entries:
            entry.pack(fill='x', expand=1, padx=10, pady=5)
        Pmw.alignlabels(entries)
        self.AutoIrrDialog2.withdraw()

 #============to add more specification for Reported irrigation
        self.ReptIrrDialog = Pmw.Dialog(parent, title='Irrigation on Report Dates')
        self.irr_group0 = Pmw.Group(self.ReptIrrDialog.interior(), tag_text = 'Puddling')
        self.irr_group0.pack(fill = 'both',side=TOP, expand = 1, padx = 10, pady = 5)  
        self.pud_date = Pmw.EntryField(self.irr_group0.interior(), labelpos = 'w',
            label_text = 'Puddling date(YYDOY):',
            validate = {'validator': 'alphanumeric', 'min' : 5, 'max' : 5, 'minstrict' : 0},value = '09346')
##        self.puddling = Pmw.EntryField(self.irr_group0.interior(), labelpos = 'w',
##            label_text = 'Puddling:',
##            validate = {'validator': 'numeric', 'min' : 0, 'max' : 1, 'minstrict' : 0},value = '0')
        self.pec_rate = Pmw.EntryField(self.irr_group0.interior(), labelpos = 'w',
            label_text = 'Percolation rate(mm/day):',
            validate = {'validator': 'real', 'min' : 0, 'max' : 100, 'minstrict' : 0},value = '2')
        #aline labels
        entries = (self.pud_date,self.pec_rate)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)
        #1st irrigation
        self.irr_group1 = Pmw.Group(self.ReptIrrDialog.interior(), tag_text = '1st irrigation')
        self.irr_group1.pack(fill = 'both',side=TOP, expand = 1, padx = 10, pady = 5)  
        self.irr_day1 = Pmw.EntryField(self.irr_group1.interior(), labelpos = 'w',
            label_text = 'Irrigation date(YYDOY):',value = 'None',   #none value is used as a flag
            validate = {'validator': 'alphanumeric', 'min' : 5, 'max' : 5, 'minstrict' : 0})
        self.height1 = Pmw.EntryField(self.irr_group1.interior(), labelpos = 'w',
            label_text = 'Bund height(mm):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 1000, 'minstrict' : 0},value = '100')
        #-flood depth
        self.flood1 = Pmw.EntryField(self.irr_group1.interior(), labelpos = 'w',
            label_text = 'Flood depth (mm):',
            validate = {'validator': 'real', 'min' : 0, 'max' : 1000, 'minstrict' : 0},value = '30')
        self.label_ir0= Label(self.irr_group1.interior(), 
            text='Constant flood depth? ',anchor=W) 
        self.label_ir1= Label(self.irr_group1.interior(), 
            text='  -Yes: Maintain constant specified flood depth until next irrigation record.',anchor=W) 
        self.label_ir2= Label(self.irr_group1.interior(), 
            text='  -No: Regular irrigation (bunded or upland)',anchor=W)
        #aline labels
        entries = (self.irr_day1, self.height1, self.flood1,self.label_ir0,self.label_ir1,self.label_ir2)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)
        
        floodVar1 = Tkinter.IntVar()
        constant_fld_option=[('Yes', 0), ('No', 1)]
        for text, value in constant_fld_option:
            Radiobutton(self.irr_group1.interior(), text=text, value=value, variable=floodVar1).pack(side=LEFT,expand=YES)
        floodVar1.set(0)  #By default- constant flooding depth
        
        #2nd irrigation
        self.irr_group2 = Pmw.Group(self.ReptIrrDialog.interior(), tag_text = '2nd irrigation')
        self.irr_group2.pack(fill = 'both', side=TOP, expand = 1, padx = 10, pady = 5)  
        self.irr_day2 = Pmw.EntryField(self.irr_group2.interior(), labelpos = 'w',
            label_text = 'Irrigation date(YYDOY):',value = 'None',
            validate = {'validator': 'alphanumeric', 'min' : 5, 'max' : 5, 'minstrict' : 0})
        self.height2 = Pmw.EntryField(self.irr_group2.interior(), labelpos = 'w',
            label_text = 'Bund height(mm):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 1000, 'minstrict' : 0},value = '150')
        #-flood depth
        self.flood2 = Pmw.EntryField(self.irr_group2.interior(), labelpos = 'w',
            label_text = 'Flood depth (mm):',
            validate = {'validator': 'real', 'min' : 0, 'max' : 1000, 'minstrict' : 0},value = '50')   
        self.label_ir4= Label(self.irr_group2.interior(), 
            text='Constant flood depth? ',anchor=W) 
        entries = (self.irr_day2, self.height2, self.flood2,self.label_ir4)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)

        floodVar2 = Tkinter.IntVar()
        for text, value in constant_fld_option:
            Radiobutton(self.irr_group2.interior(), text=text, value=value, variable=floodVar2).pack(side=LEFT,expand=YES)
        floodVar2.set(0)  #By default- constant flooding depth

        #3rd irrigation
        self.irr_group3 = Pmw.Group(self.ReptIrrDialog.interior(), tag_text = '3rd irrigation')
        self.irr_group3.pack(fill = 'both', side=TOP, expand = 1, padx = 10, pady = 5)  
        self.irr_day3 = Pmw.EntryField(self.irr_group3.interior(), labelpos = 'w',
            label_text = 'Irrigation date(YYDOY):',value = 'None',
            validate = {'validator': 'alphanumeric', 'min' : 5, 'max' : 5, 'minstrict' : 0})
        self.height3 = Pmw.EntryField(self.irr_group3.interior(), labelpos = 'w',
            label_text = 'Bund height(mm):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 1000, 'minstrict' : 0})
        #-flood depth
        self.flood3 = Pmw.EntryField(self.irr_group3.interior(), labelpos = 'w',
            label_text = 'Flood depth (mm):',
            validate = {'validator': 'real', 'min' : 1, 'max' : 1000, 'minstrict' : 0})   
        self.label_ir5= Label(self.irr_group3.interior(), 
            text='Constant flood depth? ',anchor=W) 
        #aline labels
        entries = (self.irr_day3, self.height3, self.flood3,self.label_ir5)
        for entry in entries:
            entry.pack(fill='x', side=TOP, expand=1, padx=10, pady=2)
        Pmw.alignlabels(entries)
        floodVar3 = Tkinter.IntVar()
        for text, value in constant_fld_option:
            Radiobutton(self.irr_group3.interior(), text=text, value=value, variable=floodVar3).pack(side=LEFT,expand=YES)
        floodVar3.set(0)  #By default- constant flooding depth

        self.ReptIrrDialog.withdraw()
 #============
    def empty_downscale_label(self):
        self.label12.configure(text='Not added')
        self.label22.configure(text='Not added')
        self.label26.configure(text='Not added')
        self.label28.configure(text='Not added')
        self.label20.configure(text='Not added')

##    def empty_scf_label(self):
##        self.label32.configure(text='Not added')
##        self.label34.configure(text='Not added')
##        self.label36.configure(text='Not added')
##        self.label42.configure(text='Not added')
##        self.label44.configure(text='Not added')
##        self.label46.configure(text='Not added')

    def empty_fert_label(self):
        self.label006.configure(text='Not added')
        self.label007.configure(text='Not added')
        self.label008.configure(text='Not added')
        self.label009.configure(text='Not added')
        self.label011.configure(text='Not added')
        self.label012.configure(text='Not added')
        self.label013.configure(text='Not added')
        self.label014.configure(text='Not added')
        self.label016.configure(text='Not added')
        self.label017.configure(text='Not added')
        self.label018.configure(text='Not added')
        self.label019.configure(text='Not added')
        
    def empty_irrig_label(self):
        self.label402.configure(text='Not added')
        self.label404.configure(text='Not added')
        self.label408.configure(text='Not added')
        self.label121.configure(text='Not added')
       # self.label123.configure(text='Not added')
        self.label125.configure(text='Not added')
        self.label105.configure(text='Not added')
        self.label106.configure(text='Not added')
        self.label107.configure(text='Not added')
        self.label1071.configure(text='Not added')
        self.label109.configure(text='Not added')
        self.label110.configure(text='Not added')
        self.label111.configure(text='Not added')
        self.label1111.configure(text='Not added')
        self.label113.configure(text='Not added')
        self.label114.configure(text='Not added')
        self.label115.configure(text='Not added')
        self.label1151.configure(text='Not added')
        
    def writeParam1(self):
        #cultivar info
        if self.label362.cget("text") == 'Not added':
            self.cultivar_err.activate()
        #fertilizer info
        if Fbutton1.get() == 0 :  #fertilizer button is selected
            if self.label006.cget("text") == 'Not added':
                self.fertilizer_err.activate()
        #irrigation info
        if IRbutton.get() == 0 or IRbutton.get() == 1:  #Automatic when required is selected
            if self.label402.cget("text") == 'Not added':
                self.irrigation_err.activate()
        if IRbutton.get() == 2:  #On Reported dates is selected
            if self.label105.cget("text") == 'Not added':
                self.irrigation_err.activate()
        if self.name1.getvalue() == "":
            self.writeparam_err.activate()
        else:
            sname=self.name1.getvalue()
            param_fname=Wdir_path.replace("/","\\") + "\\param_"+sname+".txt"  
            self.label54.configure(text='RI',background='honeydew1')
            self.writeParam_main(param_fname)

    def writeParam2(self):
        #cultivar info
        if self.label362.cget("text") == 'Not added':
            self.cultivar_err.activate()
        #fertilizer info
        if Fbutton1.get() == 0 :  #fertilizer button is selected
            if self.label006.cget("text") == 'Not added':
                self.fertilizer_err.activate()
        #irrigation info
        if IRbutton.get() == 0 or IRbutton.get() == 1:  #Automatic when required is selected
            if self.label402.cget("text") == 'Not added':
                self.irrigation_err.activate()
        if IRbutton.get() == 2:  #On Reported dates is selected
            if self.label105.cget("text") == 'Not added':
                self.irrigation_err.activate()

        if self.name2.getvalue() == "":
            self.writeparam_err.activate()
        else:
            sname=self.name2.getvalue()
            param_fname=Wdir_path.replace("/","\\") + "\\param_"+sname+".txt"  
            self.label55.configure(text='RI',background='honeydew1')
            self.writeParam_main(param_fname)
            
    def writeParam3(self):
        #cultivar info
        if self.label362.cget("text") == 'Not added':
            self.cultivar_err.activate()
        #fertilizer info
        if Fbutton1.get() == 0 :  #fertilizer button is selected
            if self.label006.cget("text") == 'Not added':
                self.fertilizer_err.activate()
        #irrigation info
        if IRbutton.get() == 0 or IRbutton.get() == 1:  #Automatic when required is selected
            if self.label402.cget("text") == 'Not added':
                self.irrigation_err.activate()
        if IRbutton.get() == 2:  #On Reported dates is selected
            if self.label105.cget("text") == 'Not added':
                self.irrigation_err.activate()

        if self.name3.getvalue() == "":
            self.writeparam_err.activate()
        else:
            sname=self.name3.getvalue()
            param_fname=Wdir_path.replace("/","\\") + "\\param_"+sname+".txt"  
            self.label56.configure(text='RI',background='honeydew1')
            self.writeParam_main(param_fname)

    def writeParam4(self):
        #cultivar info
        if self.label362.cget("text") == 'Not added':
            self.cultivar_err.activate()
        #fertilizer info
        if Fbutton1.get() == 0 :  #fertilizer button is selected
            if self.label006.cget("text") == 'Not added':
                self.fertilizer_err.activate()
        #irrigation info
        if IRbutton.get() == 0 or IRbutton.get() == 1:  #Automatic when required is selected
            if self.label402.cget("text") == 'Not added':
                self.irrigation_err.activate()
        if IRbutton.get() == 2:  #On Reported dates is selected
            if self.label105.cget("text") == 'Not added':
                self.irrigation_err.activate()

        if self.name4.getvalue() == "":
            self.writeparam_err.activate()
        else:
            sname=self.name4.getvalue()
            param_fname=Wdir_path.replace("/","\\") + "\\param_"+sname+".txt"  
            self.label57.configure(text='RI',background='honeydew1')
            self.writeParam_main(param_fname)

    def writeParam5(self):
        #cultivar info
        if self.label362.cget("text") == 'Not added':
            self.cultivar_err.activate()
        #fertilizer info
        if Fbutton1.get() == 0 :  #fertilizer button is selected
            if self.label006.cget("text") == 'Not added':
                self.fertilizer_err.activate()
        #irrigation info
        if IRbutton.get() == 0 or IRbutton.get() == 1:  #Automatic when required is selected
            if self.label402.cget("text") == 'Not added':
                self.irrigation_err.activate()
        if IRbutton.get() == 2:  #On Reported dates is selected
            if self.label105.cget("text") == 'Not added':
                self.irrigation_err.activate()

        if self.name5.getvalue() == "":
            self.writeparam_err.activate()
        else:
            sname=self.name5.getvalue()
            param_fname=Wdir_path.replace("/","\\") + "\\param_"+sname+".txt"  
            self.label58.configure(text='RI',background='honeydew1')
            self.writeParam_main(param_fname)

    def writeParam_main(self,param_fname):
        print 'writeParam_main: scenario name1 is  ', param_fname
        f = open(param_fname,"w") #opens file 
        working_dir=Wdir_path.replace("/","\\")
        f.write("!Working directory where DSSAT4.5 is installed and weather or soil files can be found \n")
        f.write("Directory:  " + working_dir + "\n")
        f.write("!  \n")
        f.write("!==(I) Simulation set up \n")
        f.write("!(1)Simulation mode (hindcast(0) or forecst(1)?) \n")
        f.write("sim_mode: "+str(CheckVar.get())+"\n")
        f.write("! \n")
        f.write("!(2)Simulation horizon \n")
        f.write("StartYear: "+startyear2.getvalue()+"\n")
        f.write("StartMonth: " + self.startmonth2.getvalue()[0][0:2]+"\n")
        #f.write("StartMonth: "+str(month21)+"\n")
        f.write("EndYear: "+endyear2.getvalue()+"\n")
        f.write("EndMonth: "+self.endmonth2.getvalue()[0][0:2]+"\n")
        f.write("! \n")
        f.write("!(3)Prediction horizon \n")
        f.write("StartYear: "+startyear3.getvalue()+"\n")
        f.write("StartMonth: "+self.startmonth3.getvalue()[0][0:2]+"\n")
        f.write("EndYear: "+endyear3.getvalue()+"\n")
        f.write("EndMonth: "+ self.endmonth3.getvalue()[0][0:2]+"\n")
        f.write("! \n")
        f.write("!(3)Planting date \n")
        f.write("Planting_date: "+planting_date.getvalue()+ "\n")
        f.write("!--------------------------- \n")
        f.write("!==(II) Seasonal  Forecast \n")
        f.write("!(1)Downscaling method: FResampler(0), PredWTD(1) \n")
        f.write("Temp_Downscaling: "+ str(CheckVar21.get())+"\n")
        f.write("!(1-1)if from FResampler(0) \n")
        if(CheckVar21.get() == 0):
            temp=float(self.SampFactor.getvalue())*0.01
            f.write("Factor(0-1_or>): "+str(temp)+ "\n")
            f.write("!(1-2)if from PredWTD(1)- Number of Realizations - Weather genertions \n")
            f.write("nRealz:  100  \n")
            f.write("!Flag for target forecast (Rainfall amount, frequency, intensity) \n")
            f.write("!e.g. combination of frequency and intensity(1/0=select/no-select)=>011 \n")
            f.write("Flag: 100  \n")
        else:
            f.write("Factor(0-1_or>):  1 \n")
            f.write("!(1-2)if from PredWTD(1)- Number of Realizations - Weather genertions \n")
            f.write("nRealz: " + self.nRealz.getvalue()+"\n")
            f.write("!Flag for target forecast (Rainfall amount, frequency, intensity) \n")
            f.write("!e.g. combination of frequency and intensity(1/0=select/no-select)=>011 \n")
            f.write("Flag: "+str(CheckVar31.get())+ str(CheckVar32.get())+str(CheckVar33.get())+ "\n")
        f.write("! \n")
        f.write("!(2)How to get seasonal forecast: from CPT(0), user-specified(1) \n")
     ##  f.write("Seasonal_forecast: "+str(CheckVar22.get())+"\n")
        f.write("Seasonal_forecast: 1 \n")
        f.write("!(2-1)if from CPT(0) \n")
##        if(CheckVar22.get() == 0):  #FResampler
##            f.write("CPT_file: "+CPT_path+ "\n")
##            f.write("Latitude: "+self.latitude.getvalue()+ "\n")        
##            f.write("Longitude: "+self.longitude.getvalue()+ "\n")  
##            f.write("!(2-2)if user-defined(1) \n")   
##            f.write("Below_Normal: 33 \n")         
##            f.write("Near_Normal:  34 \n")    
##            f.write("Above_Normal: 33 \n")    
##        else:  
        # CheckVar22 = 1 always because I deactivated CPT input
        f.write("CPT_file: C:\IRI\PH\Philippines Forecasts\OND_2009_Fcst_Probs.txt \n")
        f.write("Latitude:   13.5 \n")        
        f.write("Longitude:   123.0 \n")        
        f.write("!(2-2)if user-defined(1) \n")   
        f.write("Below_Normal: "+self.BN.getvalue()+" \n")
        Near_normal=100-float(self.BN.getvalue())-float(self.AN.getvalue())         
        f.write("Near_Normal: "+str(Near_normal)+" \n")    
        f.write("Above_Normal: "+self.AN.getvalue()+" \n")
        f.write("!--------------------------- \n")
        f.write("!==(III) DSSAT set up \n")
        f.write("Crop_type: Rice \n")
        f.write("!Planting method: dry seed (0) or transplanting (1) \n")
        f.write("Plt_method: "+str(Rbutton2.get())+" \n")
        f.write("!Planting detail \n")
        f.write("!Planting distribution: Hills (H), Rows (R), Brocast(B) \n")
        PLDS=self.plt_dist.getvalue()[0][0:1] #"Hills", "Rows", "Rows"
        f.write("PLDS: "+PLDS+ " \n")
        f.write("!Planting population at seedling, plant/m2 \n")
        f.write("PPOP: "+self.ppop_seed.getvalue()+ " \n")
        f.write("!Planting population at emergence, plant/m2 \n")
        f.write("PPOE: "+self.ppop_emer.getvalue()+ " \n")
        f.write("!Planting Row spacing, cm \n")
        f.write("PLRS: "+self.row_space.getvalue()+ " \n")
        f.write("!Row Direction , degrees from North \n")
        f.write("PLRD: "+self.row_dir.getvalue()+ " \n")
        f.write("!Planting depth , cm \n")
        f.write("PLDP: "+self.plt_depth.getvalue()+ " \n")
        f.write("!  \n")
        f.write("!Choose weather station \n")
        f.write("Station_name(4char): "+self.Wstation.getvalue()[0][0:4]+ " \n")
        f.write("!  \n")
        f.write("!(2) soil  \n")
        f.write("!Major soil types: SCL1(WI_ANPH007), LoamySand(WI_ANPH008), Clay(WI_VRPH021),Clay2(WI_VRPH043), SCL2(WI_CMPH009) \n")
        soil = self.soil_type.getvalue()[0][-11:-1]  #"SCL(WI_ANPH007), "LoamySand(WI_ANPH008)", "Clay(WI_VRPH021)"),"Clay(WI_VRPH043)","SCL2(WI_CMPH009)"):
        f.write("Soil_type: "+ soil + " \n")
        f.write("!Rooting depth: shallow(2), medium(1) and deep (0)  \n")
        if(self.rt_depth.getvalue()[0][0:1] == "d"): #deep"
            root_depth=0
        elif(self.rt_depth.getvalue()[0][0:1] == "m"): #medium"
            root_depth=1
        elif(self.rt_depth.getvalue()[0][0:1] == "s"): #shallow
            root_depth=2
        f.write("Rooting_depth: "+ str(root_depth)+ " \n")
        f.write("!  \n")
        f.write("!(3)Cultivar: Calibrated (0) ((short duration, medium, long, drought-tolerant)or user-defined(1) \n")
        f.write("Cultivar_type: "+ str(cul_Rbutton.get())+ " \n")
        if(cul_Rbutton.get() == 0):  #Calibrated cultivar 
            f.write("VAR_num: " + self.label362.cget("text")+ "\n")
            f.write("VAR_name: " + self.label364.cget("text")+ "\n")          
            f.write("!(3-1) if user-defined(4), specify cultivar parameters \n")   
            f.write("VAR_num:    \n")         
            f.write("VAR_name:   \n")    
            f.write("ECO_num:   \n")    
            f.write("P1:   \n")         
            f.write("P2R:  \n")    
            f.write("P5:  \n")    
            f.write("P2O:  \n")         
            f.write("G1: \n")    
            f.write("G2: \n")  
            f.write("G3:  \n")    
            f.write("G4:  \n")    
        else:
            f.write("VAR_num: NaN  \n")
            f.write("VAR_name: NaN  \n")        
            f.write("!(3-1) if user-defined(4), specify cultivar parameters \n")  
            f.write("VAR_num: "+self.label302.cget("text")+ "\n")       
            f.write("VAR_name: "+self.label304.cget("text")+ "\n") 
            f.write("ECO_num: "+self.label306.cget("text")+ "\n")    
            f.write("P1: "+self.label308.cget("text")+ "\n")         
            f.write("P2R: "+self.label310.cget("text")+ "\n")  
            f.write("P5: "+self.label312.cget("text")+ "\n")    
            f.write("P2O: "+self.label314.cget("text")+ "\n")         
            f.write("G1: "+self.label316.cget("text")+ "\n")  
            f.write("G2: "+self.label318.cget("text")+ "\n")   
            f.write("G3: "+self.label320.cget("text")+ "\n")     
            f.write("G4: "+self.label322.cget("text")+ "\n") 
        f.write("!  \n")
        f.write("!(4)Fertilizer: Yes(0), or No(1) -No automatic option \n")
        f.write("Fertilization: "+ str(Fbutton1.get())+ " \n")
        f.write("!(4-1) if Yes, 'days after sawing', 'amount','material','applications' \n")
        print 'fertilization opt: ', Fbutton1.get()
        if(Fbutton1.get() == 0):  #fertilizer applied
            print 'Number_applications: ', self.nfertilizer.getvalue()
            if self.nfertilizer.getvalue() == '':  #no of fertilization is required
                  self.nfert_err_dialog.activate()
                # self.val_dialog1.activate()
            f.write("Number_applications: "+self.nfertilizer.getvalue()+ "\n")  
            f.write("Fertilizer_1(days): "+self.label006.cget("text")+ "\n")    
            f.write("Fertilizer_1(amount): "+self.label007.cget("text")+ "\n")         
            f.write("Fertilizer_1(material): "+self.label008.cget("text")+ "\n")  
            f.write("Fertilizer_1(application): "+self.label009.cget("text")+ "\n")  
            f.write("Fertilizer_2(days): "+self.label011.cget("text")+ "\n")  
            f.write("Fertilizer_2(amount): "+self.label012.cget("text")+ "\n")        
            f.write("Fertilizer_2(material): "+self.label013.cget("text")+ "\n")     
            f.write("Fertilizer_2(application): "+self.label014.cget("text")+ "\n")   
            f.write("Fertilizer_3(days): "+self.label016.cget("text")+ "\n")     
            f.write("Fertilizer_3(amount): "+self.label017.cget("text")+ "\n")  
            f.write("Fertilizer_3(material): "+self.label018.cget("text")+ "\n")    
            f.write("Fertilizer_3(application): "+self.label019.cget("text")+ "\n")  
        else:  #no fertilizer
            f.write("Number_applications: \n")         
            f.write("Fertilizer_1(days): \n")    
            f.write("Fertilizer_1(amount): \n")    
            f.write("Fertilizer_1(material): \n")         
            f.write("Fertilizer_1(application): \n")    
            f.write("Fertilizer_2(days): \n")    
            f.write("Fertilizer_2(amount): \n")         
            f.write("Fertilizer_2(material): \n")    
            f.write("Fertilizer_2(application): \n")  
            f.write("Fertilizer_3(days): \n")    
            f.write("Fertilizer_3(amount): \n") 
            f.write("Fertilizer_3(material): \n")    
            f.write("Fertilizer_3(application): \n") 
        f.write("!  \n")
        f.write("!(5) Irrigation: Automatic when required(0),on reported dates (2), no irrigation(3) \n")
        f.write("Irrigation_method: "+ str(IRbutton.get())+ " \n")
        f.write("!(5-1)if Automatic(0) \n")
        if(IRbutton.get() == 0):  #Automatic when required
            f.write("Management_depth(cm):  "+self.label402.cget("text")+ "\n")  
            f.write("Threshold: "+self.label404.cget("text")+ "\n")    
            f.write("EndPoint: 100 \n")  #"+self.label406.cget("text")+ "\n")         
            f.write("Efficiency_Fraction: "+self.label408.cget("text")+ "\n")  
            f.write("End_of_Application: IB001 \n") #"+self.label410.cget("text")+ "\n")  
            f.write("Method: IR001 \n") #"+self.label412.cget("text")+ "\n")  
            f.write("Amount: \n")  
            f.write("!(5-2)if Manual  \n")  
            f.write("Number_irrigation: \n")   
            f.write("!(5-2-1) if transplanted \n")   
            f.write("Puddling_date: \n")   
            f.write("Puddling: \n")   
            f.write("!whether transplanted or dry seeds \n")   
            f.write("Percolation_rate: \n")   
            f.write("First_irrigation_date: \n")
            f.write("Bund_height_1: \n")
            f.write("Flood_depth_1: \n")  
            f.write("Constant_depth1?: Not added  \n")   
            f.write("Second_irrigation_date: \n")   
            f.write("Bund_height_2: \n")
            f.write("Flood_depth_2: \n")  
            f.write("Constant_depth2?: Not added   \n")   
            f.write("Third_irrigation_date: \n")   
            f.write("Bund_height_3: \n")
            f.write("Flood_depth_3: \n") 
            f.write("Constant_depth3?: Not added   \n")  
        elif(IRbutton.get() == 2):  # irrigation on report dates
            print 'Number_irrigation(on reported date): ', self.nirrigation.getvalue()
            if self.nirrigation.getvalue() == '':  #no of fertilization is required
                  self.nirr_err_dialog.activate()
            f.write("Management_depth(cm): \n") 
            f.write("Threshold: \n")   
            f.write("EndPoint: \n")        
            f.write("Efficiency_Fraction: \n") 
            f.write("End_of_Application: \n") 
            f.write("Method: \n") 
            f.write("Amount: \n")  
            f.write("!(5-2)if Manual \n")  
            f.write("Number_irrigation:  "+self.nirrigation.getvalue()+ "\n")     
            f.write("!(5-2-1) if transplanted  \n")   
            f.write("Puddling_date: "+self.label121.cget("text")+ "\n")     
            f.write("Puddling:  0 \n") #"+self.label123.cget("text")+ "\n")    
            f.write("!whether transplanted or dry seeds \n")   
            f.write("Percolation_rate: "+self.label125.cget("text")+ "\n")    
            f.write("First_irrigation_date: "+self.label105.cget("text")+ "\n")  
            f.write("Bund_height_1: "+self.label106.cget("text")+ "\n")    
            f.write("Flood_depth_1: "+self.label107.cget("text")+ "\n")
            f.write("Constant_depth1?: "+self.label1071.cget("text")+ "\n")   
            f.write("Second_irrigation_date: "+self.label109.cget("text")+ "\n")     
            f.write("Bund_height_2: "+self.label110.cget("text")+ "\n")  
            f.write("Flood_depth_2: "+self.label111.cget("text")+ "\n")
            f.write("Constant_depth2?: "+self.label1111.cget("text")+ "\n") 
            f.write("Third_irrigation_date: "+self.label113.cget("text")+ "\n")     
            f.write("Bund_height_3: "+self.label114.cget("text")+ "\n")  
            f.write("Flood_depth_3: "+self.label115.cget("text")+ "\n")
            f.write("Constant_depth3?: "+self.label1151.cget("text")+ "\n") 
        else:  #no irrigation
            f.write("Management_depth(cm):   \n") 
            f.write("Threshold:   \n")   
            f.write("EndPoint:   \n")        
            f.write("Efficiency_Fraction:   \n") 
            f.write("End_of_Application:  \n") 
            f.write("Method:   \n") 
            f.write("Amount: \n")  
            f.write("!(5-2)if Manual  \n")   
            f.write("Number_irrigation:  \n")   
            f.write("!(5-2-1) if transplanted  \n")   
            f.write("Puddling_date:  \n")   
            f.write("Puddling:   \n")   
            f.write("!whether transplanted or dry seeds \n")   
            f.write("Percolation_rate:  \n")   
            f.write("First_irrigation_date: \n")   
            f.write("Bund_height_1:   \n")  
            f.write("Flood_depth_1:   \n")
            f.write("Constant_depth1?: \n")
            f.write("Second_irrigation_date:  \n")   
            f.write("Bund_height_2: \n")   
            f.write("Flood_depth_2:  \n")
            f.write("Constant_depth2?: \n")
            f.write("Third_irrigation_date:  \n")   
            f.write("Bund_height_3: \n")   
            f.write("Flood_depth_3: \n")
            f.write("Constant_depth3?: \n")
        f.write("!---------------------------  \n")
        f.write("!==(IV) Output analysis \n")
        f.write("WSI_threshold: "+self.wsi_threshold.getvalue()+ "\n")  

        f.close()

    def RunCAMDT(self):
        entries = ("AveStress.txt", "SumStress.txt", "YIELD.txt","PgtTHRESHPct.txt",
                   "WSGD.txt", "WSGD_ana.txt", "WSGD_obs.txt", "PlantGro.OUT","Evaluate.OUT",
                   "ET.OUT","OVERVIEW.OUT","PlantN.OUT","SoilNi.OUT","INFO.OUT","Mulch.OUT","RunList.OUT",
                   "SoilNiBal.OUT","SoilNoBal.OUT","SoilTemp.OUT","SoilWat.OUT","SoilWatBal.OUT",
                   "SolNBalSum.OUT","Summary.OUT","Weather.OUT") #,"WARNING.OUT"
        os.chdir(Wdir_path) #change directory
        param_txt ="param_"+self.name1.getvalue()+".txt"  
        if os.path.isfile(param_txt):
            #Delete *.WTD from previous runs
            WTD_names=self.Wstation.getvalue()[0][0:4]+"0*.WTD"
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, WTD_names):
                   # print file
                    try:
                          os.remove(file)
                    except Exception,e:
                          print e

            print 'new directory is', os.getcwd()
            ##args = "CAMDT_PH_exe " + param_txt
            args = "CAMDT_PH " + param_txt
            #===Run executable with argument
            subprocess.call(args) #, stdout=FNULL, stderr=FNULL, shell=False)
            #create a new folder to save outputs of the target scenario
            new_folder=self.name1.getvalue()+"_output"
            if os.path.exists(new_folder):
                shutil.rmtree(new_folder)   #remove existing folder
            os.makedirs(new_folder)
            #copy outputs to the new folder
            dest_dir=Wdir_path + "\\"+new_folder
            for entry in entries:
                if os.path.isfile(entry):
                    shutil.move(entry, dest_dir)
            #move SNX file to output subfolder (EJ: 2/13/2017)
            SNX_file= self.Wstation.getvalue()[0][0:4] + '0001.SNX'
            if os.path.isfile(SNX_file):
                shutil.move(SNX_file, dest_dir)
            if os.path.isfile(param_txt):
               shutil.move(param_txt, dest_dir)

        #second scenario
        param_txt ="param_"+self.name2.getvalue()+".txt"  
        if os.path.isfile(param_txt):
            #Delete *.WTD from previous runs
            WTD_names=self.Wstation.getvalue()[0][0:4]+"0*.WTD"
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, WTD_names):
                   # print file
                    try:
                          os.remove(file)
                    except Exception,e:
                          print e

            args = "CAMDT_PH " + param_txt
            #===Run executable with argument
            subprocess.call(args) #, stdout=FNULL, stderr=FNULL, shell=False)
            #create a new folder to save outputs of the target scenario
            new_folder=self.name2.getvalue()+"_output"
            if os.path.exists(new_folder):
                shutil.rmtree(new_folder)   #remove existing folder
            os.makedirs(new_folder)
            #copy outputs to the new folder
            dest_dir=Wdir_path + "\\"+new_folder
            for entry in entries:
                if os.path.isfile(entry):
                    shutil.move(entry, dest_dir)
            #move SNX file to output subfolder (EJ: 2/13/2017)
            SNX_file= self.Wstation.getvalue()[0][0:4] + '0001.SNX'
            if os.path.isfile(SNX_file):
                shutil.move(SNX_file, dest_dir)
            if os.path.isfile(param_txt):
               shutil.move(param_txt, dest_dir)
        #3rd scenario
        param_txt ="param_"+self.name3.getvalue()+".txt"  
        if os.path.isfile(param_txt):
            #Delete *.WTD from previous runs
            WTD_names=self.Wstation.getvalue()[0][0:4]+"0*.WTD"
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, WTD_names):
                   # print file
                    try:
                          os.remove(file)
                    except Exception,e:
                          print e
            args = "CAMDT_PH " + param_txt
            #===Run executable with argument
            subprocess.call(args) #, stdout=FNULL, stderr=FNULL, shell=False)
            #create a new folder to save outputs of the target scenario
            new_folder=self.name3.getvalue()+"_output"
            if os.path.exists(new_folder):
                shutil.rmtree(new_folder)   #remove existing folder
            os.makedirs(new_folder)
            #copy outputs to the new folder
            dest_dir=Wdir_path + "\\"+new_folder
            for entry in entries:
                if os.path.isfile(entry):
                    shutil.move(entry, dest_dir)
            #move SNX file to output subfolder (EJ: 2/13/2017)
            SNX_file= self.Wstation.getvalue()[0][0:4] + '0001.SNX'
            if os.path.isfile(SNX_file):
                shutil.move(SNX_file, dest_dir)
            if os.path.isfile(param_txt):
               shutil.move(param_txt, dest_dir)
        #4th scenario
        param_txt ="param_"+self.name4.getvalue()+".txt"  
        if os.path.isfile(param_txt):
            #Delete *.WTD from previous runs
            WTD_names=self.Wstation.getvalue()[0][0:4]+"0*.WTD"
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, WTD_names):
                   # print file
                    try:
                          os.remove(file)
                    except Exception,e:
                          print e
            args = "CAMDT_PH " + param_txt
            #===Run executable with argument
            subprocess.call(args) #, stdout=FNULL, stderr=FNULL, shell=False)
            #create a new folder to save outputs of the target scenario
            new_folder=self.name4.getvalue()+"_output"
            if os.path.exists(new_folder):
                shutil.rmtree(new_folder)   #remove existing folder
            os.makedirs(new_folder)
            #copy outputs to the new folder
            dest_dir=Wdir_path + "\\"+new_folder
            for entry in entries:
                if os.path.isfile(entry):
                    shutil.move(entry, dest_dir)
            #move SNX file to output subfolder (EJ: 2/13/2017)
            SNX_file= self.Wstation.getvalue()[0][0:4] + '0001.SNX'
            if os.path.isfile(SNX_file):
                shutil.move(SNX_file, dest_dir)
            if os.path.isfile(param_txt):
               shutil.move(param_txt, dest_dir)
        #5thscenario
        param_txt ="param_"+self.name5.getvalue()+".txt"  
        if os.path.isfile(param_txt):
            #Delete *.WTD from previous runs
            WTD_names=self.Wstation.getvalue()[0][0:4]+"0*.WTD"
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, WTD_names):
                   # print file
                    try:
                          os.remove(file)
                    except Exception,e:
                          print e
            args = "CAMDT_PH " + param_txt
            #===Run executable with argument
            subprocess.call(args) #, stdout=FNULL, stderr=FNULL, shell=False)
            #create a new folder to save outputs of the target scenario
            new_folder=self.name5.getvalue()+"_output"
            if os.path.exists(new_folder):
                shutil.rmtree(new_folder)   #remove existing folder
            os.makedirs(new_folder)
            #copy outputs to the new folder
            dest_dir=Wdir_path + "\\"+new_folder
            for entry in entries:
                if os.path.isfile(entry):
                    shutil.move(entry, dest_dir)
            #move SNX file to output subfolder (EJ: 2/13/2017)
            SNX_file= self.Wstation.getvalue()[0][0:4] + '0001.SNX'
            if os.path.isfile(SNX_file):
                shutil.move(SNX_file, dest_dir)
            if os.path.isfile(param_txt):
               shutil.move(param_txt, dest_dir)

    def Yield_Analysis(self):
        #Get output YIELD.txt from all scenario
        fname=[]
        scename=[]   #scenario name
        nsimulations=[]
        sim_mode=[] #to save simulation mode (hindcast or forecast)
        temp_entries=[[self.label54.cget("text"),self.name1.getvalue()],
                      [self.label55.cget("text"),self.name2.getvalue()],
                      [self.label56.cget("text"),self.name3.getvalue()],
                      [self.label57.cget("text"),self.name4.getvalue()],
                      [self.label58.cget("text"),self.name5.getvalue()]]
        count=0
        for entry in temp_entries:
            if entry[0] != "N/A" and len(entry[1]) ==4:
                print 'yield.txt is ', Wdir_path + "\\" + entry[1] +"_output"+ "\\YIELD.txt"
                fname.append(Wdir_path + "\\" + entry[1] +"_output"+ "\\YIELD.txt")
                scename.append(entry[1])
                count=count+1
                param_fname=Wdir_path.replace("/","\\") + "\\" + entry[1] +"_output"+"\\param_"+entry[1]+".txt"  
                s_file = open(param_fname,"r") #opens param.txt
                down_method = -99 #initialize
                for line in s_file:
                    if 'sim_mode' in line:
                        sim_mode_temp=int(line[9:12])
                    if 'Temp_Downscaling' in line:
                        down_method=int(line[18:19])
                    if down_method == 0: 
                        if 'Factor' in line:
                            temp=float(line[16:25])*100
                            s_file.close()
                            break
                    elif down_method == 1: 
                         if 'nRealz:' in line:
                            temp=float(line[8:15])
                            s_file.close()
                            break                       

                nsimulations.append(temp)
                sim_mode.append(sim_mode_temp)
        print nsimulations
        max_nsimulations=int(max(nsimulations))

        #Read YIELD.txt from all scenario output
        obs=[]
        for x in range(0, count):
            temp_data = np.loadtxt(fname[x])
            n_col=temp_data.__len__() #n realizations +1 (obs)
            if sim_mode[x] == 0: #hindcast mode
                net_data=temp_data[0:n_col-1]
                obs.append(temp_data[n_col-1])
            else:
                net_data=temp_data[0:n_col]

# data = concatenate( (data, d2), 1 )
# Making a 2-D array only works if all the columns are the
# same length.  If they are not, then use a list instead.
# This is actually more efficient because boxplot converts
# a 2-D array into a list of vectors internally anyway.
            if x == 0:
                data=[net_data]
            elif x == 1:
                data=[data[0], net_data]
            elif x == 2:
                data = [data[0],data[1],net_data]
            elif x == 3:
                data = [data[0],data[1],data[2], net_data]
            elif x == 4:
                data = [data[0],data[1],data[2],data[3],net_data]
            else:
                data = [data[0],data[1],data[2],data[3],data[4],net_data]


        #Plotting
        fig = plt.figure()
        fig.suptitle('Yield Forecast', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        #fig.subplots_adjust(top=0.85)
        #ax.set_title('Yield Forecast')
        ax.set_xlabel('Scenario',fontsize=14)
        ax.set_ylabel('Yield [kg/ha]',fontsize=14)
        
        if sim_mode[0] == 0: #hindcast mode => Need to be more flexible
            #X data for plot
            myXList=[i+1 for i in range(count)]
            # Plot a line between the means of each dataset
            plt.plot(myXList, obs, 'go-')

        #ax.boxplot(yield_data,labels=scename, showmeans=True, meanline=True) #, notch=True, bootstrap=10000)
        ax.boxplot(data,labels=scename, showmeans=True, meanline=True,notch=True) #, bootstrap=10000)
        plt.show()

    def Yield_exceedance(self):
        fname=[]
        scename=[]   #scenario name
        nsimulations=[]
        sim_mode=[] #to save simulation mode (hindcast or forecast)
        temp_entries=[[self.label54.cget("text"),self.name1.getvalue()],
                      [self.label55.cget("text"),self.name2.getvalue()],
                      [self.label56.cget("text"),self.name3.getvalue()],
                      [self.label57.cget("text"),self.name4.getvalue()],
                      [self.label58.cget("text"),self.name5.getvalue()]]
        count=0
        for entry in temp_entries:
            if entry[0] != "N/A" and len(entry[1]) ==4:
                fname.append(Wdir_path + "\\" + entry[1] +"_output"+ "\\YIELD.txt")
                scename.append(entry[1])
                count=count+1
              ##  param_fname=Wdir_path.replace("/","\\") + "\\param_"+entry[1]+".txt"
                param_fname=Wdir_path.replace("/","\\") + "\\" + entry[1] +"_output"+"\\param_"+entry[1]+".txt"  
                s_file = open(param_fname,"r") #opens param.txt
                down_method = -99 #initialize
                for line in s_file:
                    if 'sim_mode' in line:
                        sim_mode_temp=int(line[9:12])
                    if 'Temp_Downscaling' in line:
                        down_method=int(line[18:19])
                    if down_method == 0: 
                        if 'Factor' in line:
                            temp=float(line[16:25])*100
                            s_file.close()
                            break
                    elif down_method == 1: 
                         if 'nRealz:' in line:
                            temp=float(line[8:15])
                            s_file.close()
                            break                       

                nsimulations.append(temp)
                sim_mode.append(sim_mode_temp)
        max_nsimulations=int(max(nsimulations))

        #create an empty matrix
        sorted_yield_data = np.empty((max_nsimulations,count))
        sorted_yield_data[:] = np.NAN
        excedp_data = np.empty((max_nsimulations,count))
        excedp_data[:] = np.NAN
           
        #Read YIELD.txt from all scenario output
        obs=[]
        for x in range(0, count):
            temp_data = np.loadtxt(fname[x])
            n_col=temp_data.__len__() #n realizations +1 (obs)
            if sim_mode[x] == 0: #hindcast mode
                net_data=temp_data[0:n_col-1]
                obs.append(temp_data[n_col-1])
            else:
                net_data=temp_data[0:n_col]

            yield_array=net_data
            #compute rank using rankdata(note: The default assigns the average rank to the tied values:)
            rank_yield=rankdata(yield_array) #from smallest to largest
            rank_yield=nsimulations[x] - rank_yield + 1  #from  largest (has rank=1) to smallest value

            #exceedance probability; p=m/(n+1) where m is the rank from above, n is total number of data
            excedp=rank_yield/(nsimulations[x]+1)

            #sort yield from smallest to largest
            sorted_yield=np.sort(yield_array)
            #get index of sorted array
            sort_index = np.argsort(yield_array)

            sorted_excedp=[]
            for i in range(yield_array.__len__()):
                sorted_excedp.append(excedp[sort_index[i]])
            excedp_array = np.array(sorted_excedp)  #convert list to array

            #save into one matrix
            for i in range(yield_array.__len__()):
                sorted_yield_data[i,x]=sorted_yield[i]
                excedp_data[i,x]=excedp_array[i]

        #Plotting
        fig = plt.figure()
        fig.suptitle('Yield Exceedance Curve', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        #fig.subplots_adjust(top=0.85)
        #ax.set_title('Yield Forecast')
        ax.set_xlabel('Yield [kg/ha]',fontsize=14)
        ax.set_ylabel('Probability of Exceedance [-]',fontsize=14)

        for x in range(0, count):
            ax.plot(sorted_yield_data[:,x],excedp_data[:,x],'o-', label=scename[x])
            if sim_mode[x] == 0: #hindcast mode which include yield with observed weather at the end
                x_data=[obs[x],obs[x]] #only two points to draw a line
                y_data=[0,1]
                temp='w/ obs wth (' + scename[x] + ')'
                ax.plot(x_data,y_data,'-.', label=temp)
                plt.ylim(0, 1)
##        #legend = ax.legend(loc='lower left', shadow=True, fontsize='large') #loc=0 => best location
        # Shrink current axis by 15%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()


    def WSI_Analysis(self):
        #Get output AveStress.txt from all scenario
        fname=[]
        scename=[]   #scenario name
        temp_entries=[[self.label54.cget("text"),self.name1.getvalue()],
                      [self.label55.cget("text"),self.name2.getvalue()],
                      [self.label56.cget("text"),self.name3.getvalue()],
                      [self.label57.cget("text"),self.name4.getvalue()],
                      [self.label58.cget("text"),self.name5.getvalue()]]
        count=0
        for entry in temp_entries:
            if entry[0] != "N/A" and len(entry[1]) ==4:
              #  print 'AveStress.txt is ', Wdir_path + "\\" + entry[1] +"_output"+ "\\AveStress.txt"
                fname.append(Wdir_path + "\\" + entry[1] +"_output"+ "\\AveStress.txt")
                scename.append(entry[1])
                count=count+1

        #Read YIELD.txt from all scenario output
        wsi_data=[]
        for x in range(0, count):
            temp_data = np.loadtxt(fname[x])
            temp_data[temp_data < 0] = np.nan  #replace -99 with nan
           # print 'AveStress file name is ', fname[x],scename[x]
            if x == 0:
                wsi_data=temp_data
            else:
                wsi_data=np.vstack((wsi_data,temp_data)) #concatenate arrays
        #transpose array before plotting       
        wsi_data=np.transpose(wsi_data)
        
        #Plotting
        fig = plt.figure()
        fig.suptitle('Average Water Stress (1-ET_act/ET_pot)', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        #fig.subplots_adjust(top=0.85)
        #ax.set_title('Yield Forecast')
        ax.set_xlabel('Days of Planting',fontsize=14)
        ax.set_ylabel('Average Water Stress [-]',fontsize=14)
        plt.ylim(ymax=1)  #y axis = 0-1

        for x in range(0, count):
            if count == 1:
                ax.plot(wsi_data,label=scename[x])
            else:
                ax.plot(wsi_data[:,x],label=scename[x])
        legend = ax.legend(loc='best', shadow=True, fontsize='large')
        plt.show()

    def Risk_Analysis(self):
        #Get output PgtTHRESHPct.txt from all scenario
        fname=[]
        scename=[]   #scenario name
        temp_entries=[[self.label54.cget("text"),self.name1.getvalue()],
                      [self.label55.cget("text"),self.name2.getvalue()],
                      [self.label56.cget("text"),self.name3.getvalue()],
                      [self.label57.cget("text"),self.name4.getvalue()],
                      [self.label58.cget("text"),self.name5.getvalue()]]
        count=0
        for entry in temp_entries:
            if entry[0] != "N/A" and len(entry[1]) ==4:
                print 'PgtTHRESHPct.txt is ', Wdir_path + "\\" + entry[1] +"_output"+ "\\PgtTHRESHPct.txt"
                fname.append(Wdir_path + "\\" + entry[1] +"_output"+ "\\PgtTHRESHPct.txt")
                scename.append(entry[1])
                count=count+1

        #Read PgtTHRESHPct.txt from all scenario output
        risk_data=[]
        for x in range(0, count):
            temp_data = np.loadtxt(fname[x])
            temp_data[temp_data < 0] = np.nan  #replace -99 with nan
            print 'PgtTHRESHPctfile name is ', fname[x],scename[x]
            if x == 0:
                risk_data=temp_data
            else:
                risk_data=np.vstack((risk_data,temp_data)) #concatenate arrays
        #transpose array before plotting       
        risk_data=np.transpose(risk_data)
        
        #Plotting
        fig = plt.figure()
        fig.suptitle('Risks of Exceeding x% Water Stress', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        #fig.subplots_adjust(top=0.85)
        #ax.set_title('Yield Forecast')
        ax.set_xlabel('Days of Planting',fontsize=14)
        ax.set_ylabel('Probability (a.k.a. Risk)',fontsize=14)
        plt.ylim(ymax=1)  #Fix my Y-axis [0,1]

        for x in range(0, count):
            if count == 1:
                ax.plot(risk_data,label=scename[x])
            else:
                ax.plot(risk_data[:,x],label=scename[x])
        legend = ax.legend(loc='best', shadow=True, fontsize='large')
        plt.show()

    def Economic_Analysis(self):
        fname=[]
        scename=[]   #scenario name
        nsimulations=[]
        sim_mode=[] #to save simulation mode (hindcast or forecast)
        costN_list=[]
        costI_list=[]
        costG_list=[]
        price_list=[]
        temp_entries=[[self.name1.getvalue(),self.price1.getvalue(),self.costN1.getvalue(),self.costI1.getvalue(),self.costG1.getvalue(),self.label54.cget("text")],
                      [self.name2.getvalue(),self.price2.getvalue(),self.costN2.getvalue(),self.costI2.getvalue(),self.costG2.getvalue(),self.label55.cget("text")],
                      [self.name3.getvalue(),self.price3.getvalue(),self.costN3.getvalue(),self.costI3.getvalue(),self.costG3.getvalue(),self.label56.cget("text")],
                      [self.name4.getvalue(),self.price4.getvalue(),self.costN4.getvalue(),self.costI4.getvalue(),self.costG4.getvalue(),self.label57.cget("text")],
                      [self.name5.getvalue(),self.price5.getvalue(),self.costN5.getvalue(),self.costI5.getvalue(),self.costG5.getvalue(),self.label58.cget("text")]]
        count=0
        for entry in temp_entries:
            if entry[0] != '':
                if entry[1] == '' or entry[5] == 'N/A':
                    self.Eanalysis_err.activate()
               # print 'yield.txt is ', Wdir_path + "\\" + entry[0] +"_output"+ "\\Summary.out"
                fname.append(Wdir_path + "\\" + entry[0] +"_output"+ "\\Summary.out")
                costN_list.append(entry[2])
                costI_list.append(entry[3])
                costG_list.append(entry[4])
                price_list.append(entry[1])
                scename.append(entry[0])
                count=count+1
        ##        param_fname=Wdir_path.replace("/","\\") + "\\param_"+entry[0]+".txt"
                param_fname=Wdir_path.replace("/","\\") + "\\" + entry[0] +"_output"+"\\param_"+entry[0]+".txt"  
                s_file = open(param_fname,"r") #opens param.txt
                down_method = -99 #initialize
                for line in s_file:
                    if 'sim_mode' in line:
                        sim_mode_temp=int(line[9:12])
                    if 'Temp_Downscaling' in line:
                        down_method=int(line[18:19])
                    if down_method == 0: 
                        if 'Factor' in line:
                            temp=float(line[16:25])*100
                            s_file.close()
                            break
                    elif down_method == 1: 
                         if 'nRealz:' in line:
                            temp=float(line[8:15])
                            s_file.close()
                            break                       

                nsimulations.append(temp)
                sim_mode.append(sim_mode_temp)
        max_nsimulations=int(max(nsimulations))

##        #create an empty matrix
##        GMargin_data = np.empty((max_nsimulations,count))
##        GMargin_data[:] = np.NAN

        GMargin_obs = [] #gross margin with observed weather
        #Read Summary.out from all scenario output
        for x in range(0, count):
            GMargin_data = []
            fr = open(fname[x],"r") #opens summary.out to read
            price=price_list[x]   #$/ton
            cost_N=costN_list[x] #$/kg N
            cost_I=costI_list[x] #$/mm irrigation cost
            cost_G=costG_list[x] #$/ha general cost
            for line in range(0,4): #read headers
                temp_str=fr.readline()
            for line in range(0,int(nsimulations[x])): #read actual simulated data
                temp_str=fr.readline()
                yield_out=float(temp_str[163:170])
                fert_amount=float(temp_str[279:284])  #NICM   Tot N app kg/ha Inorganic N applied (kg [N]/ha)    
                irr_amount=float(temp_str[225:230])   #IRCM   Irrig mm        Season irrigation (mm)
                temp_gmargin = yield_out*float(price)*0.001 - float(cost_N)*fert_amount - float(cost_I)*irr_amount - float(cost_G)#$/ha
                GMargin_data.append(temp_gmargin)
                ##GMargin_data[line,x]=yield_out*float(price)*0.001 - float(cost_N)*fert_amount - float(cost_I)*irr_amount - float(cost_G)#$/ha
            if sim_mode[x] == 0: #if hindcase, read the last line with observed weather 
                temp_str=fr.readline()
                yield_out=float(temp_str[163:170])
                fert_amount=float(temp_str[279:284])  #NICM   Tot N app kg/ha Inorganic N applied (kg [N]/ha)    
                irr_amount=float(temp_str[225:230])   #IRCM   Irrig mm        Season irrigation (mm)
                temp_gmargin=yield_out*float(price)*0.001 - float(cost_N)*fert_amount - float(cost_I)*irr_amount - float(cost_G)#$/ha
                GMargin_obs.append(temp_gmargin)
            fr.close()
# data = concatenate( (data, d2), 1 )
# Making a 2-D array only works if all the columns are the
# same length.  If they are not, then use a list instead.
# This is actually more efficient because boxplot converts
# a 2-D array into a list of vectors internally anyway.
            if x == 0:
                data=[GMargin_data]
            elif x == 1:
                data=[data[0], GMargin_data]
            elif x == 2:
                data = [data[0],data[1],GMargin_data]
            elif x == 3:
                data = [data[0],data[1],data[2], GMargin_data]
            elif x == 4:
                data = [data[0],data[1],data[2],data[3],GMargin_data]
            else:
                data = [data[0],data[1],data[2],data[3],data[4],GMargin_data]

        #Plotting
        fig = plt.figure()
        fig.suptitle('Gross Margin', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        #fig.subplots_adjust(top=0.85)
        #ax.set_title('Yield Forecast')
        ax.set_xlabel('Scenario',fontsize=14)
        ax.set_ylabel('Gross Margin[PHP/ha]',fontsize=14)

        if sim_mode[0] == 0: #hindcast mode => Need to be more flexible
            #X data for plot
            myXList=[i+1 for i in range(count)]
            # Plot a line between the means of each dataset
            plt.plot(myXList, GMargin_obs, 'go-')          
        ##ax.boxplot(GMargin_data,labels=scename, showmeans=True, meanline=True, notch=True) #, bootstrap=10000)
        ax.boxplot(data,labels=scename, showmeans=True, meanline=True, notch=True) #, bootstrap=10000)
        plt.show()

    def Margin_exceedance(self):
        fname=[]
        scename=[]   #scenario name
        sim_mode=[] #to save simulation mode (hindcast or forecast)
        nsimulations=[]
        costN_list=[]
        costI_list=[]
        costG_list=[]
        price_list=[]
        temp_entries=[[self.name1.getvalue(),self.price1.getvalue(),self.costN1.getvalue(),self.costI1.getvalue(),self.costG1.getvalue(),self.label54.cget("text")],
                      [self.name2.getvalue(),self.price2.getvalue(),self.costN2.getvalue(),self.costI2.getvalue(),self.costG2.getvalue(),self.label55.cget("text")],
                      [self.name3.getvalue(),self.price3.getvalue(),self.costN3.getvalue(),self.costI3.getvalue(),self.costG3.getvalue(),self.label56.cget("text")],
                      [self.name4.getvalue(),self.price4.getvalue(),self.costN4.getvalue(),self.costI4.getvalue(),self.costG4.getvalue(),self.label57.cget("text")],
                      [self.name5.getvalue(),self.price5.getvalue(),self.costN5.getvalue(),self.costI5.getvalue(),self.costG5.getvalue(),self.label58.cget("text")]]
        count=0
        for entry in temp_entries:
            if entry[0] != '':
                if entry[1] == '' or entry[5] == 'N/A':
                    self.Eanalysis_err.activate()
               # print 'yield.txt is ', Wdir_path + "\\" + entry[0] +"_output"+ "\\Summary.out"
                fname.append(Wdir_path + "\\" + entry[0] +"_output"+ "\\Summary.out")
                costN_list.append(entry[2])
                costI_list.append(entry[3])
                costG_list.append(entry[4])
                price_list.append(entry[1])
                scename.append(entry[0])
                count=count+1
           ##     param_fname=Wdir_path.replace("/","\\") + "\\param_"+entry[0]+".txt"
                param_fname=Wdir_path.replace("/","\\") + "\\" + entry[0] +"_output"+"\\param_"+entry[0]+".txt"  
                s_file = open(param_fname,"r") #opens param.txt
                down_method = -99 #initialize
                for line in s_file:
                    if 'sim_mode' in line:
                        sim_mode_temp=int(line[9:12])
                    if 'Temp_Downscaling' in line:
                        down_method=int(line[18:19])
                    if down_method == 0: 
                        if 'Factor' in line:
                            temp=float(line[16:25])*100
                            s_file.close()
                            break
                    elif down_method == 1: 
                         if 'nRealz:' in line:
                            temp=float(line[8:15])
                            s_file.close()
                            break                       

                nsimulations.append(temp)
                sim_mode.append(sim_mode_temp)
        max_nsimulations=int(max(nsimulations))

        #create an empty matrix
        sorted_margin_data = np.empty((max_nsimulations,count))
        sorted_margin_data[:] = np.NAN
        excedp_data = np.empty((max_nsimulations,count))
        excedp_data[:] = np.NAN
        GMargin_obs = [] #gross margin with observed weather
            
        #Read Summary.out from all scenario output
        for x in range(0, count):
            fr = open(fname[x],"r") #opens summary.out to read
            GMargin_list=[]
            price=price_list[x]   #$/ton
            cost_N=costN_list[x] #$/kg N
            cost_I=costI_list[x] #$/mm irrigation cost
            cost_G=costG_list[x] #$/ha general cost
            for line in range(0,4): #read headers
                temp_str=fr.readline()
            for line in range(0,int(nsimulations[x])): #read actual simulated data
                temp_str=fr.readline()
                yield_out=float(temp_str[163:170])
                fert_amount=float(temp_str[279:284])  #NICM   Tot N app kg/ha Inorganic N applied (kg [N]/ha)    
                irr_amount=float(temp_str[225:230])   #IRCM   Irrig mm        Season irrigation (mm)   
                temp=yield_out*float(price)*0.001 - float(cost_N)*fert_amount - float(cost_I)*irr_amount - float(cost_G)#$/ha
                GMargin_list.append(temp)
                print yield_out, temp
            if sim_mode[x] == 0: #if hindcase, read the last line with observed weather 
                temp_str=fr.readline()
                yield_out=float(temp_str[163:170])
                fert_amount=float(temp_str[279:284])  #NICM   Tot N app kg/ha Inorganic N applied (kg [N]/ha)    
                irr_amount=float(temp_str[225:230])   #IRCM   Irrig mm        Season irrigation (mm)
                temp_gmargin=yield_out*float(price)*0.001 - float(cost_N)*fert_amount - float(cost_I)*irr_amount - float(cost_G)#$/ha
                GMargin_obs.append(temp_gmargin)
            fr.close()

            #convert list to array after excluding last element which is yield with observed weather
            GMargin_array = np.array(GMargin_list)
            
            #compute rank using rankdata(note: The default assigns the average rank to the tied values:)
            rank_margin=rankdata(GMargin_array) #from smallest to largest
            rank_margin=nsimulations[x] -rank_margin+ 1  #from  largest (has rank=1) to smallest value

            #exceedance probability; p=m/(n+1) where m is the rank from above, n is total number of data
            excedp=rank_margin/(nsimulations[x]+1)

            #sort yield from smallest to largest
            sorted_margin=np.sort(GMargin_array)
            #get index of sorted array
            sort_index = np.argsort(GMargin_array)

            sorted_excedp=[]
            for i in range(GMargin_array.__len__()):
                sorted_excedp.append(excedp[sort_index[i]])
            excedp_array = np.array(sorted_excedp)  #convert list to array

            #save into one matrix
            for i in range(GMargin_array.__len__()):
                sorted_margin_data[i,x]=sorted_margin[i]
                excedp_data[i,x]=excedp_array[i]

        #Plotting
        fig = plt.figure()
        fig.suptitle('Gross Margin Exceedance Curve', fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        ax.set_xlabel('Gross Margin[PHP/ha]',fontsize=14)
        ax.set_ylabel('Probability of Exceedance [-]',fontsize=14)

        for x in range(0, count):
            ax.plot(sorted_margin_data[:,x],excedp_data[:,x],'o-', label=scename[x])
            if sim_mode[x] == 0:    #hindcast which include yield with observed weather at the end
                x_data=[GMargin_obs[x],GMargin_obs[x]] #only two points to draw a line
                y_data=[0,1]
                temp='w/ obs wth (' + scename[x] + ')'
                ax.plot(x_data,y_data,'-.', label=temp)
                plt.ylim(0, 1)
##        #legend = ax.legend(loc='lower left', shadow=True, fontsize='large') #loc=0 => best location
        # Shrink current axis by 15%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
       
    #Get irrigationinformation
    def getIrrInput(self):
        if IRbutton.get() == 0:  #Automatic when required
            self.AutoIrrDialog.activate()
            self.label402.configure(text=self.irr_depth.getvalue(),background='honeydew1')
            self.label404.configure(text=self.irr_thresh.getvalue(),background='honeydew1')
            self.label408.configure(text=self.eff_fraction.getvalue(),background='honeydew1')    
        elif IRbutton.get() == 2:  #on reported dates
            self.ReptIrrDialog.activate()
            print 'constant flooding depth?  ', floodVar1, floodVar2, floodVar3
            if self.irr_day1.getvalue() != "None":
                self.label105.configure(text=self.irr_day1.getvalue(),background='honeydew1')
                self.label106.configure(text=self.height1.getvalue(),background='honeydew1')
                self.label107.configure(text=self.flood1.getvalue(),background='honeydew1') 
                self.label121.configure(text=self.pud_date.getvalue(),background='honeydew1')       
               # self.label123.configure(text=self.puddling.getvalue(),background='honeydew1') 
                self.label125.configure(text=self.pec_rate.getvalue(),background='honeydew1')   
                if floodVar1.get() == 0:
                    self.label1071.configure(text='Yes',background='honeydew1')  
                else:
                    self.label1071.configure(text='No',background='honeydew1')  
            if self.irr_day2.getvalue() != "None":
                self.label109.configure(text=self.irr_day2.getvalue(),background='honeydew1')
                self.label110.configure(text=self.height2.getvalue(),background='honeydew1')
                self.label111.configure(text=self.flood2.getvalue(),background='honeydew1')
                if floodVar2.get() == 0:
                    self.label1111.configure(text='Yes',background='honeydew1')  
                else:
                    self.label1111.configure(text='No',background='honeydew1')  
            if self.irr_day3.getvalue() != "None":
                self.label113.configure(text=self.irr_day3.getvalue(),background='honeydew1')
                self.label114.configure(text=self.height3.getvalue(),background='honeydew1')
                self.label115.configure(text=self.flood3.getvalue(),background='honeydew1')
                if floodVar3.get() == 0:
                    self.label1151.configure(text='Yes',background='honeydew1')  
                else:
                    self.label1151.configure(text='No',background='honeydew1')  

    #Get fertilizer application information
    def getFertInput(self):
        if Fbutton1.get() == 0:
            self.fert_dialog.activate()
            if self.fert_mat1.getvalue()[0] != "None":
                self.label006.configure(text=self.day1.getvalue(),background='honeydew1')
                self.label007.configure(text=self.amount1.getvalue(),background='honeydew1')
                self.label008.configure(text=self.fert_mat1.getvalue()[0],background='honeydew1')
                self.label009.configure(text=self.fert_app1.getvalue()[0],background='honeydew1')
            if self.fert_mat2.getvalue()[0] != "None":
                self.label011.configure(text=self.day2.getvalue(),background='honeydew1')
                self.label012.configure(text=self.amount2.getvalue(),background='honeydew1')
                self.label013.configure(text=self.fert_mat2.getvalue()[0],background='honeydew1')
                self.label014.configure(text=self.fert_app2.getvalue()[0],background='honeydew1')
            if self.fert_mat3.getvalue()[0] != "None":
                self.label016.configure(text=self.day3.getvalue(),background='honeydew1')
                self.label017.configure(text=self.amount3.getvalue(),background='honeydew1')
                self.label018.configure(text=self.fert_mat3.getvalue()[0],background='honeydew1')
                self.label019.configure(text=self.fert_app3.getvalue()[0],background='honeydew1')
    #Select working directory to run CAMDT fortran executable
    def getWdir(self):
        global Wdir_path
        Wdir_path=askdirectory(initialdir="C:\\", title="Select working dir")
        #Wdir_path = askopenfilename(initialdir="C:\\Users", title="Select working dir")
        print 'Working directory is', Wdir_path
        self.WDir_label.configure(text=Wdir_path)
        self.WDir_label.configure(background='lavenderblush1')

##    #find CPT output file path
##    def getCPTfile(self):
##        global CPT_path
##        CPT_path = askopenfilename(initialdir="C:\\", title="Select files")
##        print 'CPT filename is', CPT_path
##        self.CPT_label.configure(text=CPT_path)
##        self.label32.configure(background='honeydew1')
##        self.label34.configure(background='honeydew1')
##        self.label36.configure(background='honeydew1')

    #find WTD output file path
    def getWTDfile(self):
        global WTD_path
        WTD_path = askopenfilename(initialdir="C:\\", title="Select files")
        print 'WTD filename is', WTD_path
        self.WTD_label.configure(text=WTD_path,background='honeydew1')

    #Get cultivar information
    def getCulinput(self):
        print 'cultivar infomation is  ', cul_Rbutton.get()
        if cul_Rbutton.get() == 0:
            self.cul_dialog1.activate()
            var_ID=self.calib_cul.get()[:6]
            var_name=self.calib_cul.get()[7:]
            self.label362.configure(text=var_ID,background='honeydew1')
            self.label364.configure(text=var_name,background='honeydew1')
        else:
            self.cul_dialog2.activate()
            self.label302.configure(text=self.var_ID.getvalue(),background='honeydew1')
           # self.label304.configure(text=self.var_name.getvalue(),background='honeydew1')
            self.label304.configure(text=v_name.get(),background='honeydew1')
            self.label306.configure(text=self.eco_code.getvalue(),background='honeydew1')
            self.label308.configure(text=self.P1.getvalue(),background='honeydew1')
            self.label310.configure(text=self.P2R.getvalue(),background='honeydew1')
            self.label312.configure(text=self.P5.getvalue(),background='honeydew1')
            self.label314.configure(text=self.P2O.getvalue(),background='honeydew1')
            self.label316.configure(text=self.G1.getvalue(),background='honeydew1')
            self.label318.configure(text=self.G2.getvalue(),background='honeydew1')
            self.label320.configure(text=self.G3.getvalue(),background='honeydew1')
            self.label322.configure(text=self.G4.getvalue(),background='honeydew1')
            
    def getmoreinput(self):
        print 'simulation mode is ', CheckVar.get()
        if CheckVar21.get() == 0:
            self.FRdialog.activate()
            print 'FResampler Sampling factor is ', self.SampFactor.getvalue()
            self.label12.configure(text=self.SampFactor.getvalue(),background='honeydew1')
        else:
            self.DisaggDialog.activate()
            print 'Stochastic DisAg. target (amount) is ', CheckVar31.get()
            self.label22.configure(text=self.nRealz.getvalue(),background='honeydew1')
            self.label26.configure(text=CheckVar31.get(),background='honeydew1')
            self.label28.configure(text=CheckVar32.get(),background='honeydew1')
            self.label20.configure(text=CheckVar33.get(),background='honeydew1')

##    def getSFinput(self):
##        print 'Seasonal forecast is from ', CheckVar22.get()
##        if CheckVar22.get() == 0:
##            self.CPTDialog.activate()
##            self.label32.configure(text=CPT_path)
##            self.label34.configure(text=self.latitude.getvalue())
##            self.label36.configure(text=self.longitude.getvalue())
##        else:
##            self.UserDialog.activate()
##            print 'Below normal is ', self.SampFactor.getvalue()
##            self.label42.configure(text=self.BN.getvalue(),background='honeydew1')
##            Near_normal=100-float(self.BN.getvalue())-float(self.AN.getvalue())
##            self.label44.configure(text=str(Near_normal),background='honeydew1')
##            self.label46.configure(text=self.AN.getvalue(),background='honeydew1')
    
    def changed(self):
        print 'Text changed, value is', startyear2.getvalue()

    def validate_in(self):
        month21 = int(self.startmonth2.getvalue()[0][0:2]) #planting month
        month22 = int(self.endmonth2.getvalue()[0][0:2]) #harvesting month
        month31 = int(self.startmonth3.getvalue()[0][0:2]) #prediction start month
        month32 = int(self.endmonth3.getvalue()[0][0:2]) #prediction end month
        year21=int(startyear2.getvalue())
        year22=int(endyear2.getvalue())
        year31=int(startyear3.getvalue())
        year32=int(endyear3.getvalue())
        print 'start year2 is ', year21
        print 'end year2 is ', year22
        print 'start year3 is ', year31
        print 'end year3 is ', year32
        print 'simulation mode is ', CheckVar.get()
        print 'Plabtubg date is ', planting_date.getvalue()

        p_date=int(planting_date.getvalue())
        #compare planting date and simulation horizon
        day1=datetime.date(year21,month21,1)
        #sim_doy=day1.strftime('%j')  => strftime produces string
        sim_doy=int(day1.strftime('%j'))  #convert to doy in string
        
        if year22 < year21:
             print 'Sim Horizon: End-year should be >= Start-year!'
             self.val_dialog1.activate()
        elif year22 == year21 and month22 <= month21:
             print 'Sim Horizon: End-Month should be > Start-Month!'
             self.val_dialog2.activate()
        elif (year22-year21) > 2:
            print 'Sim Horizon: Simulation period is too long! (over 2 years)'
            self.val_dialog3.activate()
        elif year32 < year31:
             print 'Pred Horizon: End-year should be >= Start-year!'
             self.val_dialog4.activate()
        elif year32 == year31 and month32 < month31:
             print 'Pred Horizon: End-Month should be > Start-Month!'
             self.val_dialog5.activate()
        elif (year32-year31) > 2:
            print 'Pred Horizon: End-year is too far!(over 2 years)'
            self.val_dialog6.activate()
        elif year31 < year21:
            print 'Pred Year should be >= Sim Year!'
            self.val_dialog7.activate()
        elif year31 == year21 and month31 < month21:
            print 'Pred Month should be >= Sim Month!'
            self.val_dialog8.activate()
        elif year31 == year32 and (month32-month31) >= 3:
            print 'Recommended pred horizon is less than 3 months! '
            self.val_dialog9.activate()
        elif (year32-year31) == 1 and (12-month31+1+month32) > 3:
            print 'Recommended pred horizon is less than 3 months! '
            self.val_dialog9.activate()
        elif sim_doy > p_date:   #checking planting date
             print 'Planting date should be later than simulation starting date!'
             self.val_dialog11.activate()
        elif month21 < 0 or month22 < 0 or month31 < 0 or month32 < 0:
             print 'Month input is missing!'
             self.val_dialog12.activate()
        else:
            print 'No issues found in Simulation horizon inputs'
            self.val_dialog10.activate()
 
######################################################################
# main program
if __name__ == '__main__':
    root = Tkinter.Tk()  #The main toplevel referred to as the "root" (Grayson p.32)
    # fonts for all widgets
    root.option_add("*Font", "Verdana 10") #"courier")
##    # font to use for label widgets
##    root.option_add("*Label.Font", "helvetica 20 bold")

    Pmw.initialise(root)
    root.title(title)  #add title = 'CAMDT User-Interface' on the main window

##    #Add a logo image as a button
##    img = PhotoImage(file=r'C:\IRI\PH\CAMDT_2017\Python_script\logo_all3.gif') 
##    logo_button=Button(root, background='white', image=img).pack(side=TOP) 

    widget = CAMDT(root)  #Calling CAMDT class as a function

    #Add an Exit button to destroy the main window
    exitButton = Tkinter.Button(root, text = 'Exit', command = root.destroy)
    exitButton.pack()
     
    #call Tkinter mainloop to process events and keep the display activated
    root.mainloop()

    
    