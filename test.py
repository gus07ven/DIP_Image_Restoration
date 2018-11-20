import PIL
from PIL import ImageTk, Image
import numpy as np
from tkinter import *
import tkinter.filedialog
from PIL import  Image
import cv2
import random
import sys
from Filtering.Filtering import Filtering
sys.path.append('Restoration_DIP/Filtering')
import math
class GUI(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)
        w,h = 1080, 1080
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        self.place()
        global flag
        global window_size



        flag = 0
        self.file = Button(self, text='Browse', command=self.choose)
        self.image = PhotoImage(file='images/placeholder_new.png').subsample(3)

        self.label = Label(image=self.image)
        self.panel = Label(image="")
        self.denoised_img = Label(image="")



        root.configure(background='#313131')


    def choose(self):
        ifile = tkinter.filedialog.askopenfile(parent=self,mode='rb',filetypes =(("jpeg", "*.jpg"),("png", "*.png"),("All Files","*.*")),title='Choose a file')
        global path
        path = ifile.name
        img = Image.open(path)
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        # self.image2 = PhotoImage(file=path)
        self.image2 = img

        self.label.configure(image=img)
        self.label.image=img
        flag = 0
        print("FLAG VAL for upload", flag)

    def blur_image(self):
        print(path)
        cvimg = cv2.imread(path)

        cv_img = cv2.blur(cvimg, (3, 3))
        print(cv_img)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        # self.panel = Label(root, image=self.photo)
        self.panel.configure(image=self.photo,width=360,height=240)

        self.panel.image = self.photo
        flag = 1


    def gaussian_noise_add(self):
        cvimg = cv2.imread(path,0)
        img = cv2.resize(cvimg, (250, 250))
        mean = 0
        variance = 3
        prob_noise = 0.10
        height, width = img.shape[:2]
        num_noise_pixels = height * width * prob_noise
        noise_array = np.zeros(256, np.uint)
        noise_mat = np.zeros(shape=(img.shape[0], img.shape[1]), dtype=np.uint8)
        for i in range(0, 256):
            fx = 1 / math.sqrt(2 * math.pi * (variance)) * math.exp(- ((i - mean) ** 2) / (2 * variance))
            noise_array[i] = int(fx * num_noise_pixels + 0.5)
            # print(noise_array)
        num_noise_pixels = 0

        for i in range(256):
            num_noise_pixels += noise_array[i]

        for i in range(0, img.shape[1]):
            for j in range(0, img.shape[0]):
                noise_random = random.randint(0, 99)  # randomly decide whether to add noise or not
                if noise_random / 99 < prob_noise:
                    index = random.randint(0, 255)  # randomly decide a noise value to add to noise matrix
                    while True:

                        if num_noise_pixels == 0:
                            break
                        if noise_array[index] > 0:
                            noise_mat[i][j] = index
                            noise_array[index] -= 1
                            num_noise_pixels -= 1

                            break
                        else:
                            index += 1
                            if index == 256:
                                index = 0
        img = img + noise_mat
        flag = 2

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
        panel = Label(root, image=self.photo, width=360, height=240)
        self.panel.configure(image=self.photo, width=250, height=250)
        n_img = np.array(img, dtype=np.uint8)
        cv2.imwrite("images/noisy_img_gauss.jpg",n_img)
        if (flag != 0):
            print("FLAG VAL", flag)

            set_Filter()
            gauss_arrow()
        return img

    def gauss(self):
        cvimg = cv2.imread(path,0)
        img = cv2.resize(cvimg, (250, 250))
        row, col = img.shape
        mean = 0
        var = 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, var, (row, col))
        print(gauss.shape)
        gauss = gauss.reshape(row, col)
        noisy = img + gauss
        # plt.hist(noisy, bins='auto')
        # plt.show()
        noisy = np.array(noisy, dtype=np.uint8)
        cv2.imwrite("images/noisy_img_gauss.jpg",noisy)

        # plt.hist(noisy, bins='auto')
        # plt.show()
        flag = 2

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(noisy))
        panel = Label(root, image=self.photo,width=360,height=240)
        self.panel.configure(image=self.photo,width=250,height=250)
        if (flag != 0):
            print("FLAG VAL", flag)

            set_Filter()
            gauss_arrow()
        return noisy
    def saltpepper(self):
        image = cv2.imread(path,0)

        prob = 0.2
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
            set_Filter()
            sp_arrow()





root = Tk()
app = GUI(master=root)
m = root.maxsize()
root.geometry('{}x{}+0+0'.format(*m))
root.title("Noise Generator")

a = StringVar()
a.set("default")

fil_b = StringVar()
fil_b.set("default")
fil_b = StringVar()
oc = StringVar(root)
oc.set("Select Noise")
fil = StringVar(root)
fil.set("Select Filter")
def adativelnf_params():
    print("adativelnf_params called")
    window_size = Entry(root)
    window_size.pack()
    window_size.focus_set()

    window_size.config(font=("Courier", 18), fg="#313131", bd="2px")
    window_size.place(x=500, y=240, anchor=N)
    can = Button(root, text='Apply Filter', fg='white', command=lambda: create_adaptive_noisereduce_filter_window(window_size))
    can.config(font=("Courier", 22), fg="#313131", bd="5px", relief="raised")
    can.place(x=760, y=240, anchor=N)
