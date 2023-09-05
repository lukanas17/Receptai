from tkinter import *
# Pagrindinis Puslapis
langas = Tk()
langas.title("Receptai")
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


def ieskoti():
    search_text = paieska.get().strip()
    langas.destroy()
    import VisiLangas
    VisiLangas.open_with_search_text(search_text)


# Migtukai, label ir paieška
title_label = Label(langas, text="Receptai", font=("Helvetica", 20))
title_label.pack()

paieska_l = Label(langas, text="Ieškoti pagal tekstą:")
paieska_l.pack()

paieska = Entry(langas, width=40)
paieska.pack()

paieska_m = Button(langas, text="Ieškoti", command=ieskoti)
paieska_m.pack()

kategorijos_label = Label(text="Ieškoti pagal kategoriją:", font=("Halvetica", 12))
kategorijos_label.pack()

mygtuku_frame = Frame(langas)
mygtuku_frame.pack()

button_font = ("Helvetica", 16)

ingredientai = Button(mygtuku_frame, text="Ingredientus", font=button_font, width=15, height=2, command=ingredientus)
ingredientai.pack(side=LEFT)

dietos = Button(mygtuku_frame, text="Dietą", font=button_font, width=10, height=2, command=dieta)
dietos.pack(side=LEFT)

Alergijos = Button(mygtuku_frame, text="Alergijas ir maisto netoleravimą", font=button_font, width=25
                   , height=2, command=alergijas)
Alergijos.pack(side=LEFT)

visi_receptai = Button(mygtuku_frame, text="Visi receptai", command=visi, font=button_font,width=10, height=2)
visi_receptai.pack(side=LEFT)

langas.mainloop()