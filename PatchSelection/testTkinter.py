from tkinter import *
from PIL import ImageTk,Image

class patchSelection:
    canvas_width = 500
    canvas_height = 500

    image_path = None # the path for the shown image
    image = None # the image used to give canvas to show
    boundingBoxSize=10


    # initial the class, if the image_path is None, use the hard coding image
    def __init__(self, image_path = None):
        if image_path is None:
            self.image_path = "Lenna.png"
            self.image = Image.open(self.image_path)

    # The action when left mouse key pressed
    # can be used for show histogram
    def LeftKeyClick(self, event):
        print("Mouse Left Key Click")
        #python_green = "#476042"
        #x1, y1 = (event.x - 1), (event.y - 1)
        #x2, y2 = (event.x + 1), (event.y + 1)
        #w.create_oval(x1, y1, x2, y2, fill=python_green)

    # Mouse move when in the image
    def motion(self, event):
        if self.image_path is not None:
            x1, y1 = (event.x - self.boundingBoxSize), (event.y - self.boundingBoxSize)
            x2, y2 = (event.x + self.boundingBoxSize), (event.y + self.boundingBoxSize)
            #print("Mouse position: (%s %s)" % (event.x, event.y))
            w.create_image(0,0,anchor=NW,image=canvas_image)
            w.create_rectangle(x1,y1,x2,y2)

    # Mouse wheel scroll, used for increase the region or shrink the region
    def mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            #print("Mouse scrollDown")
            self.boundingBoxSize = self.boundingBoxSize - 1
            if self.boundingBoxSize < 5:
                self.boundingBoxSize = 5
        elif event.num == 4 or event.delta == 120:
            #print("Mouse scrollUp")
            self.boundingBoxSize = self.boundingBoxSize + 1
            if self.boundingBoxSize > 40: # 40 should be the size of the image
                self.boundingBoxSize = 40
        self.motion(event)


master = Tk()
master.title("Mouse operation")
image = patchSelection()

# the canvas control w used for showing the noise image
w = Canvas(master,
           width=image.canvas_width,
           height=image.canvas_height)
w.pack(expand=YES, fill=BOTH)

w.bind("<Button-1>", image.LeftKeyClick)  # bind the mouse left key down and move
w.bind("<Motion>", image.motion)  #bind the mouse move
w.bind("<MouseWheel>", image.mouse_wheel)
#message = Label(master,justify=LEFT,text="Press and Drag the mouse to draw").pack()
canvas_image=ImageTk.PhotoImage(image.image)

mainloop()



