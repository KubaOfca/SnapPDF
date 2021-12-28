import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import pyautogui
from PIL import Image, ImageTk, ImageGrab
from time import sleep
import glob
import os
import webbrowser

class ActuallScreenManager(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._actutalFrame = None
        self.switch_frame(MainMenu)
        self.folderName = ""
        self.fileName = ""
        self.selected_box = None
        self.title("Screenshots to PDF")

    def switch_frame(self, _class):
        self.newFrame = _class(self)
        if self._actutalFrame is not None:
            self._actutalFrame.destroy()
        self._actutalFrame = self.newFrame
        self._actutalFrame.pack()

    def exit_program(self):
        tk.Tk.destroy(self)

    def resizeWindow(self, width, height):
        self.widthScreen = self.winfo_screenwidth()
        self.heightScreen = self.winfo_screenheight()

        self.x = (self.widthScreen / 2) - (width / 2)
        self.y = (self.heightScreen / 2) - (height / 2)

        self.geometry("{}x{}+{}+{}".format(width, height, int(self.x), int(self.y)))


class MainMenu(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # Window size
        self.master.resizeWindow(250, 250)
        # labels
        self.titleLabel = tk.Label(self, text="ScreenShoot to PDF generator")
        # buttons
        self.createButton = tk.Button(self, text="CreatePDF",
                                      command=lambda: master.switch_frame(PdfCreatorMenu), padx=10, pady=10, width=10)
        self.exitButton = tk.Button(self, text="Exit",
                                    command=lambda: master.exit_program(), padx=10, pady=10, width=10)
        self.optionsButton = tk.Button(self, text="Help",
                                       command=lambda: master.switch_frame(Help), padx=10, pady=10, width=10)
        # put on window widgets
        self.titleLabel.pack()
        self.createButton.pack(pady=10, padx=10)
        self.optionsButton.pack(pady=10, padx=10)
        self.exitButton.pack(pady=10, padx=10)

class Help(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.resizeWindow(450,200)
        self.infoLabel = tk.Label(self, text="Check how to use this program by clicking a link below")
        self.backButton = tk.Button(self, text='Back to main menu',
                                    command=lambda: master.switch_frame(MainMenu), padx=10, pady=10, width=15)
        self.link = tk.Label(self, text="https://gfycat.com/agreeablefavoritegrouper", font=('Helveticabold', 15), fg="blue", cursor="hand2")
        self.infoLabel.pack(pady=10, padx=10)
        self.link.pack(pady=10, padx=10)
        self.link.bind("<Button-1>", lambda e: self.callback("https://gfycat.com/agreeablefavoritegrouper"))
        self.backButton.pack(pady=10, padx=10)

    def callback(self, url):
        webbrowser.open_new_tab(url)

class PdfCreatorMenu(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Window size
        master.resizeWindow(550, 375)
        #Frames
        self.folderFrame = tk.LabelFrame(self, text='Select a folder where you want to save')
        self.fileFrame = tk.LabelFrame(self, text='Enter a filename of PDF')
        #Entry
        self.entry_FolderName = tk.Entry(self.folderFrame, width=50)
        self.entry_FileName = tk.Entry(self.fileFrame, width=50)
        #Buttons
        self.buttonBrowse = tk.Button(self.folderFrame, text="Browse", command=self.selectPath)
        self.buttonAccept = tk.Button(self, text="Ok", command=self.accept, width=10)
        self.buttonBack = tk.Button(self, text="Back to main menu", command=lambda: master.switch_frame(MainMenu), width=15)
        #Pack
        self.folderFrame.pack(padx=10, pady=10)
        self.fileFrame.pack(padx=10, pady=20)
        #Grid in Frames
        self.entry_FolderName.grid(row=0, column=0, padx=10, pady=15, ipadx=5)
        self.buttonBrowse.grid(row=0, column=1, padx=10, pady=15)
        self.entry_FileName.pack(padx=10, pady=15, ipadx=38)
        self.buttonAccept.pack()
        self.buttonBack.pack(padx=10, pady=15, ipady=10)


    def __callback(self):
        pass

    def getFolderName(self):
         self.master.folderName = self.entry_FolderName.get()

    def getFileName(self):
         self.master.fileName = self.entry_FileName.get()

    def selectPath(self):
        self.entry_FolderName.delete(0, "end")
        self.entry_FolderName.insert(0, filedialog.askdirectory())

    def accept(self):

        if not self.entry_FolderName.get():
            messagebox.showerror("Erorr!", "Enter a folder path")
            return
        if not self.entry_FileName.get():
            messagebox.showerror("Erorr!", "Enter a file name")
            return

        for PDFfilename in glob.glob("{}/*.pdf".format(self.entry_FolderName.get())):

            if PDFfilename == "{}\{}.pdf".format(self.entry_FolderName.get(), self.entry_FileName.get()):
                answer = messagebox.askyesno(title="Warning!",
                                             message="This filename already exists. Do you want to overwrite?")
                if answer:
                    break
                else:
                    return

        self.getFolderName() # do poprawy ale tu jest zapis do zmiennej globalnej nazwy pliku
        self.getFileName()
        self.master.switch_frame(CaptureAreaMenu)



class CaptureAreaMenu(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.withdraw()
        sleep(.5) # wait for minimalize screen
        self.makeScreenShotOfFullSizeWindow()
        sleep(.5) # wait for max screen
        master.deiconify()
        #Winow size
        self.master.attributes('-fullscreen', True)
        self.path = r'{}/main.png'.format(master.folderName) # change this
        self.canvas = tk.Canvas(self, width=self.master.winfo_width(), height=self.master.winfo_height(), cursor="cross", highlightthickness=5,
                             highlightbackground="blue")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.im = Image.open(self.path)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)
        self.textSize = 40
        self.textXpos = (self.winfo_screenwidth()/2) - (self.textSize/2)
        self.canvas.create_text(self.textXpos, 45, text="Select the area for the screenshot", font=('Helvetica', self.textSize),
                                fill="white")
        self.canvas.create_text(self.textXpos, 40, text="Select the area for the screenshot", font=('Helvetica', self.textSize), fill="blue")



    def makeScreenShotOfFullSizeWindow(self):
        self.screenshot = pyautogui.screenshot()
        self.screenshot.save(r'{}/main.png'.format(self.master.folderName))

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='yellow', tag='rect', width=5)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
        self.end_x = curX
        self.end_y = curY

    def on_button_release(self, event):
        self.master.selected_box = (self.start_x, self.start_y, self.end_x, self.end_y)
        #wywolaj funkcje do akcpetacji albo nie obszaru
        self.acceptOrResetSelectedArea()

    def acceptOrResetSelectedArea(self):
        answer = messagebox.askyesno(title="CaptureScreen!",
                                     message="Click \"Yes\" if you want to make a ss of already selected area\n"
                                             "Click \"No\" if you want to select area once again")
        if answer:
            os.remove("{}/main.png".format(self.master.folderName))
            self.master.attributes('-fullscreen', False)
            self.master.switch_frame(FunctionWidnow)
        else:
            self.canvas.delete('rect')


class FunctionWidnow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.resizeWindow(350, 125)
        self.ctr = 0
        self.ssButton = tk.Button(self, text="Make screen shot", command=self.ss, width=40, height=2, bg='red',
                               fg='white')
        self.endSesionButton = tk.Button(self, text="End sesion", command=self.makePDF)
        self.ctrLabel = tk.Label(self, text="{}".format(self.ctr))
        self.ctrTextLabel = tk.Label(self, text="Number of ss:")
        self.showFolderButton = tk.Button(self, text="Show Folder", command=self.showFolder)

        self.ssButton.grid(row=0, column=0, padx=5, pady=5, ipadx=5, columnspan=4)
        self.ctrTextLabel.grid(row=1, column=0, padx=5, pady=10)
        self.ctrLabel.grid(row=1, column=1, padx=10, pady=10, sticky='W')
        self.showFolderButton.grid(row=1, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        self.endSesionButton.grid(row=1, column=3, padx=10, pady=10, ipadx=5, ipady=5)

    def __callback(self):
        pass

    def ss(self):
        image = ImageGrab.grab(
            bbox=(self.master.selected_box[0], self.master.selected_box[1], self.master.selected_box[2], self.master.selected_box[3]))
        image.save(r'{}/{}.png'.format(self.master.folderName, self.ctr))
        self.ctr = self.ctr + 1
        self.ctrLabel.config(text="{}".format(self.ctr))

    def makePDF(self):
        if self.ctr == 0:
            messagebox.showerror("Error!", "Make a screen shot first!")
            return
        if self.ctr > 0:
            imgList = []
            for filename in glob.glob("{}/*.png".format(self.master.folderName)):
                im = Image.open(filename)
                imgList.append(im.convert('RGB'))

            imgList[0].save("{}/{}.pdf".format(self.master.folderName, self.master.fileName), save_all=True, append_images=imgList[1:])
            for file in os.listdir(self.master.folderName):
                if file.endswith('.png'):
                    os.remove("{}/{}".format(self.master.folderName, file))
            self.master.switch_frame(MainMenu)

    def showFolder(self):
        path = "{}".format(self.master.folderName)
        path = os.path.realpath(path)
        os.startfile(path)


# Main
# root = Tk()
# root.title("SS to PDF")
# mainMenu = MainMenu(root)
# root.mainloop()
app = ActuallScreenManager()
app.mainloop()