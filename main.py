from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np


def getImage():
	filename = filedialog.askopenfilename(title='pen')
	return filename

def openImage():
	global size, img

	name = getImage()
	img = Image.open(name)
	img = ImageOps.grayscale(img)

	A = np.asarray(img)
	s = A.shape

	size = [s[1]+10, s[0]+30]

	root.geometry(f"{size[0]}x{size[1]}")
	updateImage(img)

	# drop.configure(x=size[0]-86, y=3)
	drop.place(x=size[0]-86, y=3)


def matrixConvulation(a, b, A, X):
    c = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            c += (kernels[X][1+i][1+j])*(A[a+i][b+j])
    return c

def conv(*args):
	A = np.asarray(img)
	output = np.zeros(np.shape(A), int)

	for i in range(len(A)):
		for j in range(len(A[0])):
			if i == 0 or i == len(A)-1 or j == 0 or j == len(A[0])-1:
				output[i][j] = A[i][j]
			else:
				output[i][j] = matrixConvulation(i, j, A, args[0])
	result = Image.fromarray(output.astype(np.uint8), 'L')
	updateImage(result)

def updateImage(image):
	Oimg = ImageTk.PhotoImage(image)
	panel.configure(image=Oimg)
	panel.image = Oimg

	print("Updated")


root = Tk()
img = None
size = [1000, 1000]
panel = Label(root)
panel.place(x=3, y=28)

kernels = {"Identity":[[0, 0, 0],
						[0, 1, 0],
						[0, 0, 0]],
			
			"Blur":[[0.0625, 0.125, 0.0625],
					[0.125, 0.25, 0.125],
					[0.0625, 0.125, 0.0625]],

			"Outline":[[-1, -1, -1],
						[-1, 8, -1],
						[-1, -1, -1]],

			"Sharpen":[[0, -1, 0],
						[-1, 5, -1],
						[0, -1, 0]]
}


opBtn = Button(root, text="Open", command=openImage).place(x=3, y=3)
options = [
	"Identity",
    "Blur",
    "Outline",
    "Sharpen",
]
clicked = StringVar()
clicked.set("Identity")

drop = OptionMenu( root , clicked , *options , command=conv)
drop.place(x=1000, y=1000)

root.mainloop()
