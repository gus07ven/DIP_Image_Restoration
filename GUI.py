import PIL
from PIL import ImageTk, Image
import numpy as np
from tkinter import *
import tkinter.filedialog
from PIL import Image
import cv2
import random
import sys
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from Filtering.Filtering import Filtering
sys.path.append('Restoration_DIP/Filtering')


class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        w, h = 1080, 1080
        master.minsize(width=w, height=h)
        master.maxsize(width=2000, height=2000)
        self.place()
        self.labelMean = Label(root, text='Mean:')
        self.labelVariance = Label(root, text='Variance:')
        self.labelProbability = Label(root, text='Probability')
        self.labelWindowSize = Label(root, text='Window size:')
        self.labelDParam = Label(root, text='D:')
        self.labelQParam = Label(root, text='Q:')
        self.file = Button(self, text='Browse', command=self.choose)
        self.image = PhotoImage(file='images/placeholder_new.png').subsample(3)
        self.label = Label(image=self.image)
        self.panel = Label(image="")
        self.denoised_img = Label(image="")
        self.mp_window_size = Entry(root)
        self.ch_window_size = Entry(root)
        self.qpara = Entry(root)
        self.t = Button()
        self.cans = Button()
        self.alnf_can = Button()
        self.adpwindow_size = Entry(root)
        self.hm_window_size = Entry(root)
        self.hmcans = Button()
        self.noise_mean = Entry(root)
        self.noise_variance = Entry(root)
        self.noise_probability = Entry(root)
        # self.filter_window_size = Entry(root)
        # self.filter_q_param = Entry(root)
        # self.filter_d_param = Entry(root)

        global flag
        global window_size
        global mp_window_size
        global hm_window_size
        global qpara
        global ch_window_size
        global cans
        global atrim
        global alnf_can
        global adpwindow_size
        global adp
        global mp
        global ch
        global t
        global txt # label for all the hint
        global path
        mp = 1
        ch = 1
        flag = 0
        root.configure(background='#ffffff')

    def reset(self):
        print("reset called")

# Clicking upload image brings you here.
    def choose(self):
        ifile = tkinter.filedialog.askopenfile(parent=self,mode='rb',filetypes =(("jpeg", "*.jpg"),("png", "*.png"),("All Files","*.*")),title='Choose a file')
        global path
        path = ifile.name
        img = Image.open(path)
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.image2 = img
        self.label.configure(image=img)
        self.label.image=img
        flag = 0
        print("FLAG VAL for upload", flag)

    def gauss(self, mean_parameter, variance_parameter):
        global path
        cvimg = cv2.imread(path, 0)
        img = cv2.resize(cvimg, (250, 250))
        row, col = img.shape
        mean = int(mean_parameter.get())   # 0
        var = int(variance_parameter.get()) # 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, var, (row, col))
        print(gauss.shape)
        gauss = gauss.reshape(row, col)
        noisy = img + gauss
        # plt.hist(noisy, bins='auto')
        # plt.show()
        noisy = np.array(noisy, dtype=np.uint8)
        cv2.imwrite("images/noisy_img_DIP.jpg", noisy)

        plt.hist(noisy, bins='auto')
        hist_img = plt.hist(noisy, bins='auto')
        # plt.show()
        flag = 2

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(noisy))
        panel = Label(root, image=self.photo,width=360,height=240)
        self.panel.configure(image=self.photo,width=250,height=250)
        if (flag != 0):
            print("FLAG VAL", flag)

            set_filter()
            gauss_arrow()
        return noisy

    def saltpepper(self, probability_param):
        global path
        image = cv2.imread(path, 0)
        image = cv2.resize(image, (250, 250))
        prob = float(probability_param.get()) # was 0.2
        thres = 1 - prob
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                rdn = random.random()
                if rdn < prob:
                    image[i][j] = 0
                elif rdn > thres:
                    image[i][j] = 255
                else:

                    image[i][j] = image[i][j]
        noisy = np.array(image, dtype=np.uint8)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(noisy))
        panel = Label(root, image=self.photo, width=360, height=240)
        self.panel.configure(image=self.photo, width=250, height=250)
        cv2.imwrite("images/noisy_img_DIP.jpg", noisy)
        flag = 3

        if (flag != 0):
            print("FLAG VAL", flag)
            set_filter()
            sp_arrow()

    def exponentialNoise(self):
        global path
        image = cv2.imread(path, 0)
        image = cv2.resize(image, (250, 250))
        row, col = image.shape
        exponen = np.random.exponential(scale=3, size=(row, col))
        image = image + exponen
        noisy = np.array(image, dtype=np.uint8)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(noisy))
        self.panel.configure(image=self.photo, width=250, height=250)
        flag = 4
        cv2.imwrite("images/noisy_img_DIP.jpg", noisy)
        if (flag != 0):
            print("FLAG VAL", flag)
            set_filter()
            exp_arrow()
        return noisy

