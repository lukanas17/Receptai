from tkinter import *
# Pagrindinis Puslapis
langas = Tk()
langas.title("Receptai be interneto")
langas.geometry('800x180')

# Funkcijos

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


# Migtukai, label ir paieška
title_label = Label(langas, text="Gamink skaniai net ir dingus internetui!", font=("Helvetica", 18))
title_label.pack()

paieska_l = Label(langas,font=("Helvetica", 12), text="Ieškoti pagal tekstą:")
paieska_l.pack()

paieska = Entry(langas, width=60)
paieska.pack()

paieska_m = Button(langas,font=("Ariel", 12), text="Ieškoti")
paieska_m.pack()

kategorijos_label = Label(text="Ieškoti pagal:", font=("Helvetica", 13))
kategorijos_label.pack()

mygtuku_frame = Frame(langas)
mygtuku_frame.pack()

button_font = ("Helvetica", 16)

ingredientai = Button(mygtuku_frame, text="Ingredientus", font=button_font, width=11, height=2, command=ingredientus)
ingredientai.pack(side=LEFT)

dietos = Button(mygtuku_frame, text="Dietos, alergijos ir netoleravimas",
                font=button_font, width=27, height=2, command=dieta)
dietos.pack(side=LEFT)

visi_receptai = Button(mygtuku_frame, text="Visi receptai", command=visi, font=button_font,width=11, height=2)
visi_receptai.pack(side=LEFT)

langas.mainloop()