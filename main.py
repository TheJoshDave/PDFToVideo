import tkinter as tk
from functools import partial
import os
from tkinter.filedialog import askopenfilename
PDFToImages = r"Scripts/PDFToImages.py"
PDFToTXT = r"Scripts/PDFToTXT.py"
TTS = r"Scripts/TTS.py"
AudioImageFFMPEG = r"Scripts/AudioImageFFMPEG.py"


def create_button(text, action_with_arg):
    return tk.Button(r, text=text, width=25, command=action_with_arg, activebackground="black", activeforeground="grey", height=5)


def PDFtoTXTPNG():
    root_folder = askopenfilename(title='Select pdf', filetypes=[("PDF Files", "*.pdf")])
    os.system("python " + PDFToImages + " " + root_folder)
    os.system("python " + PDFToTXT + " " + root_folder)


def TXTtoMP3toMP4toFinish():
    root_folder = askopenfilename(title='Select pdf', filetypes=[("PDF Files", "*.pdf")])
    os.system("python " + TTS + " " + root_folder)
    os.system("python " + AudioImageFFMPEG + " " + root_folder)


r = tk.Tk()
r.title('PDF To Video')
create_button("PDF->TXT+PNG", partial(PDFtoTXTPNG)).pack()
create_button("Easy Format Application", partial(print, "Must run through ahk")).pack()
create_button("TXT->MP3->MP4->Finish", partial(TXTtoMP3toMP4toFinish)).pack()
create_button("cancel", partial(r.destroy)).pack()
r.mainloop()
