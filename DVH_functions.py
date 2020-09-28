#-----------------------------------------------------------------------------------
# DVH_functions.py
# version 18.08.20
#
# To be used related to the tab DVH in Fidora.
#
#-----------------------------------------------------------------------------------

import Globals
import tkinter as tk
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL,simpledialog,\
    PhotoImage, BOTH, Canvas, N, S, W, E, ALL, Frame, SUNKEN, Radiobutton, GROOVE, \
        ACTIVE, FLAT, END, Scrollbar, HORIZONTAL, VERTICAL, ttk, TOP, RIGHT, LEFT, \
            ttk, Checkbutton, IntVar
import os
from os.path import normpath, basename
from PIL import Image, ImageTk
import cv2
from cv2 import imread, IMREAD_ANYCOLOR, IMREAD_ANYDEPTH, imwrite
import pydicom
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import \
    FigureCanvasTkAgg,  NavigationToolbar2Tk
import numpy as np
import random

def nothingButton():
#--------------------------------------------------
# Function to only return
# Is used in cases where nothing should happen in
# a active button (they will later be reconfigured)
#--------------------------------------------------
    return

def clearAll():
#--------------------------------------------------
# Function to reset all variables
#
# This function is called when the user
# wants to restart the program
#--------------------------------------------------
    for widget in Globals.DVH_view_film_doseplan_ROI.winfo_children():
        widget.destroy()
    Globals.temp_image_canvas = tk.Canvas(Globals.DVH_view_film_doseplan_ROI)
    Globals.temp_image_canvas.grid(row=0, column=0, sticky=N+S+W+E)
    Globals.temp_image_canvas.config(bg='#ffffff',bd=0, \
        highlightthickness=0,relief=FLAT)
    Globals.temp_image_canvas.create_image(270,150, image=Globals.dVH_temp_image)

    Globals.DVH_export_button.config(state=DISABLED, command=nothingButton)

    Globals.DVH_film_orientation.set('-')
    Globals.DVH_number_of_doseplans = 0
    Globals.DVH_number_of_doseplans_row_count = 4
    Globals.DVH_doseplans_grid_config_count = 6
    Globals.DVH_doseplans_filenames = []
    Globals.DVH_doseplans_factor_text = []
    Globals.DVH_doseplans_factor_input = []
    Globals.DVH_doseplan_dataset_ROI_several = []
    Globals.DVH_several_img = []

    Globals.profiles_film_factor = None
    Globals.DVH_film_orientation_menu = None
    Globals.DVH_film_factor_input = None
    Globals.DVH_film_factor = None
    Globals.DVH_film_dataset = None
    Globals.DVH_film_dataset_red_channel = None
    Globals.DVH_film_dataset_ROI = None
    Globals.DVH_film_dataset_ROI_red_channel = None
    Globals.DVH_doseplan_dataset_ROI = None
    Globals.DVH_film_dataset_ROI_red_channel_dose = None
    Globals.DVH_film_write_image = None
    Globals.DVH_film_dose_write_image = None
    Globals.DVH_max_dose_film = None
    Globals.DVH_max_dose_doseplan = None

    Globals.DVH_iscoenter_coords = []
    Globals.DVH_film_isocenter = None
    Globals.DVH_film_reference_point = None
    Globals.DVH_distance_isocenter_ROI = []
    Globals.DVH_distance_reference_point_ROI = []
    Globals.DVH_mark_isocenter_up_down_line = []
    Globals.DVH_mark_isocenter_right_left_line = []
    Globals.DVH_mark_isocenter_oval = []
    Globals.DVH_mark_ROI_rectangle = []
    Globals.DVH_mark_reference_point_oval = []
    Globals.DVH_ROI_coords = []
    Globals.DVH_film_variable_ROI_coords = None

    Globals.DVH_done_button = None
    Globals.DVH_done_button_reference_point = None
    Globals.DVH_isocenter_check=False
    Globals.DVH_reference_point_check = False
    Globals.DVH_ROI_check = False
    Globals.DVH_ROI_reference_point_check = False
    Globals.DVH_film_batch.set(0)
    Globals.DVH_popt_red = np.zeros(3)

    Globals.DVH_upload_button_doseplan.config(state=DISABLED)
    Globals.DVH_upload_button_film.config(state=ACTIVE)
    Globals.DVH_upload_button_rtplan.config(state=DISABLED)
    Globals.DVH_upload_button_struct.config(state=DISABLED)

    Globals.DVH_dataset_doseplan=None
    Globals.DVH_dataset_rtplan = None
    Globals.DVH_dataset_structure_file = None

    Globals.DVH_test_if_added_doseplan = False
    Globals.DVH_test_if_added_rtplan = False
    Globals.DVH_test_if_added_struct = False

    Globals.DVH_isocenter_mm=None
    Globals.DVH_dose_scaling_doseplan = None
    Globals.DVH_contour_names = None
    Globals.DVH_ROIContourSequence = None
    Globals.DVH_contours = []

    Globals.DVH_doseplan_write_image = None
    Globals.DVH_doseplan_write_image_width = None
    Globals.DVH_doseplan_write_image_height = None
    Globals.DVH_doseplan_lateral_displacement = None
    Globals.DVH_doseplan_vertical_displacement = None
    Globals.DVH_doseplan_longitudianl_displacement = None
    Globals.DVH_doseplan_patient_position = None

    Globals.DVH_reference_point_in_doseplan = None
    Globals.DVH_input_lateral_displacement = None
    Globals.DVH_input_longitudinal_displacement = None
    Globals.DVH_input_vertical_displacement = None
    Globals.DVH_slice_offset = None
    Globals.DVH_offset = None
    Globals.DVH_isocenter_or_reference_point = None

    Globals.DVH_lateral = None
    Globals.DVH_vertical = None
    Globals.DVH_longitudinal = None

    for widget in Globals.DVH_plot_canvas.winfo_children():
        widget.destroy()
    DVH_initial_fig = Figure(figsize=(10,6))
    DVH_a = DVH_initial_fig.add_subplot(111, ylim=(0,1), xlim=(0,50))
    DVH_initial_plot_canvas = FigureCanvasTkAgg\
        (DVH_initial_fig, master=Globals.DVH_plot_canvas)
    DVH_initial_plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, \
        sticky=N+E+W+S, padx=(5,0), pady=(0,0))
    DVH_a.set_title ("Dose volume histogram", fontsize=12)
    DVH_a.set_ylabel("Volume (%)", fontsize=12)
    DVH_a.set_xlabel("Dose (Gy)", fontsize=12)
    DVH_initial_fig.tight_layout()

    for widget in Globals.DVH_list_contours_canvas.winfo_children():
        widget.destroy()
    return 

def calculateDVH(data, data_film, initial, include_contours):
#--------------------------------------------------
# Function to calculate the dose volume histogram
#
# The function is called in processDoseplan_Isocenter
# and processDoseplan_Reference_Point, as well as
# it is a callback function for the button
# check indise this function
#--------------------------------------------------
    names = [item[0] for item in data]
    dose_array = [item[1] for item in data]
    prc_array = [item[2] for item in data]
    dose_array_film = [item[1] for item in data_film]
    prc_array_film = [item[2] for item in data_film]
    if initial:
        include_contours = []
        checkbuttons = []
        for name in names:
            var = IntVar()
            var.set(1)
            check = Checkbutton(Globals.DVH_list_contours_canvas, \
                text=name, variable=var, command=lambda: \
                    calculateDVH(data, data_film, False, include_contours))
            check.pack(side=LEFT)
            check.config(bg='#ffffff')
            include_contours.append(var)
            checkbuttons.append(check)

    DVH_fig = Figure(figsize=(10,6))
    DVH_a = DVH_fig.add_subplot(111, ylim=(-0.1,1.1), xlim=(0,50))
    DVH_plot_canvas = FigureCanvasTkAgg(DVH_fig, master=Globals.DVH_plot_canvas)
    DVH_plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, \
        sticky=N+E+W+S, padx=(5,0), pady=(0,0))
    legend_names = []
    for i in range(len(include_contours)):
        if include_contours[i].get():
            color = (random.random(), random.random(), random.random())
            plot_dose_array = list(dose_array[i])
            plot_dose_array.insert(0,0)
            plot_dose_array.insert(len(plot_dose_array),100)
            plot_prc_array = list(prc_array[i])
            plot_prc_array.insert(0,1)
            plot_prc_array.insert(len(plot_prc_array),0)
            DVH_a.plot(np.array(plot_dose_array),np.array(plot_prc_array), c=color)

            plot_dose_array_film = list(dose_array_film[i])
            plot_dose_array_film.insert(0,0)
            plot_dose_array_film.insert(len(plot_dose_array_film),100)
            plot_prc_array_film = list(prc_array_film[i])
            plot_prc_array_film.insert(0,1)
            plot_prc_array_film.insert(len(plot_prc_array_film), 0)
            DVH_a.plot(np.array(plot_dose_array_film), \
                np.array(plot_prc_array_film), c=color, ls='--')

            legend_names.append(names[i])
            legend_names.append(names[i] + " (Film)")

    def export_plot():
        messagebox.showinfo("Info", "This button has not been written")
        return

    Globals.DVH_export_button.config(state=ACTIVE, command=export_plot)

    DVH_a.legend(legend_names,loc='center left', bbox_to_anchor=(1, 0.5))
    DVH_a.set_title ("Dose volume histogram", fontsize=12)
    DVH_a.set_ylabel("Volume (%)", fontsize=12)
    DVH_a.set_xlabel("Dose (Gy)", fontsize=12)
    DVH_fig.tight_layout()

