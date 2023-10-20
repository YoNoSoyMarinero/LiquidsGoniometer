from tkinter.constants import CENTER
from PIL.ImageColor import colormap
from PIL import Image, ImageTk
from ttkbootstrap import Style
from tkinter import font, ttk
from tkinter import filedialog as fd
import tkinter.messagebox
from measure_app import main
import cv2


current_photo = ''
current_img_measurment = ''
angle_img_ = ''


def save_commad():
    global angle_img_
    if angle_img_ == '':
        tkinter.messagebox.showerror("Error!", 'Please select photo!')
        return
    global current_img_measurment
    a = fd.asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('JPEG', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
    # Save
    path = r'{}.jpg'.format(a)
    print(path)
    cv2.imwrite(path, angle_img_)


def run_command():
    global current_img_measurment
    global angle_img_
    if current_photo == '':
        tkinter.messagebox.showerror("Error!", 'Please select photo!')
        return
    angle, angle_img = main(current_photo)
    angle_img_ = angle_img
    angle_label['text'] = "Contact angle of current measurment is: {}".format(
        angle[:7] + '°')
    b, g, r = cv2.split(angle_img)
    angle_img = cv2.merge((r, g, b))
    im = Image.fromarray(angle_img)
    current_img_measurment = ImageTk.PhotoImage(image=im)
    measurement_picture_frame.configure(image=current_img_measurment)
    measurement_picture_frame.image = current_img_measurment


def exit_command():
    window.destroy()


def remove_command():
    global current_photo
    global current_img_measurment
    global angle_img_
    picture = ImageTk.PhotoImage(Image.open('Capture.png'))
    measurement_picture_frame.configure(image=picture)
    measurement_picture_frame.image = picture
    angle_label['text'] = "Contact angle of current measurment is: {}".format(
        str(0) + '°')
    current_photo = ''
    current_img_measurment = ''
    angle_img_ = ''


def measure_command():
    panel.pack_forget()
    panel_.pack()


def get_back_command():
    panel_.pack_forget()
    panel.pack()


def upload_command():
    global current_photo
    global current_img_measurment
    global angle_img_
    angle_label['text'] = "Contact angle of current measurment is: {}".format(
        str(0) + '°')
    filename = fd.askopenfilename()
    picture = ImageTk.PhotoImage(Image.open(filename))
    measurement_picture_frame.configure(image=picture)
    measurement_picture_frame.image = picture
    current_photo = r'{}'.format(filename)
    current_img_measurment = ''
    angle_img_ = ''


style = Style(theme='darkly')

font = "Helvetica"
size = 70
weight = "bold"

window = style.master
window.title("Goniometer")
window.iconbitmap("ico.ico")

# Welcoming page START
panel = ttk.Frame(window, height=700,
                  width=600)
panel.pack()
head_label = ttk.Label(panel, text='Goniometer',
                       foreground='#857f72', font=(font, size, weight))
desc_label = ttk.Label(panel, text='Best app for measuring the contact angle of your fluids',
                       foreground='#BB86FC', font=(font, 20, weight))
measure_button = ttk.Button(panel, text="Measure! ",
                            style='success.Outline.TButton', width=30, command=measure_command)
exit_button = ttk.Button(panel, text="Exit",
                         style='danger.Outline.TButton', width=30, command=exit_command)
credentials_label = ttk.Label(panel, text='powerd by BME ® 2020/2021',
                              foreground='#BB86FC', font=(font, 10, weight))


picture = ImageTk.PhotoImage(Image.open('rsz_capture.png'))
picture_panel = ttk.Label(panel, image=picture)
picture_panel.photo = picture
picture_panel.grid(row=2, column=0, pady=(30, 10))

head_label.grid(row=0, column=0, pady=(30, 10))
desc_label.grid(row=1, column=0)
measure_button.grid(row=3, column=0, pady=(50, 10))
exit_button.grid(row=4, column=0)
credentials_label.grid(row=5, column=0, pady=(100, 10))
# Welcoming page END
panel_ = ttk.Frame(window, height=700,
                   width=800)
panel_.pack()
place_holder_picture = ImageTk.PhotoImage(Image.open('Capture.png'))
measurement_picture_frame = ttk.Label(panel_, image=place_holder_picture)
measurement_picture_frame.grid(row=0, column=0, sticky='s')

button_panel = ttk.Frame(panel_)
button_panel.grid(row=0, column=1, padx=50)

upload_button = ttk.Button(button_panel, text="Upload picture ",
                           style='warning.Outline.TButton', width=30, command=upload_command)
row = 0
upload_button.grid(row=row, column=2, sticky='e', pady=15)
row += 1
run_button = ttk.Button(button_panel, text="Measure ",
                        style='success.Outline.TButton', width=30, command=run_command)
run_button.grid(row=row, column=2, sticky='e', pady=15)
row += 1
remove_button = ttk.Button(button_panel, text="Remove picture ",
                           style='danger.Outline.TButton', width=30, command=remove_command)
remove_button.grid(row=row, column=2, sticky='e', pady=15)
row += 1
save_button = ttk.Button(button_panel, text="Save measurment",
                         style='info.Outline.TButton', width=30, command=save_commad)
save_button.grid(row=row, column=2, sticky='e', pady=15)
back_button = ttk.Button(button_panel, text="Go back ",
                         style='primary.Outline.TButton', width=30, command=get_back_command)
row += 1
back_button.grid(row=row, column=2, sticky='e', pady=15)


angle_label = ttk.Label(
    panel_, text="Contact angle of current measurment is: ",
    foreground='#BB86FC', font=(font, 20, weight))
angle_label.grid(row=1, column=0, pady=40)

window.minsize(1200, 600)
window.maxsize(1400, 700)
get_back_command()
window.mainloop()
