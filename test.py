from tkinter import Frame
import PIL
from PIL import ImageTk, Image
import numpy as np
from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import askdirectory
from PIL import  Image
import cv2
import scipy
class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        w,h = 1080, 1080
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        self.place()
        global flag
        flag = 0

        self.file = Button(self, text='Browse', command=self.choose)
        # self.choose = Label(self, text="Choose file")

        # self.file.place(x=590, y=200, anchor=N)
        # self.choose.place(x=560, y=200, anchor=N)
        self.image = PhotoImage(file='images/placeholder_new.png').subsample(3)

        self.label = Label(image=self.image)
        self.panel = Label(image="")


        # self.b = Button(self, text='Add noise', command=self.blur_image)
        # self.b.config(highlightbackground="white")
        #
        #
        # self.b.pack()
        # self.file.pack(padx=(10, 10), pady=(0, 0))

        root.configure(background='#313131')


        # C = Canvas(root, bg="blue", height=250, width=300)
        # filename = PhotoImage(file="bgimg.jpg")
        # background_label = Label(root, image=filename)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #
        # C.pack()

        # self.panel.pack(padx=3, pady=1, side=RIGHT)


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
    def gauss(self):
        cvimg = cv2.imread(path)
        img = cv2.resize(cvimg, (250, 250))
        row, col, ch = img.shape
        mean = 0
        gauss = np.random.normal(mean, 1, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = img + gauss
        n = noisy.astype('uint8')
        flag = 2

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(n))
        panel = Label(root, image=self.photo,width=360,height=240)
        self.panel.configure(image=self.photo,width=250,height=250)
        return noisy
    def saltpepper(self):
        #median or morphological filter can be used to reduce the noise
        cvimg = cv2.imread(path)
        img = cv2.resize(cvimg, (250, 250))
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(img)
        # Salt mode
        num_salt = np.ceil(amount * img.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in img.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in img.shape]
        out[coords] = 0
        sp = img + out
        n = sp.astype('uint8')
        print(n)

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(n))
        self.panel.configure(image=self.photo,width=250,height=250)
        flag = 3

        if(flag != 0):
            print("FLAG VAL",flag)

            set_Filter()
            sp_arrow()

root = Tk()
app = GUI(master=root)
m = root.maxsize()
root.geometry('{}x{}+0+0'.format(*m))
root.title("Noise Generator")

a = StringVar()
a.set("default")

oc = StringVar(root)
oc.set("Select Noise")

def set_Filter():
    can = Button(root, text='Apply Filter', fg='white', command=app.choose)

    can.config(font=("Courier", 32), fg="#313131", bd="5px", relief="raised")
    can.place(x=590, y=240, anchor=N)



def sp_arrow():
    root.spimage = PhotoImage(file='images/icons8-arrow-sp-bg.png').subsample(2)

    # root.spimage = PhotoImage(image=np.array(cvimg)).subsample(3)
    root.splbl = Label(image=root.spimage,state='normal',bg="#313131",relief="flat")

    root.splbl.place(x=540, y=310, anchor=N)


def Noise_Select_function(x):
    if x == "default":
        a.set("default")
        print(a.get())
    elif x == "gaussian":
        a.set("gaussian")
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

o.place(x=590, y=200, anchor=N)
# app.file.pack(side=LEFT  ,padx=(0, 0))
# app.choose.pack(side=LEFT)

app.label.place(x=20, y=310)

app.panel.place(x=710, y=310)

can = Button(root, text='Upload Image',fg='white',command=app.choose)

# can.bind("<Button-1>", app.choose)

can.config(font=("Courier", 32), fg="#313131", bd="5px", relief="raised")
can.place(x=590, y=150, anchor=N)


app.mainloop()
root.destroy()