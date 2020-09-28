#-----------------------------------------------------------------------------------
#
# Version 16.08.20
# 
# Fuctions used in relation to the tab Dose Response
#-----------------------------------------------------------------------------------

import Globals
import tkinter as tk
import tkinter.ttk 
from tkinter import filedialog, INSERT, DISABLED, messagebox, NORMAL, simpledialog, \
    PhotoImage, BOTH, Toplevel, GROOVE, ACTIVE, FLAT, N, S, W, E, ALL, ttk, LEFT, \
        RIGHT, Y, Label, X, END, Button, StringVar, Scrollbar
import cv2
import numpy as np
import os
from os.path import normpath, basename
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.optimize import curve_fit
from scipy.optimize import curve_fit, OptimizeWarning
from PIL import Image, ImageTk
import sys
from datetime import datetime
import re
import warnings
warnings.filterwarnings("error")

def nothingButton():
#--------------------------------------------------
# Function to only return
# Is used in cases where nothing should happen in
# a active button (they will later be reconfigured)
#--------------------------------------------------
    return



def saveCalibration():
#--------------------------------------------------
# Function to save the calibration performed
#
# This is a callback function for the button
# dose_response_save_calibration_button in
# notebook.py
#--------------------------------------------------
    ask_batch_window = tk.Toplevel(Globals.tab2)
    ask_batch_window.geometry("400x180")
    ask_batch_window.grab_set()
    ask_batch_window_canvas = tk.Canvas(ask_batch_window)
    ask_batch_window_canvas.config(bg='#ffffff', bd=0, highlightthickness=0)
    ask_batch_window_canvas.pack(expand=True, fill=BOTH)

    batch_info = tk.Text(ask_batch_window_canvas, width=50, height=3)
    batch_info.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W, \
        padx=(10,10), pady=(30,10))
    ask_batch_window_canvas.grid_columnconfigure(0, weight=0)
    ask_batch_window_canvas.grid_rowconfigure(0, weight=0)
    batch_info.insert(INSERT, 'Write the LOT number of current GafChromic film:\n\
        (Defaults to -)')
    batch_info.config(state=DISABLED, bd = 0, font=('calibri', '12'))

    batch = tk.Text(ask_batch_window_canvas, width=20, height=1)
    batch.grid(row=1, column=0, sticky=N+S+W+E, padx=(5,5), pady=(10,10))
    ask_batch_window_canvas.grid_columnconfigure(1, weight=0)
    ask_batch_window_canvas.grid_rowconfigure(1, weight=0)
    batch.insert(INSERT, " ")
    batch.config(state=NORMAL, bd = 3, font=('calibri', '12'))

    def save_batch():
    #--------------------------------------------------
    # Function to read the earlier saved calibration-file
    #
    # This is a callback function for the button
    # save_batch_button in function save_calibration
    #--------------------------------------------------
        Globals.dose_response_batch_number= batch.get("1.0",'end-1c')
        if(Globals.dose_response_batch_number == " "):
            Globals.dose_response_batch_number = "-"
            save_batch_button.config(state=DISABLED)
            ask_batch_window.destroy()
        elif(re.match("^[A-Za-z0-9_]*$", \
            (Globals.dose_response_batch_number).lstrip())==None):
            messagebox.showerror("Error","LOT number can only contain letters and/or numbers")
            ask_batch_window.destroy()
            saveCalibration()
            return
        else:
            save_batch_button.config(state=DISABLED)
            ask_batch_window.destroy()

        f = open('calibration.txt', 'r')
        lines = f.readlines()
        f.close()
        string_to_file = str(datetime.now()) + " " + \
            str(Globals.dose_response_batch_number) + " " + \
            str(Globals.popt_red[0]) + " " + str(Globals.popt_red[1]) \
                + " " + str(Globals.popt_red[2]) + "\n"
        if(len(lines) < 5):
            f = open('calibration.txt', 'a')
            f.write(string_to_file)
            f.close()
        else:
            new_lines = [lines[1], lines[2], lines[3], lines[4], string_to_file]
            f = open('calibration.txt', 'w')
            for i in range(len(new_lines)):
                f.write(new_lines[i])
            f.close()

        messagebox.showinfo("Info", "The calibration has been saved")

    save_button_frame = tk.Frame(ask_batch_window_canvas)
    save_button_frame.grid(row=1, column = 1, padx=(5,5), pady=(10,10))
    ask_batch_window_canvas.grid_columnconfigure(2, weight=0)
    ask_batch_window_canvas.grid_rowconfigure(2, weight=0)
    save_button_frame.config(bg = '#ffffff')

    save_batch_button = tk.Button(save_button_frame, text='Save', \
        image=Globals.save_button, cursor='hand2',font=('calibri', '14'),\
            relief=FLAT, state=ACTIVE, command=save_batch)
    save_batch_button.pack(fill=BOTH, expand=True)
    save_batch_button.image = Globals.save_button