def processDoseplan_usingReferencePoint(only_one):
#--------------------------------------------------
# Function to process the doseplan when reference
# point is choosen to define the position.
# Is called in UploadDoseplan
#
# Parameter: only_one -to test if only one doseplan
# is uploaded in Fidora.
#--------------------------------------------------

    ################  RT Plan ######################
    iso_1 = abs(Globals.DVH_dataset_doseplan.ImagePositionPatient[0] - \
        Globals.DVH_isocenter_mm[0])
    iso_2 = abs(Globals.DVH_dataset_doseplan.ImagePositionPatient[1] - \
        Globals.DVH_isocenter_mm[1])
    iso_3 = abs(Globals.DVH_dataset_doseplan.ImagePositionPatient[2] - \
        Globals.DVH_isocenter_mm[2])
    Globals.DVH_isocenter_mm = [iso_1, iso_2, iso_3]
    
    try:
        Globals.DVH_vertical = int(Globals.DVH_vertical)
    except:
        messagebox.showerror("Error", "Could not read the vertical \
displacements\n (Code: displacements to integer)")
        return
    try:
        Globals.DVH_lateral = int(Globals.DVH_lateral)
    except:
        messagebox.showerror("Error", "Could not read the lateral \
displacements\n (Code: displacements to integer)")
        return
    try:
        Globals.DVH_longitudinal = int(Globals.DVH_longitudinal)
    except:
        messagebox.showerror("Error", "Could not read the longitudinal \
displacements\n (Code: displacements to integer)")
        return

    lateral = Globals.DVH_lateral
    longit = Globals.DVHlongitudinal
    vertical = Globals.DVH_vertical
    isocenter_px = np.zeros(3)
    distance_in_doseplan_ROI_reference_point_px = []
    if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
        isocenter_px[0] = np.round(iso_1)
        isocenter_px[1] = np.round(iso_2)
        isocenter_px[2] = np.round(iso_3)

        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_reference_point_ROI[0][0]),\
                np.round(Globals.DVH_distance_reference_point_ROI[0][1])])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_reference_point_ROI[1][0]),\
                np.round(Globals.DVH_distance_reference_point_ROI[1][1])])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_reference_point_ROI[2][0]),\
                np.round(Globals.DVH_distance_reference_point_ROI[2][1])])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_reference_point_ROI[3][0]),\
                np.round(Globals.DVH_distance_reference_point_ROI[3][1])])

        lateral_px = np.round(lateral)
        vertical_px = np.round(vertical)
        longit_px = np.round(longit)

        doseplan_lateral_displacement_px = \
            np.round(Globals.DVH_doseplan_lateral_displacement)
        doseplan_vertical_displacement_px = \
            np.round(Globals.DVH_doseplan_vertical_displacement)
        doseplan_longitudinal_displacement_px = \
            np.round(Globals.DVH_doseplan_longitudianl_displacement)

    elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
        isocenter_px[0] = np.round(iso_1/2)
        isocenter_px[1] = np.round(iso_2/2)
        isocenter_px[2] = np.round(iso_3/2)

        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[0][0])/2),\
                np.round((Globals.DVH_distance_reference_point_ROI[0][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[1][0])/2),\
                np.round((Globals.DVH_distance_reference_point_ROI[1][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[2][0])/2),\
                np.round((Globals.DVH_distance_reference_point_ROI[2][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[3][0])/2),\
                np.round((Globals.DVH_distance_reference_point_ROI[3][1])/2)])

        lateral_px = np.round(lateral/2)
        vertical_px = np.round(vertical/2)
        longit_px = np.round(longit/2)

        doseplan_lateral_displacement_px = \
            np.round((Globals.DVH_doseplan_lateral_displacement)/2)
        doseplan_vertical_displacement_px = \
            np.round((Globals.DVH_doseplan_vertical_displacement)/2)
        doseplan_longitudinal_displacement_px = \
            np.round((Globals.DVH_doseplan_longitudianl_displacement)/2)

    else:
        isocenter_px[0] = np.round(iso_1/3)
        isocenter_px[1] = np.round(iso_2/3)
        isocenter_px[2] = np.round(iso_3/3)

        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[0][0])/3),\
                np.round((Globals.DVH_distance_reference_point_ROI[0][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[1][0])/3),\
                np.round((Globals.DVH_distance_reference_point_ROI[1][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[2][0])/3),\
                np.round((Globals.DVH_distance_reference_point_ROI[2][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_reference_point_ROI[3][0])/3),\
                np.round((Globals.DVH_distance_reference_point_ROI[3][1])/3)])

        lateral_px = np.round(lateral/3)
        vertical_px = np.round(vertical/3)
        longit_px = np.round(longit/3)

        doseplan_lateral_displacement_px = \
            np.round((Globals.DVH_doseplan_lateral_displacement)/3)
        doseplan_vertical_displacement_px = \
            np.round((Globals.DVH_doseplan_vertical_displacement)/3)
        doseplan_longitudinal_displacement_px = \
            np.round((Globals.DVH_doseplan_longitudianl_displacement)/3)

    temp_ref_point_doseplan = np.zeros(3)

    if(Globals.DVH_doseplan_patient_position=='HFS'):
        temp_ref_point_doseplan[0] = int(isocenter_px[0]+ \
            doseplan_lateral_displacement_px - lateral_px)
        temp_ref_point_doseplan[1] = int(isocenter_px[1]- \
            doseplan_vertical_displacement_px + vertical_px)
        temp_ref_point_doseplan[2] = int(isocenter_px[2]+ \
            doseplan_longitudinal_displacement_px - longit_px)
    elif(Globals.DVH_doseplan_patient_position=='HFP'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- \
            doseplan_lateral_displacement_px+ lateral_px
        temp_ref_point_doseplan[1] = isocenter_px[1]+ \
            doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[2] = isocenter_px[2]+ \
            doseplan_longitudinal_displacement_px - longit_px
    elif(Globals.DVH_doseplan_patient_position=='HFDR'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- \
            doseplan_vertical_displacement_px + vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1]+ \
            doseplan_lateral_displacement_px - lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]+ \
            doseplan_longitudinal_displacement_px - longit_px
    elif(Globals.DVH_doseplan_patient_position=='HFDL'):
        temp_ref_point_doseplan[0] = isocenter_px[0]+ \
            doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1]- \
            doseplan_lateral_displacement_px + lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]+ \
            doseplan_longitudinal_displacement_px - longit_px
    elif(Globals.DVH_doseplan_patient_position=='FFS'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- \
            doseplan_lateral_displacement_px + lateral_px
        temp_ref_point_doseplan[1] = isocenter_px[1]+ \
            doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- \
            doseplan_longitudinal_displacement_px + longit_px
    elif(Globals.DVH_doseplan_patient_position=='FFP'):
        temp_ref_point_doseplan[0] = isocenter_px[0]+ \
            doseplan_lateral_displacement_px- lateral_px
        temp_ref_point_doseplan[1] = isocenter_px[1]- \
            doseplan_vertical_displacement_px + vertical_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- \
            doseplan_longitudinal_displacement_px + longit_px
    elif(Globals.DVH_doseplan_patient_position=='FFDR'):
        temp_ref_point_doseplan[0] = isocenter_px[0]- \
            doseplan_vertical_displacement_px + vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1]- \
            doseplan_lateral_displacement_px + lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- \
            doseplan_longitudinal_displacement_px + longit_px
    else:
        temp_ref_point_doseplan[0] = isocenter_px[0] + \
            doseplan_vertical_displacement_px - vertical_px
        temp_ref_point_doseplan[1] = isocenter_px[1] + \
            doseplan_lateral_displacement_px - lateral_px
        temp_ref_point_doseplan[2] = isocenter_px[2]- \
            doseplan_longitudinal_displacement_px + longit_px

    Globals.DVH_reference_point_in_doseplan = temp_ref_point_doseplan
    reference_point = np.zeros(3)

    ######################## Struct file ##################################
    i=0
    for name in Globals.DVH_contour_names:
        sequences = Globals.DVH_ROIContourSequence[i].ContourSequence
        temp_x = [];temp_y = [];temp_z = []
        for sequence in sequences:
            if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
                temp_x.append([int(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[0]-x)) for x in sequence.ContourData[0::3]])
                temp_y.append([int(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[1]-y)) for y in sequence.ContourData[1::3]])
                temp_z.append([int(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[2]-z)) for z in sequence.ContourData[2::3]])
            elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
                temp_x.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[0]-x)/2)) for \
                        x in sequence.ContourData[0::3]])
                temp_y.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[1]-y)/2)) for \
                        y in sequence.ContourData[1::3]])
                temp_z.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[2]-z)/2)) for \
                        z in sequence.ContourData[2::3]])
            else:
                temp_x.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[0]-x)/3)) for \
                        x in sequence.ContourData[0::3]])
                temp_y.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[1]-y)/3)) for \
                        y in sequence.ContourData[1::3]])
                temp_z.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[2]-z)/3)) for \
                        z in sequence.ContourData[2::3]])
        Globals.DVH_contours.append\
            ([i, name.ROIObservationLabel, temp_x, temp_y, temp_z])
        i+=1

    ######################## Doseplan ##################################
    if(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 1, 0]):
        reference_point[0] = temp_ref_point_doseplan[2]
        reference_point[1] = temp_ref_point_doseplan[1]
        reference_point[2] = temp_ref_point_doseplan[0]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_z
            Globals.DVH_contours[i][3] = temp_y
            Globals.DVH_contours[i][4] = temp_x
        
        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = Globals.DVH_dataset_doseplan.pixel_array
        else:
            messagebox.showerror("Error", "Something has gone wrong here.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 0, 1]):
        reference_point[0] = temp_ref_point_doseplan[1]
        reference_point[1] = temp_ref_point_doseplan[2]
        reference_point[2] = temp_ref_point_doseplan[0]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_y
            Globals.DVH_contours[i][3] = temp_z
            Globals.DVH_contours[i][4] = temp_x

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = Globals.DVH_dataset_doseplan.pixel_array
        elif(Globals.DCH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 1, 0, 0]):
        reference_point[0] = temp_ref_point_doseplan[2]
        reference_point[1] = temp_ref_point_doseplan[0]
        reference_point[2] = temp_ref_point_doseplan[1]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_z
            Globals.DVH_contours[i][3] = temp_x
            Globals.DVH_contours[i][4] = temp_y

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 0, 0, 1]):
        reference_point[0] = temp_ref_point_doseplan[0]
        reference_point[1] = temp_ref_point_doseplan[2]
        reference_point[2] = temp_ref_point_doseplan[1]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_x
            Globals.DVH_contours[i][3] = temp_z
            Globals.DVH_contours[i][4] = temp_y

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 1, 0, 0]):
        reference_point[0] = temp_ref_point_doseplan[1]
        reference_point[1] = temp_ref_point_doseplan[0]
        reference_point[2] = temp_ref_point_doseplan[2]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_y
            Globals.DVH_contours[i][3] = temp_x
            Globals.DVH_contours[i][4] = temp_z

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 0, 1, 0]):
        reference_point[0] = temp_ref_point_doseplan[0]
        reference_point[1] = temp_ref_point_doseplan[1]
        reference_point[2] = temp_ref_point_doseplan[2]

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = Globals.DVH_dataset_doseplan.pixel_array
        elif(Globals.DCH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    else:
        messagebox.showerror("Error", "Something has gone wrong.")
        clearAll()
        return
    
    if(reference_point[0]<0 or reference_point[0]>dataset_swapped.shape[0]):
        messagebox.showerror("Error", "Reference point is outside of dosematrix\n\
            (Code: first dimension, number of frames in dosematrix)")
        return
    if(reference_point[1]<0 or reference_point[1]>dataset_swapped.shape[1]):
        messagebox.showerror("Error", "Reference point is outside of dosematrix\n\
            (Code: second dimension, rows in dosematrix)")
        return
    if(reference_point[2]<0 or reference_point[2]>dataset_swapped.shape[2]):
        messagebox.showerror("Error", "Reference point is outside of dosematrix\n\
            (Code: third dimension, columns in dosematrix)")
        return

    dose_slice = dataset_swapped[int(reference_point[0]),:,:]
    
    structures_in_plane = []
    for contour in Globals.DVH_contours:
        in_plane = False
        temp_row=[];temp_column=[]
        for i in range(len(contour[2])):
            lst = contour[2][i]
            for j in range(len(lst)):
                plane = lst[j]
                if(plane == int(reference_point[0])):
                    temp_row.append(contour[3][i][j])
                    temp_column.append(contour[4][i][j])
                    in_plane = True
        if in_plane:
            structures_in_plane.append([contour[1], temp_row, temp_column])   

    
    doseplan_ROI_coords = []
    top_left_test_side = False; top_left_test_down = False
    top_right_test_side = False; top_right_test_down = False
    bottom_left_test_side = False; bottom_left_test_down = False
    bottom_right_test_side = False; bottom_right_test_down = False
    top_left_side_corr = 0; top_left_down_corr = 0
    top_right_side_corr = 0; top_right_down_corr = 0
    bottom_left_side_corr = 0; bottom_left_down_corr = 0
    bottom_right_side_corr = 0; bottom_right_down_corr = 0


    top_left_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[0][0]
    top_left_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[0][1]
    if(top_left_to_side < 0):
        top_left_test_side = True
        top_left_side_corr = abs(top_left_to_side)
        top_left_to_side = 0
    if(top_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_left_down < 0):
        top_left_test_down = True
        top_left_down_corr = abs(top_left_down)
        top_left_down = 0
    if(top_left_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    
    top_right_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[1][0]
    top_right_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[1][1]
    if(top_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_right_to_side > dose_slice.shape[1]):
        top_right_test_side = True
        top_right_side_corr = top_right_to_side - dose_slice.shape[1]
        top_right_to_side = dose_slice.shape[1]
    if(top_right_down < 0):
        top_right_test_down = True
        top_right_down_corr = abs(top_right_down)
        top_right_down = 0
    if(top_right_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return

    bottom_left_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[2][0]
    bottom_left_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[2][1]
    if(bottom_left_to_side < 0):
        bottom_left_test_side = True
        bottom_left_side_corr = abs(bottom_left_to_side)
        bottom_left_to_side = 0
    if(bottom_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down > dose_slice.shape[0]):
        bottom_left_down_corr = bottom_left_down - dose_slice.shape[0]
        bottom_left_down = dose_slice.shape[0]
        bottom_left_test_down = True
    
    bottom_right_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[3][0]
    bottom_right_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[3][1]
    if(bottom_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_to_side > dose_slice.shape[1]):
        bottom_right_side_corr = bottom_right_to_side - dose_slice.shape[1]
        bottom_right_to_side = dose_slice.shape[1]
        bottom_right_test_side = True
    if(bottom_right_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_down > dose_slice.shape[0]):
        bottom_right_down_corr = bottom_right_down - dose_slice.shape[0]
        bottom_right_down = dose_slice.shape[0]
        bottom_right_test_down = True
    

    if(top_right_test_side or top_right_test_down or top_left_test_side or \
        top_left_test_down or bottom_right_test_side or bottom_right_test_down \
            or bottom_left_test_side or bottom_left_test_down):
        ROI_info = "Left side: " \
            + str(max(top_left_side_corr, bottom_left_side_corr)) + " pixels.\n"\
                + "Right side: " + str(max(top_right_side_corr, \
                    bottom_right_side_corr)) + " pixels.\n "+ "Top side: " + \
                        str(max(top_left_down_corr, top_right_down_corr)) +\
                             " pixels.\n"+ "Bottom side: " + \
                                str(max(bottom_left_down_corr, \
                                    bottom_right_down_corr)) + " pixels."  
        messagebox.showinfo("ROI info", "The ROI marked on \
the film did not fit with the size of the doseplan and had to \
be cut.\n" + ROI_info )

    for i in range(len(structures_in_plane)):
        for j in range(len(structures_in_plane[i][1])):
            row = structures_in_plane[i][1][j]
            if row < top_left_down:
                structures_in_plane[i][1][j] = 0
            elif row > bottom_left_down:
                structures_in_plane[i][1][j] = bottom_left_down-top_left_down
            else:
                structures_in_plane[i][1][j] = row - top_left_down
        for k in range(len(structures_in_plane[i][2])):
            column = structures_in_plane[i][2][k]
            if column < top_left_to_side:
                structures_in_plane[i][2][k] = 0
            elif column > top_right_to_side:
                structures_in_plane[i][2][k] = top_right_to_side-top_left_to_side
            else:
                structures_in_plane[i][2][k] = column - top_left_to_side


    doseplan_ROI_coords.append([top_left_to_side, top_left_down])
    doseplan_ROI_coords.append([top_right_to_side, top_right_down])
    doseplan_ROI_coords.append([bottom_left_to_side, bottom_left_down])
    doseplan_ROI_coords.append([bottom_right_to_side, bottom_right_down])

    if only_one:
        Globals.DVH_doseplan_dataset_ROI = \
            dose_slice[int(top_left_down):int(bottom_left_down), \
                int(top_left_to_side):int(top_right_to_side)]*\
                    Globals.DVH_dataset_doseplan.DoseGridScaling
   
        if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
            factor = 5
        elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
            factor = 10
        else:
            factor = 15

        img=Globals.DVH_doseplan_dataset_ROI
        drawing_of_contours = dose_slice[int(top_left_down):int(bottom_left_down)+1,\
            int(top_left_to_side):int(top_right_to_side)+1]*\
                Globals.DVH_dataset_doseplan.DoseGridScaling
        img_film = Globals.DVH_film_dataset_ROI_red_channel_dose/100

        structures = []
        for j in range(len(structures_in_plane)):
            temp_struct = []
            for i in range(len(structures_in_plane[j][1])):
                drawing_of_contours[int(structures_in_plane[j][1][i]), \
                    int(structures_in_plane[j][2][i])] = 0
                temp_struct.append(np.array([int(structures_in_plane[j][1][i]), \
                    int(structures_in_plane[j][2][i])]))
            structures.append(temp_struct)
        
        dvh_data = []
        dvh_data_film = []
        for k in range(len(structures)):
            number_of_points = 0
            dose = []
            dose_film = []
            number_of_points_per_dose = []
            number_of_points_per_dose_film = []
            vertics = mpl.path.Path(structures[k])
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if vertics.contains_point((i,j)):
                        number_of_points+=1
                        try:
                            idx = dose.index(img[i,j])
                            exist = True
                        except:
                            exist = False
                        if not exist:
                            dose.append(img[i,j])
                            number_of_points_per_dose.append(1)
                        else:
                            number_of_points_per_dose[idx] +=1
                        try:
                            idx_film = dose_film.index(img_film[i*factor, j*factor])
                            exist_film = True
                        except:
                            exist_film = False
                        if not exist_film:
                            if not i == img.shape[0]:
                                dose_film.append(img_film[i*factor,j*factor])
                                number_of_points_per_dose_film.append(1)
                        else:
                            number_of_points_per_dose_film[idx_film] +=1

            temp_dvh_data = []
            for i in range(len(dose)):
                temp_dvh_data.append([dose[i], number_of_points_per_dose[i]])
            temp_dvh_data.sort(key=lambda x: x[0])

            temp_dvh_data_film = []
            for i in range(len(dose_film)):
                temp_dvh_data_film.append([dose_film[i], \
                    number_of_points_per_dose_film[i]])
            temp_dvh_data_film.sort(key=lambda x: x[0])
        
            dose_array = np.array([item[0] for item in temp_dvh_data])
            prc_array = [item[1] for item in temp_dvh_data]
            for i in range(len(dose_array)):
                temp = prc_array[i:len(prc_array)]
                prc_array[i] = sum(temp)
            dvh_data.append([structures_in_plane[k][0], dose_array, \
                np.array(prc_array)/number_of_points])

            dose_array_film = np.array([item[0] for item in temp_dvh_data_film])
            prc_array_film = [item[1] for item in temp_dvh_data_film]
            for i in range(len(dose_array)):
                temp = prc_array_film[i:len(prc_array_film)]
                prc_array_film[i] = sum(temp)
            dvh_data_film.append([structures_in_plane[k][0], dose_array_film, \
                np.array(prc_array_film)/number_of_points])

        if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
            img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
        elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
            img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
        else:
            img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        mx=np.max(img)
        Globals.DVH_max_dose_doseplan = mx*Globals.DVH_dose_scaling_doseplan
        img = img/mx
        PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img)*255))

        wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
        Globals.temp_image_canvas.destroy()
        doseplan_canvas = tk.Canvas(Globals.DVH_view_film_doseplan_ROI)
        doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
        doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())

        Globals.DVH_doseplan_write_image = tk.Canvas(doseplan_canvas)
        Globals.DVH_doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
        Globals.DVH_doseplan_write_image.config(bg='#ffffff', relief=FLAT,\
            highlightthickness=0, width=wid, height=heig)

        scaled_image_visual = PIL_img_doseplan_ROI
        scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
        Globals.DVH_doseplan_write_image_width = scaled_image_visual.width()
        Globals.DVH_doseplan_write_image_height = scaled_image_visual.height()
        Globals.DVH_doseplan_write_image.create_image(0,0,\
            image=scaled_image_visual, anchor="nw")
        Globals.DVH_doseplan_write_image.image = scaled_image_visual

        calculateDVH(dvh_data, dvh_data_film, True, [])
    
