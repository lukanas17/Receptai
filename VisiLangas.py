import tkinter as tk
import sqlite3
import tkinter.font as tkFont
from io import BytesIO
from PIL import Image, ImageTk
import requests

# Funkcijos ištraukti duomenys iš duomenų bazės


def duomenys():
    connection = sqlite3.connect("Receptai.db")
    cursor = connection.cursor()
    cursor.execute("SELECT pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka FROM receptai")
    data = cursor.fetchall()
    connection.close()
    return data

# Atnaujinti listboxą


def atnaujinti():
    data = duomenys()
    listas.delete(0, tk.END)
    for item in data:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = item
        listas.insert(tk.END, f"{pavadinimas} - {paruosimo_laikas}min.")
        listas.item_data.append(item)

# Ijungti receptą ant jo du kartus paspaudus


def parodyti(event):
    def paveiksliukas(image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(isokantis, image=photo)
                image_label.image = photo
                image_label.pack()
        except Exception as e:
            print("Nepavyko užkrauti nuotraukos, error:", e)

    selected_text = listas.get(listas.curselection())
    for item in listas.item_data:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = item
        if selected_text.startswith(pavadinimas):
            isokantis = tk.Toplevel(Langas)
            isokantis.title("Recepto Informacija")
            isokantis.geometry("1000x450")
            fontas = tkFont.Font(size=12)
            text_widget = tk.Text(isokantis, wrap=tk.WORD, font=fontas)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            paveiksliukas(nuotrauka)
            details_text = f"Pavadinimas: {pavadinimas}\nParuošimo laikas: {paruosimo_laikas}min\n" \
                           f"Porcijos dydis: {porcijos}\nIngredientai:\n {ingredientai}\n\nInstrukcija:\n\n {instrukcija}"
            text_widget.insert(tk.END, details_text)
            text_widget.tag_configure("bold", font=(fontas.actual("family"), fontas.actual("size"), "bold"))
            text_widget.tag_add("bold", "1.0", "1.13")
            text_widget.tag_add("bold", "2.0", "2.17")
            text_widget.tag_add("bold", "3.0", "3.15")
            text_widget.tag_add("bold", "4.0", "4.16")
            scrollbar = tk.Scrollbar(isokantis, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)
            break


# Migtukas pasirinkti


def pasirinkti():
    parodyti(None)

# Paieskos langelis


def ieskoti_recepto():
    search = paieska.get().strip()
    data = duomenys()
    listas.delete(0, tk.END)
    for item in data:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = item
        if search.lower() in pavadinimas.lower():
            listas.insert(tk.END, f"{pavadinimas} - {paruosimo_laikas}min.")
            listas.item_data.append(item)

# Langas, migtukai, labels, listas


Langas = tk.Tk()
Langas.title("Receptai")

listas = tk.Listbox(Langas, width=50, height=30, font=("Arial", 14))
listas.pack()

scrollbar = tk.Scrollbar(Langas, command=listas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listas.config(yscrollcommand=scrollbar.set)
listas.item_data = []
listas.bind("<Double-Button-1>", parodyti)

pa_migtukas = tk.Button(Langas, text="Pasirinkti", command=pasirinkti, padx=10, pady=5, font=("Arial", 11, "bold"))
pa_migtukas.pack(side=tk.LEFT)

paieskos_m = tk.Button(Langas, text="Ieškoti", command=ieskoti_recepto, padx=10, pady=5, font=("Arial", 11, "bold"))
paieskos_m.pack(side=tk.RIGHT)
paieska = tk.Entry(Langas, width=30, font=("Arial", 14))
paieska.bind("<Return>", lambda event=None: ieskoti_recepto())
paieska.pack(side=tk.RIGHT)

atnaujinti()
Langas.mainloop()