# Main
root = Tk()
app = GUI(master=root)
m = root.maxsize()

root.geometry('{}x{}+0+0'.format(*m))
root.title("IUF18 Image Restorer")

a = StringVar()
a.set("default")

fil_b = StringVar()
fil_b.set("default")
fil_b = StringVar()

oc = StringVar(root)
oc.set("Select Noise")

fil = StringVar(root)
fil.set("Select Filter")


def adp_callback(event): # note that you must include the event as an arg, even if you don't use it.
    app.adpwindow_size.delete(0, "end")
    return None


def mp_callback(event): # note that you must include the event as an arg, even if you don't use it.
    app.mp_window_size.delete(0, "end")
    return None


def alphatrim_callback_ch(event): # note that you must include the event as an arg, even if you don't use it.
    app.ch_window_size.delete(0, "end")
    return None


def alphatrim_callback_d(event): # note that you must include the event as an arg, even if you don't use it.
    app.qpara.delete(0, "end")
    return None


def alpha_trimmed_filter_params(filter_name):
    atrim = 1
    if atrim != 0 or mp == 0:
        app.mp_window_size.destroy()
        app.mp_window_size.update()
        app.cans.destroy()
        app.adpwindow_size.destroy()
        app.alnf_can.destroy()
        app.hm_window_size.destroy()
        app.hmcans.destroy()
        app.labelWindowSize['text'] = ''
        app.labelDParam['text'] = ''
        app.labelQParam['text'] = ''
        app.qpara.destroy()

    app.labelWindowSize = Label(root, text='Window Size:')
    app.labelWindowSize.config(font=("Arial", 20), fg="black")
    app.labelWindowSize.place(x=500, y=240)

    print("alpha_Trimmed_params called")
    app.ch_window_size = Entry(root)
    app.ch_window_size.pack()
    app.ch_window_size.focus_set()
    app.ch_window_size.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
    app.ch_window_size.place(x=650, y=240)
    app.ch_window_size.insert(0, '0')

    if filter_name == 'Alpha trimmed':
        app.labelDParam = Label(root, text='D:')
        app.labelDParam.config(font=("Arial", 20), fg="black")
        app.labelDParam.place(x=725, y=240)
    elif filter_name == 'Contraharmonic mean':
        app.labelQParam = Label(root, text='Q:')
        app.labelQParam.config(font=("Arial", 20), fg="black")
        app.labelQParam.place(x=725, y=240)

    print("atrim", atrim)
    print("mp in atrim", mp)
    app.qpara = Entry(root)
    app.qpara.pack()
    app.qpara.focus_set()
    app.qpara.insert(0, '0')
    app.qpara.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
    app.qpara.place(x=775, y=240)

    app.t = Button(root, text='Apply Filter', fg='white',
                   command=lambda: create_alpha_trimmed_filter_window(app.ch_window_size, app.qpara))
    app.t.config(font=("Arial", 22), fg="#313131", bd="5px", relief="raised")
    app.t.place(x=850, y=240)
    app.ch_window_size.bind("<Button-1>", alphatrim_callback_ch)
    app.qpara.bind("<Button-1>", alphatrim_callback_d)