def UploadAction(new_window, event=None):
#--------------------------------------------------
# Function upload scanned film files.
#
# This is a callback function for the button
# upload_button in the function create_window()
#--------------------------------------------------
    file = filedialog.askopenfilename()
    ext = os.path.splitext(file)[-1].lower()
    if(ext==".tif"):
        Globals.dose_response_uploaded_filenames = \
            np.append(Globals.dose_response_uploaded_filenames, file)
        uploaded_filename = tk.Text(new_window, height=1, width=1)
        uploaded_filename.grid(row=Globals.dose_response_new_window_row_count, \
            column=0, columnspan=2, sticky=E+W, pady=(5,5), padx=(100,0))
        new_window.grid_columnconfigure\
            (Globals.dose_response_new_window_weight_count, weight=0)
        new_window.grid_rowconfigure\
            (Globals.dose_response_new_window_weight_count, weight=0)
        uploaded_filename.insert(INSERT, basename(normpath(file))) 
        uploaded_filename.config(state=DISABLED, bd=0, \
            font=('calibri', '12'), fg='gray')
        Globals.dose_response_new_window_row_count+=1
        Globals.dose_response_new_window_weight_count+=1
    elif(ext==""):
        return 
    else:
        messagebox.showerror("Error", "The file must be a .tif file")

