from tkinter import *
from PIL import Image, ImageTk

# Pagrindinis Puslapis
langas = Tk()
langas.title("Receptai be interneto")
langas.geometry('610x370')
langas.configure(bg="white")
# Backgroundas
image = Image.open('pics/start_page.jpg')
image = image.resize((610, 250))
photo = ImageTk.PhotoImage(image)
balta = "white"

# Funkcijos importuojančios kitus filus ir uždarančoios šitą


def ingredientus():
    langas.destroy()
    import IngLangas


def dieta():
    langas.destroy()
    import DietaLangas


def alergijas():
    langas.destroy()
    import AleLangas


def visi():
    langas.destroy()
    import VisiLangas

# Pakeisti spalvą užėjus ant migtuko ir nuėjus


def pakeisti_spalva(widget, target_color, current_color, step, steps, duration):
    if step > steps:
        widget.config(bg=target_color)
        return
    r, g, b = widget.winfo_rgb(current_color)
    r_target, g_target, b_target = widget.winfo_rgb(target_color)
    r_step = int((r_target - r) / steps)
    g_step = int((g_target - g) / steps)
    b_step = int((b_target - b) / steps)
    new_color = "#{:02X}{:02X}{:02X}".format(r + r_step, g + g_step, b + b_step)
    widget.config(bg=new_color)
    widget.after(duration // steps, pakeisti_spalva, widget, target_color, new_color, step + 1, steps, duration)


def uzeiti(event):
    pakeisti_spalva(event.widget, "light blue", balta, 1, 10, 300)


def nueiti(event):
    pakeisti_spalva(event.widget, balta, "light blue", 1, 10, 300)

# Migtukai, labels, paveikslelis


pav_label = Label(langas, text="Gamink skaniai net ir dingus internetui!", bg=balta, font=("Helvetica", 18))
pav_label.pack()

image_label = Label(langas, image=photo)
image_label.pack()

kategorijos_label = Label(text="Ieškoti pagal:", font=("Helvetica", 13), bg=balta)
kategorijos_label.pack()

migtukai = []
migtuku_frame = Frame(langas)
migtuku_frame.pack()
mygtuku_font = ("Helvetica", 16)

ingredientai = Button(migtuku_frame, text="Ingredientus",
                      command=ingredientus, font=mygtuku_font, width=11, height=2, bg=balta)
migtukai.append(ingredientai)
ingredientai.pack(side=LEFT)
ingredientai.bind("<Enter>", uzeiti)
ingredientai.bind("<Leave>", nueiti)

dietos = Button(migtuku_frame, text="Dietos, alergijos ir netoleravimas", command=dieta,
                font=mygtuku_font, width=27, height=2, bg=balta)
migtukai.append(dietos)
dietos.pack(side=LEFT)
dietos.bind("<Enter>", uzeiti)
dietos.bind("<Leave>", nueiti)

visi_receptai = Button(migtuku_frame, text="Visi receptai", command=visi,
                       font=mygtuku_font, width=11, height=2, bg=balta)
migtukai.append(visi_receptai)
visi_receptai.pack(side=LEFT)
visi_receptai.bind("<Enter>", uzeiti)
visi_receptai.bind("<Leave>", nueiti)

langas.mainloop()