def get_filter_parameters(filter_name):
    print("midpoint_filter_params called")
    mp = 1

    if mp != 0:
        app.ch_window_size.destroy()
        app.qpara.destroy()
        app.adpwindow_size.destroy()
        app.hm_window_size.destroy()
        app.adpwindow_size.destroy()
        app.alnf_can.destroy()
        app.hmcans.destroy()
        app.labelWindowSize['text'] = ''
        app.labelQParam['text'] = ''
        app.labelDParam['text'] = ''

    app.labelWindowSize = Label(root, text='Window Size:')
    app.labelWindowSize.config(font=("Arial", 20), fg="black")
    app.labelWindowSize.place(x=500, y=240)
    app.mp_window_size = Entry(root)
    app.mp_window_size.pack()
    app.mp_window_size.focus_set()

    app.mp_window_size.config(font=("Arial", 18), fg="#313131", bd="2px", width=3)
    app.mp_window_size.place(x=650, y=240)
    app.mp_window_size.insert(0, '0')

    app.cans = Button(root, text='Apply Filter', fg='white',
                      command=lambda: create_filter_window(app.mp_window_size, filter_name))
    app.cans.config(font=("Arial", 22), fg="#313131", bd="5px", relief="raised")
    app.cans.place(x=850, y=240)
    app.mp_window_size.bind("<Button-1>", mp_callback)


def hm_callback(event):
    app.hm_window_size.delete(0, "end")
    return None


def create_filter_window(window_size, filter_name):
    img = 'images/noisy_img_DIP.jpg'
    input_image = cv2.imread(img, 0)
    test = Filtering(input_image)
    print("print window size", int(window_size.get()))
    if filter_name == "Adaptive median":
        print("Result is adaptive median")
        result = test.adaptive_median_filter(input_image, int(window_size.get()))
    if filter_name == "Arithmetic mean":
        print("Result is arithmetic mean")
        result = test.arithmetic_mean_filter(input_image, int(window_size.get()))
    if filter_name == "Contraharmonic mean":
        print("Result is contraharmonic mean")
        result = test.contraharmonic_mean_filter(input_image, int(q_param.get()), int(window_size.get()))
    if filter_name == "Geometric mean":
        print("Result is geometric mean")
        result = test.geometric_mean_filter(input_image, int(window_size.get()))
    if filter_name == "Harmonic mean":
        print("Result is harmonic mean")
        result = test.harmonic_mean_filter(input_image, int(window_size.get()))
    if filter_name == "Max":
        print("Result is max")
        result = test.max_filter(input_image, int(window_size.get()))
    if filter_name == "Median":
        print("Result is median")
        result = test.median_filter(input_image, int(window_size.get()))
    if filter_name == "Midpoint":
        print("Result is midpoint")
        result = test.midpoint_filter(input_image, int(window_size.get()))
    if filter_name == "Min":
        print("Result is min")
        result = test.min_filter(input_image, int(window_size.get()))
    # cv2.imshow("Denoised_Image", result)
    app.photos = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(result))
    app.denoised_img.configure(image=app.photos, width=250, height=250)
    stringss = window_size.get()
    print(int(stringss))
    stringss = window_size.get()
    print(int(stringss))


def create_alpha_trimmed_filter_window(ch_window_size, qpara):
    img = 'images/noisy_img_DIP.jpg'
    input_image = cv2.imread(img, 0)
    test = Filtering(input_image)
    print("print window size", int(ch_window_size.get()))
    result = test.alpha_trimmed_filter(input_image, d=int(qpara.get()), window_size=int(ch_window_size.get()))
    # cv2.imshow("Denoised_Image", result)
    app.photos = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(result))
    app.denoised_img.configure(image=app.photos, width=250, height=250)
    stringss = ch_window_size.get()
    print(int(stringss))
    stringss = ch_window_size.get()
    print(int(stringss))