def readImage(filename):
    image = cv2.imread(filename, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if(image is None):
        current_folder = os.getcwd()
        parent = os.path.dirname(filename)
        os.chdir(parent)
        image=cv2.imread(basename(normpath(filename)), \
            cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        os.chdir(current_folder)
    if(image is None):
         messagebox.showerror("Error", \
             "Something has happen. Check that the filename does not contain Æ,Ø,Å")
         return
    
    if(image.shape[2] == 3):
        if(image.shape[0]==1270 and image.shape[1]==1016):
            Globals.doseResponse_dpi.set("127")
            image = abs(image-Globals.correctionMatrix127)
            image = np.clip(image, 0, 65535)
        elif(image.shape[0]==720 and image.shape[1]==576):
            Globals.doseResponse_dpi.set("72")
            image = abs(image - Globals.correctionMatrix72)
            image = np.clip(image, 0, 65535)
        else:
            messagebox.showerror("Error",\
                "The resolution of the image is not consistent with dpi")

    else:
        messagebox.showerror("Error","The uploaded image need to be in RGB-format")

    sum_red=0;sum_green=0;sum_blue=0
    if(Globals.doseResponse_dpi.get() == "127"):        
        for i in range(622,647):
            for j in range(495, 520):
                sum_red += image[i,j,2]
                sum_green += image[i,j,1]
                sum_blue += image[i,j,0]
        sum_red = sum_red/(25*25)
        sum_green = sum_green/(25*25)
        sum_blue = sum_blue/(25*25)
        return sum_red, sum_green, sum_blue
    elif(Globals.doseResponse_dpi.get() == "72"):
        for i in range(352,367):
            for j in range(280,295):
                sum_red+=image[i,j,2]
                sum_green+=image[i,j,1]
                sum_blue+=image[i,j,0]
        sum_red = sum_red/(15*15)
        sum_green = sum_green/(15*15)
        sum_blue = sum_blue/(15*15)
        return sum_red, sum_green, sum_blue
    else:
        messagebox.showerror("Error", \
            "Something has gone wrong with the doseResponse_dpi")
        return False


def plot_dose_response():
#--------------------------------------------------
# Function to plot the dose response curve
#
# The function is called on in delete_lines(),
# avgAllFiles() and clear_all().
#--------------------------------------------------
    sd_red_arr=[];sd_green_arr=[];sd_blue_arr=[]
    temp_dose = [item[0] for item in Globals.avg_red_vector]
    temp_avg_red = [item[1] for item in Globals.avg_red_vector]
    temp_avg_green = [item[1] for item in Globals.avg_green_vector]
    temp_avg_blue = [item[1] for item in Globals.avg_blue_vector]
    
    for i in range(len(temp_dose)):
        sd_red_arr.append(np.std(Globals.dose_response_sd_list_red[i]))
        sd_green_arr.append(np.std(Globals.dose_response_sd_list_green[i]))
        sd_blue_arr.append(np.std(Globals.dose_response_sd_list_blue[i]))
    
    if(len(sd_red_arr) > 0):
        Globals.dose_response_sd_avg_red.set(sum(sd_red_arr)/len(sd_red_arr))
        Globals.dose_response_sd_avg_green.set(sum(sd_green_arr)/len(sd_green_arr))
        Globals.dose_response_sd_avg_blue.set(sum(sd_blue_arr)/len(sd_blue_arr))

        Globals.dose_response_sd_max_red.set(max(sd_red_arr))
        Globals.dose_response_sd_max_red_dose.set(str(temp_dose[sd_red_arr.index\
            (Globals.dose_response_sd_max_red.get())]))
        Globals.dose_response_sd_max_green.set(max(sd_green_arr))
        Globals.dose_response_sd_max_green_dose.set(str(temp_dose[sd_green_arr.index\
            (Globals.dose_response_sd_max_green.get())]))
        Globals.dose_response_sd_max_blue.set(max(sd_blue_arr))
        Globals.dose_response_sd_max_blue_dose.set(str(temp_dose[sd_blue_arr.index\
            (Globals.dose_response_sd_max_blue.get())]))

        Globals.dose_response_sd_min_red.set(min(sd_red_arr))
        Globals.dose_response_sd_min_red_dose.set(str(temp_dose[sd_red_arr.index\
            (Globals.dose_response_sd_min_red.get())]))
        Globals.dose_response_sd_min_green.set(min(sd_green_arr))
        Globals.dose_response_sd_min_green_dose.set(str(temp_dose[sd_green_arr.index\
            (Globals.dose_response_sd_min_green.get())]))
        Globals.dose_response_sd_min_blue.set(min(sd_blue_arr))
        Globals.dose_response_sd_min_blue_dose.set(str(temp_dose[sd_blue_arr.index\
            (Globals.dose_response_sd_min_blue.get())]))

    else:
        Globals.dose_response_sd_avg_red.set(0)
        Globals.dose_response_sd_avg_green.set(0)
        Globals.dose_response_sd_avg_blue.set(0)
        Globals.dose_response_sd_max_red.set(0)
        Globals.dose_response_sd_max_red_dose.set('-')
        Globals.dose_response_sd_max_green.set(0)
        Globals.dose_response_sd_max_green_dose.set('-')
        Globals.dose_response_sd_max_blue.set(0)
        Globals.dose_response_sd_max_blue_dose.set('-')
        Globals.dose_response_sd_min_red.set(0)
        Globals.dose_response_sd_min_red_dose.set('-')
        Globals.dose_response_sd_min_green.set(0)
        Globals.dose_response_sd_min_green_dose.set('-')
        Globals.dose_response_sd_min_blue.set(0)
        Globals.dose_response_sd_min_blue_dose.set('-')

    for widget in Globals.dose_response_plot_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6,4))
    a = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=Globals.dose_response_plot_frame)
    canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+S+E+W,\
         padx=(25,0), pady=(0,0))
    if(Globals.dose_response_var1.get()):
        a.errorbar(temp_dose,temp_avg_red,yerr=sd_red_arr, fmt='ro')
    if(Globals.dose_response_var2.get()):
        a.errorbar(temp_dose, temp_avg_green, yerr=sd_green_arr, fmt='g^')
    if(Globals.dose_response_var3.get()):
        a.errorbar(temp_dose, temp_avg_blue, yerr=sd_blue_arr, fmt='bs')
    
    if(len(temp_avg_red) > 3):
        sorted_temp_red = sorted(Globals.avg_red_vector,key=lambda l:l[0])
        sorted_temp_avg_red = [item[1] for item in sorted_temp_red]
        sorted_temp_dose = [item[0] for item in sorted_temp_red]

        sorted_temp_green = sorted(Globals.avg_green_vector, key=lambda l:l[0])
        sorted_temp_avg_green = [item[1] for item in sorted_temp_green]
    
        sorted_temp_blue = sorted(Globals.avg_blue_vector, key=lambda l:l[0])
        sorted_temp_avg_blue = [item[1] for item in sorted_temp_blue]

        try:
            Globals.popt_red, Globals.pcov_red = curve_fit(fitted_dose_response, \
                sorted_temp_dose, sorted_temp_avg_red, \
                    p0=[1700, 15172069, -390], maxfev=10000)
            popt_green, pcov_green = curve_fit(fitted_dose_response, \
                sorted_temp_dose, sorted_temp_avg_green, \
                    p0=[1700, 15172069, -390], maxfev=10000)
            
            try:
                Globals.dose_response_equation_image.destroy()
            except:
                nothingButton()
            perr = np.sqrt(np.diag(Globals.pcov_red))
            perr_prosent = np.array([perr[0]/Globals.popt_red[0], \
                perr[1]/Globals.popt_red[1], perr[2]/Globals.popt_red[2]])*100
            fitting_uncertainty = np.sqrt(perr_prosent[0]**2 + \
                perr_prosent[1]**2 + perr_prosent[2]**2)
            xdata = np.linspace(0,2000,1001)
            ydata_red = np.zeros(len(xdata));ydata_green=np.zeros(len(xdata))
            for i in range(len(xdata)):
                ydata_red[i] = fitted_dose_response(xdata[i], Globals.popt_red[0], \
                    Globals.popt_red[1], Globals.popt_red[2])
                ydata_green[i] = fitted_dose_response(xdata[i], popt_green[0], \
                    popt_green[1], popt_green[2])
            if(Globals.dose_response_var1.get()):
                a.plot(xdata, ydata_red, color='red')
            if(Globals.dose_response_var2.get()):
                a.plot(xdata, ydata_green, color='green')
            if(Globals.dose_response_var3.get()):
                a.plot(sorted_temp_dose, sorted_temp_avg_blue , color='blue')

            a.set_title("Dose-response", fontsize=12)
            a.set_ylabel("Pixel value", fontsize=12)
            a.set_xlabel("Dose", fontsize=12)
            fig.tight_layout()

            out_text_function = "Pixel value = " + str(round(Globals.popt_red[0])) \
                + " + " + str(round(Globals.popt_red[1])) + "/(dose - (" \
                    + str(round(Globals.popt_red[2])) + "))"
            standardavvik_rgb = "Standard deviation red = " + \
                str(round(Globals.dose_response_sd_avg_red.get()))
            fitting_inc = str(round(fitting_uncertainty))
            def drawEquation(a,b,c):
                tmptext = StringVar()
                if c < 0:
                    c = abs(c)
                    a=str(a);b=str(b);c=str(c)
                    latex= a   + "+ " "\\frac {" + f"{b}" + "}{"+ "D" + "+" \
                        + f"{c}" + "}"
                else:
                    a=str(a);b=str(b);c=str(c)
                    latex= a   + "+ " "\\frac {" + f"{b}" + "}{"+ "D" + "-" \
                        + f"{c}" + "}"
                
                tmptext.set(latex)
                tmptext = "$"+tmptext.get()+"$"
                
                axLatex.clear()
                axLatex.text(0.01,0.5, "PV = "+tmptext, fontsize = 6)
                canvasLatex.draw()

            labelLatex = Label(Globals.dose_response_equation_frame)
            labelLatex.grid(row=0,column=0, rowspan=15, sticky=N+W)
            labelLatex.config(bg='#ffffff', bd=0, highlightthickness=0)
            

            figLatex = matplotlib.figure.Figure(figsize=(1.2, 1), dpi=250)
            figLatex.subplots_adjust(bottom=-0.01, top=1.2, left=-0.01, right=2)
            axLatex = figLatex.add_subplot(111)

            canvasLatex = FigureCanvasTkAgg(figLatex, master=labelLatex)
            canvasLatex.get_tk_widget().grid(row=0, column=0, sticky="N")
            canvasLatex._tkcanvas.grid(row=0, column=0,sticky="N") 

            axLatex.get_xaxis().set_visible(False)
            axLatex.get_yaxis().set_visible(False)

            a_=round(Globals.popt_red[0])
            b_=round(Globals.popt_red[1])
            c_=round(Globals.popt_red[2])
            drawEquation(a_,b_,c_)
 

            def drawSD(sd_text,sd_text_1,sd_text_2,sd_text_3,sd_text_4,sd_text_5,\
                sd_text_6,sd_text_7,sd_text_8,sd_text_9,sd_text_10,sd_text_11,\
                sd_text_12,sd_text_13,sd_text_14,sd_text_15,sd_text_16,sd_text_17):
                
                text = "Standard deviations (SD): "
                sd_text.config(state=NORMAL)
                sd_text.insert(INSERT, text)
                sd_text.config(state=DISABLED)

                sd_text_1.config(state=NORMAL)
                sd_text_1.insert(INSERT, " ")
                sd_text_1.config(state=DISABLED)

                sd_text_2.config(state=NORMAL)
                sd_text_2.insert(INSERT, "Average")
                sd_text_2.config(state=DISABLED)

                sd_text_3.config(state=NORMAL)
                sd_text_3.insert(INSERT, "Minimum")
                sd_text_3.config(state=DISABLED)

                sd_text_4.config(state=NORMAL)
                sd_text_4.insert(INSERT, "Maximum")
                sd_text_4.config(state=DISABLED)

                sd_text_5.config(state=NORMAL)
                sd_text_5.insert(INSERT, "Red:")
                sd_text_5.config(state=DISABLED)

                avgR=str(round(Globals.dose_response_sd_avg_red.get()))
                sd_text_6.config(state=NORMAL)
                sd_text_6.insert(INSERT, avgR)
                sd_text_6.config(state=DISABLED)

                minR=str(round(Globals.dose_response_sd_min_red.get()))
                sd_text_7.config(state=NORMAL)
                sd_text_7.insert(INSERT, minR)
                sd_text_7.config(state=DISABLED)

                maxR=str(round(Globals.dose_response_sd_max_red.get()))
                sd_text_8.config(state=NORMAL)
                sd_text_8.insert(INSERT, maxR)
                sd_text_8.config(state=DISABLED)

                sd_text_9.config(state=NORMAL)
                sd_text_9.insert(INSERT, "Green:")
                sd_text_9.config(state=DISABLED)

                avgG=str(round(Globals.dose_response_sd_avg_green.get()))
                sd_text_10.config(state=NORMAL)
                sd_text_10.insert(INSERT, avgG)
                sd_text_10.config(state=DISABLED)
                
                minG=str(round(Globals.dose_response_sd_min_green.get()))
                sd_text_11.config(state=NORMAL)
                sd_text_11.insert(INSERT, minG)
                sd_text_11.config(state=DISABLED)

                maxG=str(round(Globals.dose_response_sd_max_green.get()))
                sd_text_12.config(state=NORMAL)
                sd_text_12.insert(INSERT, maxG)
                sd_text_12.config(state=DISABLED)

                sd_text_13.config(state=NORMAL)
                sd_text_13.insert(INSERT, "Blue:")
                sd_text_13.config(state=DISABLED)

                avgB=str(round(Globals.dose_response_sd_avg_blue.get()))
                sd_text_14.config(state=NORMAL)
                sd_text_14.insert(INSERT, avgB)
                sd_text_14.config(state=DISABLED)

                minB=str(round(Globals.dose_response_sd_min_blue.get()))
                sd_text_15.config(state=NORMAL)
                sd_text_15.insert(INSERT, minB)
                sd_text_15.config(state=DISABLED)

                maxB=str(round(Globals.dose_response_sd_max_blue.get()))
                sd_text_16.config(state=NORMAL)
                sd_text_16.insert(INSERT, maxB)
                sd_text_16.config(state=DISABLED)

                latex_fitting="Fitting uncertainty of the plot: " + fitting_inc
                out = str(latex_fitting)
                sd_text_17.config(state=NORMAL)
                sd_text_17.insert(INSERT, out)
                sd_text_17.config(state=DISABLED)

            sd_text = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=40)
            sd_text.grid(row=0, column=1, columnspan=4, sticky=N+S+W+E)
            sd_text.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_1 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=4)
            sd_text_1.grid(row=1, column=1, sticky=N+S+W+E)
            sd_text_1.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_2 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_2.grid(row=1, column=2, sticky=N+S+W+E)
            sd_text_2.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_3 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_3.grid(row=1, column=3, sticky=N+S+W+E)
            sd_text_3.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_4 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_4.grid(row=1, column=4, sticky=N+S+W+E)
            sd_text_4.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_5 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=4)
            sd_text_5.grid(row=2, column=1, sticky=N+S+W+E)
            sd_text_5.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_6 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_6.grid(row=2, column=2, sticky=N+S+W+E)
            sd_text_6.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_7 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_7.grid(row=2, column=3, sticky=N+S+W+E)
            sd_text_7.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_8 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_8.grid(row=2, column=4, sticky=N+S+W+E)
            sd_text_8.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_9 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=4)
            sd_text_9.grid(row=3, column=1, sticky=N+S+W+E)
            sd_text_9.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_10 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_10.grid(row=3, column=2, sticky=N+S+W+E)
            sd_text_10.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_11 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_11.grid(row=3, column=3, sticky=N+S+W+E)
            sd_text_11.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_12 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_12.grid(row=3, column=4, sticky=N+S+W+E)
            sd_text_12.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_13 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=4)
            sd_text_13.grid(row=4, column=1, sticky=N+S+W+E)
            sd_text_13.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_14 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_14.grid(row=4, column=2, sticky=N+S+W+E)
            sd_text_14.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_15 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_15.grid(row=4, column=3, sticky=N+S+W+E)
            sd_text_15.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_16 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=1)
            sd_text_16.grid(row=4, column=4, sticky=N+S+W+E)
            sd_text_16.config(state=DISABLED, bd=0, font=('calibri', '12'))
            sd_text_17 = tk.Text(Globals.dose_response_equation_frame, \
                height=1, width=40)
            sd_text_17.grid(row=5, column=1, columnspan=4, sticky=N+S+W+E)
            sd_text_17.config(state=DISABLED, bd=0, font=('calibri', '12'))
            drawSD(sd_text,sd_text_1,sd_text_2,sd_text_3,sd_text_4,sd_text_5,\
                sd_text_6,sd_text_7,sd_text_8,sd_text_9,sd_text_10,sd_text_11,\
                sd_text_12,sd_text_13,sd_text_14,sd_text_15,sd_text_16,sd_text_17)

            Globals.dose_response_save_calibration_button.config(state=ACTIVE)   
        except OptimizeWarning:
            messagebox.showwarning("Warning", \
"It appears that you have optimization problems. \
Try adding more data points to improve the optimization.\
 Or, check that your specified dose matches your uploaded files.")
        except RuntimeError:
            messagebox.showwarning("Warning", \
"It appears that you have optimization problems. \
Try adding more data points to improve the optimization. \
Or, check that your specified dose matches your uploaded files.")

    a.set_title("Dose-response", fontsize=12)
    a.set_ylabel("Pixel value", fontsize=12)
    a.set_xlabel("Dose", fontsize=12)
    fig.tight_layout()


