#-----------------------------------------------------------------------------------
#
#
# Version 17.08.20
# 
# Written by Stine Gustavsen and Ane Vigre Håland as part of 
# a master thesis in Biophysics and Medical Technology at NTNU.
# The program is originally meant to be used at St. Olavs Hospital 
# in the radiation clinic.
#
#-----------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, INSERT, DISABLED, GROOVE, CURRENT, Radiobutton, \
    NORMAL, ACTIVE, messagebox, Menu, IntVar, Checkbutton, FLAT, PhotoImage, Label,\
        SOLID, N, S, W, E, END, LEFT, Scrollbar, RIGHT, Y, BOTH, TOP, OptionMenu, \
            SUNKEN, RIDGE, BOTTOM, X
import Globals
import re
import CoMet_functions, intro_tab_functions, Map_Dose_functions
import Dose_response_functions, Profile_functions, DVH_functions
from PIL import Image, ImageTk
import os
import sys


Globals.form.title("FIDORA")
Globals.form.configure(bg='#ffffff')
Globals.form.state('zoomed')

Globals.form.tk.call('wm', 'iconphoto', Globals.form._w, \
    PhotoImage(file='logo_fidora.png'))
Globals.form.iconbitmap(default='logo_fidora.png')
load = Image.open("fidora_logo.png")
render = ImageTk.PhotoImage(load)
label = Label(Globals.scroll_frame, image=render)
label.image = render
label.grid(row = 0, column = 0, sticky=W)
label.config(bg='#FFFFFF') 

Globals.tab_parent.add(Globals.intro_tab, text='FIDORA')
Globals.tab_parent.add(Globals.tab1, text='CoMet')
Globals.tab_parent.add(Globals.tab2, text='Dose Response')
#Globals.tab_parent.add(Globals.tab3, text='Map dose') #Under development
Globals.tab_parent.add(Globals.tab4, text='Profiles')
Globals.tab_parent.add(Globals.tab5,text='DVH')

#-----------------------------------------------------------------------------------
# Set the style for all GUI related to Fidora.
# Style is choosen by the authors
#
#Horizontal.TProgressbar -> progressbar used in CoMet
#TNotebook -> Notebook which holds every functionality in Fidora
#TNotebook.tab -> set style for each tab
#Treeview -> listbox used in Profiles
#-----------------------------------------------------------------------------------
style = ttk.Style()
style.theme_create('MyStyle', parent= 'classic', settings={
    ".": {
        "configure": {
            "background": '#FFFFFF',
            "font": 'red'
        }
    },
    "Horizontal.TProgressbar":{
        "configure": {
            "background": '#2C8EAD',
            "bordercolor": '#32A9CE',
            "troughcolor": "#ffffff",
        }
    },
    "TNotebook": {
        "configure": {
            "background":'#ffffff',
            "tabmargins": [5, 5, 10, 10],
            "tabposition": 'wn',
            "borderwidth": 0,
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#0A7D76',
            "foreground": '#ffffff',
            "padding": [30,35, 20,35],
            "font": ('#FFFFFF', '15'),
            "borderwidth": 1,
            "equalTabs": True,
            "width": 13
        },
        "map": {
            "background": [("selected", '#02B9A5')],
            "expand": [("selected", [1, 1, 1, 0])]
        }
    },
    "Treeview":{
        "configure":{
            "font": ('calibri', '9'),
            "highlightthickness": 0,
            "relief": FLAT,
            "borderwidth": 0
        }
    },
    "Treeview.Heading":{
        "configure":{
            "font": ('calibri', '9'),
            "highlightthickness": 0,
            "relief": FLAT,
            "borderwidth": 0,
            "anchor": W
        }
    }
})
style.theme_use('MyStyle')

#-----------------------------------------------------------------------------------
# Creating a menubar (visible at top left of window)
# Buttons: File, Help, Specification
#   File -> Restart, open, exit
#   Help -> Help, about
#   Specification -> Scanner settings, calibration, raystation
#-----------------------------------------------------------------------------------
menubar = Menu(Globals.form)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Restart", command=CoMet_functions.nothingButton)
filemenu.add_command(label="Open", command=CoMet_functions.nothingButton)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=Globals.form.quit)
menubar.add_cascade(label="File", menu=filemenu)

#helpmenu = Menu(menubar, tearoff=0)
#helpmenu.add_command(label="Help", command=CoMet_functions.nothingButton)
#helpmenu.add_command(label="About", command=CoMet_functions.nothingButton)
#menubar.add_cascade(label="Help", menu=helpmenu)

scannermenu=Menu(menubar, tearoff=0)
scannermenu.add_command(label="Scanner settings", \
    command=intro_tab_functions.createScannerSettingsWindow)
#scannermenu.add_command(label="Calibration", \
#    command=intro_tab_functions.createCalibrationWindow)
#scannermenu.add_command(label="Raystation", \
#    command=intro_tab_functions.createRaystationWindow)
menubar.add_cascade(label="Specifications", menu=scannermenu)

Globals.form.config(menu=menubar)

#-----------------------------------------------------------------------------------
# Upload all images used in Fidora.
# Images is created by the authors.
#-----------------------------------------------------------------------------------
upload_button_file = "uploadbutton3.png" 
Globals.upload_button_image = ImageTk.PhotoImage(file=upload_button_file)

select_folder_button_file = "select_folder_button2.png"
select_folder_image = ImageTk.PhotoImage(file=select_folder_button_file)

help_button_file = "help_button.png"
Globals.help_button = ImageTk.PhotoImage(file=help_button_file)

done_button_file = "done_button.png"
Globals.done_button_image = ImageTk.PhotoImage(file=done_button_file)

CoMet_border_dark_file = "border.png"
CoMet_border_dark = ImageTk.PhotoImage(file=CoMet_border_dark_file)

CoMet_border_light_file = "border_light.png"
CoMet_border_light = ImageTk.PhotoImage(file=CoMet_border_light_file)

CoMet_save_button_file = "save_button2.png"
CoMet_save_button = ImageTk.PhotoImage(file=CoMet_save_button_file)
Globals.save_button = ImageTk.PhotoImage(file=CoMet_save_button_file)

CoMet_correct_button_file = "correct_button.png"
CoMet_correct_button_image= ImageTk.PhotoImage(file=CoMet_correct_button_file)

CoMet_clear_all_button_file = "icon_clear_all.png"
CoMet_clear_all_button_image = ImageTk.PhotoImage(file=CoMet_clear_all_button_file)

dose_response_clear_all_button_file = "icon_clear_all_small.png"
dose_response_clear_all_button_image = \
    ImageTk.PhotoImage(file=dose_response_clear_all_button_file)

CoMet_empty_image_file = "empty_corrected_image.png"
CoMet_empty_image_image = ImageTk.PhotoImage(file=CoMet_empty_image_file)

dose_response_calibration_button_file = "save_calibration_button.png"
dose_response_calibration_button_image = \
    ImageTk.PhotoImage(file=dose_response_calibration_button_file)

dose_response_dose_border_file = "dose_border.png"
Globals.dose_response_dose_border = \
    ImageTk.PhotoImage(file=dose_response_dose_border_file)

profiles_add_doseplan_button_file = "add_doseplan_button.png"
Globals.profiles_add_doseplan_button_image = \
    ImageTk.PhotoImage(file=profiles_add_doseplan_button_file)

profiles_add_film_button_file = "add_film_button.png"
profiles_add_film_button_image = \
    ImageTk.PhotoImage(file=profiles_add_film_button_file)

profiles_add_rtplan_button_file = "add_rtplan_button.png"
profiles_add_rtplan_button_image = \
    ImageTk.PhotoImage(file=profiles_add_rtplan_button_file)

profiles_showPlanes_file = "planes.png"
Globals.profiles_showPlanes_image = \
    ImageTk.PhotoImage(file=profiles_showPlanes_file)

profiles_showDirections_file = 'depth_directions.png'
Globals.profiles_showDirections_image = \
    ImageTk.PhotoImage(file=profiles_showDirections_file)

profiles_mark_isocenter_button_file = 'mark_isocenter_button.png'
Globals.profiles_mark_isocenter_button_image = \
    ImageTk.PhotoImage(file=profiles_mark_isocenter_button_file)

profiles_mark_ROI_button_file = "mark_ROI_button.png"
Globals.profiles_mark_ROI_button_image = \
    ImageTk.PhotoImage(file=profiles_mark_ROI_button_file)

profiles_scanned_image_text_image_file = "scanned_image_text_image.png"
Globals.profiles_scanned_image_text_image = \
    ImageTk.PhotoImage(file=profiles_scanned_image_text_image_file)

profiles_film_dose_map_text_image_file = "film_dose_map_text_image.png"
Globals.profiles_film_dose_map_text_image = \
    ImageTk.PhotoImage(file=profiles_film_dose_map_text_image_file)

profiles_doseplan_text_image_file = "doseplan_text_image.png"
Globals.profiles_doseplan_text_image = \
    ImageTk.PhotoImage(file=profiles_doseplan_text_image_file)