def midpoint_filter_params():
    print("midpoint_filter_params called")
    window_size = Entry(root)
    window_size.pack()
    window_size.focus_set()

    window_size.config(font=("Courier", 18), fg="#313131", bd="2px")
    window_size.place(x=500, y=240, anchor=N)
    can = Button(root, text='Apply Filter', fg='white', command=lambda: create_midpoint_filter_window(window_size))
    can.config(font=("Courier", 22), fg="#313131", bd="5px", relief="raised")
    can.place(x=760, y=240, anchor=N)

def create_adaptive_noisereduce_filter_window(window_size):
        img = '/Users/saikrishnaramalingam/PycharmProjects/Restoration_DIP/images/noisy_img_DIP.jpg'
        input_image = cv2.imread(img, 0)
        test = Filtering(input_image)
        print("print window size",int(window_size.get()))
        result = test.adaptive_median_filter(input_image,int(window_size.get()))
        # cv2.imshow("Denoised_Image", result)

        app.photos = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(result))
        app.denoised_img.configure(image=app.photos, width=200, height=200)
        stringss = window_size.get()
        print(int(stringss))
        stringss = window_size.get()
        print(int(stringss))


def create_midpoint_filter_window(window_size):
    img = '/Users/saikrishnaramalingam/PycharmProjects/Restoration_DIP/images/noisy_img_DIP.jpg'
    input_image = cv2.imread(img, 0)
    test = Filtering(input_image)
    print("print window size", int(window_size.get()))
    result = test.midpoint_filter(input_image, int(window_size.get()))
    # cv2.imshow("Denoised_Image", result)

    app.photos = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(result))
    app.denoised_img.configure(image=app.photos, width=200, height=200)
    stringss = window_size.get()
    print(int(stringss))
    stringss = window_size.get()
    print(int(stringss))


def set_Filter():

    filter_select_menu = OptionMenu(root, fil,"midpoint_filter","alpha_trimmed_filter","adaptive_local_noise_reduction_filter", "adaptive_mean", "harmonic", "contra_harmonic", command=Filter_Select_function)

    filter_select_menu.config(font=("Courier", 14), fg="#313131", bd="5px", relief="raised")
    filter_select_menu.place(x=160, y=240, anchor=N)




def sp_arrow():
    root.spimage = PhotoImage(file='images/icons8-arrow-sp-transp.png').subsample(2)

    # root.spimage = PhotoImage(image=np.array(cvimg)).subsample(3)
    root.splbl = Label(image=root.spimage,state='normal',bg="#313131",relief="flat")

    root.splbl.place(x=540, y=310, anchor=N)

def gauss_arrow():
    root.spimage = PhotoImage(file='images/icons8-arrow-480-transp.png').subsample(2)

    # root.spimage = PhotoImage(image=np.array(cvimg)).subsample(3)
    root.splbl = Label(image=root.spimage, state='normal', bg="#313131", relief="flat")

    root.splbl.place(x=540, y=310, anchor=N)
    root.splbl['bg'] = '#313131'
def Filter_Select_function(x):
    if x == "default":
        fil_b.set("default")
        print(fil_b.get())
    elif x == "midpoint_filter":
        fil_b.set("midpoint_filter")
        # app.gauss()
        midpoint_filter_params()
        print(fil_b.get())

    elif x == "adaptive_local_noise_reduction_filter":
        fil_b.set("adaptive_local_noisefilter")
        adativelnf_params()
        print(fil_b.get())
    elif x == "erlang":
        fil_b.set("erlang")
        print(fil_b.get())

def Noise_Select_function(x):
    if x == "default":
        a.set("default")
        print(a.get())
    elif x == "gaussian":
        a.set("gaussian")
        # app.gauss()
        app.gauss()
        print(a.get())

    elif x == "saltandPepper":
        a.set("saltandPepper")
        app.saltpepper()
        print(a.get())
    elif x == "erlang":
        a.set("erlang")
        print(a.get())


o = OptionMenu(root, oc,  "gaussian", "saltandPepper", "erlang", command=Noise_Select_function)

z = a.get()
print(z)

txt = Label(root, text='Image Restoration')
txt.config(font=("Courier", 32), fg="white", bg="#313131", bd="5px", relief="raised")

txt.place(x=10, y=30)
#old val was 590 for x then 390 now 100
o.place(x=150, y=180, anchor=N)
# app.file.pack(side=LEFT  ,padx=(0, 0))
# app.choose.pack(side=LEFT)
app.label.place(x=100, y=310)

app.panel.place(x=710, y=310)
app.denoised_img.place(x=410,y=570)
can = Button(root, text='Upload Image',fg='white',command=app.choose)

# can.bind("<Button-1>", app.choose)

can.config(font=("Courier", 32), fg="#313131", bd="5px", relief="raised")
can.place(x=200, y=120, anchor=N)



app.mainloop()
root.destroy()