def delete_line(delete_button):
#--------------------------------------------------
# Function to delete a measurement
#
# The function is a callback funtion to the 
# button delete_button defined in function
# avgAllFiles()
#--------------------------------------------------
    button_index = Globals.dose_response_delete_buttons.index(delete_button)
    Globals.dose_response_red_list[button_index].destroy()
    Globals.dose_response_green_list[button_index].destroy()
    Globals.dose_response_blue_list[button_index].destroy()
    Globals.dose_response_dose_list[button_index].destroy()
    Globals.dose_response_delete_buttons[button_index].destroy()
    del(Globals.dose_response_red_list[button_index])
    del(Globals.dose_response_green_list[button_index])
    del(Globals.dose_response_blue_list[button_index])
    del(Globals.dose_response_dose_list[button_index])
    
    if(len(Globals.dose_response_delete_buttons) > 1):
        del(Globals.avg_red_vector[button_index])
        del(Globals.avg_green_vector[button_index])
        del(Globals.avg_blue_vector[button_index])
        del(Globals.dose_response_delete_buttons[button_index])
        del(Globals.dose_response_sd_list_red[button_index])
        del(Globals.dose_response_sd_list_green[button_index])
        del(Globals.dose_response_sd_list_blue[button_index])
    else:
        Globals.avg_red_vector = []
        Globals.avg_green_vector = []
        Globals.avg_blue_vector = []
        Globals.dose_response_delete_buttons = []
        Globals.dose_response_sd_list_red = []
        Globals.dose_response_sd_list_green = []
        Globals.dose_response_sd_list_blue = []
    
    Globals.dose_response_files_row_count = 2
    for i in range(len(Globals.dose_response_delete_buttons)):
        Globals.dose_response_red_list[i].grid\
            (row=Globals.dose_response_files_row_count, column=1, \
                sticky=N+S+W+E, padx=(0,0))
        Globals.dose_response_green_list[i].grid\
            (row=Globals.dose_response_files_row_count, column=3, \
                sticky=N+S+W+E, padx=(0,0))
        Globals.dose_response_blue_list[i].grid\
            (row=Globals.dose_response_files_row_count, column=5, \
                sticky=N+S+W+E, padx=(0,5))
        Globals.dose_response_dose_list[i].grid\
            (row=Globals.dose_response_files_row_count, column=0, \
                sticky=N+S+W+E, padx=(0,15))
        Globals.dose_response_delete_buttons[i].grid\
            (row=Globals.dose_response_files_row_count, column=7, \
                sticky=N+S+W+E, padx=(5,5))
        Globals.dose_response_files_row_count+=1
    
    if(len(Globals.dose_response_delete_buttons) < 4):
        Globals.dose_response_save_calibration_button.config(state=DISABLED)

    plot_dose_response()