profiles_mark_point_file = "mark_point_button.png"
Globals.profiles_mark_point_button_image = \
    ImageTk.PhotoImage(file=profiles_mark_point_file)

profiles_add_doseplans_button_file = "add_doseplan.png"
Globals.profiles_add_doseplans_button_image = \
    ImageTk.PhotoImage(file=profiles_add_doseplans_button_file)

adjust_button_left_file = "adjust_button_left.png"
Globals.adjust_button_left_image = ImageTk.PhotoImage(file=adjust_button_left_file)

adjust_button_right_file = "adjust_button_right.png"
Globals.adjust_button_right_image = \
    ImageTk.PhotoImage(file=adjust_button_right_file)

adjust_button_down_file = "adjust_button_down.png"
Globals.adjust_button_down_image = ImageTk.PhotoImage(file=adjust_button_down_file)

adjust_button_up_file = "adjust_button_up.png"
Globals.adjust_button_up_image = ImageTk.PhotoImage(file=adjust_button_up_file)

dose_response_upload_files_here_file = "upload_here_dose_response.png"
Globals.dose_response_upload_files_here = \
    ImageTk.PhotoImage(file=dose_response_upload_files_here_file)

dose_response_equation_will_be_here_file = "equation_will_be_here.png"
Globals.dose_response_equation_written_here = \
    ImageTk.PhotoImage(file=dose_response_equation_will_be_here_file)

export_plot_file = "export_plot_button.png"
Globals.export_plot_button_image = ImageTk.PhotoImage(file=export_plot_file)

DVH_add_structure_file = "add_structure.png"
DVH_add_structure_button_image = ImageTk.PhotoImage(file=DVH_add_structure_file)

DVH_temp_image_file = "temp_doseplan_roi.png"
Globals.dVH_temp_image = ImageTk.PhotoImage(file=DVH_temp_image_file)


####################################                 ###############################
#################################### Tab 1 INTRO TAB ###############################
####################################                 ###############################

#-----------------------------------------------------------------------------------
# Code to place all widgets on the first tab "Fidora" in Fidora
# They are all placed in a canvas, intro_tab_canvas given in the global tab 
# intro_tab, which is defined in the file Globals.py.
#-----------------------------------------------------------------------------------
intro_tab_canvas = tk.Canvas(Globals.intro_tab)
intro_tab_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

tab1_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab1_text_box.grid(row=0, column=0, pady=(30,30), padx=(55,0))
tab1_text_box.config(bd=0, bg='#E5f9ff')

tab1_title_text = tk.Text(tab1_text_box, height=1, width=6)
tab1_title_text.insert(END, "CoMet")
tab1_title_text.grid(in_=tab1_text_box, row=0, column = 0, \
    pady=(15,5), padx=(10,10))
tab1_title_text.config(state=DISABLED, bd=0, bg ='#E5f9ff', \
    fg='#130e07', font=('calibri', '25', 'bold'))
tab1_text_box.grid_columnconfigure(0,weight=1)
tab1_text_box.grid_rowconfigure(0,weight=1)

tab1_text = tk.Text(tab1_text_box, height=4, width=43)
tab1_text.grid(in_=tab1_text_box, row=1, column=0, sticky=N+S+W+E, \
    pady=(0,0), padx=(20,20))
tab1_text.insert(INSERT,"Correct your scanned images using CoMet. A method \n\
developed to correct for non-uniformity introduced\n by the scanner. \
The correction is based on absolute \nsubtraction.")
tab1_text.config(state=DISABLED, bd=0, bg='#E5f9ff', \
    fg='#130E07', font=('calibri', '13'))
tab1_text_box.grid_columnconfigure(1,weight=1)
tab1_text_box.grid_rowconfigure(1,weight=1) 

tab1_box_figure = Image.open("icon_comet.png")
tab1_figure = ImageTk.PhotoImage(tab1_box_figure)
tab1_figure_label = Label(tab1_text_box, image=tab1_figure)
tab1_figure_label.image = tab1_figure
tab1_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab1_figure_label.config(bg='#E5f9ff')
tab1_text_box.grid_columnconfigure(3, weight=1)
tab1_text_box.grid_rowconfigure(3, weight=1)

tab2_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab2_text_box.grid(row=0, column=1, pady=(30,30), padx=(65,0))
tab2_text_box.config(bd=0, bg='#E5f9ff')

tab2_title = tk.Text(tab2_text_box, height=1, width=12)
tab2_title.grid(in_=tab2_text_box, row=0, column = 0, \
    pady=(15,5), padx=(10,10))
tab2_title.insert(INSERT, "Dose response")
tab2_title.config(state=DISABLED, bd=0, bg = '#E5f9ff', \
    fg='#130e07', font=('calibri', '25', 'bold'))
tab2_text_box.grid_columnconfigure(0, weight=1)
tab2_text_box.grid_rowconfigure(0, weight=1)

