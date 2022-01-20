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
        self.actutal_frame = None
        self.switch_frame(MainMenu)
        self.folder_name = ""
        self.file_name = ""
        self.selected_box = None
        self.title("Screenshots to PDF")

    def switch_frame(self, _class):
        self.new_frame = _class(self)
        if self.actutal_frame is not None:
            self.actutal_frame.destroy()
        self.actutal_frame = self.new_frame
        self.actutal_frame.pack()

    def exit_program(self):
        tk.Tk.destroy(self)

    def resize_window(self, width, height):
        self.width_screen = self.winfo_screenwidth()
        self.height_screen = self.winfo_screenheight()

        self.x = (self.width_screen / 2) - (width / 2)
        self.y = (self.height_screen / 2) - (height / 2)

        self.geometry("{}x{}+{}+{}".format(width, height, int(self.x), int(self.y)))


class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # Window size
        self.master.resize_window(250, 250)
        # labels
        self.title_label = tk.Label(self, text="ScreenShoot to PDF generator")
        # buttons
        self.create_button = tk.Button(self, text="CreatePDF",
                                       command=lambda: master.switch_frame(PdfCreatorMenu), padx=10, pady=10, width=10)
        self.exit_button = tk.Button(self, text="Exit",
                                     command=lambda: master.exit_program(), padx=10, pady=10, width=10)
        self.options_button = tk.Button(self, text="Help",
                                        command=lambda: master.switch_frame(Help), padx=10, pady=10, width=10)
        # put on window widgets
        self.title_label.pack()
        self.create_button.pack(pady=10, padx=10)
        self.options_button.pack(pady=10, padx=10)
        self.exit_button.pack(pady=10, padx=10)