def fitted_dose_response(D, a, b, c):
#--------------------------------------------------
# Function to map between pixel value and dose
#
# The function is a called in the funtion
# plot_dose_response()
#--------------------------------------------------
    return a + b/(D-c)


def avgAllFiles(write_dose_box, new_window):
#--------------------------------------------------
# Function to find the mean of uploaded 
# images with same dose.
#
# The function is a callback function for 
# the button done_button in create_window()
#--------------------------------------------------
    dose_input = write_dose_box.get("1.0",'end-1c')
    if (dose_input == " "):
        messagebox.showerror("Error", "Input dose")
        return
    try:
        dose_input = float(dose_input)
    except:
        messagebox.showerror("Error","The dose must be a number")
        return
    if(len(Globals.dose_response_uploaded_filenames) == 0):
        messagebox.showerror("Error", "No files uploaded")
        return

    try:
        Globals.upload_files_here_canvas.destroy()
    except:
        nothingButton()

    avg_red=0;avg_green=0;avg_blue=0
    red_temp_sd_list = []; green_temp_sd_list = []; blue_temp_sd_list = []
    for i in range(0, len(Globals.dose_response_uploaded_filenames)):
        if(readImage(Globals.dose_response_uploaded_filenames[i])==False):
            messagebox.showerror("Error", "A mistake has happend in readImage()")
            return
        red, green, blue = readImage(Globals.dose_response_uploaded_filenames[i])
        avg_red+=red
        avg_green+=green
        avg_blue+=blue

        red_temp_sd_list.append(red)
        green_temp_sd_list.append(green)
        blue_temp_sd_list.append(blue)


    avg_red = avg_red/len(Globals.dose_response_uploaded_filenames)
    avg_green = avg_green/len(Globals.dose_response_uploaded_filenames)
    avg_blue = avg_blue/len(Globals.dose_response_uploaded_filenames)
    temp_dose = [item[0] for item in Globals.avg_red_vector]
    isTest = False
    try:
        indx = temp_dose.index(dose_input)
        Globals.avg_red_vector[indx][1] = (avg_red + \
            Globals.avg_red_vector[indx][1])/2
        Globals.avg_green_vector[indx][1] = (avg_green + \
            Globals.avg_green_vector[indx][1])/2
        Globals.avg_blue_vector[indx][1] = (avg_blue + \
            Globals.avg_blue_vector[indx][1])/2

        for i in range(0, len(red_temp_sd_list)):
            Globals.dose_response_sd_list_red[indx].append(red_temp_sd_list[i])
            Globals.dose_response_sd_list_green[indx].append(green_temp_sd_list[i])
            Globals.dose_response_sd_list_blue[indx].append(blue_temp_sd_list[i])

    except:
        Globals.avg_red_vector.append([dose_input, avg_red])
        Globals.avg_green_vector.append([dose_input, avg_green])
        Globals.avg_blue_vector.append([dose_input, avg_blue])

        Globals.dose_response_sd_list_red.append(red_temp_sd_list)
        Globals.dose_response_sd_list_green.append(green_temp_sd_list)
        Globals.dose_response_sd_list_blue.append(blue_temp_sd_list)

        isTest = True

    temp_dose = [item[0] for item in Globals.avg_red_vector]

    if(isTest):
        result_red = tk.Text(Globals.tab2_canvas_files, height=1, width=7)
        result_red.insert(INSERT, round(avg_red))
        result_red.grid(row=Globals.dose_response_files_row_count, column=1, \
            sticky=N+S+W+E, padx=(0,0))
        Globals.tab2_canvas_files.grid_columnconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        Globals.tab2_canvas_files.grid_rowconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        result_red.config(state=DISABLED, bd=0, font=('calibri', '12'))
        Globals.dose_response_red_list.append(result_red)
        Globals.dose_response_files_weightcount+=1

        result_green = tk.Text(Globals.tab2_canvas_files, height=1, width=7)
        result_green.insert(INSERT, round(avg_green))
        result_green.grid(row=Globals.dose_response_files_row_count, column=3, \
            sticky=N+S+W+E, padx=(0,0))
        Globals.tab2_canvas_files.grid_columnconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        Globals.tab2_canvas_files.grid_rowconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        result_green.config(state=DISABLED, bd=0, font=('calibri', '12'))
        Globals.dose_response_green_list.append(result_green)
        Globals.dose_response_files_weightcount+=1

        result_blue = tk.Text(Globals.tab2_canvas_files, height=1, width=7)
        result_blue.insert(INSERT, round(avg_blue))
        result_blue.grid(row=Globals.dose_response_files_row_count, column=5, \
            sticky=N+S+W+E, padx=(0,5))
        Globals.tab2_canvas_files.grid_columnconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        Globals.tab2_canvas_files.grid_rowconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        result_blue.config(state=DISABLED, bd=0, font=('calibri', '12'))
        Globals.dose_response_blue_list.append(result_blue)
        Globals.dose_response_files_weightcount+=1

        dose_print = tk.Text(Globals.tab2_canvas_files, height=1, width=10)
        dose_print.insert(INSERT, dose_input)
        dose_print.grid(row=Globals.dose_response_files_row_count, column=0, \
            sticky=N+S+W+E, padx=(0,15))
        Globals.tab2_canvas_files.grid_columnconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        Globals.tab2_canvas_files.grid_rowconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        dose_print.config(state=DISABLED, bd=0, font=('calibri', '12'))
        Globals.dose_response_dose_list.append(dose_print)
        Globals.dose_response_files_weightcount+=1

        path = os.path.dirname(sys.argv[0])
        path = path + r"\delete.png"
        img = ImageTk.PhotoImage(file=path)

        delete_button = tk.Button(Globals.tab2_canvas_files, text='Remove', \
            image=img, cursor='hand2',font=('calibri', '18'),\
                highlightthickness= 0, relief=FLAT, state=ACTIVE, width = 15)
        delete_button.image = img
        Globals.dose_response_delete_buttons.append(delete_button)
        delete_button.config(command=lambda: delete_line(delete_button))
        delete_button.grid(row=Globals.dose_response_files_row_count, column=7, \
            sticky=N+S+W+E, padx=(5,5))
        Globals.tab2_canvas_files.grid_columnconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        Globals.tab2_canvas_files.grid_rowconfigure\
            (Globals.dose_response_files_weightcount, weight=0)
        delete_button.config(bg='#ffffff', activebackground='#ffffff', \
            activeforeground='#ffffff', highlightthickness=0)
        Globals.dose_response_files_row_count+=1
        Globals.dose_response_files_weightcount+=1

    else:
        Globals.dose_response_red_list[indx].config(state=NORMAL)
        Globals.dose_response_red_list[indx].delete('1.0', END)
        Globals.dose_response_red_list[indx].insert(INSERT, \
            round(Globals.avg_red_vector[indx][1]))
        Globals.dose_response_red_list[indx].config(state=DISABLED)

        Globals.dose_response_green_list[indx].config(state=NORMAL)
        Globals.dose_response_green_list[indx].delete('1.0', END)
        Globals.dose_response_green_list[indx].insert(INSERT, \
            round(Globals.avg_green_vector[indx][1]))
        Globals.dose_response_green_list[indx].config(state=DISABLED)

        Globals.dose_response_blue_list[indx].config(state=NORMAL)
        Globals.dose_response_blue_list[indx].delete('1.0', END)
        Globals.dose_response_blue_list[indx].insert(INSERT, \
            round(Globals.avg_blue_vector[indx][1]))
        Globals.dose_response_blue_list[indx].config(state=DISABLED)

    plot_dose_response()
    new_window.destroy()