def processDoseplan_usingIsocenter(only_one):
#--------------------------------------------------
# Function to process the doseplan when isocenter
#  is choosen to define the position.
# Is called in UploadDoseplan
#
# Parameter: only_one -to test if only one doseplan
# is uploaded in Fidora.
#--------------------------------------------------

    ################  RT Plan ######################
    iso_1 = abs(Globals.DVH_dataset_doseplan.ImagePositionPatient[0] - \
        Globals.DVH_isocenter_mm[0])
    iso_2 = abs(Globals.DVH_dataset_doseplan.ImagePositionPatient[1] - \
        Globals.DVH_isocenter_mm[1])
    iso_3 = abs(Globals.DVH_dataset_doseplan.ImagePositionPatient[2] - \
        Globals.DVH_isocenter_mm[2])

    Globals.DVH_isocenter_mm = [iso_1, iso_2, iso_3]

    isocenter_px = np.zeros(3)
    distance_in_doseplan_ROI_reference_point_px = []
    if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
        isocenter_px[0] = np.round(iso_1)
        isocenter_px[1] = np.round(iso_2)
        isocenter_px[2] = np.round(iso_3)

        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_isocenter_ROI[0][0]),\
                np.round(Globals.DVH_distance_isocenter_ROI[0][1])])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_isocenter_ROI[1][0]),\
                np.round(Globals.DVH_distance_isocenter_ROI[1][1])])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_isocenter_ROI[2][0]),\
                np.round(Globals.DVH_distance_isocenter_ROI[2][1])])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round(Globals.DVH_distance_isocenter_ROI[3][0]),\
                np.round(Globals.DVH_distance_isocenter_ROI[3][1])])
    
    elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
        isocenter_px[0] = np.round(iso_1/2)
        isocenter_px[1] = np.round(iso_2/2)
        isocenter_px[2] = np.round(iso_3/2)
       
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[0][0])/2),\
                np.round((Globals.DVH_distance_isocenter_ROI[0][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[1][0])/2),\
                np.round((Globals.DVH_distance_isocenter_ROI[1][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[2][0])/2),\
                np.round((Globals.DVH_distance_isocenter_ROI[2][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[3][0])/2),\
                np.round((Globals.DVH_distance_isocenter_ROI[3][1])/2)])

    else:
        isocenter_px[0] = np.round(iso_1/3)
        isocenter_px[1] = np.round(iso_2/3)
        isocenter_px[2] = np.round(iso_3/3)

        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[0][0])/3),\
                np.round((Globals.DVH_distance_isocenter_ROI[0][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[1][0])/3),\
                np.round((Globals.DVH_distance_isocenter_ROI[1][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[2][0])/3),\
                np.round((Globals.DVH_distance_isocenter_ROI[2][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append\
            ([np.round((Globals.DVH_distance_isocenter_ROI[3][0])/3),\
                np.round((Globals.DVH_distance_isocenter_ROI[3][1])/3)])

    reference_point = np.zeros(3)
    

    ######################## Struct file ##################################
    i=0
    for name in Globals.DVH_contour_names:
        sequences = Globals.DVH_ROIContourSequence[i].ContourSequence
        temp_x = [];temp_y = [];temp_z = []
        for sequence in sequences:
            if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
                temp_x.append([int(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[0]-x)) for x in sequence.ContourData[0::3]])
                temp_y.append([int(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[1]-y)) for y in sequence.ContourData[1::3]])
                temp_z.append([int(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[2]-z)) for z in sequence.ContourData[2::3]])
            elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
                temp_x.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[0]-x)/2)) for \
                        x in sequence.ContourData[0::3]])
                temp_y.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[1]-y)/2)) for \
                        y in sequence.ContourData[1::3]])
                temp_z.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[2]-z)/2)) for \
                        z in sequence.ContourData[2::3]])
            else:
                temp_x.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[0]-x)/3)) for \
                        x in sequence.ContourData[0::3]])
                temp_y.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[1]-y)/3)) for \
                        y in sequence.ContourData[1::3]])
                temp_z.append([int(np.round(abs(Globals.DVH_dataset_doseplan.\
                    ImagePositionPatient[2]-z)/3)) for \
                        z in sequence.ContourData[2::3]])
        Globals.DVH_contours.append\
            ([i, name.ROIObservationLabel, temp_x, temp_y, temp_z])
        i+=1

    ######################## Doseplan ##################################
    if(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 1, 0]):
    
        reference_point[0] = isocenter_px[2]
        reference_point[1] = isocenter_px[1]
        reference_point[2] = isocenter_px[0]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_z
            Globals.DVH_contours[i][3] = temp_y
            Globals.DVH_contours[i][4] = temp_x

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = Globals.DVH_dataset_doseplan.pixel_array
        else:
            messagebox.showerror("Error", "Something has gone wrong here.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 0, 1]):
        reference_point[0] = isocenter_px[1]
        reference_point[1] = isocenter_px[2]
        reference_point[2] = isocenter_px[0]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_y
            Globals.DVH_contours[i][3] = temp_z
            Globals.DVH_contours[i][4] = temp_x

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = Globals.DVH_dataset_doseplan.pixel_array
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 1, 0, 0]):
        reference_point[0] = isocenter_px[2]
        reference_point[1] = isocenter_px[0]
        reference_point[2] = isocenter_px[1]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_z
            Globals.DVH_contours[i][3] = temp_x
            Globals.DVH_contours[i][4] = temp_y

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 0, 0, 1]):
        reference_point[0] = isocenter_px[0]
        reference_point[1] = isocenter_px[2]
        reference_point[2] = isocenter_px[1]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_x
            Globals.DVH_contours[i][3] = temp_z
            Globals.DVH_contours[i][4] = temp_y

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 1, 0, 0]):
        reference_point[0] = isocenter_px[1]
        reference_point[1] = isocenter_px[0]
        reference_point[2] = isocenter_px[2]
        for i in range(len(Globals.DVH_contours)):
            temp_x = Globals.DVH_contours[i][2]
            temp_y = Globals.DVH_contours[i][3]
            temp_z = Globals.DVH_contours[i][4]
            Globals.DVH_contours[i][2] = temp_y
            Globals.DVH_contours[i][3] = temp_x
            Globals.DVH_contours[i][4] = temp_z

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_4
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.DVH_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 0, 1, 0]):
        reference_point[0] = isocenter_px[0]
        reference_point[1] = isocenter_px[1]
        reference_point[2] = isocenter_px[2]

        if(Globals.DVH_film_orientation.get()=='Coronal'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][3]
                Globals.DVH_contours[i][3] = temp_c
        elif(Globals.DVH_film_orientation.get()=='Sagittal'):
            dataset_swapped = Globals.DVH_dataset_doseplan.pixel_array
        elif(Globals.DVH_film_orientation.get()=='Axial'):
            dataset_swapped = \
                np.swapaxes(Globals.DVH_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            for i in range(len(Globals.DVH_contours)):
                temp_c = Globals.DVH_contours[i][2]
                Globals.DVH_contours[i][2] = Globals.DVH_contours[i][4]
                Globals.DVH_contours[i][4] = temp_c
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    else:
        messagebox.showerror("Error", "Something has gone wrong.")
        clearAll()
        return



    ####################### Match film and doseplan ###############################
    if Globals.DVH_dataset_doseplan.PixelSpacing == [1, 1]:
        offset = int(np.round(Globals.DVH_offset))
        dose_slice = dataset_swapped[int(reference_point[0]) + offset,:,:]
    elif Globals.DVH_dataset_doseplan.PixelSpacing == [2, 2]:
        offset = int(np.round(Globals.DVH_offset/2))
        dose_slice = dataset_swapped[int(reference_point[0] + offset),:,:]
    else:
        offset = int(np.round(Globals.DVH_offset/3))
        dose_slice = dataset_swapped[int(reference_point[0]) + offset,:,:]

    
    structures_in_plane = []
    for contour in Globals.DVH_contours:
        in_plane = False
        temp_row=[];temp_column=[]
        for i in range(len(contour[2])):
            lst = contour[2][i]
            for j in range(len(lst)):
                plane = lst[j]
                if(plane == int(reference_point[0])+offset):
                    temp_row.append(contour[3][i][j]) 
                    temp_column.append(contour[4][i][j])
                    in_plane = True
        if in_plane:
            structures_in_plane.append([contour[1], temp_row, temp_column])
    
    doseplan_ROI_coords = []
    top_left_test_side = False; top_left_test_down = False
    top_right_test_side = False; top_right_test_down = False
    bottom_left_test_side = False; bottom_left_test_down = False
    bottom_right_test_side = False; bottom_right_test_down = False
    top_left_side_corr = 0; top_left_down_corr = 0
    top_right_side_corr = 0; top_right_down_corr = 0
    bottom_left_side_corr = 0; bottom_left_down_corr = 0
    bottom_right_side_corr = 0; bottom_right_down_corr = 0


    top_left_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[0][0]
    top_left_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[0][1]
    if(top_left_to_side < 0):
        top_left_test_side = True
        top_left_side_corr = abs(top_left_to_side)
        top_left_to_side = 0
    if(top_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_left_down < 0):
        top_left_test_down = True
        top_left_down_corr = abs(top_left_down)
        top_left_down = 0
    if(top_left_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    
    top_right_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[1][0]
    top_right_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[1][1]
    if(top_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_right_to_side > dose_slice.shape[1]):
        top_right_test_side = True
        top_right_side_corr = top_right_to_side - dose_slice.shape[1]
        top_right_to_side = dose_slice.shape[1]
    if(top_right_down < 0):
        top_right_test_down = True
        top_right_down_corr = abs(top_right_down)
        top_right_down = 0
    if(top_right_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return

    bottom_left_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[2][0]
    bottom_left_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[2][1]
    if(bottom_left_to_side < 0):
        bottom_left_test_side = True
        bottom_left_side_corr = abs(bottom_left_to_side)
        bottom_left_to_side = 0
    if(bottom_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down > dose_slice.shape[0]):
        bottom_left_down_corr = bottom_left_down - dose_slice.shape[0]
        bottom_left_down = dose_slice.shape[0]
        bottom_left_test_down = True
    
    bottom_right_to_side = reference_point[2] - \
        distance_in_doseplan_ROI_reference_point_px[3][0]
    bottom_right_down = reference_point[1] - \
        distance_in_doseplan_ROI_reference_point_px[3][1]
    if(bottom_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_to_side > dose_slice.shape[1]):
        bottom_right_side_corr = bottom_right_to_side - dose_slice.shape[1]
        bottom_right_to_side = dose_slice.shape[1]
        bottom_right_test_side = True
    if(bottom_right_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: \
marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_down > dose_slice.shape[0]):
        bottom_right_down_corr = bottom_right_down - dose_slice.shape[0]
        bottom_right_down = dose_slice.shape[0]
        bottom_right_test_down = True
    

    if(top_right_test_side or top_right_test_down or top_left_test_side or \
        top_left_test_down or bottom_right_test_side or bottom_right_test_down or\
            bottom_left_test_side or bottom_left_test_down):
            ROI_info = "Left side: " + str(max(top_left_side_corr, \
                bottom_left_side_corr)) + " pixels.\n"+ "Right side: " + \
                    str(max(top_right_side_corr, bottom_right_side_corr)) +\
                        " pixels.\n "+ "Top side: " + str(max(top_left_down_corr,\
                            top_right_down_corr)) + " pixels.\n"+ "Bottom side: " + \
                                str(max(bottom_left_down_corr, \
                                    bottom_right_down_corr)) + " pixels."  
            messagebox.showinfo("ROI info", "The ROI marked on the film did not \
fit with the size of the doseplan and had to be cut.\n" + ROI_info)

    for i in range(len(structures_in_plane)):
        for j in range(len(structures_in_plane[i][1])):
            row = structures_in_plane[i][1][j]
            if row < top_left_down:
                structures_in_plane[i][1][j] = 0
            elif row > bottom_left_down:
                structures_in_plane[i][1][j] = bottom_left_down-top_left_down
            else:
                structures_in_plane[i][1][j] = row - top_left_down
        for k in range(len(structures_in_plane[i][2])):
            column = structures_in_plane[i][2][k]
            if column < top_left_to_side:
                structures_in_plane[i][2][k] = 0
            elif column > top_right_to_side:
                structures_in_plane[i][2][k] = top_right_to_side-top_left_to_side
            else:
                structures_in_plane[i][2][k] = column - top_left_to_side


    doseplan_ROI_coords.append([top_left_to_side, top_left_down])
    doseplan_ROI_coords.append([top_right_to_side, top_right_down])
    doseplan_ROI_coords.append([bottom_left_to_side, bottom_left_down])
    doseplan_ROI_coords.append([bottom_right_to_side, bottom_right_down])

    #dose_slice = cv2.flip(dose_slice, 1)
    if(only_one):
        Globals.DVH_doseplan_dataset_ROI = \
            dose_slice[int(top_left_down):int(bottom_left_down), \
                int(top_left_to_side):int(top_right_to_side)]*\
                    Globals.DVH_dataset_doseplan.DoseGridScaling
    
        if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
            factor = 5
        elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
            factor = 10
        else:
            factor = 15

        img=Globals.DVH_doseplan_dataset_ROI
        img_film = Globals.DVH_film_dataset_ROI_red_channel_dose/100
        drawing_of_contours = dose_slice[int(top_left_down):\
            int(bottom_left_down)+1, int(top_left_to_side):int(top_right_to_side)+1]\
                *Globals.DVH_dataset_doseplan.DoseGridScaling
        
        structures = []
        for j in range(len(structures_in_plane)):
            temp_struct = []
            temp_struct_film = []
            for i in range(len(structures_in_plane[j][1])):
                drawing_of_contours[int(structures_in_plane[j][1][i]), \
                    int(structures_in_plane[j][2][i])] = 0
                temp_struct.append(np.array([int(structures_in_plane[j][1][i]), \
                    int(structures_in_plane[j][2][i])]))
            structures.append(temp_struct)

       

        dvh_data = []
        dvh_data_film = []

        for k in range(len(structures)):
            number_of_points = 0
            dose = []
            dose_film = []
            number_of_points_per_dose = []
            number_of_points_per_dose_film = []
            vertics = mpl.path.Path(structures[k])
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if vertics.contains_point((i,j)):
                        number_of_points+=1
                        try:
                            idx = dose.index(img[i,j])
                            exist = True
                        except:
                            exist = False
                        if not exist:
                            dose.append(img[i,j])
                            number_of_points_per_dose.append(1)
                        else:
                            number_of_points_per_dose[idx] +=1
                        try:
                            idx_film = dose_film.index(img_film[i*factor, j*factor])
                            exist_film = True
                        except:
                            exist_film = False
                        if not exist_film:
                            if not i == img.shape[0]:
                                dose_film.append(img_film[i*factor,j*factor])
                                number_of_points_per_dose_film.append(1)
                        else:
                            number_of_points_per_dose_film[idx_film] +=1

            temp_dvh_data = []
            for i in range(len(dose)):
                temp_dvh_data.append([dose[i], number_of_points_per_dose[i]])
            temp_dvh_data.sort(key=lambda x: x[0])
        
            temp_dvh_data_film = []
            for i in range(len(dose_film)):
                temp_dvh_data_film.append([dose_film[i], \
                    number_of_points_per_dose_film[i]])
            temp_dvh_data_film.sort(key=lambda x: x[0])

            dose_array = np.array([item[0] for item in temp_dvh_data])
            prc_array = [item[1] for item in temp_dvh_data]
            for i in range(len(dose_array)):
                temp = prc_array[i:len(prc_array)]
                prc_array[i] = sum(temp)
            dvh_data.append([structures_in_plane[k][0], dose_array, \
                np.array(prc_array)/number_of_points])

            dose_array_film = np.array([item[0] for item in temp_dvh_data_film])
            prc_array_film = [item[1] for item in temp_dvh_data_film]
            for i in range(len(dose_array_film)):
                temp = prc_array_film[i:len(prc_array_film)]
                prc_array_film[i] = sum(temp)
            dvh_data_film.append([structures_in_plane[k][0], \
                dose_array_film, np.array(prc_array_film)/number_of_points])
        
        
        if(Globals.DVH_dataset_doseplan.PixelSpacing==[1, 1]):
            img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
        elif(Globals.DVH_dataset_doseplan.PixelSpacing==[2, 2]):
            img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
        else:
            img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        mx=np.max(img)

        Globals.DVH_max_dose_doseplan = mx*Globals.DVH_dose_scaling_doseplan
        max_dose = mx*Globals.DVH_dose_scaling_doseplan
        img = img/mx
        PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img)*255))

        wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
        Globals.temp_image_canvas.destroy()
        doseplan_canvas = tk.Canvas(Globals.DVH_view_film_doseplan_ROI)
        doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
        doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())


        Globals.DVH_doseplan_write_image = tk.Canvas(doseplan_canvas)
        Globals.DVH_doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
        Globals.DVH_doseplan_write_image.config(bg='#ffffff', relief=FLAT, \
            highlightthickness=0, width=wid, height=heig)

        scaled_image_visual = PIL_img_doseplan_ROI
        scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
        Globals.DVH_doseplan_write_image_width = scaled_image_visual.width()
        Globals.DVH_doseplan_write_image_height = scaled_image_visual.height()
        Globals.DVH_doseplan_write_image.create_image(0,0,\
            image=scaled_image_visual, anchor="nw")
        Globals.DVH_doseplan_write_image.image = scaled_image_visual

        calculateDVH(dvh_data, dvh_data_film, True, [])


