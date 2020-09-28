#-----------------------------------------------------------------------------------------------------
#
# CoMet_functions.py
# version 26.07.20
#
# To be used related to the tab CoMet in Fidora.
#
#-----------------------------------------------------------------------------------------------------


import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, \
    PhotoImage, BOTH, E, S, N, W, ACTIVE, FLAT
import os
from os.path import normpath, basename
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import numpy as np
import SimpleITK as sitk
import pydicom
from PIL import Image, ImageTk


def nothingButton():
#--------------------------------------------------
# Function to only return
# Is used in cases where nothing should happen in
# a active button (they will later be reconfigured)
#--------------------------------------------------
    return


def UploadAction(event=None):
#--------------------------------------------------
# Function to upload the scanned image of film.
# Callback function to the button 
# CoMet_upload_button in notebook.py.
#--------------------------------------------------
    Globals.CoMet_uploaded_filename.set(filedialog.askopenfilename())
    ext = os.path.splitext(Globals.CoMet_uploaded_filename.get())[-1].lower()
    if(ext==".tif"):
        Globals.CoMet_uploaded_file_text = \
            tk.Text(Globals.CoMet_border_1_label,  height=1, width=32)
        Globals.CoMet_uploaded_file_text.grid(row=0, column=0, columnspan=2, \
            sticky=E+W, pady=(20,20), padx=(100,0))
        Globals.CoMet_uploaded_file_text.insert(INSERT, \
            basename(normpath(Globals.CoMet_uploaded_filename.get())))
        Globals.CoMet_uploaded_file_text.config(state=DISABLED, bd=0, \
            font=('calibri', '10'), fg='gray', bg='#ffffff')

        if (Globals.CoMet_progressbar_check_file):
            Globals.CoMet_progressbar_counter +=1
            Globals.CoMet_progressbar_check_file = False
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        Globals.CoMet_progressbar_text = \
            tk.Text(Globals.tab1_canvas, height = 1, width=5)
        Globals.CoMet_progressbar_text.grid(row=1, column=0, columnspan=1, \
            sticky=E, padx=(0,158), pady=(0,36))
        Globals.CoMet_progressbar_text.insert(INSERT, \
            str(Globals.CoMet_progressbar_counter*25)+"%")
        if(Globals.CoMet_progressbar_counter*25 == 100):
            Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, \
                relief=FLAT, bg='#2C8EAD', font=('calibri', '10', 'bold'))
        else:
            Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, \
                relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
        
    elif(ext==""):
        Globals.CoMet_uploaded_filename.set("Error!") 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")
        Globals.CoMet_uploaded_filename.set("Error!") 