class Help(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.resize_window(450, 200)
        self.info_label = tk.Label(self, text="Check how to use this program by clicking a link below")
        self.back_button = tk.Button(self, text='Back to main menu',
                                     command=lambda: master.switch_frame(MainMenu), padx=10, pady=10, width=15)
        self.link = tk.Label(self, text="https://gfycat.com/agreeablefavoritegrouper", font=('Helveticabold', 15),
                             fg="blue", cursor="hand2")
        self.info_label.pack(pady=10, padx=10)
        self.link.pack(pady=10, padx=10)
        self.link.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://gfycat.com/agreeablefavoritegrouper"))
        self.back_button.pack(pady=10, padx=10)


class PdfCreatorMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # Window size
        master.resize_window(550, 375)
        # Frames
        self.folder_frame = tk.LabelFrame(self, text='Select a folder where you want to save')
        self.file_frame = tk.LabelFrame(self, text='Enter a filename of PDF')
        # Entry
        self.entry_folder_name = tk.Entry(self.folder_frame, width=50)
        self.entry_file_name = tk.Entry(self.file_frame, width=50)
        # Buttons
        self.button_browse = tk.Button(self.folder_frame, text="Browse", command=self.select_path)
        self.button_accept = tk.Button(self, text="Ok", command=self.accept, width=10)
        self.button_back = tk.Button(self, text="Back to main menu",
                                     command=lambda: master.switch_frame(MainMenu), width=15)
        # Pack
        self.folder_frame.pack(padx=10, pady=10)
        self.file_frame.pack(padx=10, pady=20)
        # Grid in Frames
        self.entry_folder_name.grid(row=0, column=0, padx=10, pady=15, ipadx=5)
        self.button_browse.grid(row=0, column=1, padx=10, pady=15)
        self.entry_file_name.pack(padx=10, pady=15, ipadx=38)
        self.button_accept.pack()
        self.button_back.pack(padx=10, pady=15, ipady=10)

    def __callback(self):
        pass

    def get_folder_name(self):
        self.master.folder_name = self.entry_folder_name.get()

    def get_file_name(self):
        self.master.file_name = self.entry_file_name.get()

    def select_path(self):
        self.entry_folder_name.delete(0, "end")
        self.entry_folder_name.insert(0, filedialog.askdirectory())

    def accept(self):
        if not self.entry_folder_name.get():
            messagebox.showerror("Error!", "Enter a folder path")
            return
        if not self.entry_file_name.get():
            messagebox.showerror("Error!", "Enter a file name")
            return

        for PDF_file_name in glob.glob("{}/*.pdf".format(self.entry_folder_name.get())):

            if PDF_file_name == r"{}\{}.pdf".format(self.entry_folder_name.get(), self.entry_file_name.get()):
                answer = messagebox.askyesno(title="Warning!",
                                             message="This filename already exists. Do you want to overwrite?")
                if answer:
                    break
                else:
                    return

        self.get_folder_name()  # do poprawy ale tu jest zapis do zmiennej globalnej nazwy pliku
        self.get_file_name()
        self.master.switch_frame(CaptureAreaMenu)


class CaptureAreaMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.withdraw()
        sleep(.5)  # wait for minimize screen
        self.make_screen_shot_of_full_size_window()
        sleep(.5)  # wait for max screen
        master.deiconify()
        # Window size
        self.master.attributes('-fullscreen', True)
        self.path = r'{}/main.png'.format(master.folder_name)  # change this
        self.canvas = tk.Canvas(self, width=self.master.winfo_width(), height=self.master.winfo_height(),
                                cursor="cross", highlightthickness=5, highlightbackground="blue")
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
        self.text_size = 40
        self.text_x_pos = (self.winfo_screenwidth() / 2) - (self.text_size / 2)
        self.canvas.create_text(self.text_x_pos, 45, text="Select the area for the screenshot",
                                font=('Helvetica', self.text_size), fill="white")
        self.canvas.create_text(self.text_x_pos, 40, text="Select the area for the screenshot",
                                font=('Helvetica', self.text_size), fill="blue")

    def make_screen_shot_of_full_size_window(self):
        self.screenshot = pyautogui.screenshot()
        self.screenshot.save(r'{}/main.png'.format(self.master.folder_name))

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
        self.accept_or_reset_selected_area()

    def accept_or_reset_selected_area(self):
        answer = messagebox.askyesno(title="CaptureScreen!",
                                     message="Click \"Yes\" if you want to make a ss of already selected area\n"
                                             "Click \"No\" if you want to select area once again")
        if answer:
            os.remove("{}/main.png".format(self.master.folder_name))
            self.master.attributes('-fullscreen', False)
            self.master.switch_frame(FunctionWidnow)
        else:
            self.canvas.delete('rect')


class FunctionWidnow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.resize_window(350, 125)
        self.ctr = 0
        self.ss_button = tk.Button(self, text="Make screen shot", command=self.ss, width=40, height=2, bg='red',
                                   fg='white')
        self.end_session_button = tk.Button(self, text="End session", command=self.make_PDF)
        self.ctr_label = tk.Label(self, text="{}".format(self.ctr))
        self.ctr_text_label = tk.Label(self, text="Number of ss:")
        self.show_folder_button = tk.Button(self, text="Show Folder", command=self.show_folder)

        self.ss_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, columnspan=4)
        self.ctr_text_label.grid(row=1, column=0, padx=5, pady=10)
        self.ctr_label.grid(row=1, column=1, padx=10, pady=10, sticky='W')
        self.show_folder_button.grid(row=1, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        self.end_session_button.grid(row=1, column=3, padx=10, pady=10, ipadx=5, ipady=5)

    def __callback(self):
        pass

    def ss(self):
        image = ImageGrab.grab(
            bbox=(self.master.selected_box[0], self.master.selected_box[1],
                  self.master.selected_box[2], self.master.selected_box[3]))
        image.save(f'{self.master.folder_name}/{self.ctr:08d}.png') # fix
        self.ctr = self.ctr + 1
        self.ctr_label.config(text="{}".format(self.ctr))

    def make_PDF(self):
        if self.ctr == 0:
            messagebox.showerror("Error!", "Make a screen shot first!")
            return
        if self.ctr > 0:
            img_list = []
            print()
            for file_name in glob.glob("{}/*.png".format(self.master.folder_name)):
                print(file_name)
                im = Image.open(file_name)
                img_list.append(im.convert('RGB'))

            img_list[0].save("{}/{}.pdf".format(self.master.folder_name, self.master.file_name), save_all=True,
                             append_images=img_list[1:])
            for file in os.listdir(self.master.folder_name):
                if file.endswith('.png'):
                    os.remove("{}/{}".format(self.master.folder_name, file))
            self.master.switch_frame(MainMenu)

    def show_folder(self):
        path = "{}".format(self.master.folder_name)
        path = os.path.realpath(path)
        os.startfile(path)


# Main
app = ActuallScreenManager()
app.mainloop()