def create_window():
#--------------------------------------------------
# Function to create the window where the user
# upload the files of scanned film
#
# The function is a callback function for 
# the button dose_response_upload_button
# in notebook.py
#--------------------------------------------------
    new_window = tk.Toplevel(Globals.tab2)
    new_window.geometry("360x500")
    new_window.grab_set()
    
    new_window_frame = tk.Frame(new_window)
    new_window_frame.config(relief=FLAT, bg='#ffffff', highlightthickness=0)

    new_window_scroll_canvas = tk.Canvas(new_window_frame)
    new_window_scroll_canvas.config(bg='#ffffff', height=450, \
        width=200,highlightthickness=0, relief=FLAT)
    new_window_scroll_canvas.grid_propagate(0)

    new_window_scroll = Scrollbar(new_window_frame, \
        command=new_window_scroll_canvas.yview)

    scrollable_frame= tk.Frame(new_window_scroll_canvas)
    scrollable_frame.config(highlightthickness=0, relief=FLAT)

    scrollable_frame.bind("<Configure>", lambda e: \
        new_window_scroll_canvas.configure\
            (scrollregion=new_window_scroll_canvas.bbox('all')))
    new_window_scroll_canvas.create_window\
        ((0,0), window=scrollable_frame, anchor='nw')
    new_window_scroll_canvas.configure(yscrollcommand=new_window_scroll.set)

    new_window_canvas = tk.Canvas(scrollable_frame)
    new_window_canvas.config(relief=FLAT, bg='#ffffff', highlightthickness=0)
    new_window_canvas.pack(fill=BOTH, expand=True)

    new_window_frame.pack(expand=True, fill = BOTH)
    new_window_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    new_window_scroll.pack(side=RIGHT, fill=Y)


    Globals.dose_response_uploaded_filenames = []

    explain_text = tk.Text(new_window_canvas, height=11, width = 47)
    explain_text.grid(row=0, column = 0, rowspan = 3, columnspan=2, \
        sticky=N+S+W+E, pady=(20,10), padx=(10,10))
    new_window_canvas.grid_columnconfigure(0, weight=0)
    new_window_canvas.grid_rowconfigure(0, weight=0)
    explain_text.insert(INSERT, "\
Here you can upload several files all irradiated with \nthe same dose. \
Fill in dose and an average will be \ncalculated and used in the calibration. \
You are also \nable to upload only one file each time, and FIDORA \nwill keep \
track and average before fitting the \ndose-response.")
    explain_text.config(state=DISABLED, bd=0, font=('calibri', '11'))

    write_dose_box_frame = tk.Frame(new_window_canvas)
    write_dose_box_frame.grid(row=2, column=1, sticky=N+S+E+W,\
         pady=(0,30), padx=(0,10))
    new_window_canvas.grid_columnconfigure(1, weight=0)
    new_window_canvas.grid_rowconfigure(1, weight=0)
    write_dose_box_frame.config(bg='#ffffff')

    dose_border_label = Label(write_dose_box_frame, \
        image = Globals.dose_response_dose_border)
    dose_border_label.image=Globals.dose_response_dose_border
    dose_border_label.config(bg='#ffffff', borderwidth=0)
    dose_border_label.pack(expand=True, fill=BOTH)

    write_dose_text = tk.Text(new_window_canvas, height=1, width=19)
    write_dose_text.insert(INSERT, "Write dose here (cGy):")
    write_dose_text.config(state=DISABLED, bd=0, \
        font=('calibri', '11'), bg='#ffffff')
    write_dose_text.grid(row=1, column=1, sticky=E+W, pady=(140,0), padx=(5,5))
    new_window_canvas.grid_columnconfigure(3, weight=0)
    new_window_canvas.grid_rowconfigure(3, weight=0)

    write_dose_box = tk.Text(dose_border_label, height=1, width=8)
    write_dose_box.grid(row=0,column=0, sticky=N+S+W+E, pady=(10,0), padx=(20,5))
    write_dose_box.insert(INSERT, " ")
    write_dose_box.config(state=NORMAL, bd=0, font=('calibri', '18'), bg='#ffffff')

    upload_button_frame = tk.Frame(new_window_canvas)
    upload_button_frame.grid(row=2, column=0, sticky=N+S+W+E, pady=(0,30))
    new_window_canvas.grid_columnconfigure(2, weight=0)
    new_window_canvas.grid_rowconfigure(2, weight=0)
    upload_button_frame.config(bg='#ffffff')

    upload_button = tk.Button(upload_button_frame, text='Upload file', \
        image=Globals.upload_button_image, cursor='hand2', font=('calibri', '14'), \
        relief=FLAT, state=ACTIVE,command=lambda: UploadAction(new_window_canvas))
    upload_button.pack(expand=True, fill=BOTH)
    upload_button.config(bg='#ffffff', activebackground='#ffffff', \
        activeforeground='#ffffff', highlightthickness=0)
    upload_button.image=Globals.upload_button_image

    Globals.dose_response_inOrOut = True
    done_button = tk.Button(new_window, text='DONE', cursor='hand2', \
        font=('calibri', '20', 'bold'),relief=FLAT, state=ACTIVE,\
            command=lambda: avgAllFiles(write_dose_box, new_window))
    done_button.config(activebackground='#04BAA6', bg= '#04BAA6', \
        activeforeground='#ffffff', fg='#ffffff', height=1)
    done_button.pack(expand=True, fill=X)
    