def setCoMet_export_folder():
#--------------------------------------------------
# Function to choose which folder to place the
# corrected image resulting in CoMet.
# Callback function to the button
# CoMet_folder_button in notebook.py.
#--------------------------------------------------
    Globals.CoMet_export_folder.set(filedialog.askdirectory())
    if(Globals.CoMet_export_folder.get() == ""):
        Globals.CoMet_export_folder.set("Error!")
    else:
        current_folder = os.getcwd()
        os.chdir(Globals.CoMet_export_folder.get())
        save_to_folder=\
            tk.Text(Globals.CoMet_border_2_label, height=1, width=32)
        save_to_folder.grid(row=0, column=0, columnspan=3, \
            sticky=E+W, pady=(20,20), padx=(100,0))
        save_to_folder.insert(INSERT, \
            basename(normpath(Globals.CoMet_export_folder.get())))
        save_to_folder.config(state=DISABLED, bd=0, \
            font=('calibri', '10'), fg='gray', bg='#ffffff')
        os.chdir(current_folder)
        if(Globals.CoMet_progressbar_check_folder):
            Globals.CoMet_progressbar_counter +=1
            Globals.CoMet_progressbar_check_folder = False
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        Globals.CoMet_progressbar_text = \
            tk.Text(Globals.tab1_canvas, height=1, width=5)
        Globals.CoMet_progressbar_text.grid(row=1, column=0, \
            columnspan=1, sticky=E, padx=(0,158), pady=(0,36))
        Globals.CoMet_progressbar_text.insert(INSERT, \
            str(Globals.CoMet_progressbar_counter*25) + "%")
        if(Globals.CoMet_progressbar_counter*25 == 100):
            Globals.CoMet_progressbar_text.config(state=DISABLED, \
                bd=0, relief=FLAT, bg='#2C8EAD', font=('calibri', '10', 'bold'))
        else:
            Globals.CoMet_progressbar_text.config(state=DISABLED, \
                bd=0, relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
        

def checkAllWidgets(*args):
#--------------------------------------------------
# Function to check if all actions has been done
# in CoMet and the user are ready to perform
# the correction on the uploaded image.
# Used in the function Correct() in current file.
#--------------------------------------------------
    if(Globals.CoMet_uploaded_filename.get()=="Error!" or \
        Globals.CoMet_export_folder.get()=="Error!" or \
            Globals.CoMet_corrected_image_filename.get()=="Error!"):
        return False
    else:
        return True


def correctionMatrix():
#--------------------------------------------------
# Function that performes the correction on the
# uploaded image. This happens as an absolute
# subtraction between the pixel values in the
# image and the correction matrix.
# Called in the function Correct() in current file.
#--------------------------------------------------
    dataset = cv2.imread(Globals.CoMet_uploaded_filename.get().lstrip(), \
        cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if(dataset is None):
        current_folder = os.getcwd()
        script_path = Globals.CoMet_uploaded_filename.get()
        parent = os.path.dirname(script_path)
        os.chdir(parent)
        dataset=cv2.imread(basename(normpath(script_path)), \
            cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        os.chdir(current_folder)
    if(dataset is None):
         messagebox.showerror("Error", \
"Something has happen. Check that the filename does not contain Æ,Ø,Å")
         return
    
    if(dataset.shape[2] == 3):
        if(dataset.shape[0]==1270 and dataset.shape[1]==1016):
            temp = abs(dataset-Globals.correctionMatrix127)
            Globals.CoMet_correctedImage = np.clip(temp, 0, 65535)
        elif(dataset.shape[0]==720 and dataset.shape[1]==576):
            temp = abs(dataset - Globals.correctionMatrix72)
            Globals.CoMet_correctedImage = np.clip(temp, 0, 65535)
        else:
            messagebox.showerror("Error",\
"The resolution of the image is not \
consistent with dpi. Must be either 72 or 127")

    else:
        messagebox.showerror("Error",\
            "The uploaded image need to be in RGB-format")


def Correct():
#--------------------------------------------------
# Function to initiate the correction on the 
# uploaded image. 
# Callback function to the button
# CoMet_correct_button in notebook.py.
#--------------------------------------------------
    if(checkAllWidgets() is False):
        messagebox.showerror("Error", "All boxes must be filled")
        return
    current_folder = os.getcwd()
    os.chdir(Globals.CoMet_export_folder.get())
    if(os.path.exists(Globals.CoMet_export_folder.get() + '/' + \
        Globals.CoMet_corrected_image_filename.get().lstrip() + \
            Globals.CoMet_saveAs.get()) is True):
        os.chdir(current_folder)
        messagebox.showerror("Error", \
            "Filename already exists in folder. Please write a new filename")
        Globals.CoMet_progressbar_counter -= 1
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        Globals.CoMet_progressbar_text = \
            tk.Text(Globals.tab1_canvas, width = 5, height=1)
        Globals.CoMet_progressbar_text.grid(row=1, column=0, \
            columnspan=1, sticky=E, padx=(0,158), pady=(0,36))
        Globals.CoMet_progressbar_text.insert(INSERT, \
            str(Globals.CoMet_progressbar_counter*25) + "%")
        if(Globals.CoMet_progressbar_counter*25 == 100):
            Globals.CoMet_progressbar_text.config(state=DISABLED, \
                bd=0, relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
        else:
            Globals.CoMet_progressbar_text.config(state=DISABLED, \
                bd=0, relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
        Globals.CoMet_save_button_1.config(state=ACTIVE)
        Globals.CoMet_save_filename.config(state=NORMAL)
        return

    os.chdir(current_folder)    
    correctionMatrix()
    
    if (Globals.CoMet_correctedImage is None):
        messagebox.showerror("Error", \
"The image could not be corrected. \
Please check all the specifications and try again.")
        Globals.CoMet_progressbar["value"]=0
        Globals.CoMet_progressbar_text = \
            tk.Text(Globals.tab1_canvas, height=1, width=5)
        Globals.CoMet_progressbar_text.grid(row=1, column=0, columnspan=1, \
            sticky=E, padx=(0,158), pady=(0,36))
        Globals.CoMet_progressbar_text.insert(INSERT, "0%")
        Globals.CoMet_progressbar_text.config(state=DISABLED, bd=0, \
            relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))
    else:
        Globals.CoMet_progressbar_counter +=1
        Globals.CoMet_progressbar["value"] = Globals.CoMet_progressbar_counter*25
        Globals.CoMet_progressbar_text = \
            tk.Text(Globals.tab1_canvas, height=1, width=5)
        Globals.CoMet_progressbar_text.grid(row=1, column=0, \
            columnspan=1, sticky=E, padx=(0,158), pady=(0,36))
        Globals.CoMet_progressbar_text.insert(INSERT, \
            str(Globals.CoMet_progressbar_counter*25) + "%")
        if(Globals.CoMet_progressbar_counter*25 == 100):
            Globals.CoMet_progressbar_text.config(state=DISABLED, \
                bd=0, relief=FLAT, bg='#2C8EAD', font=('calibri', '10', 'bold'))
        else:
            Globals.CoMet_progressbar_text.config(state=DISABLED, \
                bd=0, relief=FLAT, bg='#ffffff', font=('calibri', '10', 'bold'))

    R=Globals.CoMet_correctedImage[:,:,2]
    G=Globals.CoMet_correctedImage[:,:,1]
    B=Globals.CoMet_correctedImage[:,:,0]

    if(Globals.CoMet_dpi.get()=="127"):
        corrImg_dicom = np.zeros((1270,1016,3))
        corrImg_dicom = corrImg_dicom.astype('uint16')
        corrImg_dicom[:,:,0]=R; corrImg_dicom[:,:,1]=G;corrImg_dicom[:,:,2]=B
    elif(Globals.CoMet_dpi.get() =="72"):
        corrImg_dicom = np.zeros((720,576,3))
        corrImg_dicom = corrImg_dicom.astype('uint16')
        corrImg_dicom[:,:,0]=R; corrImg_dicom[:,:,1]=G;corrImg_dicom[:,:,2]=B
    else:
        messagebox.showerror("Error", \
"Wrong DPI in image. No correction.\n\
Please check all specifications and try again.")
        
    corrImg_dicom = np.moveaxis(corrImg_dicom,-2,1)
    corrImg_dicom = np.rollaxis(corrImg_dicom,2,0)
    img_dicom = sitk.GetImageFromArray(corrImg_dicom)
    current_folder = os.getcwd()
    os.chdir(Globals.CoMet_export_folder.get())
    sitk.WriteImage(img_dicom, \
        Globals.CoMet_corrected_image_filename.get().lstrip() + Globals.CoMet_saveAs.get())
    os.chdir(current_folder)
    mod_NameAndModality = pydicom.dcmread(Globals.CoMet_export_folder.get() + \
        '/' + Globals.CoMet_corrected_image_filename.get().lstrip() + \
            Globals.CoMet_saveAs.get())
    mod_NameAndModality.Modality = "RTDOSE"
    if(Globals.CoMet_patientName.get() != "Error!"):
        mod_NameAndModality.PatientName = Globals.CoMet_patientName.get()
    else:
        mod_NameAndModality.PatientName = "First^Last"
        
    mod_NameAndModality.save_as(Globals.CoMet_export_folder.get() + '/' \
        + Globals.CoMet_corrected_image_filename.get().lstrip() \
            + Globals.CoMet_saveAs.get())

    ds = pydicom.dcmread(Globals.CoMet_export_folder.get() + '/' \
        + Globals.CoMet_corrected_image_filename.get().lstrip() \
            + Globals.CoMet_saveAs.get() )

    img = ds.pixel_array
    RGB_image = np.zeros((img.shape[1], img.shape[2], 3))
    
    for i in range(img.shape[0]):
        RGB_image[:,:,i] = img[i, :,:]
 
    img8 = (RGB_image/256).astype('uint8')
    img8 = cv2.resize(img8, dsize=(int(img8.shape[1]/2.67),\
        int(img8.shape[0]/2.67)))
    height, width, channels = img8.shape 
    img8 = Image.fromarray(img8, 'RGB')
    
    Globals.CoMet_image_to_canvas =  ImageTk.PhotoImage(image=img8)
    Globals.CoMet_print_corrected_image.delete('all')
    Globals.CoMet_print_corrected_image.create_image(180,250,\
        image=Globals.CoMet_image_to_canvas)
    Globals.CoMet_print_corrected_image.image = Globals.CoMet_image_to_canvas
   