def UploadDoseplan(only_one):
#--------------------------------------------------
# Function to upload the doseplan
#
# Is called in function UploadDoseplan_button()
#--------------------------------------------------

    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(not(ext == '.dcm')):
        if(ext == ""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dcm file")
            return
    
    current_folder = os.getcwd()
    parent = os.path.dirname(file)
    os.chdir(parent)
    dataset = pydicom.dcmread(file)
    try:
        dose_summation_type = dataset.DoseSummationType
    except:
        messagebox.showerror("Error", "Could not upload the \
doseplan correctly. Try again or another file.\n (Code: dose summation)")
        return
    
    if(not(dose_summation_type == "PLAN")):
        ok = messagebox.askokcancel("Dose summation", "You \
did not upload the full doseplan. Do you want to continue?")
        if not ok:
            return
    os.chdir(current_folder)
    doseplan_dataset = dataset.pixel_array
    if(not((dataset.PixelSpacing==[1, 1] and dataset.SliceThickness==1) \
        or (dataset.PixelSpacing==[2, 2] and dataset.SliceThickness==2) \
        or (dataset.PixelSpacing==[3, 3] and dataset.SliceThickness==3))):
        messagebox.showerror("Error", "The resolution \
in doseplan must be 1x1x1, 2x2x2 or 3x3x3")
        return
    if(not(dataset.ImageOrientationPatient==[1, 0, 0, 0, 1, 0] or \
        dataset.ImageOrientationPatient==[1, 0, 0, 0, 0, 1] or \
        dataset.ImageOrientationPatient==[0, 1, 0, 1, 0, 0] or \
        dataset.ImageOrientationPatient==[0, 1, 0, 0, 0, 1] or \
        dataset.ImageOrientationPatient==[0, 0, 1, 1, 0, 0] or \
        dataset.ImageOrientationPatient==[0, 0, 1, 0, 1, 0])):
        messagebox.showerror("Error", "The Image Orientation \
(Patient) must be parallel to one of the main \
axis and perpendicular to the two others.")
        return

    Globals.DVH_dataset_doseplan = dataset
    Globals.DVH_dose_scaling_doseplan = dataset.DoseGridScaling
    Globals.DVH_test_if_added_doseplan = True
    if(Globals.DVH_test_if_added_rtplan and Globals.DVH_test_if_added_struct):
        if(Globals.DVH_isocenter_or_reference_point == "Isocenter"):
            processDoseplan_usingIsocenter(only_one)
        elif(Globals.DVH_isocenter_or_reference_point == "Ref_point"):
            processDoseplan_usingReferencePoint(only_one)
        else:
            messagebox.showerror("Error", "Something went wrong. Try again.\n\
(Code: processDoseplan)")
            return

    if only_one:
        Globals.DVH_upload_button_doseplan.config(state=DISABLED)

def UploadDoseplan_button_function():
#--------------------------------------------------
# Function to call on the function to upload doseplan
#
# Is a callback function for button 
# DVH_upload_button_doseplan in notebook.py
#--------------------------------------------------
    UploadDoseplan(True)

def UploadRTplan():
#--------------------------------------------------
# Function to upload the RT Plan file
#
# Is a callback function for button 
# DVH_upload_button_rtplan in notebook.py
#--------------------------------------------------
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(not(ext == '.dcm')):
        if(ext == ""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dcm file")
            return
    
    current_folder = os.getcwd()
    parent = os.path.dirname(file)
    os.chdir(parent)
    dataset = pydicom.dcmread(file)
    os.chdir(current_folder)
    Globals.DVH_dataset_rtplan = dataset

    try:
        isocenter_mm = \
            dataset.BeamSequence[0].ControlPointSequence[0].IsocenterPosition
        Globals.DVH_isocenter_mm = isocenter_mm
        
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. \
Try again or try another file.\n\
(Code: isocenter reading)")
        return

    try:
        Globals.DVH_doseplan_vertical_displacement = \
            dataset.PatientSetupSequence[0].TableTopVerticalSetupDisplacement
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. \
Try again or try another file. \n\
(Code: vertical table displacement)")

    try:
        Globals.DVH_doseplan_lateral_displacement = \
            dataset.PatientSetupSequence[0].TableTopLateralSetupDisplacement
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. \
Try again or try another file-\n\
(Code: lateral table displacement)")

    try:
        Globals.DVH_doseplan_longitudianl_displacement = \
            dataset.PatientSetupSequence[0].TableTopLongitudinalSetupDisplacement
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. \
Try again or try another file\n\
(Code: longitudinal table displacement)")

    try:
        patient_position = dataset.PatientSetupSequence[0].PatientPosition
        Globals.DVH_doseplan_patient_position = patient_position
    except:
        messagebox.showerror("Error", "Could not read the RT plan file. \
Try again or try another file\n\
(Code: Patient position)")
    
    if(not(patient_position=='HFS' or patient_position=='HFP' or\
        patient_position=='HFDR' or patient_position == 'HFDL'or \
            patient_position=='FFDR' or patient_position=='FFDL' or \
                patient_position=='FFP' or patient_position=='FFS')):
        messagebox.showerror("Error", "Fidora does only support \
patient positions: \nHFS, HFP, HFDR, HFDL, FFP, FFS, FFDR, FFDL")
        return
    
    Globals.DVH_test_if_added_rtplan = True
    Globals.DVH_upload_button_struct.config(state=ACTIVE)
    Globals.DVH_upload_button_rtplan.config(state=DISABLED)

def UploadStruct():
#--------------------------------------------------
# Function to upload the structure file
#
# Is a callback function for button 
# DVH_upload_button_struct in notebook.py
#--------------------------------------------------
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(not(ext == '.dcm')):
        if(ext == ""):
            return
        else:
            messagebox.showerror("Error", "The file must be a *.dcm file")
            return
    
    current_folder = os.getcwd()
    parent = os.path.dirname(file)
    os.chdir(parent)
    dataset = pydicom.dcmread(file)
    os.chdir(current_folder)
    Globals.DVH_dataset_structure_file = dataset

    try:
        Globals.DVH_contour_names = dataset.RTROIObservationsSequence
    except:
        messagebox.showerror("Error", "You must upload a strucure file \n\
(Code: UploadStruct())")
        return
    
    try:
        Globals.DVH_ROIContourSequence = dataset.ROIContourSequence
    except:
        messagebox.showerror("Error", "You must upload a strucure file \n\
(Code: UploadStruct())")
        return

    Globals.DVH_test_if_added_struct = True
    Globals.DVH_upload_button_doseplan.config(state=ACTIVE)
    Globals.DVH_upload_button_struct.config(state=DISABLED)



def pixel_to_dose(P,a,b,c):
#--------------------------------------------------
# Function to map between pixel value and dose
#
#--------------------------------------------------
    ret = c + b/(P-a)
    return ret

def markIsocenter(img, new_window_isocenter_tab, image_canvas, cv2Img):
#--------------------------------------------------
# Function mark the Isocenter
#
# Is a callback function for the button
# mark_isocenter_button in UploadFilm()
#--------------------------------------------------
    if(len(Globals.DVH_mark_isocenter_oval)>0):
        image_canvas.delete(Globals.DVH_mark_isocenter_up_down_line[0])
        image_canvas.delete(Globals.DVH_mark_isocenter_right_left_line[0])
        image_canvas.delete(Globals.DVH_mark_isocenter_oval[0])

        Globals.DVH_mark_isocenter_oval=[]
        Globals.DVH_mark_isocenter_right_left_line=[]
        Globals.DVH_mark_isocenter_up_down_line=[]

    Globals.DVH_iscoenter_coords = []
    img_mark_isocenter = ImageTk.PhotoImage(image=img)
    mark_isocenter_window = tk.Toplevel(new_window_isocenter_tab)
    mark_isocenter_window.geometry("1035x620+10+10")
    mark_isocenter_window.grab_set()

    mark_isocenter_over_all_frame = tk.Frame(mark_isocenter_window, \
        bd=0, relief=FLAT)
    mark_isocenter_over_all_canvas = Canvas(mark_isocenter_over_all_frame)

    mark_isocenter_xscrollbar = Scrollbar(mark_isocenter_over_all_frame, \
        orient=HORIZONTAL, command=mark_isocenter_over_all_canvas.xview)
    mark_isocenter_yscrollbar = Scrollbar(mark_isocenter_over_all_frame, \
        command=mark_isocenter_over_all_canvas.yview)

    mark_isocenter_scroll_frame = ttk.Frame(mark_isocenter_over_all_canvas)
    mark_isocenter_scroll_frame.bind("<Configure>", lambda e: \
        mark_isocenter_over_all_canvas.configure\
            (scrollregion=mark_isocenter_over_all_canvas.bbox('all')))

    mark_isocenter_over_all_canvas.create_window((0,0), \
        window=mark_isocenter_scroll_frame, anchor='nw')
    mark_isocenter_over_all_canvas.configure\
        (xscrollcommand=mark_isocenter_xscrollbar.set, \
            yscrollcommand=mark_isocenter_yscrollbar.set)

    mark_isocenter_over_all_frame.config(highlightthickness=0, bg='#ffffff')
    mark_isocenter_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
    mark_isocenter_over_all_frame.pack(expand=True, fill=BOTH)
    mark_isocenter_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
    mark_isocenter_over_all_frame.grid_columnconfigure(0, weight=1)
    mark_isocenter_over_all_frame.grid_rowconfigure(0, weight=1)
    mark_isocenter_xscrollbar.grid(row=1, column=0, sticky=E+W)
    mark_isocenter_over_all_frame.grid_columnconfigure(1, weight=0)
    mark_isocenter_over_all_frame.grid_rowconfigure(1, weight=0)
    mark_isocenter_yscrollbar.grid(row=0, column=1, sticky=N+S)
    mark_isocenter_over_all_frame.grid_columnconfigure(2, weight=0)
    mark_isocenter_over_all_frame.grid_rowconfigure(2, weight=0)

    mark_isocenter_image_canvas = tk.Canvas(mark_isocenter_scroll_frame)
    mark_isocenter_image_canvas.grid(row=0,column=0, rowspan=10, \
        columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
    mark_isocenter_scroll_frame.grid_columnconfigure(0, weight=0)
    mark_isocenter_scroll_frame.grid_rowconfigure(0, weight=0)

    mark_isocenter_image_canvas.create_image(0,0,\
        image=img_mark_isocenter,anchor="nw")
    mark_isocenter_image_canvas.image = img_mark_isocenter
    mark_isocenter_image_canvas.config(cursor='hand2', \
        bg='#ffffff', relief=FLAT, bd=0, \
        scrollregion=mark_isocenter_image_canvas.bbox(ALL), \
            height=img_mark_isocenter.height(), width=img_mark_isocenter.width())
    mark_isocenter_image_canvas.grid_propagate(0)

    def findCoords(event):
        mark_isocenter_image_canvas.create_oval\
            (event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        if(Globals.DVH_iscoenter_coords==[]):
            Globals.DVH_iscoenter_coords.append([event.x, event.y])
            mark_isocenter_image_canvas.config(cursor='hand2')

        elif(len(Globals.DVH_iscoenter_coords)==1):
            Globals.DVH_iscoenter_coords.append([event.x, event.y])
            Globals.DVH_film_isocenter = \
                [Globals.DVH_iscoenter_coords[0][0], \
                    Globals.DVH_iscoenter_coords[1][1]]
            x1,y1 = Globals.DVH_iscoenter_coords[0]
            x4,y4 = Globals.DVH_iscoenter_coords[1]
            x2 = x1;y3=y4
            y2=2*Globals.DVH_film_isocenter[1]-y1
            x3=2*Globals.DVH_film_isocenter[0]-x4
            up_down_line = image_canvas.create_line\
                (int(x1/2),int(y1/2),int(x2/2),int(y2/2),\
                    fill='purple', smooth=1, width=2)
            right_left_line = image_canvas.create_line\
                (int(x3/2),int(y3/2),int(x4/2),int(y4/2), \
                    fill='purple', smooth=1, width=2)
            oval = image_canvas.create_oval\
                (int(Globals.DVH_film_isocenter[0]/2)-3, \
                    int(Globals.DVH_film_isocenter[1]/2)-3,\
                        int(Globals.DVH_film_isocenter[0]/2)+3, \
                            int(Globals.DVH_film_isocenter[1]/2)+3, fill='red')

            Globals.DVH_mark_isocenter_up_down_line.append(up_down_line)
            Globals.DVH_mark_isocenter_right_left_line.append(right_left_line)
            Globals.DVH_mark_isocenter_oval.append(oval)

            mark_isocenter_window.after(500, lambda: mark_isocenter_window.destroy())
            Globals.DVH_isocenter_check = True
            if(Globals.DVH_ROI_check):
                Globals.DVH_done_button.config(state=ACTIVE)
            
    mark_isocenter_image_canvas.bind("<Button 1>",findCoords)

def markReferencePoint(img, new_window_reference_point_tab, \
    image_canvas_reference_tab, cv2Img):
#--------------------------------------------------
# Function to mark reference point
#
# Is a callback function for button 
# mark_point_button in UploadFilm()
#--------------------------------------------------
    if(len(Globals.DVH_mark_reference_point_oval)>0):
        image_canvas_reference_tab.delete(Globals.DVH_mark_reference_point_oval[0])
        Globals.DVH_mark_reference_point_oval=[]
     
    img_mark_reference_point = ImageTk.PhotoImage(image=img)
    mark_reference_point_window = tk.Toplevel(new_window_reference_point_tab)
    mark_reference_point_window.geometry("1035x620+10+10")
    mark_reference_point_window.grab_set()

    mark_reference_point_over_all_frame = tk.Frame(mark_reference_point_window, \
        bd=0, relief=FLAT)
    mark_reference_point_over_all_canvas = \
        Canvas(mark_reference_point_over_all_frame)

    mark_reference_point_xscrollbar = \
        Scrollbar(mark_reference_point_over_all_frame, orient=HORIZONTAL, \
            command=mark_reference_point_over_all_canvas.xview)
    mark_reference_point_yscrollbar = \
        Scrollbar(mark_reference_point_over_all_frame, \
            command=mark_reference_point_over_all_canvas.yview)

    mark_reference_point_scroll_frame = \
        ttk.Frame(mark_reference_point_over_all_canvas)
    mark_reference_point_scroll_frame.bind("<Configure>", \
        lambda e: mark_reference_point_over_all_canvas.configure\
            (scrollregion=mark_reference_point_over_all_canvas.bbox('all')))

    mark_reference_point_over_all_canvas.create_window((0,0), \
        window=mark_reference_point_scroll_frame, anchor='nw')
    mark_reference_point_over_all_canvas.configure\
        (xscrollcommand=mark_reference_point_xscrollbar.set, \
            yscrollcommand=mark_reference_point_yscrollbar.set)

    mark_reference_point_over_all_frame.config(highlightthickness=0, bg='#ffffff')
    mark_reference_point_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
    mark_reference_point_over_all_frame.pack(expand=True, fill=BOTH)
    mark_reference_point_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
    mark_reference_point_over_all_frame.grid_columnconfigure(0, weight=1)
    mark_reference_point_over_all_frame.grid_rowconfigure(0, weight=1)
    mark_reference_point_xscrollbar.grid(row=1, column=0, sticky=E+W)
    mark_reference_point_over_all_frame.grid_columnconfigure(1, weight=0)
    mark_reference_point_over_all_frame.grid_rowconfigure(1, weight=0)
    mark_reference_point_yscrollbar.grid(row=0, column=1, sticky=N+S)
    mark_reference_point_over_all_frame.grid_columnconfigure(2, weight=0)
    mark_reference_point_over_all_frame.grid_rowconfigure(2, weight=0)

    mark_reference_point_image_canvas = tk.Canvas(mark_reference_point_scroll_frame)
    mark_reference_point_image_canvas.grid(row=0,column=0, rowspan=10, \
        columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
    mark_reference_point_scroll_frame.grid_columnconfigure(0, weight=0)
    mark_reference_point_scroll_frame.grid_rowconfigure(0, weight=0)

    mark_reference_point_image_canvas.create_image(0,0,\
        image=img_mark_reference_point,anchor="nw")
    mark_reference_point_image_canvas.image = img_mark_reference_point
    mark_reference_point_image_canvas.config(cursor='hand2', \
        bg='#ffffff', relief=FLAT, bd=0, \
        scrollregion=mark_reference_point_image_canvas.bbox(ALL), \
            height=img_mark_reference_point.height(), \
                width=img_mark_reference_point.width())
    mark_reference_point_image_canvas.grid_propagate(0)


    def findCoords(event):
        mark_reference_point_image_canvas.create_oval\
            (event.x-2, event.y-2, event.x+2, event.y+2, fill='red')
        Globals.DVH_film_reference_point = [event.x, event.y]
        oval = image_canvas_reference_tab.create_oval\
            (int(Globals.DVH_film_reference_point[0]/2)-3, \
                int(Globals.DVH_film_reference_point[1]/2)-3, \
                    int(Globals.DVH_film_reference_point[0]/2)+3, \
                        int(Globals.DVH_film_reference_point[1]/2)+3, fill='red')
        Globals.DVH_mark_reference_point_oval.append(oval)

        mark_reference_point_window.after(500, \
            lambda: mark_reference_point_window.destroy())
        Globals.DVH_reference_point_check = True
        if(Globals.DVH_ROI_reference_point_check):
            Globals.DVH_done_button_reference_point.config(state=ACTIVE)

    mark_reference_point_image_canvas.bind("<Button 1>",findCoords)

def markROI(img, tab, canvas, ref_point_test):
#--------------------------------------------------
# Function to mark ROI
#
# Is a callback function for button 
# mark_ROI_button in UploadFilm()
#--------------------------------------------------
    if(len(Globals.DVH_mark_ROI_rectangle)>0):
        canvas.delete(Globals.DVH_mark_ROI_rectangle[0])
        Globals.DVH_mark_ROI_rectangle = []

    Globals.DVH_ROI_coords = []

    img_mark_ROI = ImageTk.PhotoImage(image=img)
    mark_ROI_window = tk.Toplevel(tab)
    mark_ROI_window.geometry("1035x620+10+10")
    mark_ROI_window.grab_set()

    mark_ROI_over_all_frame = tk.Frame(mark_ROI_window, bd=0, relief=FLAT)
    mark_ROI_over_all_canvas = Canvas(mark_ROI_over_all_frame)

    mark_ROI_xscrollbar = Scrollbar(mark_ROI_over_all_frame, \
        orient=HORIZONTAL, command=mark_ROI_over_all_canvas.xview)
    mark_ROI_yscrollbar = Scrollbar(mark_ROI_over_all_frame, \
        command=mark_ROI_over_all_canvas.yview)

    mark_ROI_scroll_frame = ttk.Frame(mark_ROI_over_all_canvas)
    mark_ROI_scroll_frame.bind("<Configure>", lambda e: \
        mark_ROI_over_all_canvas.configure\
            (scrollregion=mark_ROI_over_all_canvas.bbox('all')))

    mark_ROI_over_all_canvas.create_window((0,0), \
        window=mark_ROI_scroll_frame, anchor='nw')
    mark_ROI_over_all_canvas.configure\
        (xscrollcommand=mark_ROI_xscrollbar.set, \
            yscrollcommand=mark_ROI_yscrollbar.set)

    mark_ROI_over_all_frame.config(highlightthickness=0, bg='#ffffff')
    mark_ROI_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
    mark_ROI_over_all_frame.pack(expand=True, fill=BOTH)
    mark_ROI_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
    mark_ROI_over_all_frame.grid_columnconfigure(0, weight=1)
    mark_ROI_over_all_frame.grid_rowconfigure(0, weight=1)
    mark_ROI_xscrollbar.grid(row=1, column=0, sticky=E+W)
    mark_ROI_over_all_frame.grid_columnconfigure(1, weight=0)
    mark_ROI_over_all_frame.grid_rowconfigure(1, weight=0)
    mark_ROI_yscrollbar.grid(row=0, column=1, sticky=N+S)
    mark_ROI_over_all_frame.grid_columnconfigure(2, weight=0)
    mark_ROI_over_all_frame.grid_rowconfigure(2, weight=0)

    mark_ROI_image_canvas = tk.Canvas(mark_ROI_scroll_frame)
    mark_ROI_image_canvas.grid(row=0,column=0, rowspan=10, \
        columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
    mark_ROI_scroll_frame.grid_columnconfigure(0, weight=0)
    mark_ROI_scroll_frame.grid_rowconfigure(0, weight=0)
    mark_ROI_image_canvas.create_image(0,0,image=img_mark_ROI,anchor="nw")
    mark_ROI_image_canvas.image = img_mark_ROI
    mark_ROI_image_canvas.config(bg='#E5f9ff', relief=FLAT, bd=0, \
        scrollregion=mark_ROI_image_canvas.bbox(ALL), \
            height=img_mark_ROI.height(), width=img_mark_ROI.width())
    mark_ROI_image_canvas.grid_propagate(0)

    rectangle = mark_ROI_image_canvas.create_rectangle(0,0,0,0,outline='green')
    rectangle_top_corner = []
    rectangle_bottom_corner = []
    def buttonPushed(event):
        rectangle_top_corner.append([event.x, event.y])
      
    def buttonMoving(event):
        mark_ROI_image_canvas.coords(rectangle, rectangle_top_corner[0][0], \
            rectangle_top_corner[0][1], event.x, event.y)

    def buttonReleased(event):
        rectangle_bottom_corner.append([event.x, event.y])
        mark_ROI_image_canvas.coords(rectangle, rectangle_top_corner[0][0], \
            rectangle_top_corner[0][1],rectangle_bottom_corner[0][0], \
                rectangle_bottom_corner[0][1])
        mark_ROI_image_canvas.itemconfig(rectangle, outline='Blue')

        Globals.DVH_ROI_coords.append([rectangle_top_corner[0][0], \
            rectangle_top_corner[0][1]])
        Globals.DVH_ROI_coords.append([rectangle_bottom_corner[0][0], \
            rectangle_top_corner[0][1]])
        Globals.DVH_ROI_coords.append([rectangle_top_corner[0][0], \
            rectangle_bottom_corner[0][1]])
        Globals.DVH_ROI_coords.append([rectangle_bottom_corner[0][0], \
            rectangle_bottom_corner[0][1]])

        rect = canvas.create_rectangle(int((rectangle_top_corner[0][0])/2), \
            int((rectangle_top_corner[0][1])/2),\
                int((rectangle_bottom_corner[0][0])/2), \
                    int((rectangle_bottom_corner[0][1])/2), outline='Blue', width=2)
        Globals.DVH_mark_ROI_rectangle.append(rect)

        if(ref_point_test):
            Globals.DVH_ROI_reference_point_check = True
            if(Globals.DVH_reference_point_check):
                Globals.DVH_done_button_reference_point.config(state=ACTIVE)
        else:
            Globals.DVH_ROI_check = True
            if(Globals.DVH_isocenter_check):
                Globals.DVH_done_button.config(state=ACTIVE)


        mark_ROI_window.after(500, lambda: mark_ROI_window.destroy())

    mark_ROI_image_canvas.bind("<B1-Motion>", buttonMoving)
    mark_ROI_image_canvas.bind("<Button-1>", buttonPushed)
    mark_ROI_image_canvas.bind("<ButtonRelease-1>", buttonReleased)

def UploadFilm():
#--------------------------------------------------
# Function to upload the Film
#
# Is a callback function for button 
# DVH_upload_button_film in notebook.py
#--------------------------------------------------
    if(Globals.DVH_film_orientation.get() == '-'):
        messagebox.showerror("Missing parameter", "Film orientation missing \n \
(Code: UploadFilm)")
        return
    if Globals.DVH_film_factor_input.get("1.0", 'end-1c') == " ":
        Globals.DVH_film_factor = 1
    else:
        try:
            Globals.DVH_film_factor = \
                float(Globals.DVH_film_factor_input.get("1.0", 'end-1c'))
        except:
            messagebox.showerror("Missing parameter", "Film factor invalid format.\n\
(Code: UploadFilm)")
            return

    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(ext == '.tif'):
        current_folder = os.getcwd()
        parent = os.path.dirname(file)
        os.chdir(parent)
        img = Image.open(file)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        cv2Img = cv2.imread(basename(normpath(file)), \
            cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        cv2Img = cv2.medianBlur(cv2Img, 5)
        if(cv2Img is None):
            messagebox.showerror("Error", "Something has gone wrong. \
Check that the filename only contain english letters")
            return
        if(cv2Img.shape[2] == 3):
            if(cv2Img.shape[0]==1270 and cv2Img.shape[1]==1016):
                cv2Img = abs(cv2Img-Globals.correctionMatrix127)
                cv2Img = np.clip(cv2Img, 0, 65535)
                cv2Img = cv2.flip(cv2Img,1)
                img_scaled = img.resize((508, 635), Image.ANTIALIAS)
                img_scaled = ImageTk.PhotoImage(image=img_scaled)
                

                Globals.DVH_film_dataset = cv2Img
                Globals.DVH_film_dataset_red_channel = cv2Img[:,:,2]
            else:
                messagebox.showerror("Error","The resolution of \
the image is not consistent with dpi")
                return
        else:
            messagebox.showerror("Error","The uploaded \
image need to be in RGB-format")
            return

        os.chdir(current_folder)

        if(not (img.width == 1016)):
            messagebox.showerror("Error", "Dpi in image has to be 127")
            return

        Globals.DVH_film_orientation_menu.configure(state=DISABLED)
        Globals.DVH_film_factor_input.config(state=DISABLED)

        h = 635 + 20
        w = 508 + 625
        new_window = tk.Toplevel(Globals.tab5)
        new_window.geometry("%dx%d+0+0" % (w, h))
        new_window.grab_set()

        new_window_over_all_frame = tk.Frame(new_window, bd=0, relief=FLAT)
        new_window_over_all_canvas = Canvas(new_window_over_all_frame)

        new_window_xscrollbar = Scrollbar(new_window_over_all_frame, \
            orient=HORIZONTAL, command=new_window_over_all_canvas.xview)
        new_window_yscrollbar = Scrollbar(new_window_over_all_frame, \
            command=new_window_over_all_canvas.yview)

        new_window_scroll_frame = ttk.Frame(new_window_over_all_canvas)
        new_window_scroll_frame.bind("<Configure>", lambda e: \
            new_window_over_all_canvas.configure\
                (scrollregion=new_window_over_all_canvas.bbox('all')))

        new_window_over_all_canvas.create_window((0,0), \
            window=new_window_scroll_frame, anchor='nw')
        new_window_over_all_canvas.configure\
            (xscrollcommand=new_window_xscrollbar.set, \
                yscrollcommand=new_window_yscrollbar.set)

        new_window_over_all_frame.config(highlightthickness=0, bg='#ffffff')
        new_window_over_all_canvas.config(highlightthickness=0, bg='#ffffff')
        new_window_over_all_frame.pack(expand=True, fill=BOTH)
        new_window_over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
        new_window_over_all_frame.grid_columnconfigure(0, weight=1)
        new_window_over_all_frame.grid_rowconfigure(0, weight=1)
        new_window_xscrollbar.grid(row=1, column=0, sticky=E+W)
        new_window_over_all_frame.grid_columnconfigure(1, weight=0)
        new_window_over_all_frame.grid_rowconfigure(1, weight=0)
        new_window_yscrollbar.grid(row=0, column=1, sticky=N+S)
        new_window_over_all_frame.grid_columnconfigure(2, weight=0)
        new_window_over_all_frame.grid_rowconfigure(2, weight=0)

        new_window_explain_text = tk.Text(new_window_scroll_frame,\
             height= 3, width=120)
        new_window_explain_text.insert(INSERT, \
"To match the film with the doseplan you have to mark either isocenter or a \
reference point on the film of your choice.In the case of the reference point \
you \nwill be asked to input the lenght in lateral, longitudinal and vertical \
to a reference point used in the linac. It the reference point in the film is \
the same as \nthe one in the phantom/linac you can input all zeros, in other \
cases your input is in mm. Later you will have the oppertunity to make small\
adjustments \nto the placement of either the reference point or isocenter.")
        new_window_explain_text.config(state=DISABLED, \
            font=('calibri', '13', 'bold'), bg = '#ffffff', relief=FLAT)
        new_window_explain_text.grid(row=0, column=0, columnspan=5, \
            sticky=N+S+W+E, pady=(15,5), padx=(10,10))
        new_window_scroll_frame.grid_rowconfigure(0, weight=0)
        new_window_scroll_frame.grid_columnconfigure(0, weight=0)

        new_window_notebook = ttk.Notebook(new_window_scroll_frame)
        new_window_notebook.borderWidth=0
        new_window_notebook.grid(row=2, column=0, columnspan=5, \
            sticky=E+W+N+S, pady=(0,0), padx =(0,0))
        new_window_scroll_frame.grid_rowconfigure(4, weight=0)
        new_window_scroll_frame.grid_columnconfigure(4, weight=0)

        new_window_isocenter_tab = ttk.Frame(new_window_notebook)
        new_window_notebook.add(new_window_isocenter_tab, text='Isocenter')
        new_window_reference_point_tab = ttk.Frame(new_window_notebook)
        new_window_notebook.add(new_window_reference_point_tab, \
            text='Reference point')
        new_window_manually_tab = ttk.Frame(new_window_notebook)
        new_window_notebook.add(new_window_manually_tab, text='Manually')

        image_canvas = tk.Canvas(new_window_isocenter_tab)
        image_canvas.grid(row=0,column=0, rowspan=12, columnspan=3, \
            sticky=N+S+E+W, padx=(0,0), pady=(0,0))
        new_window_isocenter_tab.grid_rowconfigure(1, weight=0)
        new_window_isocenter_tab.grid_columnconfigure(1, weight=0)
        image_canvas.create_image(0,0,image=img_scaled,anchor="nw")
        image_canvas.image = img_scaled
        image_canvas.config(bg='#ffffff', relief=FLAT, bd=0, \
            scrollregion=image_canvas.bbox(ALL), \
                height=img_scaled.height(), width=img_scaled.width())
        image_canvas.grid_propagate(0)

        image_canvas_reference_tab = tk.Canvas(new_window_reference_point_tab)
        image_canvas_reference_tab.grid(row=0,column=0, rowspan=10, \
            columnspan=3, sticky=N+S+E+W, padx=(0,0), pady=(0,0))
        new_window_reference_point_tab.grid_rowconfigure(1, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(1, weight=0)
        image_canvas_reference_tab.create_image(0,0,image=img_scaled,anchor="nw")
        image_canvas_reference_tab.image = img_scaled
        image_canvas_reference_tab.config(bg='#ffffff', relief=FLAT, bd=0, \
            scrollregion=image_canvas.bbox(ALL), \
                height=img_scaled.height(), width=img_scaled.width())
        image_canvas_reference_tab.grid_propagate(0)

        film_window_mark_isocenter_text = \
            tk.Text(new_window_isocenter_tab, width=55, height=7)
        film_window_mark_isocenter_text.insert(INSERT, \
"When clicking the button \"Mark isocenter\" a window showing \n\
the image will appear and you are to click on the markers \n\
made on the film upon irradiation to find the isocenter. Start \n\
with the marker showing the direction of the film (see the \n\
specifications in main window). When both marks are made \n\
you will see the isocenter in the image. If you are not happy \n\
with the placement click the button again and repeat.")
        film_window_mark_isocenter_text.config(bg='#ffffff', relief=FLAT, bd=0, \
        state=DISABLED, font=('calibri', '11'))
        film_window_mark_isocenter_text.grid(row=0, column=3, rowspan=3, \
            sticky=N+S+E+W, padx=(10,10), pady=(10,0))
        new_window_isocenter_tab.columnconfigure(2, weight=0)
        new_window_isocenter_tab.rowconfigure(2, weight=0)

        film_window_mark_reference_point_text = \
            tk.Text(new_window_reference_point_tab, width=55, height=5)
        film_window_mark_reference_point_text.insert(INSERT, \
"When clicking the button \"Mark point\" a window showing \n\
the image will appear and you are to click on the marker \n\
made on the film upon irradiation to find the point. When\n\
the mark are made you will see the isocenter in the image.\n\
If you are not happy with the placement click the button \n\
again and repeat.")
        film_window_mark_reference_point_text.config(bg='#ffffff', \
            relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_reference_point_text.grid(row=0, column=3, \
            rowspan=3, sticky=N+S+E+W, padx=(10,10), pady=(5,0))
        new_window_reference_point_tab.columnconfigure(2, weight=0)
        new_window_reference_point_tab.rowconfigure(2, weight=0)
            
        mark_isocenter_button_frame = tk.Frame(new_window_isocenter_tab)
        mark_isocenter_button_frame.grid(row=3, column=3, padx=(10,10), pady=(0,10))
        mark_isocenter_button_frame.configure(bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(3, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(3, weight=0)

        mark_isocenter_button = tk.Button(mark_isocenter_button_frame, \
            text='Browse', image=Globals.profiles_mark_isocenter_button_image,\
                cursor='hand2',font=('calibri', '14'), relief=FLAT, state=ACTIVE, \
                    command=lambda: markIsocenter(img, new_window_isocenter_tab, \
                        image_canvas, cv2Img))
        mark_isocenter_button.pack(expand=True, fill=BOTH)
        mark_isocenter_button.config(bg='#ffffff', activebackground='#ffffff', \
            activeforeground='#ffffff', highlightthickness=0)
        mark_isocenter_button.image=Globals.profiles_mark_isocenter_button_image

        mark_point_button_frame = tk.Frame(new_window_reference_point_tab)
        mark_point_button_frame.grid(row=3, column=3, padx=(10,10), pady=(30,0))
        mark_point_button_frame.configure(bg='#ffffff')
        new_window_reference_point_tab.grid_columnconfigure(3, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(3, weight=0)

        mark_point_button = tk.Button(mark_point_button_frame, text='Browse', \
            image=Globals.profiles_mark_point_button_image,\
                cursor='hand2',font=('calibri', '14'), relief=FLAT, \
                    state=ACTIVE, command=lambda: markReferencePoint(img, \
                        new_window_reference_point_tab, image_canvas_reference_tab, \
                            cv2Img))
        mark_point_button.pack(expand=True, fill=BOTH)
        mark_point_button.config(bg='#ffffff', activebackground='#ffffff', \
            activeforeground='#ffffff', highlightthickness=0)
        mark_point_button.image=Globals.profiles_mark_point_button_image

        write_displacement_relative_to_reference_point = \
            tk.Text(new_window_reference_point_tab, width = 55, height=3)
        write_displacement_relative_to_reference_point.insert(INSERT, "\
If the marked reference points in the film does not match\n\
the reference point in the phantom you can write the\n\
displacemnet here (in mm). Defaults to zero ")
        write_displacement_relative_to_reference_point.grid(row=4, column=3, \
            rowspan=2, sticky=N+S+E+W, padx=(10,10), pady=(0,10))
        write_displacement_relative_to_reference_point.config(bg='#ffffff', \
            relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        new_window_reference_point_tab.grid_rowconfigure(6, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(6, weight=0)

        input_lateral_text = tk.Text(new_window_reference_point_tab, \
            width=12, height=1)
        input_lateral_text.insert(INSERT, "Lateral:")
        input_lateral_text.config(bg='#ffffff', relief=FLAT, bd=0, \
        state=DISABLED, font=('calibri', '10'))
        input_lateral_text.grid(row=5, column=3, sticky=N+S, \
            padx=(0,250), pady=(25,0))
        new_window_reference_point_tab.grid_rowconfigure(10, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(10, weight=0)

        Globals.DVH_input_lateral_displacement = \
            tk.Text(new_window_reference_point_tab, width=5, height=1)
        Globals.DVH_input_lateral_displacement.insert(INSERT, " ")
        Globals.DVH_input_lateral_displacement.config(bg='#E5f9ff', \
            relief=GROOVE, bd=2, state=NORMAL, font=('calibri', '11'))
        Globals.DVH_input_lateral_displacement.grid(row=5, column=3, \
            padx=(0,285), pady=(35,0))
        new_window_reference_point_tab.grid_rowconfigure(7, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(7, weight=0)

        input_vertical_text = tk.Text(new_window_reference_point_tab, \
            width=12, height=1)
        input_vertical_text.insert(INSERT, "Vertical:")
        input_vertical_text.config(bg='#ffffff', relief=FLAT, bd=0, \
            state=DISABLED, font=('calibri', '10'))
        input_vertical_text.grid(row=5, column=3, sticky=N+S, \
            padx=(0,0), pady=(25,0))
        new_window_reference_point_tab.grid_rowconfigure(11, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(11, weight=0)

        Globals.DVH_input_vertical_displacement = \
            tk.Text(new_window_reference_point_tab, width=4, height=1)
        Globals.DVH_input_vertical_displacement.insert(INSERT, " ")
        Globals.DVH_input_vertical_displacement.config(bg='#E5f9ff', \
            relief=GROOVE, bd=2, state=NORMAL, font=('calibri', '11'))
        Globals.DVH_input_vertical_displacement.grid(row=5, column=3, \
            padx=(0,25), pady=(35,0))
        new_window_reference_point_tab.grid_rowconfigure(8, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(8, weight=0)   

        input_long_text = tk.Text(new_window_reference_point_tab, \
            width=12, height=1)
        input_long_text.insert(INSERT, "Longitudinal:")
        input_long_text.config(bg='#ffffff', relief=FLAT, bd=0, \
            state=DISABLED, font=('calibri', '10'))
        input_long_text.grid(row=5, column=3, sticky=N+S, \
            padx=(250,0), pady=(25,0))
        new_window_reference_point_tab.grid_rowconfigure(12, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(12, weight=0)

        Globals.DVH_input_longitudinal_displacement = \
            tk.Text(new_window_reference_point_tab, width=5, height=1)
        Globals.DVH_input_longitudinal_displacement.insert(INSERT, " ")
        Globals.DVH_input_longitudinal_displacement.config\
            (bg='#E5f9ff', relief=GROOVE, bd=2, state=NORMAL, font=('calibri', '11'))
        Globals.DVH_input_longitudinal_displacement.grid\
            (row=5, column=3, padx=(240,0), pady=(35,0))
        new_window_reference_point_tab.grid_rowconfigure(9, weight=0)
        new_window_reference_point_tab.grid_columnconfigure(9, weight=0)     

        film_window_mark_ROI_text = tk.Text(new_window_isocenter_tab,\
             width=55, height=7)
        film_window_mark_ROI_text.insert(INSERT, \
"When clicking the button \"Mark ROI\" a window showing the\n\
image will appear and you are to drag a rectangle marking \n\
the region of interest. Fidora will assume the film has been\n\
scanned in either portrait or landscape orientation. When\n\
the ROI has been marked it will appear on the image. If you\n\
are not happy with the placement click the button again.")
        film_window_mark_ROI_text.config(bg='#ffffff', relief=FLAT, \
            bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_ROI_text.grid(row=5, column=3, rowspan=4, \
            sticky=N+S+E+W, padx=(10,10), pady=(0,0))
        new_window_isocenter_tab.grid_columnconfigure(4, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(4, weight=0)
        
        film_window_mark_ROI_reference_point_text = \
            tk.Text(new_window_reference_point_tab, width=55, height=5)
        film_window_mark_ROI_reference_point_text.insert(INSERT, \
"When clicking the button \"Mark ROI\" a window showing the\n\
image will appear and you are to drag a rectangle marking \n\
the region of interest. Fidora will assume the film has been\n\
scanned in either portrait or landscape orientation. When\n\
the ROI has been marked it will appear on the image. If you\n\
are not happy with the placement click the button again.")
        film_window_mark_ROI_reference_point_text.config(bg='#ffffff', \
            relief=FLAT, bd=0, state=DISABLED, font=('calibri', '11'))
        film_window_mark_ROI_reference_point_text.grid(row=6, column=3, \
            rowspan=3, sticky=N+E+W, padx=(10,10), pady=(10,0))
        new_window_reference_point_tab.grid_columnconfigure(4, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(4, weight=0)
        
        mark_ROI_button_frame = tk.Frame(new_window_isocenter_tab)
        mark_ROI_button_frame.grid(row=8, column=3, padx=(10,0), pady=(0,5))
        mark_ROI_button_frame.configure(bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(5, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(5, weight=0)

        mark_ROI_button = tk.Button(mark_ROI_button_frame, text='Browse', \
            image=Globals.profiles_mark_ROI_button_image,cursor='hand2',\
                font=('calibri', '14'), relief=FLAT, state=ACTIVE, command=lambda:\
                    markROI(img, new_window_isocenter_tab, image_canvas, False))
        mark_ROI_button.pack(expand=True, fill=BOTH)
        mark_ROI_button.config(bg='#ffffff', activebackground='#ffffff', \
            activeforeground='#ffffff', highlightthickness=0)
        mark_ROI_button.image=Globals.profiles_mark_ROI_button_image

        slice_offset_text = tk.Text(new_window_isocenter_tab, width=25, height=1)
        slice_offset_text.insert(INSERT, "Slice offset, mm (default 0):")
        slice_offset_text.config(state=DISABLED, font=('calibri', '10'), \
            bd = 0, relief=FLAT)   
        slice_offset_text.grid(row=9, column=3, padx=(5,110), pady=(0,0))
        new_window_isocenter_tab.grid_columnconfigure(6, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(6, weight=0)

        Globals.DVH_slice_offset = tk.Text(new_window_isocenter_tab, \
            width=8, height=1)
        Globals.DVH_slice_offset.grid(row=9, column=3, padx=(110,10), pady=(0,0))
        Globals.DVH_slice_offset.insert(INSERT, " ")
        Globals.DVH_slice_offset.config(state=NORMAL, \
            font=('calibri', '10'), bd = 2, bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(7, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(7, weight=0)

        mark_ROI_button_reference_point_frame = \
            tk.Frame(new_window_reference_point_tab)
        mark_ROI_button_reference_point_frame.grid(row=9, column=3, \
            padx=(10,10), pady=(0,5))
        mark_ROI_button_reference_point_frame.configure(bg='#ffffff')
        new_window_reference_point_tab.grid_columnconfigure(5, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(5, weight=0)

        mark_ROI_reference_point_button = \
            tk.Button(mark_ROI_button_reference_point_frame, text='Browse', \
                image=Globals.profiles_mark_ROI_button_image,cursor='hand2',\
                    font=('calibri', '14'), relief=FLAT, state=ACTIVE, \
                        command=lambda: markROI(img, \
                            new_window_reference_point_tab, \
                                image_canvas_reference_tab, True))
        mark_ROI_reference_point_button.pack(expand=True, fill=BOTH)
        mark_ROI_reference_point_button.config(bg='#ffffff', \
            activebackground='#ffffff', activeforeground='#ffffff', \
            highlightthickness=0)
        mark_ROI_reference_point_button.image=\
            Globals.profiles_mark_ROI_button_image

        def finishFilmMarkers(ref_test):
            Globals.DVH_slice_offset.config(state=DISABLED)
            if(ref_test):
                if(not(Globals.DVH_input_lateral_displacement.get\
                    ("1.0",'end-1c')==" ")):
                    try:
                        test = float(Globals.DVH_input_lateral_displacement.get\
                            ("1.0",'end-1c'))
                        Globals.DVH_lateral = test
                    except:
                        messagebox.showerror("Error", "The displacements \
must be numbers\n (Code: lateral displacement)")
                        return
                else:
                    Globals.DVH_lateral = 0
                if(not(Globals.DVH_input_longitudinal_displacement.get\
                    ("1.0",'end-1c')==" ")):
                    try:
                        test = float(Globals.DVH_input_longitudinal_displacement.get\
                            ("1.0", 'end-1c'))
                        Globals.DVH_longitudinal = test
                    except:
                        messagebox.showerror("Error", "The displacements must \
be numbers\n (Code: longitudinal displacement)")
                        return
                else:
                    Globals.DVH_longitudinal = 0
                if(not(Globals.DVH_input_vertical_displacement.get\
                    ("1.0",'end-1c')==" ")):
                    try:
                        test = float(Globals.DVH_input_vertical_displacement.get\
                            ("1.0", 'end-1c'))
                        Globals.DVH_vertical = test
                    except:
                        messagebox.showerror("Error", "The displacements \
must be numbers\n (Code: vertical displacement)")
                        return
                else:
                    Globals.DVH_vertical = 0
                Globals.DVH_input_vertical_displacement.config(state=DISABLED)
                Globals.DVH_input_longitudinal_displacement.config(state=DISABLED)
                Globals.DVH_input_lateral_displacement.config(state=DISABLED)
            else:
                if not Globals.DVH_slice_offset.get("1.0",'end-1c')==" ":
                    try:
                        offset = float(Globals.DVH_slice_offset.get("1.0",'end-1c'))
                        Globals.DVH_offset = offset
                    except:
                        messagebox.showerror("Error", "Slice offset must \
be a number \n(Code: finishFilmMarkers(false)")
                        return
                else:
                    Globals.DVH_offset = 0
            if(ref_test):
                choose_batch_window = tk.Toplevel(new_window_reference_point_tab)
            else:
                choose_batch_window = tk.Toplevel(new_window_isocenter_tab)

            choose_batch_window.geometry("670x380+50+50")
            choose_batch_window.grab_set()

            choose_batch_frame = tk.Frame(choose_batch_window)
            choose_batch_frame.pack(expand=True, fill=BOTH)
            choose_batch_frame.configure(bg='#ffffff')

            batch_cnt = 0
            weight_cnt = 0
            read = open('calibration.txt', 'r')
            lines = read.readlines()
            read.close()
            row_cnt=0
            for l in lines:
                words = l.split()
                line = "Batch nr.  : " + words[2] + ".    Date:   " + words[0] +\
                     "  " + words[1] + "."
                write_batch_nr = tk.Text(choose_batch_frame, width=10, height=1)
                write_batch_nr.grid(row=row_cnt, column=0, sticky=N+S+W+E, \
                    padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_batch_nr.insert(INSERT, "Batch nr.: ")
                write_batch_nr.config(state=DISABLED, bd = 0, \
                    font=('calibri', '12', 'bold'))
                weight_cnt+=1
                write_batch = tk.Text(choose_batch_frame, width=20, height=1)
                write_batch.grid(row=row_cnt, column=1, sticky=N+S+W+E, \
                    padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_batch.insert(INSERT, words[2])
                write_batch.config(state=DISABLED, bd = 0, font=('calibri', '12'))
                weight_cnt+=1
                write_batch_date = tk.Text(choose_batch_frame, width=8, height=1)
                write_batch_date.grid(row=row_cnt, column=2, sticky=N+S+W+E, \
                    padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_batch_date.insert(INSERT, "Date: ")
                write_batch_date.config(state=DISABLED, bd = 0, \
                    font=('calibri', '12', 'bold'))
                weight_cnt+=1
                write_date = tk.Text(choose_batch_frame, width=30, height=1)
                write_date.grid(row=row_cnt, column=3, sticky=N+S+W+E, \
                    padx=(10,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                write_date.insert(INSERT, words[0] + ", " + words[1] + "")
                write_date.config(state=DISABLED, bd = 0, \
                    font=('calibri', '12'))
                weight_cnt+=1

                Radiobutton(choose_batch_frame, text='',bg='#ffffff', \
                    cursor='hand2',font=('calibri', '14'), \
                        variable=Globals.DVH_film_batch, value=batch_cnt).\
                            grid(row=row_cnt, column=4, sticky=N+S+W+E, \
                                padx=(5,5), pady=(10,10))
                choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
                choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)
                weight_cnt+=1;row_cnt+=1;batch_cnt+=1

            def set_batch():
                choose_batch_window.destroy()
                f = open('calibration.txt', 'r')
                lines = f.readlines()
                words = lines[Globals.DVH_film_batch.get()].split()
                Globals.DVH_popt_red[0] = float(words[3])
                Globals.DVH_popt_red[1] = float(words[4])
                Globals.DVH_popt_red[2] = float(words[5])
                f.close()

                Globals.DVH_film_dataset_ROI_red_channel_dose = \
                    np.zeros((Globals.DVH_film_dataset_ROI_red_channel.shape[0],\
                    Globals.DVH_film_dataset_ROI_red_channel.shape[1]))
                for i in range\
                    (Globals.DVH_film_dataset_ROI_red_channel_dose.shape[0]):
                    for j in range\
                        (Globals.DVH_film_dataset_ROI_red_channel_dose.shape[1]):
                        Globals.DVH_film_dataset_ROI_red_channel_dose[i,j] = \
                            Globals.DVH_film_factor*pixel_to_dose\
                                (Globals.DVH_film_dataset_ROI_red_channel[i,j], \
                                    Globals.DVH_popt_red[0], \
                                        Globals.DVH_popt_red[1], \
                                            Globals.DVH_popt_red[2])

                Globals.DVH_film_dataset_red_channel_dose = \
                    np.zeros((Globals.DVH_film_dataset_red_channel.shape[0],\
                    Globals.DVH_film_dataset_red_channel.shape[1]))
                for i in range\
                    (Globals.DVH_film_dataset_red_channel_dose.shape[0]):
                    for j in range\
                        (Globals.DVH_film_dataset_red_channel_dose.shape[1]):
                        Globals.DVH_film_dataset_red_channel_dose[i,j] = \
                            Globals.DVH_film_factor*pixel_to_dose\
                                (Globals.DVH_film_dataset_red_channel[i,j], \
                                    Globals.DVH_popt_red[0], \
                                        Globals.DVH_popt_red[1], \
                                            Globals.DVH_popt_red[2])


                mx_film=np.max(Globals.DVH_film_dataset_ROI_red_channel_dose)
                Globals.DVH_max_dose_film = mx_film
                
                new_window.destroy()

            set_batch_button_frame = tk.Frame(choose_batch_frame)
            set_batch_button_frame.grid(row=row_cnt, column=1, columnspan=3, \
                padx=(10,0), pady=(5,5))
            set_batch_button_frame.configure(bg='#ffffff')
            choose_batch_frame.grid_columnconfigure(weight_cnt, weight=0)
            choose_batch_frame.grid_rowconfigure(weight_cnt, weight=0)

            set_batch_button = tk.Button(set_batch_button_frame, text='OK', \
                image=Globals.done_button_image, cursor='hand2',\
                    font=('calibri', '14'), relief=FLAT, state=ACTIVE, \
                        command=set_batch)
            set_batch_button.pack(expand=True, fill=BOTH)
            set_batch_button.image=Globals.done_button_image
            

            img_ROI = Globals.DVH_film_dataset[Globals.DVH_ROI_coords[0][1]:\
                Globals.DVH_ROI_coords[2][1],Globals.DVH_ROI_coords[0][0]:\
                    Globals.DVH_ROI_coords[1][0], :]
            img_ROI_red_channel = img_ROI[:,:,2]
            Globals.DVH_film_variable_ROI_coords = \
                [Globals.DVH_ROI_coords[0][1], Globals.DVH_ROI_coords[2][1],\
                    Globals.DVH_ROI_coords[0][0], Globals.DVH_ROI_coords[1][0]]
            Globals.DVH_film_dataset_ROI = img_ROI
            Globals.DVH_film_dataset_ROI_red_channel = img_ROI_red_channel
            R = img_ROI[:,:,2];B = img_ROI[:,:,0]; G = img_ROI[:,:,1]
            img_ROI_RGB = np.zeros(img_ROI.shape)
            img_ROI_RGB[:,:,0]=R; img_ROI_RGB[:,:,1]=G; img_ROI_RGB[:,:,2]=B 


            Globals.DVH_upload_button_doseplan.config(state=DISABLED)
            Globals.DVH_upload_button_rtplan.config(state=ACTIVE)
            Globals.DVH_upload_button_film.config(state=DISABLED)

            if(ref_test):
                Globals.DVH_distance_reference_point_ROI.append\
                    ([(Globals.DVH_film_reference_point[0]-\
                        Globals.DVH_ROI_coords[0][0])*0.2, \
                        (Globals.DVH_film_reference_point[1] -\
                            Globals.DVH_ROI_coords[0][1])*0.2])
                Globals.DVH_distance_reference_point_ROI.append\
                    ([(Globals.DVH_film_reference_point[0] - \
                        Globals.DVH_ROI_coords[1][0])*0.2,\
                            (Globals.DVH_film_reference_point[1] - \
                                Globals.DVH_ROI_coords[1][1])*0.2])
                Globals.DVH_distance_reference_point_ROI.append\
                    ([(Globals.DVH_film_reference_point[0] - \
                        Globals.DVH_ROI_coords[2][0])*0.2,\
                            (Globals.DVH_film_reference_point[1] - \
                                Globals.DVH_ROI_coords[2][1])*0.2])
                Globals.DVH_distance_reference_point_ROI.append\
                    ([(Globals.DVH_film_reference_point[0] - \
                        Globals.DVH_ROI_coords[3][0])*0.2,\
                            (Globals.DVH_film_reference_point[1] - \
                                Globals.DVH_ROI_coords[3][1])*0.2])
                
                Globals.DVH_isocenter_or_reference_point = "Ref_point"
            else:
                Globals.DVH_distance_isocenter_ROI.append\
                    ([(Globals.DVH_film_isocenter[0]-\
                        Globals.DVH_ROI_coords[0][0])*0.2, \
                            (Globals.DVH_film_isocenter[1] -\
                                Globals.DVH_ROI_coords[0][1])*0.2])
                Globals.DVH_distance_isocenter_ROI.append\
                    ([(Globals.DVH_film_isocenter[0] - \
                        Globals.DVH_ROI_coords[1][0])*0.2,\
                            (Globals.DVH_film_isocenter[1] - \
                                Globals.DVH_ROI_coords[1][1])*0.2])
                Globals.DVH_distance_isocenter_ROI.append\
                    ([(Globals.DVH_film_isocenter[0] - \
                        Globals.DVH_ROI_coords[2][0])*0.2,\
                            (Globals.DVH_film_isocenter[1] - \
                                Globals.DVH_ROI_coords[2][1])*0.2])
                Globals.DVH_distance_isocenter_ROI.append\
                    ([(Globals.DVH_film_isocenter[0] - \
                        Globals.DVH_ROI_coords[3][0])*0.2,\
                            (Globals.DVH_film_isocenter[1] - \
                                Globals.DVH_ROI_coords[3][1])*0.2])

                Globals.DVH_isocenter_or_reference_point = "Isocenter"

            
        done_button_frame = tk.Frame(new_window_isocenter_tab)
        done_button_frame.grid(row=10, column=3, padx=(10,10), \
            pady=(5,5), sticky=N+S+W+E)
        done_button_frame.configure(bg='#ffffff')
        new_window_isocenter_tab.grid_columnconfigure(5, weight=0)
        new_window_isocenter_tab.grid_rowconfigure(5, weight=0)

        Globals.DVH_done_button = tk.Button(done_button_frame, text='Done', \
            image=Globals.done_button_image,cursor='hand2', font=('calibri', '14'),\
                relief=FLAT, state=DISABLED, command=lambda: \
                    finishFilmMarkers(False))
        Globals.DVH_done_button.pack(expand=True, fill=BOTH)
        Globals.DVH_done_button.config(bg='#ffffff', activebackground='#ffffff', \
            activeforeground='#ffffff', highlightthickness=0)
        Globals.DVH_done_button.image=Globals.done_button_image

        done_button_reference_point_frame = \
            tk.Frame(new_window_reference_point_tab)
        done_button_reference_point_frame.grid(row=10, column=3, \
            padx=(10,10), pady=(5,5), sticky=N+S+W+E)
        done_button_reference_point_frame.configure(bg='#ffffff')
        new_window_reference_point_tab.grid_columnconfigure(5, weight=0)
        new_window_reference_point_tab.grid_rowconfigure(5, weight=0)

        Globals.DVH_done_button_reference_point= \
            tk.Button(done_button_reference_point_frame, text='Done', \
                image=Globals.done_button_image,cursor='hand2', \
                    font=('calibri', '14'), relief=FLAT, state=DISABLED, \
                        command=lambda: finishFilmMarkers(True))
        Globals.DVH_done_button_reference_point.pack(expand=True, fill=BOTH)
        Globals.DVH_done_button_reference_point.config(bg='#ffffff', \
            activebackground='#ffffff', activeforeground='#ffffff', \
                highlightthickness=0)
        Globals.DVH_done_button_reference_point.image=Globals.done_button_image


    elif(ext==""):
        return 
    else:
        messagebox.showerror("Error", "The file must be a *.tif file")


def help_showPlanes():
    new_window = tk.Toplevel(Globals.tab5)
    w = Globals.profiles_showPlanes_image.width()
    h = Globals.profiles_showPlanes_image.height()
    new_window.geometry("%dx%d+0+0" % (w, h))
    new_window.grab_set()

    canvas = tk.Canvas(new_window)
    canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    canvas.create_image(0, 0, image=Globals.profiles_showPlanes_image, anchor='nw')
    canvas.pack(expand=True, fill=BOTH)