def set_filter():
    filter_select_menu = OptionMenu(root, fil, "Adaptive median", "Adaptive local noise reduction", "Alpha trimmed",
                                    "Arithmetic mean", "Contraharmonic mean", "Geometric mean", "Harmonic mean", "Max",
                                    "Median", "Midpoint",
                                    "Min", command=select_filter)
    filter_select_menu.config(font=("Arial", 20), fg="#313131", bd="10px", relief="raised")
    filter_select_menu.place(x=200, y=240)


def sp_arrow():
    root.spimage = PhotoImage(file='images/icons8-arrow-sp-transp.png').subsample(2)
    # root.spimage = PhotoImage(image=np.array(cvimg)).subsample(3)
    root.splbl = Label(image=root.spimage, state='normal', bg="#313131", relief="flat")
    root.splbl.place(x=540, y=310, anchor=N)


def exp_arrow():
    root.spimage = PhotoImage(file='images/icons8-arrow-480-exp.png').subsample(2)
    # root.spimage = PhotoImage(image=np.array(cvimg)).subsample(3)
    root.splbl = Label(image=root.spimage, state='normal', bg="#313131", relief="flat")
    root.splbl.place(x=540, y=310, anchor=N)


def gauss_arrow():
    root.spimage = PhotoImage(file='images/icons8-arrow-480-transp.png').subsample(2)
    # root.spimage = PhotoImage(image=np.array(cvimg)).subsample(3)
    root.splbl = Label(image=root.spimage, state='normal', bg="#313131", relief="flat")
    root.splbl.place(x=540, y=310, anchor=N)
    root.splbl['bg'] = '#313131'


def select_filter(filter_type):
    if filter_type == "default":
        fil_b.set("default")
        print(fil_b.get())
    elif filter_type == "Midpoint" or filter_type == "Arithmetic mean" \
            or filter_type == "Geometric mean" or filter_type == "Median" or filter_type == "Max"\
            or filter_type == "Min" or filter_type == "Midpoint" or filter_type == "Adaptive median"\
            or filter_type == "Harmonic mean":
        fil_b.set("midpoint_filter")
        get_filter_parameters(filter_type)
        print(fil_b.get())
    elif filter_type == "Alpha trimmed" or filter_type == "Contraharmonic mean" \
            or filter_type == "Adaptive local noise reduction":
        fil_b.set("alpha_trimmed_filter filter")
        alpha_trimmed_filter_params(filter_type)
        print(fil_b.get())