tab2_text = tk.Text(tab2_text_box, height=4, width=43)
tab2_text.grid(in_=tab2_text_box, row=1, column=0, \
    sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab2_text.insert(INSERT,"Make a calibration curve and read the dose response \n\
function. For every new batch of GafChromic film \nthere is a need to update\
the dose response. All three \nchannels (RGB) are read and calculated.")
tab2_text.config(state=DISABLED, bd=0, bg='#E5f9ff', \
    fg='#130E07', font=('calibri', '13')) 
tab2_text_box.grid_columnconfigure(1, weight=1)
tab2_text_box.grid_rowconfigure(1, weight=1)

tab2_box_figure = Image.open("icon_map_dose.png")
tab2_figure = ImageTk.PhotoImage(tab2_box_figure)
tab2_figure_label = Label(tab2_text_box, image=tab2_figure)
tab2_figure_label.image = tab2_figure
tab2_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab2_figure_label.config(bg='#E5f9ff')
tab2_text_box.grid_columnconfigure(3, weight=1)
tab2_text_box.grid_rowconfigure(3, weight=1)

tab3_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab3_text_box.grid(row=1, column=0, pady=(0,30), padx=(55,0))
tab3_text_box.config(bd=0, bg='#E5f9ff')

tab3_title = tk.Text(tab3_text_box, height=1, width=8)
tab3_title.grid(in_=tab3_text_box, row=0, column = 0, pady=(15,5), padx=(10,10))
tab3_title.insert(INSERT, "Profiles")
tab3_title.config(state=DISABLED, bd=0, bg = '#E5f9ff', \
    fg='#130e07', font=('calibri', '25', 'bold'))
tab3_text_box.grid_columnconfigure(0, weight=1)
tab3_text_box.grid_rowconfigure(0, weight=1)

tab3_text = tk.Text(tab3_text_box, height=4, width=43)
tab3_text.grid(in_=tab3_text_box, row=1, column=0, \
    sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab3_text.insert(INSERT,"Investigate profiles measured using GafChromic \n\
film and compare with the profiles in your treatment \nplan. Draw vertical, \
horizontal or manually drawn profiles.")
tab3_text.config(state=DISABLED, bd=0, bg='#E5f9ff', \
    fg='#130E07', font=('calibri', '13'))
tab3_text_box.grid_columnconfigure(1, weight=1)
tab3_text_box.grid_rowconfigure(1, weight=1)

tab3_box_figure = Image.open("icon_dose_response.png")
tab3_figure = ImageTk.PhotoImage(tab3_box_figure)
tab3_figure_label = Label(tab3_text_box, image=tab3_figure)
tab3_figure_label.image = tab3_figure
tab3_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab3_figure_label.config(bg='#E5f9ff')
tab3_text_box.grid_columnconfigure(3, weight=1)
tab3_text_box.grid_rowconfigure(3, weight=1)

tab4_text_box = tk.Frame(intro_tab_canvas, height=230, width=400)
tab4_text_box.grid(row=1, column=1, pady=(0,30), padx=(65,0))
tab4_text_box.config(bd=0, bg='#E5f9ff')

tab4_title = tk.Text(tab4_text_box, height=1, width=7)
tab4_title.grid(in_=tab4_text_box, row=0, column = 0, pady=(15,5), padx=(10,10))
tab4_title.insert(INSERT, "DVH")
tab4_title.config(state=DISABLED, bd=0, bg = '#E5f9ff', \
    fg='#130e07', font=('calibri', '25', 'bold'))
tab4_text_box.grid_columnconfigure(0,weight=1)
tab4_text_box.grid_rowconfigure(0, weight=1)

tab4_text = tk.Text(tab4_text_box, height=4, width=43)
tab4_text.grid(in_=tab4_text_box, row=1, column=0, \
    sticky=N+S+W+E, pady=(0,0), padx=(20,20))
tab4_text.insert(INSERT,"Study the dose volume histogram measured\n\
in your scanned film and doseplan for comparison. \nInclude the \
volumes of your choice.")
tab4_text.config(state=DISABLED, bd=0, bg='#E5f9ff', \
    fg='#130E07', font=('calibri', '13')) 
tab4_text_box.grid_columnconfigure(1, weight=1)
tab4_text_box.grid_rowconfigure(1, weight=1)

tab4_box_figure = Image.open("icon_profiles.png")
tab4_figure = ImageTk.PhotoImage(tab4_box_figure)
tab4_figure_label = Label(tab4_text_box, image=tab4_figure)
tab4_figure_label.image = tab4_figure
tab4_figure_label.grid(row=3, sticky=N+S+W+E, pady=(0,10))
tab4_figure_label.config(bg='#E5f9ff')
tab4_text_box.grid_columnconfigure(3, weight=1)
tab4_text_box.grid_rowconfigure(3, weight=1)

intro_tab_canvas.grid(row=0, column=0, sticky=N+S+W)

####################################               #################################
#################################### TAB 2 - CoMet #################################
####################################               #################################

#-----------------------------------------------------------------------------------
# Code to place widgets in the second tab "CoMet" in Fidora
# They are all placed in the global canvas tab1_canvas defined
# in the the file Globals.py. Where functions is called the
# functions are written in the file CoMet_functions.py
#-----------------------------------------------------------------------------------

Globals.tab1_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

CoMet_explained = tk.Text(Globals.tab1_canvas, height=5, width=84)
CoMet_explained.insert(INSERT, \
"Start the correction by choosing the correct *.tif file containing the scanned \n\
image of the GafChromic film. The film should be scanned using Epson Perfection \n\
v750 Pro with dpi setting 72 or 127. Then pick which folder the corrected file \n\
should be uploaded to. The corrected file will be saved as a DICOM. Write \
filename \nand patient name (optional) before doing the correction. An illustration \
of the \ncorrected image will appear.")
CoMet_explained.grid(row=0, column = 0, columnspan=1, \
    sticky=N+S+E+W, padx=(20,0), pady=(10,10))
Globals.tab1_canvas.grid_columnconfigure(0, weight=0)
Globals.tab1_canvas.grid_rowconfigure(0, weight=0)
CoMet_explained.config(state=DISABLED, bg='#ffffff', \
    font=('calibri', '11'), relief=FLAT)

Globals.CoMet_border_1_label = Label(Globals.tab1_canvas, \
    image = CoMet_border_dark,width=50)
Globals.CoMet_border_1_label.image=CoMet_border_dark
Globals.CoMet_border_1_label.grid(row=2, column=0, columnspan=2, \
    sticky=N+E+W, padx=(0,80), pady=(0,0))
Globals.tab1_canvas.grid_columnconfigure(1, weight=0)
Globals.tab1_canvas.grid_rowconfigure(1, weight=0)
Globals.CoMet_border_1_label.config(bg='#ffffff', borderwidth=0)

CoMet_upload_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_upload_button_frame.grid(row=2, column = 0, \
    padx = (200, 0), pady=(0,0), sticky=N)
Globals.tab1_canvas.grid_columnconfigure(2, weight=0)
Globals.tab1_canvas.grid_rowconfigure(2, weight=0)
CoMet_upload_button_frame.config(bg = '#ffffff')

CoMet_upload_button = tk.Button(CoMet_upload_button_frame, text='Browse', \
    image = Globals.upload_button_image, cursor='hand2',font=('calibri', '9'), \
        relief=FLAT, state=ACTIVE, command=CoMet_functions.UploadAction)
CoMet_upload_button.pack(expand=True, fill=BOTH)
CoMet_upload_button.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
CoMet_upload_button.image = Globals.upload_button_image

Globals.CoMet_uploaded_file_text = tk.Text(Globals.CoMet_border_1_label, \
    height=1, width=31)
Globals.CoMet_uploaded_file_text.grid(row=0, column=0, columnspan=2, \
    sticky=E, pady=(20,20), padx=(100,0))
Globals.CoMet_uploaded_file_text.insert(INSERT, \
    "Upload the image you want to correct")
Globals.CoMet_uploaded_file_text.config(state=DISABLED, bd=0, \
    font=('calibri', '10'), fg='gray', bg='#ffffff')

Globals.CoMet_border_2_label = Label(Globals.tab1_canvas, image = \
    CoMet_border_dark,width=50)
Globals.CoMet_border_2_label.image=CoMet_border_dark
Globals.CoMet_border_2_label.grid(row=3, column=0, columnspan=2, \
    sticky = N+W+E, padx = (0, 80), pady=(5,0))
Globals.tab1_canvas.grid_columnconfigure(3, weight=0)
Globals.tab1_canvas.grid_rowconfigure(3, weight=0)
Globals.CoMet_border_2_label.config(bg='#ffffff', borderwidth=0)

CoMet_folder_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_folder_button_frame.grid(row=3, column = 0, padx = (200, 0), \
    pady=(10,0), sticky=N)
Globals.tab1_canvas.grid_columnconfigure(4, weight=0)
Globals.tab1_canvas.grid_rowconfigure(4, weight=0)
CoMet_folder_button_frame.config(bg = '#ffffff')

CoMet_folder_button = tk.Button(CoMet_folder_button_frame, text='Browse', \
    image = select_folder_image ,cursor='hand2',font=('calibri', '14'),\
    relief=FLAT, state=ACTIVE, command=CoMet_functions.setCoMet_export_folder)
CoMet_folder_button.pack(expand=True, fill=BOTH)
CoMet_folder_button.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
CoMet_folder_button.image=select_folder_image

CoMet_save_to_folder = tk.Text(Globals.CoMet_border_2_label, height=1, width=31)
CoMet_save_to_folder.grid(row=0, column=0, columnspan=2, \
    sticky=E, pady=(20,20), padx=(100,0))
CoMet_save_to_folder.insert(INSERT,"Folder to save the corrected image")
CoMet_save_to_folder.config(state=DISABLED, bd=0, \
    font=('calibri', '10'), fg='gray', bg='#ffffff') 

def testFilename():
#----------------------------------------------------
# Function to test the filename the user chooses for 
# the corrected image. The filename must be no longer
# than 20 characters and only letters and/or
# numbers are valid characters. Default: "Error!".
# Once approved the filename is given to the global
# variable CoMet_corrected_image_filename
#----------------------------------------------------
    Globals.CoMet_corrected_image_filename.set\
        (Globals.CoMet_save_filename.get("1.0",'end-1c'))
    if(Globals.CoMet_corrected_image_filename.get() == \
        " " or Globals.CoMet_corrected_image_filename.get() == "Filename"):
        Globals.CoMet_corrected_image_filename.set("Error!")
    elif(len(Globals.CoMet_corrected_image_filename.get()) >21):
        messagebox.showerror("Error", "The filename must be under 20 characters")
        Globals.CoMet_corrected_image_filename.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", \
        (Globals.CoMet_corrected_image_filename.get()).lstrip())==None):
        messagebox.showerror\
            ("Error","Filename can only contain letters and/or numbers")
        Globals.CoMet_corrected_image_filename.set("Error!")
    else:
        Globals.CoMet_save_button_1.config(state=DISABLED)
        Globals.CoMet_save_filename.config(state=DISABLED)
        Globals.CoMet_progressbar_counter += 1
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        Globals.CoMet_progressbar_text = \
            tk.Text(Globals.tab1_canvas, width = 5, height=1)
        Globals.CoMet_progressbar_text.grid(row=1, column=0, columnspan=1, \
            sticky=E, padx=(0,158), pady=(0,36))
        Globals.CoMet_progressbar_text.insert(INSERT, \
            str(Globals.CoMet_progressbar_counter*25) + "%")
        if(Globals.CoMet_progressbar_counter*25 == 100):
            Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, \
                relief=FLAT, bg='#2C8EAD', font=('calibri', '10', 'bold'))
        else:
            Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, \
                relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
    

Globals.CoMet_border_3_label = Label(Globals.tab1_canvas, \
    image = CoMet_border_dark)
Globals.CoMet_border_3_label.image=CoMet_border_dark
Globals.CoMet_border_3_label.grid(row=4, column=0, columnspan=2, \
    sticky = N+W+E, padx = (0,80), pady=(5,0))
Globals.tab1_canvas.grid_columnconfigure(5, weight=0)
Globals.tab1_canvas.grid_rowconfigure(5, weight=0)
Globals.CoMet_border_3_label.config(bg='#ffffff', borderwidth=0)

Globals.CoMet_save_button_frame_1 = tk.Frame(Globals.tab1_canvas)
Globals.CoMet_save_button_frame_1.grid(row=4, column = 0, \
    padx = (200, 0), pady=(10,0), sticky=N)
Globals.tab1_canvas.grid_columnconfigure(6, weight=0)
Globals.tab1_canvas.grid_rowconfigure(6, weight=0)
Globals.CoMet_save_button_frame_1.config(bg = '#ffffff')

Globals.CoMet_save_button_1 = tk.Button(Globals.CoMet_save_button_frame_1, \
    text='Save', image = CoMet_save_button ,cursor='hand2',font=('calibri', '14'),\
        relief=FLAT, state=ACTIVE, command=testFilename)
Globals.CoMet_save_button_1.pack(expand=True, fill=BOTH)
Globals.CoMet_save_button_1.config(bg='#ffffff', \
    activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.CoMet_save_button_1.image = CoMet_save_button

Globals.CoMet_save_filename = tk.Text(Globals.CoMet_border_3_label,\
     height=1, width=30)
Globals.CoMet_save_filename.grid(row=0, column=0, columnspan=2, \
    sticky=E+W, pady=(20,20), padx=(100,0))
Globals.CoMet_save_filename.insert(END,"Filename (will be saved as *.dcm)")
Globals.CoMet_save_filename.config(state=NORMAL, bd=0, \
    font=('calibri', '10'), fg='gray', bg='#ffffff')

def writeFilename(event):
#----------------------------------------------------
# Callback function to mouse-events.
# Function to delete the default text "Filename (will
# be saved as *.dcm)\n" in the global textbox
# CoMet_save_filename when focus is on textbox and
# insert the default text as focus is out unless 
# a filename has been written by the user.
#----------------------------------------------------
    current = Globals.CoMet_save_filename.get("1.0", tk.END)
    if(current == "Filename (will be saved as *.dcm)\n"):
        Globals.CoMet_save_filename.delete("1.0", tk.END)
    else:
        Globals.CoMet_save_filename.insert("1.0", \
            "Filename (will be saved as *.dcm)")

Globals.CoMet_save_filename.bind("<FocusIn>", writeFilename)
Globals.CoMet_save_filename.bind("<FocusOut>", writeFilename)


def testName():
#----------------------------------------------------
# Function to test if the user defined global 
# variable CoMet_patientName has been given a valid 
# value. The patient name/ID must be less than 30 
# characters and letters and/or numbers. Once the 
# value is approved it is given to the gloabal 
# variable CoMet_patientName
#----------------------------------------------------
    Globals.CoMet_patientName.set(CoMet_save_patientName.get("1.0",'end-1c'))
    if(Globals.CoMet_patientName.get() == " " or \
        Globals.CoMet_patientName.get() == "Patient name"):
        Globals.CoMet_patientName.set("Error!")
    elif(len(Globals.CoMet_patientName.get()) >31):
        messagebox.showerror("Error", "The Name must be under 30 characters")
        Globals.CoMet_patientName.set("Error!")
    elif(re.match("^[A-Za-z0-9_]*$", \
        (Globals.CoMet_patientName.get()).lstrip())==None):
        messagebox.showerror("Error",\
            "Name can only contain letters (not æ,ø,å) and no spaces")
        Globals.CoMet_patientName.set("Error!")
    else:
        CoMet_save_button_2.config(state=DISABLED)
        CoMet_save_patientName.config(state=DISABLED)


Globals.CoMet_border_4_label = Label(Globals.tab1_canvas, \
    image = CoMet_border_dark)
Globals.CoMet_border_4_label.image=CoMet_border_dark
Globals.CoMet_border_4_label.grid(row=5, column=0, columnspan=2, \
    sticky =N+W+E, padx = (0, 80), pady=(0,3))
Globals.tab1_canvas.grid_columnconfigure(7, weight=0)
Globals.tab1_canvas.grid_rowconfigure(7, weight=0)
Globals.CoMet_border_4_label.config(bg='#ffffff', borderwidth=0)

CoMet_save_button_frame_2 = tk.Frame(Globals.tab1_canvas)
CoMet_save_button_frame_2.grid(row=5, column = 0, \
    padx = (200, 0), pady=(3,0), sticky=N)
Globals.tab1_canvas.grid_columnconfigure(8, weight=0)
Globals.tab1_canvas.grid_rowconfigure(8, weight=0)
CoMet_save_button_frame_2.config(bg = '#ffffff')

CoMet_save_button_2 = tk.Button(CoMet_save_button_frame_2, \
    text='Save', image = CoMet_save_button ,cursor='hand2',\
        font=('calibri', '14'),relief=FLAT, state=ACTIVE, command=testName)
CoMet_save_button_2.pack(expand=True, fill=BOTH)
CoMet_save_button_2.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
CoMet_save_button_2.image = CoMet_save_button

CoMet_save_patientName = tk.Text(Globals.CoMet_border_4_label, height=1, width=30)
CoMet_save_patientName.grid(row=0, column=0, columnspan=2, \
    sticky=E+W, pady=(20,20), padx=(100,0))
CoMet_save_patientName.insert(END,"Patient name (Optional)")
CoMet_save_patientName.config(state=NORMAL, bd=0, \
    font=('calibri', '10'), fg='gray', bg='#ffffff')

def writePname(event):
#----------------------------------------------------
# Callback function to mouse-events.
# Function to delete the default text "Patient name
# (Optional)\n" when focus is on the textbox
# CoMet_save_patientName, and insert the default text
# when focus is out of the textbox, unless the user
# has defined a valid value to the variable
# CoMet_save_patientName
#----------------------------------------------------
    current = CoMet_save_patientName.get("1.0", tk.END)
    if(current == "Patient name (Optional)\n"):
        CoMet_save_patientName.delete("1.0", tk.END)
    else:
        CoMet_save_patientName.insert("1.0", "Patient name (Optional)")

CoMet_save_patientName.bind("<FocusIn>", writePname)
CoMet_save_patientName.bind("<FocusOut>", writePname)

CoMet_correct_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_correct_button_frame.grid(row=6, column=0,rowspan=1, \
    padx = (150, 0), pady=(10,0), sticky=W)
Globals.tab1_canvas.grid_columnconfigure(9, weight=0)
Globals.tab1_canvas.grid_rowconfigure(9, weight=0)
CoMet_correct_button_frame.config(bg = '#ffffff')

CoMet_correct_button = tk.Button(CoMet_correct_button_frame, text='Correct', \
    image = CoMet_correct_button_image ,cursor='hand2',font=('calibri', '14'),\
        relief=FLAT, state=ACTIVE, command=CoMet_functions.Correct)
CoMet_correct_button.pack(expand=True, fill=BOTH)
CoMet_correct_button.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
CoMet_correct_button.image = CoMet_correct_button_image

Globals.CoMet_print_corrected_image = tk.Canvas(Globals.tab1_canvas)
Globals.CoMet_print_corrected_image.grid(row=0, column=2, rowspan=7, \
    sticky=N+W+S, pady=(20,0), padx=(0,150))
Globals.CoMet_print_corrected_image.config(bg='#ffffff', bd = 0, \
    relief=FLAT, highlightthickness=0)
Globals.tab1_canvas.grid_columnconfigure(11,weight=0)
Globals.tab1_canvas.grid_rowconfigure(11, weight=0)
Globals.CoMet_print_corrected_image.create_image(180,250,\
    image=CoMet_empty_image_image)
Globals.CoMet_print_corrected_image.image=CoMet_empty_image_image


def clearAll():
#----------------------------------------------------
# Function to reset every variable created in the
# tab CoMet. This will delete every value saved
# in variables related to CoMet
#----------------------------------------------------
    #Clear out filename
    Globals.CoMet_uploaded_file_text = tk.Text(Globals.CoMet_border_1_label, \
        height=1, width=31)
    Globals.CoMet_uploaded_file_text.grid(row=0, column=0, columnspan=2, \
        sticky=E+W, pady=(20,20), padx=(100,0))
    Globals.CoMet_uploaded_file_text.insert(INSERT, \
        "Upload the image you want to correct")
    Globals.CoMet_uploaded_file_text.config(state=DISABLED, \
        bd=0, font=('calibri', '10'), fg='gray', bg='#ffffff')
    Globals.CoMet_uploaded_filename.set("Error!")

    #Clear out folder
    CoMet_save_to_folder = tk.Text(Globals.CoMet_border_2_label, \
        height=1, width=31)
    CoMet_save_to_folder.grid(row=0, column=0, columnspan=2, \
        sticky=E+W, pady=(20,20), padx=(100,0))
    CoMet_save_to_folder.insert(INSERT,"Folder to save the corrected image")
    CoMet_save_to_folder.config(state=DISABLED, bd=0, font=('calibri', '10'), \
        fg='gray', bg='#ffffff')
    Globals.CoMet_export_folder.set("Error!")

    #Clear filename of corrected file
    Globals.CoMet_save_filename = tk.Text(Globals.CoMet_border_3_label, \
        height=1, width=30)
    Globals.CoMet_save_filename.grid(row=0, column=0, columnspan=2, \
        sticky=E+W, pady=(20,20), padx=(100,0))
    Globals.CoMet_save_filename.insert(END,"Filename (will be saved as *.dcm)")
    Globals.CoMet_save_filename.config(state=NORMAL, bd=0, \
        font=('calibri', '10'), fg='gray', bg='#ffffff')
    Globals.CoMet_corrected_image_filename.set("Error!")
    Globals.CoMet_save_button_1.config(state=ACTIVE)

    def writeFilename(event):
#----------------------------------------------------
# Callback function to mouse-events.
# Function to delete the default text "Filename (will
# be saved as *.dcm)\n" in the global textbox
# CoMet_save_filename when focus is on textbox and
# insert the default text as focus is out unless 
# a filename has been written by the user.
#----------------------------------------------------
        current = Globals.CoMet_save_filename.get("1.0", tk.END)
        if(current == "Filename (will be saved as *.dcm)\n"):
            Globals.CoMet_save_filename.delete("1.0", tk.END)
        else:
            Globals.CoMet_save_filename.insert("1.0", \
                "Filename (will be saved as *.dcm)")

    Globals.CoMet_save_filename.bind("<FocusIn>", writeFilename)
    Globals.CoMet_save_filename.bind("<FocusOut>", writeFilename)

    #Clear patientname
    CoMet_save_patientName = tk.Text(Globals.CoMet_border_4_label, \
        height=1, width=30)
    CoMet_save_patientName.grid(row=0, column=0, columnspan=2, \
        sticky=E+W, pady=(20,20), padx=(100,0))
    CoMet_save_patientName.insert(END,"Patient name (Optional)")
    CoMet_save_patientName.config(state=NORMAL, bd=0, \
        font=('calibri', '10'), fg='gray', bg='#ffffff')
    Globals.CoMet_patientName.set("Error!")
    CoMet_save_button_2.config(state=ACTIVE)

    def writePname(event):
#----------------------------------------------------
# Callback function to mouse-events.
# Function to delete the default text "Patient name
# (Optional)\n" when focus is on the textbox
# CoMet_save_patientName, and insert the default text
# when focus is out of the textbox, unless the user
# has defined a valid value to the variable
# CoMet_save_patientName
#----------------------------------------------------
        current = CoMet_save_patientName.get("1.0", tk.END)
        if(current == "Patient name (Optional)\n"):
            CoMet_save_patientName.delete("1.0", tk.END)
        else:
            CoMet_save_patientName.insert("1.0", "Patient name (Optional)")


    CoMet_save_patientName.bind("<FocusIn>", writePname)
    CoMet_save_patientName.bind("<FocusOut>", writePname)

    #Clear image
    Globals.CoMet_print_corrected_image.delete('all')
    Globals.CoMet_print_corrected_image.create_image\
        (123,148,image=CoMet_empty_image_image)
    Globals.CoMet_print_corrected_image.image = CoMet_empty_image_image

    #Clear progressbar
    Globals.CoMet_progressbar["value"]=0
    Globals.CoMet_progressbar_counter = 0
    Globals.CoMet_progressbar_check_file = True
    Globals.CoMet_progressbar_check_folder = True
    CoMet_progressbar_text = tk.Text(Globals.tab1_canvas, height=1, width=5)
    CoMet_progressbar_text.grid(row=1, column=0, columnspan=1, \
        sticky=E, padx=(0,158), pady=(0,36))
    CoMet_progressbar_text.insert(INSERT, "0%")
    CoMet_progressbar_text.config(state=DISABLED, bd=0, \
        relief=FLAT, bg='#ffffff',font=('calibri', '10', 'bold'))


CoMet_clear_all_button_frame = tk.Frame(Globals.tab1_canvas)
CoMet_clear_all_button_frame.grid(row=6, column=0, rowspan=1, \
    padx=(350,0), pady=(10,0), sticky=W)
Globals.tab1_canvas.grid_columnconfigure(13, weight=0)
Globals.tab1_canvas.grid_rowconfigure(13, weight=0)
CoMet_clear_all_button_frame.config(bg='#ffffff')

CoMet_clear_all_button = tk.Button(CoMet_clear_all_button_frame, text="Clear all",\
    image=dose_response_clear_all_button_image, cursor='hand2', \
        font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=clearAll)
CoMet_clear_all_button.pack(expand=True, fill=BOTH)
CoMet_clear_all_button.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
CoMet_clear_all_button.image=dose_response_clear_all_button_image

Globals.tab1_canvas.pack(expand=True, fill=BOTH)


################################                       #############################
################################ TAB 3 - Dose Response #############################
################################                       #############################

#-----------------------------------------------------------------------------------
# Code to place all widgets related to the tab "Dose Response" in Fidora.
# They are all placed in the global canvas tab2_canvas defines in 
# the file Globals.py. Whenever a function is called the function 
# is written in the file Dose_Response_Function.
#-----------------------------------------------------------------------------------

Globals.tab2_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

dose_response_explain_text = tk.Text(Globals.tab2_canvas, height=4, width=140)
dose_response_explain_text.insert(INSERT, "\
Upload the scanned *.tif files (there should be at least 3 of each dose level) \
and save. The dose response curve along with the equation will appear when \n\
enough data points are given. The uploaded files must have dpi setting 72 or 127. \
When saving the calibration the dose response data will be saved and can be \
\nchosen for later use of this software. The dose response curve will be found \
for all three color channels, but can be removed using the check boxes. A dose \
\nresponse equation will only be fitted for the red channel.  " )
dose_response_explain_text.grid(row=0, column=0, columnspan=5, \
    sticky=N+S+E+W, pady=(20,20), padx=(20,10))
Globals.tab2_canvas.grid_columnconfigure(0, weight=0)
Globals.tab2_canvas.grid_rowconfigure(0, weight=0)
dose_response_explain_text.config(state=DISABLED, \
    font=('calibri', '11'), bg ='#ffffff', relief=FLAT)

dose_response_upload_button_frame = tk.Frame(Globals.tab2_canvas_files)
dose_response_upload_button_frame.grid(row=0, column = 0, \
    columnspan=8, padx = (60, 0), pady=(10,5))
Globals.tab2_canvas_files.grid_columnconfigure(0, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(0, weight=0)
dose_response_upload_button_frame.config(bg = '#ffffff')

dose_response_upload_button = \
    tk.Button(dose_response_upload_button_frame, text='Upload file', \
    image=Globals.upload_button_image,cursor='hand2', font=('calibri', '14'), \
        relief=FLAT, state=ACTIVE, command=Dose_response_functions.create_window)
dose_response_upload_button.pack(expand=True, fill=BOTH)
dose_response_upload_button.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
dose_response_upload_button.image = Globals.upload_button_image

check1 = Checkbutton(Globals.tab2_canvas_files, variable=Globals.dose_response_var1,\
    command=Dose_response_functions.plot_dose_response)
check1.grid(row=1, column=1, sticky=E, padx=(30,15))
Globals.tab2_canvas_files.grid_columnconfigure(5, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(5, weight=0)
check1.config(bg='#ffffff')

check2 = Checkbutton(Globals.tab2_canvas_files, \
    variable=Globals.dose_response_var2, \
        command=Dose_response_functions.plot_dose_response)
check2.grid(row=1, column=3, sticky=E, padx=(45,15))
Globals.tab2_canvas_files.grid_columnconfigure(6, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(6, weight=0)
check2.config(bg='#ffffff')

check3 = Checkbutton(Globals.tab2_canvas_files, \
    variable=Globals.dose_response_var3, \
        command=Dose_response_functions.plot_dose_response)
check3.grid(row=1, column=5, sticky=E, padx=(35,10))
Globals.tab2_canvas_files.grid_columnconfigure(7, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(7, weight=0)
check3.config(bg='#ffffff')

red = tk.Text(Globals.tab2_canvas_files, height=1, width=4)
red.insert(INSERT, "Red")
red.grid(row=1, column=1, sticky=W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(1, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(1, weight=0)
red.config(state=DISABLED, bd=0, font=('calibri', '12'))

green = tk.Text(Globals.tab2_canvas_files, height=1, width=5)
green.insert(INSERT, "Green")
green.grid(row = 1, column = 3, sticky=W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(2, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(2, weight=0)
green.config(state=DISABLED, bd=0, font=('calibri', '12'))

blue = tk.Text(Globals.tab2_canvas_files, height=1, width=4)
blue.insert(INSERT, "Blue")
blue.grid(row=1, column=5, sticky=W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(3, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(3, weight=0)
blue.config(state=DISABLED, bd=0, font=('calibri', '12'))

dose_title = tk.Text(Globals.tab2_canvas_files, height=1, width=10)
dose_title.insert(INSERT, "Dose (cGy)")
dose_title.grid(row=1, column=0, sticky=N+S+W+E, padx=(0,15))
Globals.tab2_canvas_files.grid_columnconfigure(4, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(4, weight=0)
dose_title.config(state=DISABLED, bd=0, font=('calibri', '12'))

Globals.upload_files_here_canvas = tk.Canvas(Globals.tab2_canvas_files)
Globals.upload_files_here_canvas.grid(row=3, column=0, \
    columnspan=13, sticky=N+S+W+E)
Globals.tab2_canvas_files.grid_columnconfigure(50, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(50, weight=0)
Globals.upload_files_here_canvas.config(relief=FLAT, bd=0, \
    bg='#ffffff',highlightthickness=0)
Globals.upload_files_here_canvas.create_image(70,30,\
    image=Globals.dose_response_upload_files_here, anchor='nw')

Globals.dose_response_equation_image = \
    tk.Canvas(Globals.dose_response_equation_frame, width=650)
Globals.dose_response_equation_image.grid(row=0, column=0, sticky=N+S+W+E)
Globals.dose_response_equation_frame.grid_columnconfigure(50, weight=0)
Globals.dose_response_equation_frame.grid_rowconfigure(50, weight=0)
Globals.dose_response_equation_image.config(bg='#ffffff', \
    relief=FLAT, highlightthickness=0)
Globals.dose_response_equation_image.create_image(170,0, \
    image=Globals.dose_response_equation_written_here, anchor='nw')

dose_response_save_calibration_button_frame = tk.Frame(Globals.tab2_canvas)
dose_response_save_calibration_button_frame.grid(row=3, column = 1, \
    sticky=N+S+E+W, padx=(0,0), pady=(0,0))
Globals.tab2_canvas.grid_columnconfigure(10, weight=0)
Globals.tab2_canvas.grid_rowconfigure(10, weight=0)
dose_response_save_calibration_button_frame.config\
    (bg = '#ffffff', height=1, width=100)
dose_response_save_calibration_button_frame.grid_propagate(0)

Globals.dose_response_save_calibration_button = \
    tk.Button(dose_response_save_calibration_button_frame, text='Save calibration', \
        image=dose_response_calibration_button_image, \
            cursor='hand2', font=('calibri', '12'),relief=FLAT, state=DISABLED, \
                command=Dose_response_functions.saveCalibration)
Globals.dose_response_save_calibration_button.pack(expand=True, fill=BOTH, side=TOP)
Globals.dose_response_save_calibration_button.config(bg='#ffffff', \
    activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.dose_response_save_calibration_button.image = \
    dose_response_calibration_button_image

dose_response_clear_all_button_frame = tk.Frame(Globals.tab2_canvas)
dose_response_clear_all_button_frame.grid(row=3, column=0, \
    sticky=N+S+E+W, padx=(30,0), pady=(0,0))
Globals.tab2_canvas.grid_columnconfigure(11, weight=0)
Globals.tab2_canvas.grid_rowconfigure(11, weight=0)
dose_response_clear_all_button_frame.config(bg='#ffffff', height=1, width=100)
dose_response_clear_all_button_frame.grid_propagate(0)

dose_response_clear_all_button = tk.Button(dose_response_clear_all_button_frame, \
    text='Clear all', image=dose_response_clear_all_button_image, \
        cursor='hand2', font=('calibri', '12'), relief=FLAT, state=ACTIVE, \
            command=Dose_response_functions.clear_all)
dose_response_clear_all_button.pack(expand=True, fill=BOTH, side=TOP)
dose_response_clear_all_button.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
dose_response_clear_all_button.image = dose_response_clear_all_button_image

delete_text = tk.Text(Globals.tab2_canvas_files, height=1, widt=7)
delete_text.insert(INSERT, "Delete")
delete_text.grid(row=1, column=7, sticky=N+S+E+W, padx=(0,0))
Globals.tab2_canvas_files.grid_columnconfigure(4, weight=0)
Globals.tab2_canvas_files.grid_rowconfigure(4, weight=0)
delete_text.config(state=DISABLED, bd=0, font=('calibri', '12'))

Globals.tab2_canvas.pack(expand=True, fill=BOTH)



####################################                  ##############################
#################################### TAB 4 - Profiles ##############################
####################################                  ##############################
#-----------------------------------------------------------------------------------
# Code to place all widgets related to the tab "Profiles" in Fidora
# They are all placed in the global canvas tab4_canvas defines
# in the file Globals.py.
# Whereever a function is called the function is written in 
# the file Profiles_functions.py.
#-----------------------------------------------------------------------------------

Globals.tab4_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

profiles_explain_text = tk.Text(Globals.tab4_canvas, height=4, width=140)
profiles_explain_text.insert(INSERT, "\
Upload a scanned image of film, along with the RT Plan and doseplan files from the \
corresponding doseplan and investigate the profiles. There are three \npossible \
profiles, horizontal, vertical and manually drawn profile.To make up for any \
positional error when scanning the film, or marking the \nisocenter/reference \
point, it is possible to make adjustments to the placement of the ROI in the film. \
This is done using the arrow buttons above the plot." )
profiles_explain_text.grid(row=0, column=0, columnspan=3, \
    sticky=N+S+E+W, pady=(20,20), padx=(20,10))
Globals.tab4_canvas.grid_columnconfigure(0, weight=0)
Globals.tab4_canvas.grid_rowconfigure(0, weight=0)
profiles_explain_text.config(state=DISABLED, \
    font=('calibri', '11'), bg ='#ffffff', relief=FLAT)
profiles_explain_text.grid_propagate(0)

profiles_upload_film_frame = tk.Frame(Globals.tab4_canvas)
profiles_upload_film_frame.grid(row=3, column = 0, sticky=N+S+W+E)
Globals.tab4_canvas.grid_columnconfigure(1, weight=0)
Globals.tab4_canvas.grid_rowconfigure(1, weight=0)
profiles_upload_film_frame.config(bg = '#ffffff', height=1, width=1)
profiles_upload_film_frame.grid_propagate(0)

Globals.profiles_upload_button_film = \
    tk.Button(profiles_upload_film_frame, text='Browse',\
    image = profiles_add_film_button_image, cursor='hand2',font=('calibri', '14'), \
        relief=FLAT, state=ACTIVE, command=Profile_functions.UploadFilm)
Globals.profiles_upload_button_film.pack(expand=True, fill=BOTH)
Globals.profiles_upload_button_film.config(bg='#ffffff', activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_upload_button_film.image = profiles_add_film_button_image

profiles_upload_doseplan_frame = tk.Frame(Globals.tab4_canvas)
profiles_upload_doseplan_frame.grid(row=5, column = 0, sticky=N+S+E+W)
Globals.tab4_canvas.grid_columnconfigure(3, weight=0)
Globals.tab4_canvas.grid_rowconfigure(3, weight=0)
profiles_upload_doseplan_frame.config(bg = '#ffffff', height=1, width=1)
profiles_upload_doseplan_frame.grid_propagate(0)

Globals.profiles_upload_button_doseplan = \
    tk.Button(profiles_upload_doseplan_frame, text='Browse',\
    image=Globals.profiles_add_doseplan_button_image, cursor='hand2', \
        font=('calibri', '14'), relief=FLAT, state=DISABLED, \
            command=Profile_functions.UploadDoseplan_button_function)
Globals.profiles_upload_button_doseplan.pack(expand=True, fill=BOTH)
Globals.profiles_upload_button_doseplan.configure(bg='#ffffff', \
    activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_upload_button_doseplan.image = \
    Globals.profiles_add_doseplan_button_image

profiles_upload_rtplan_frame = tk.Frame(Globals.tab4_canvas)
profiles_upload_rtplan_frame.grid(row=4, column=0, sticky=N+S+W+E)
Globals.tab4_canvas.grid_columnconfigure(10, weight=0)
Globals.tab4_canvas.grid_rowconfigure(10, weight=0)
profiles_upload_rtplan_frame.config(bg='#ffffff', height=1, width=1)
profiles_upload_rtplan_frame.grid_propagate(0)

Globals.profiles_upload_button_rtplan = \
    tk.Button(profiles_upload_rtplan_frame, text='Browse',\
    image=profiles_add_rtplan_button_image,cursor='hand2', font=('calibri', '14'), \
        relief=FLAT, state=DISABLED, command=Profile_functions.UploadRTplan)
Globals.profiles_upload_button_rtplan.pack(expand=True, fill=BOTH)
Globals.profiles_upload_button_rtplan.configure(bg='#ffffff', \
    activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_upload_button_rtplan.image=profiles_add_rtplan_button_image

profiles_film_orientation_frame = tk.Frame(Globals.tab4_canvas)
profiles_film_orientation_frame.grid(row=1, column=0, sticky=N+S+W+E)
profiles_film_orientation_frame.config(relief=FLAT, highlightthickness=0, \
    bd=0, bg='#ffffff', height=1, width=1)
Globals.tab4_canvas.grid_columnconfigure(2, weight=0)
Globals.tab4_canvas.grid_rowconfigure(2, weight=0)
profiles_film_orientation_frame.grid_propagate(0)

film_orientation_menu_text = tk.Text(profiles_film_orientation_frame, \
    width=14, height=1)
film_orientation_menu_text.insert(INSERT, "Film orientation:")
film_orientation_menu_text.config(state=DISABLED, \
    font=('calibri', '10'), bd = 0, relief=FLAT)
film_orientation_menu_text.pack(side=LEFT)

Globals.profiles_film_orientation_menu = OptionMenu(profiles_film_orientation_frame,\
    Globals.profiles_film_orientation, 'Axial', 'Coronal', 'Sagittal')
Globals.profiles_film_orientation_menu.pack(side=LEFT)
Globals.profiles_film_orientation_menu.config(bg = '#ffffff', width=15, relief=FLAT)

profiles_film_orientation_help_frame = tk.Frame(profiles_film_orientation_frame)
profiles_film_orientation_help_frame.pack(side=LEFT)
profiles_film_orientation_help_frame.configure(bg='#ffffff')

profiles_help_button_orientation = \
    tk.Button(profiles_film_orientation_help_frame, text='help',\
        image=Globals.help_button, cursor='hand2', font=('calibri', '14'), \
            relief=FLAT, state=ACTIVE, command=Profile_functions.help_showPlanes)
profiles_help_button_orientation.pack(expand=True, fill=BOTH)
profiles_help_button_orientation.configure(bg='#ffffff',activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
profiles_help_button_orientation.image=Globals.help_button

profiles_film_factor_frame = tk.Frame(Globals.tab4_canvas)
profiles_film_factor_frame.grid(row=2, column=0, sticky=N+S+W+E)
Globals.tab4_canvas.grid_columnconfigure(30, weight=0)
Globals.tab4_canvas.grid_rowconfigure(30, weight=0)
profiles_film_factor_frame.config(relief=FLAT, \
    highlightthickness=0, bd=0, bg='#ffffff', height=1, width=1)
profiles_film_factor_frame.grid_propagate(0)

profiles_film_factor = tk.Text(profiles_film_factor_frame, width=20, height=2)
profiles_film_factor.insert(INSERT, "Film factor \n(number of fractions):")
profiles_film_factor.config(state=DISABLED, \
    font=('calibri', '10'), bd = 0, relief=FLAT)
profiles_film_factor.pack(side=LEFT)

Globals.profiles_film_factor_input = \
    tk.Text(profiles_film_factor_frame, width=8, height=1)
Globals.profiles_film_factor_input.pack(side=LEFT)
Globals.profiles_film_factor_input.insert(INSERT, " ")
Globals.profiles_film_factor_input.config(state=NORMAL, \
    font=('calibri', '10'), bd = 2, bg='#ffffff')
Globals.tab4_canvas.grid_columnconfigure(31, weight=0)
Globals.tab4_canvas.grid_rowconfigure(31, weight=0)

profiles_resetAll_frame = tk.Frame(Globals.tab4_canvas)
profiles_resetAll_frame.grid(row=7,column=0, sticky=N+S+W+E)
Globals.tab4_canvas.grid_columnconfigure(5, weight=0)
Globals.tab4_canvas.grid_rowconfigure(5, weight=0)
profiles_resetAll_frame.config(bg='#ffffff', height=1, width=1)
profiles_resetAll_frame.grid_propagate(0)

profiles_resetAll_button = tk.Button(profiles_resetAll_frame, text='Reset', \
    image=dose_response_clear_all_button_image, cursor='hand2', \
        font=('calibri', '14'),relief=FLAT, state=ACTIVE, \
            command=Profile_functions.clearAll)
profiles_resetAll_button.pack(expand=True, fill=BOTH)
profiles_resetAll_button.configure(bg='#ffffff', activebackground='#ffffff', \
activeforeground='#ffffff', highlightthickness=0)
profiles_resetAll_button.image = dose_response_clear_all_button_image

Globals.profiles_adjust_button_left = \
    tk.Button(Globals.profiles_redefine_film_ROI_frame, \
    text="left", image=Globals.adjust_button_left_image,cursor='hand2', \
        font=('calibri', '12'), relief=FLAT, state=DISABLED, command=lambda: \
            Profile_functions.adjustROILeft\
                (Globals.profiles_choice_of_profile_line_type.get()))
Globals.profiles_adjust_button_left.pack(side=LEFT)
Globals.profiles_adjust_button_left.config(bg='#ffffff', activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_adjust_button_left.image = Globals.adjust_button_left_image

Globals.profiles_adjust_button_up = \
    tk.Button(Globals.profiles_redefine_film_ROI_frame, \
        text="left", image=Globals.adjust_button_up_image,cursor='hand2', \
            font=('calibri', '12'), relief=FLAT, state=DISABLED, command=lambda: \
                Profile_functions.adjustROIUp\
                    (Globals.profiles_choice_of_profile_line_type.get()))
Globals.profiles_adjust_button_up.pack(side=LEFT)
Globals.profiles_adjust_button_up.config(bg='#ffffff', activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_adjust_button_up.image = Globals.adjust_button_up_image

Globals.profiles_adjust_button_down = \
    tk.Button(Globals.profiles_redefine_film_ROI_frame, \
    text="left", image=Globals.adjust_button_down_image,cursor='hand2', \
        font=('calibri', '12'), relief=FLAT, state=DISABLED, command=lambda: \
            Profile_functions.adjustROIDown\
                (Globals.profiles_choice_of_profile_line_type.get()))
Globals.profiles_adjust_button_down.pack(side=LEFT)
Globals.profiles_adjust_button_down.config(bg='#ffffff', activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_adjust_button_down.image = Globals.adjust_button_down_image

Globals.profiles_adjust_button_right = \
    tk.Button(Globals.profiles_redefine_film_ROI_frame, text="left", \
        image=Globals.adjust_button_right_image,cursor='hand2', \
            font=('calibri', '12'),relief=FLAT, state=DISABLED, command=lambda: \
                Profile_functions.adjustROIRight\
                    (Globals.profiles_choice_of_profile_line_type.get()))
Globals.profiles_adjust_button_right.pack(side=LEFT)
Globals.profiles_adjust_button_right.config(bg='#ffffff',activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_adjust_button_right.image = Globals.adjust_button_right_image

Globals.profiles_adjust_button_return = \
    tk.Button(Globals.profiles_redefine_film_ROI_frame, \
    text="Original",cursor='hand2', font=('calibri', '12'), relief=FLAT, \
        state=DISABLED, command=lambda:Profile_functions.\
            returnToOriginalROICoordinates\
                (Globals.profiles_choice_of_profile_line_type.get()))
Globals.profiles_adjust_button_return.pack(side=LEFT)
Globals.profiles_adjust_button_return.config(bg='#ffffff',\
    activebackground='#ffffff',activeforeground='#ffffff', highlightthickness=0)

profiles_export_plot_frame= tk.Frame(Globals.tab4_canvas)
profiles_export_plot_frame.grid(row=6,column=0, sticky=N+S+W+E)
Globals.tab4_canvas.grid_columnconfigure(20, weight=0)
Globals.tab4_canvas.grid_rowconfigure(20, weight=0)
profiles_export_plot_frame.config(bg='#ffffff', height=1, width=1)
profiles_export_plot_frame.grid_propagate(0)

Globals.profiles_export_plot_button = \
    tk.Button(profiles_export_plot_frame, text = "Export plot", \
        image=Globals.export_plot_button_image, cursor='hand2', \
            font=('calibri', '12'), relief=FLAT, state=DISABLED, \
                command=Profile_functions.nothing_function)
Globals.profiles_export_plot_button.pack()
Globals.profiles_export_plot_button.config(bg='#ffffff',activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
Globals.profiles_export_plot_button.image = Globals.export_plot_button_image


Globals.profiles_choice_of_profile_line_type.trace_add('write', \
    Profile_functions.trace_profileLineType)


Globals.tab4_canvas.pack(expand=True, fill=BOTH)

##################################           #######################################
################################## Tab 5 DVH #######################################
##################################           #######################################
#-----------------------------------------------------------------------------------
# Code to place all widgets related to the tab "DVH" in Fidora. 
# They are all places in the global canvas tab5_canvas defined
# in the file Globals.py.
# Whereever a function is called the function is written in the
# file DVH_functions.py
#-----------------------------------------------------------------------------------

Globals.tab5_canvas.config(bg='#ffffff', bd = 0, relief=FLAT, highlightthickness=0)

DVH_explain_text = tk.Text(Globals.tab5_canvas, height=4, width=140)
DVH_explain_text.insert(INSERT, "\
Upload the scanned images of film, along with RT plan, stucture and doseplan \
files and study the dose volume histogram \nof the different defined volumes. \
By un-checking the buttons for each volume it is possible to hide the volume \n\
in the plot, making it easier to study each of them separately.")
DVH_explain_text.grid(row=0, column=0, columnspan=7, \
    sticky=N+S+E+W, pady=(20,20), padx=(20,10))
Globals.tab5_canvas.grid_columnconfigure(0, weight=0)
Globals.tab5_canvas.grid_rowconfigure(0, weight=0)
DVH_explain_text.config(state=DISABLED, \
    font=('calibri', '11'), bg ='#ffffff', relief=FLAT)

DVH_upload_film_frame = tk.Frame(Globals.tab5_canvas)
DVH_upload_film_frame.grid(row=3,column=0,padx=(50,40),pady=(10,20),sticky=N+S+W)
Globals.tab5_canvas.grid_columnconfigure(1, weight=0)
Globals.tab5_canvas.grid_rowconfigure(1, weight=0)
DVH_upload_film_frame.config(bg = '#ffffff')

Globals.DVH_upload_button_film = tk.Button(DVH_upload_film_frame, text='Browse', \
    image = profiles_add_film_button_image, cursor='hand2',font=('calibri', '14'),\
        relief=FLAT, state=ACTIVE, command=DVH_functions.UploadFilm)
Globals.DVH_upload_button_film.pack(expand=True, fill=BOTH)
Globals.DVH_upload_button_film.config(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
Globals.DVH_upload_button_film.image = profiles_add_film_button_image

DVH_upload_doseplan_frame = tk.Frame(Globals.tab5_canvas)
DVH_upload_doseplan_frame.grid(row=4,column=0,\
    padx=(210,0),sticky=N+S+W,pady=(10,20))
Globals.tab5_canvas.grid_columnconfigure(3, weight=0)
Globals.tab5_canvas.grid_rowconfigure(3, weight=0)
DVH_upload_film_frame.config(bg = '#ffffff')

Globals.DVH_upload_button_doseplan = \
    tk.Button(DVH_upload_doseplan_frame, text='Browse',\
    image=Globals.profiles_add_doseplan_button_image,cursor='hand2', \
        font=('calibri', '14'),relief=FLAT, state=DISABLED, \
            command=DVH_functions.UploadDoseplan_button_function)
Globals.DVH_upload_button_doseplan.pack(expand=True, fill=BOTH)
Globals.DVH_upload_button_doseplan.configure(bg='#ffffff', \
    activebackground='#ffffff',activeforeground='#ffffff', highlightthickness=0)
Globals.DVH_upload_button_doseplan.image = \
    Globals.profiles_add_doseplan_button_image

DVH_upload_rtplan_frame = tk.Frame(Globals.tab5_canvas)
DVH_upload_rtplan_frame.grid(row=3, column=0, \
    padx=(210,0), sticky=N+S+W, pady=(10,20))
Globals.tab5_canvas.grid_columnconfigure(10, weight=0)
Globals.tab5_canvas.grid_rowconfigure(10, weight=0)
DVH_upload_rtplan_frame.config(bg='#ffffff')

Globals.DVH_upload_button_rtplan = tk.Button(DVH_upload_rtplan_frame, text='Browse',\
    image=profiles_add_rtplan_button_image,cursor='hand2', font=('calibri', '14'),\
        relief=FLAT, state=DISABLED, command=DVH_functions.UploadRTplan)
Globals.DVH_upload_button_rtplan.pack(expand=True, fill=BOTH)
Globals.DVH_upload_button_rtplan.configure(bg='#ffffff', activebackground='#ffffff',\
activeforeground='#ffffff', highlightthickness=0)
Globals.DVH_upload_button_rtplan.image=profiles_add_rtplan_button_image

DVH_upload_struct_frame = tk.Frame(Globals.tab5_canvas)
DVH_upload_struct_frame.grid(row=4, column=0, \
    padx=(50,40), sticky=N+S+W, pady=(10,20))
Globals.tab5_canvas.grid_columnconfigure(32, weight=0)
Globals.tab5_canvas.grid_rowconfigure(32, weight=0)
DVH_upload_struct_frame.config(bg='#ffffff')

Globals.DVH_upload_button_struct = tk.Button(DVH_upload_struct_frame, \
    text='Upload struct', image=DVH_add_structure_button_image,\
        cursor='hand2', font=('calibri', '14'), \
            relief=FLAT, state=DISABLED, command=DVH_functions.UploadStruct)
Globals.DVH_upload_button_struct.pack(expand=True, fill=BOTH)
Globals.DVH_upload_button_struct.configure(bg='#ffffff', \
    activebackground='#ffffff', activeforeground='#ffffff', highlightthickness=0)
Globals.DVH_upload_button_struct.image = DVH_add_structure_button_image

film_orientation_frame = tk.Frame(Globals.tab5_canvas)
film_orientation_frame.grid(row=1, column=0, sticky=N+S+E+W, \
    pady=(10,20), padx=(40,30))
Globals.tab5_canvas.grid_columnconfigure(2, weight=0)
Globals.tab5_canvas.grid_rowconfigure(2, weight=0)
film_orientation_frame.config(bg='#ffffff', bd=0, highlightthickness=0, relief=FLAT)

film_orientation_menu_text = tk.Text(film_orientation_frame, width=14, height=1)
film_orientation_menu_text.insert(INSERT, "Film orientation:")
film_orientation_menu_text.config(state=DISABLED, \
    font=('calibri', '10'), bd = 0, relief=FLAT)
film_orientation_menu_text.pack(side=LEFT)

Globals.DVH_film_orientation_menu = OptionMenu(film_orientation_frame, \
    Globals.DVH_film_orientation, 'Axial', 'Coronal', 'Sagittal')
Globals.DVH_film_orientation_menu.pack(side=LEFT)
Globals.DVH_film_orientation_menu.config(bg = '#ffffff', width=15, relief=FLAT)

DVH_film_orientation_help_frame = tk.Frame(film_orientation_frame)
DVH_film_orientation_help_frame.pack(side=LEFT)
DVH_film_orientation_help_frame.configure(bg='#ffffff')

DVH_help_button_orientation = \
    tk.Button(DVH_film_orientation_help_frame, text='help', \
    image=Globals.help_button, cursor='hand2', font=('calibri', '14'), \
        relief=FLAT, state=ACTIVE, command=DVH_functions.help_showPlanes)
DVH_help_button_orientation.pack(expand=True, fill=BOTH)
DVH_help_button_orientation.configure(bg='#ffffff',activebackground='#ffffff',\
    activeforeground='#ffffff', highlightthickness=0)
DVH_help_button_orientation.image=Globals.help_button

DVH_film_factor_frame = tk.Frame(Globals.tab5_canvas)
DVH_film_factor_frame.grid(row=2, column=0, sticky=N+S+E+W, \
    pady=(10,20), padx=(40,30))
Globals.tab5_canvas.grid_columnconfigure(30, weight=0)
Globals.tab5_canvas.grid_rowconfigure(30, weight=0)
DVH_film_factor_frame.config(bg='#ffffff', bd=0, highlightthickness=0, relief=FLAT)

DVH_film_factor = tk.Text(DVH_film_factor_frame, width=20, height=2)
DVH_film_factor.insert(INSERT, "Film factor \n(number of fractions):")
DVH_film_factor.config(state=DISABLED, font=('calibri', '10'), bd = 0, relief=FLAT)
DVH_film_factor.pack(side=LEFT)

Globals.DVH_film_factor_input = tk.Text(DVH_film_factor_frame, width=8, height=1)
Globals.DVH_film_factor_input.pack(side=LEFT)
Globals.DVH_film_factor_input.insert(INSERT, " ")
Globals.DVH_film_factor_input.config(state=NORMAL, \
    font=('calibri', '10'), bd = 2, bg='#ffffff')

DVH_resetAll_frame = tk.Frame(Globals.tab5_canvas)
DVH_resetAll_frame.grid(row=5,column=0, padx=(50,40), sticky=S+N+W, pady=(10,20))
Globals.tab5_canvas.grid_columnconfigure(5, weight=0)
Globals.tab5_canvas.grid_rowconfigure(5, weight=0)
profiles_resetAll_frame.config(bg='#ffffff')

DVH_resetAll_button = tk.Button(DVH_resetAll_frame, text='Reset', \
    image=dose_response_clear_all_button_image, \
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=ACTIVE, \
        command=DVH_functions.clearAll)
DVH_resetAll_button.pack(expand=True, fill=BOTH)
DVH_resetAll_button.configure(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
DVH_resetAll_button.image = dose_response_clear_all_button_image

DVH_export_frame = tk.Frame(Globals.tab5_canvas)
DVH_export_frame.grid(row=5,column=0, padx=(210,0), sticky=S+N+W, pady=(10,20))
Globals.tab5_canvas.grid_columnconfigure(50, weight=0)
Globals.tab5_canvas.grid_rowconfigure(50, weight=0)
DVH_export_frame.config(bg='#ffffff')

Globals.DVH_export_button = tk.Button(DVH_export_frame, text='Reset', \
    image=Globals.export_plot_button_image, \
    cursor='hand2', font=('calibri', '14'), relief=FLAT, state=DISABLED, \
        command=DVH_functions.nothingButton)
Globals.DVH_export_button.pack(expand=True, fill=BOTH)
Globals.DVH_export_button.configure(bg='#ffffff', activebackground='#ffffff', \
    activeforeground='#ffffff', highlightthickness=0)
Globals.DVH_export_button.image = Globals.export_plot_button_image

Globals.temp_image_canvas = tk.Canvas(Globals.DVH_view_film_doseplan_ROI)
Globals.temp_image_canvas.grid(row=0, column=0, sticky=N+S+W+E)
Globals.temp_image_canvas.config(bg='#ffffff', bd=0, \
    highlightthickness=0,relief=FLAT)
Globals.temp_image_canvas.create_image(270,150, image=Globals.dVH_temp_image)


Globals.tab5_canvas.pack(expand=True, fill=BOTH)


##################################### End statement ################################
Globals.form.mainloop()