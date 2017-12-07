from adb import *
import tkinter as tk
from time import time
from PIL import ImageTk, Image
from io import BytesIO

window = tk.Tk()
window.title("Image")
window.geometry("360x660")
window.configure(background='grey')

panel = tk.Label(window)
panel.pack(side="bottom", fill="both", expand="yes")

previous_time = time()
frames_drawn = 0
while True:
	data = run_adb('exec-out screencap -p', clean=False)
	im = Image.open(BytesIO(data))
	im.thumbnail((im.size[0] * .33, im.size[1] * .33), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(im)
	panel.configure(image=img)
	panel.image = img
	window.update_idletasks()
	window.update()
	frames_drawn += 1
	if time() > previous_time + 10:
		print('FPS:', frames_drawn / (time() - previous_time))
		previous_time = time()
		frames_drawn = 0