# Select noise drop down
def select_noise(x):
    if x == "default":
        app.labelMean['text'] = ''
        app.labelVariance['text'] = ''
        app.labelProbability['text'] = ''
        a.set("default")
        print(a.get())

    elif x == "Gaussian":
        app.noise_mean.destroy()
        app.noise_variance.destroy()
        app.noise_probability.destroy()
        app.labelMean['text'] = ''
        app.labelVariance['text'] = ''
        app.labelProbability['text'] = ''
        a.set("gaussian")

        app.labelMean = Label(root, text='Mean:')
        app.labelMean.config(font=("Arial", 20), fg="black")
        app.labelMean.place(x=400, y=180)

        app.noise_mean = Entry(root)
        app.noise_mean.pack()
        app.noise_mean.focus_set()
        app.noise_mean.insert(0, '0')
        app.noise_mean.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
        app.noise_mean.place(x=475, y=180)

        app.labelVariance = Label(root, text='Variance:')
        app.labelVariance.config(font=("Arial", 20), fg="black")
        app.labelVariance.place(x=550, y=180)

        app.noise_variance = Entry(root)
        app.noise_variance.pack()
        app.noise_variance.focus_set()
        app.noise_variance.insert(0, '0')
        app.noise_variance.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
        app.noise_variance.place(x=650, y=180)

        app.t = Button(root, text='Add noise', fg='white', command=lambda: app.gauss(app.noise_mean, app.noise_variance))
        app.t.config(font=("Arial", 22), fg="#313131", bd="10px", relief="raised")
        app.t.place(x=850, y=180, anchor=N)
        print(a.get())

    elif x == "Salt and pepper":
        app.noise_mean.destroy()
        app.noise_variance.destroy()
        app.noise_probability.destroy()
        app.labelMean['text'] = ''
        app.labelVariance['text'] = ''
        app.labelProbability['text'] = ''
        a.set("saltandPepper")

        app.labelProbability = Label(root, text='Probability:')
        app.labelProbability.config(font=("Arial", 20), fg="black")
        app.labelProbability.place(x=500, y=180)

        app.noise_probability = Entry(root)
        app.noise_probability.pack()
        app.noise_probability.focus_set()
        app.noise_probability.insert(0, '0.0')
        app.noise_probability.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
        app.noise_probability.place(x=625, y=180)

        app.t = Button(root, text='Add noise', fg='white', command=lambda: app.saltpepper(app.noise_probability))
        app.t.config(font=("Arial", 22), fg="#313131", bd="10px", relief="raised")
        app.t.place(x=850, y=180, anchor=N)
        print(a.get())

    elif x == "Exponential":
        app.noise_mean.destroy()
        app.noise_variance.destroy()
        app.noise_probability.destroy()
        app.labelMean['text'] = ''
        app.labelVariance['text'] = ''
        app.labelProbability['text'] = ''

        a.set("Exponential")
        app.labelMean = Label(root, text='Mean:')
        app.labelMean.config(font=("Arial", 20), fg="black")
        app.labelMean.place(x=400, y=180)

        app.noise_mean = Entry(root)
        app.noise_mean.pack()
        app.noise_mean.focus_set()
        app.noise_mean.insert(0, '0')
        app.noise_mean.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
        app.noise_mean.place(x=475, y=180)

        app.labelVariance = Label(root, text='Variance:')
        app.labelVariance.config(font=("Arial", 20), fg="black")
        app.labelVariance.place(x=550, y=180)

        app.noise_variance = Entry(root)
        app.noise_variance.pack()
        app.noise_variance.focus_set()
        app.noise_variance.insert(0, '0')
        app.noise_variance.config(font=("Arial", 20), fg="#313131", bd="2px", width=3)
        app.noise_variance.place(x=650, y=180)

        app.t = Button(root, text='Add noise', fg='white', command=lambda: app.exponentialNoise())
        app.t.config(font=("Arial", 22), fg="#313131", bd="10px", relief="raised")
        app.t.place(x=850, y=180, anchor=N)
        print(a.get())


o = OptionMenu(root, oc,  "Gaussian", "Salt and pepper", "Exponential", command=select_noise)
o.config(font=("Arial", 20), fg="#313131", bd="10px", relief="raised")
z = a.get()
print(z)

# GUI Header
txt = Label(root, text='Image Restoration')
txt.config(font=("Arial", 32), fg="white", bg="#0000ff", bd="5px", relief="raised")
txt.place(x=10, y=30)
#old val was 590 for x then 390 now 100
o.place(x=200, y=180)

# app.file.pack(side=LEFT  ,padx=(0, 0))
# app.choose.pack(side=LEFT)
app.label.place(x=100, y=310)
app.panel.place(x=710, y=310)
app.denoised_img.place(x=410,y=570)

can = Button(root, text='Upload Image', command=app.choose)
# can.bind("<Button-1>", app.choose)
can.config(font=("Arial", 20), fg="#313131", bd="10px", relief="raised")
can.place(x=200, y=120)
# can = Button(root, text='Reset', fg='white', command=app.choose)     Does reset do anything right now?
# # can.bind("<Button-1>", app.choose)
# can.config(font=("Arial", 20), fg="#313131", bd="10px", relief="raised")
# can.place(x=400, y=120, anchor=N)

var = IntVar()
# R1 = Radiobutton(root, text="Option 1", variable=var, value=1,
#                   command="dd")
# R1.pack( anchor = W )
#
# R2 = Radiobutton(root, text="Option 2", variable=var, value=2,
#                   command="dd")
# R2.pack( anchor = W )
#
# R3 = Radiobutton(root, text="Option 3", variable=var, value=3,
#                   command="dd")
# R3.pack( anchor = W)

app.mainloop()
root.destroy()