def clear_all():
#--------------------------------------------------
# Function to clear are variables
#
# The function is a callback function for 
# the button dose_response_clear_all_button
# in notebook.py
#--------------------------------------------------
    for i in range(len(Globals.dose_response_delete_buttons)):
        Globals.dose_response_red_list[i].destroy()
        Globals.dose_response_green_list[i].destroy()
        Globals.dose_response_blue_list[i].destroy()
        Globals.dose_response_delete_buttons[i].destroy()
        Globals.dose_response_dose_list[i].destroy()

    Globals.dose_response_dose_list = []
    Globals.dose_response_red_list = []
    Globals.dose_response_green_list = []
    Globals.dose_response_blue_list = []
    Globals.dose_response_delete_buttons = []
    
    Globals.dose_response_sd_list_red = []
    Globals.dose_response_sd_list_green = []
    Globals.dose_response_sd_list_blue = []

    Globals.dose_response_var1.set(1)
    Globals.dose_response_var2.set(1)
    Globals.dose_response_var3.set(1)

    Globals.avg_red_vector = []
    Globals.avg_green_vector = []
    Globals.avg_blue_vector = []

    Globals.dose_response_batch_number = "-"
    Globals.popt_red = np.zeros(3)
    Globals.dose_response_inOrOut = True
    Globals.dose_response_files_weightcount = 8
    Globals.dose_response_files_row_count = 2

    Globals.dose_response_save_calibration_button.config(state=DISABLED)
    
    plot_dose_response()