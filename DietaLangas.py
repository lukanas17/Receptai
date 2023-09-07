import tkinter as tk
import sqlite3
import tkinter.font as tkFont
from io import BytesIO
from PIL import Image, ImageTk
import requests

# Funkcijos ištraukti duomenys iš duomenų bazės


def duomenys():
    conn = sqlite3.connect('Receptai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pavadinimas FROM dietos')
    options = cursor.fetchall()
    conn.close()
    return options


def receptai(recepto_pav):
    conn = sqlite3.connect('Receptai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka '
                   'FROM receptai '
                   'WHERE pavadinimas = ?', (recepto_pav,))
    recepto_det = cursor.fetchone()
    conn.close()
    return recepto_det

def alergijos():
    global recipes
    conn = sqlite3.connect('Receptai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pavadinimas FROM alergijos')
    options = cursor.fetchall()
    conn.close()
    return options

# Atnaujinti listboxą


def atnaujinti(recipes):
    listas.delete(0, tk.END)
    for i, receptas in enumerate(recipes):
        recepto_pav = receptas[0]
        listas.insert(tk.END, f"{recepto_pav} - {receptas[1]} min")

# Ijungti receptą ant jo du kartus paspaudus


def parodyti_recepta(event):
    def paveiksliukas(image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(frame, image=photo)
                image_label.image = photo
                image_label.grid(row=0, column=2, padx=0, pady=0)
        except Exception as e:
            print("Nepavyko užkrauti nuotraukos, error:", e)
    selected_index = listas.curselection()
    if selected_index:
        selected_recipe = recipes[selected_index[0]]
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = selected_recipe
        isokantis = tk.Toplevel(langas)
        isokantis.title("Recepto Informacija")
        isokantis.geometry("1150x450")
        frame = tk.Frame(isokantis)
        frame.pack(fill=tk.BOTH, expand=True)
        paveiksliukas(nuotrauka)
        fontas = tkFont.Font(size=12)
        text_widget = tk.Text(frame, wrap=tk.WORD, font=fontas)
        text_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        details_text = f"Pavadinimas: {pavadinimas}\nParuošimo laikas: {paruosimo_laikas} min\n" \
                       f"Porcijos dydis: {porcijos}\nIngredientai:\n {ingredientai}\n\nInstrukcija:\n\n {instrukcija}"
        text_widget.insert(tk.END, details_text)
        text_widget.tag_configure("bold", font=(fontas.actual("family"), fontas.actual("size"), "bold"))
        text_widget.tag_add("bold", "1.0", "1.13")
        text_widget.tag_add("bold", "2.0", "2.17")
        text_widget.tag_add("bold", "3.0", "3.15")
        text_widget.tag_add("bold", "4.0", "4.16")
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        text_widget.config(yscrollcommand=scrollbar.set)

# Funkcijos parodančius receptus pagal pasirinktus checkboxus


def parodyti():
    global recipes
    pasirinkta_dieta = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    if not pasirinkta_dieta:
        pasirinktas_t.set("Pasirinkite bent vieną dietą")
    else:
        conn = sqlite3.connect('Receptai.db')
        cursor = conn.cursor()

        query = """
        SELECT r.pavadinimas, r.paruosimo_laikas, r.porcijos, r.ingredientai, r.instrukcija, r.nuotrauka
        FROM receptai AS r
        WHERE r.id NOT IN (
            SELECT rd.receptas_id
            FROM receptai_dieta AS rd
            JOIN dietos AS d ON rd.dieta_id = d.id
            WHERE d.pavadinimas IN ({})
        )
        """.format(', '.join(['?'] * len(pasirinkta_dieta)))

        cursor.execute(query, pasirinkta_dieta)
        recipes = cursor.fetchall()
        if not recipes:
            listas.delete(0, tk.END)
            pasirinktas_t.set("Receptų su tokia ingredientų kombinacija dar nėra")
        else:
            pasirinktas_t.set("")
            atnaujinti(recipes)


def pasirinkti_alergijas():
    global recipes
    pasirinktos_alergijos = [options_alergijos[i][0] for i, var in enumerate(option_vars_alergijos) if var.get()]

    if not pasirinktos_alergijos:
        pasirinktas_t_alergijos.set("Pasirinkite bent vieną alergiją")
    else:
        conn = sqlite3.connect('Receptai.db')
        cursor = conn.cursor()

        query = """
        SELECT r.pavadinimas, r.paruosimo_laikas, r.porcijos, r.ingredientai, r.instrukcija, r.nuotrauka
        FROM receptai AS r
        WHERE r.id NOT IN (
            SELECT ra.receptas_id
            FROM receptai_alergijos AS ra
            JOIN alergijos AS a ON ra.alergija_id = a.id
            WHERE a.pavadinimas IN ({})
        )
        """.format(', '.join(['?'] * len(pasirinktos_alergijos)))

        cursor.execute(query, pasirinktos_alergijos)
        recipes = cursor.fetchall()
        conn.close()
        if not recipes:
            listas.delete(0, tk.END)
            pasirinktas_t_alergijos.set("Receptų su tokia ingredientų kombinacija dar nėra")
        else:
            pasirinktas_t_alergijos.set("")
            atnaujinti(recipes)


def pasirinkti_abu():
    global recipes
    pasirinkta_dieta = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    pasirinktos_alergijos = [options_alergijos[i][0] for i, var in enumerate(option_vars_alergijos) if var.get()]

    if not pasirinkta_dieta and not pasirinktos_alergijos:
        pasirinktas_t_alergijos.set("Pasirinkite bent vieną dietą ir alergiją")
    else:
        conn = sqlite3.connect('Receptai.db')
        cursor = conn.cursor()
        query = """
        SELECT r.pavadinimas, r.paruosimo_laikas, r.porcijos, r.ingredientai, r.instrukcija, r.nuotrauka
        FROM receptai AS r
        WHERE r.id NOT IN (
            SELECT rd.receptas_id
            FROM receptai_dieta AS rd
            JOIN dietos AS d ON rd.dieta_id = d.id
            WHERE (d.pavadinimas IN ({}) OR {} = 0)
        ) AND r.id NOT IN (
            SELECT ra.receptas_id
            FROM receptai_alergijos AS ra
            JOIN alergijos AS a ON ra.alergija_id = a.id
            WHERE (a.pavadinimas IN ({}) OR {} = 0)
        )
        """.format(', '.join(['?'] * len(pasirinkta_dieta)), len(pasirinkta_dieta),
                   ', '.join(['?'] * len(pasirinktos_alergijos)), len(pasirinktos_alergijos))

        cursor.execute(query, pasirinkta_dieta + pasirinktos_alergijos)
        recipes = cursor.fetchall()
        conn.close()
        if not recipes:
            listas.delete(0, tk.END)
            pasirinktas_t_alergijos.set("Pasirinkite iš abiejų pusių arba tokių receptų nėra")
        else:
            pasirinktas_t_alergijos.set("")
            atnaujinti(recipes)

# Langas, migtukai, checkboxai, labels, listboxas


langas = tk.Tk()
langas.title("Pasirinkite patiekalą")
image = Image.open('pics/ingredients.jpg')
photo = ImageTk.PhotoImage(image)
background_label = tk.Label(langas, image=photo)
background_label.place(relwidth=1, relheight=1)

options = duomenys()
option_vars = [tk.BooleanVar() for _ in options]
checkbox_frame = tk.Frame(langas, bg="white")
checkbox_frame.grid(row=0, column=0, sticky='nw')
checkbox2_frame = tk.Frame(langas, bg="white")
checkbox2_frame.grid(row=0, column=3, sticky='ne')
checkboxes = []

for i, option_name in enumerate(options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option_name[0], variable=option_vars[i], bg='white')
    checkbox.grid()
    checkboxes.append(checkbox)

options_alergijos = alergijos()
option_vars_alergijos = [tk.BooleanVar() for _ in range(len(options_alergijos))]

for i, option_name in enumerate(options_alergijos):
    checkbox = tk.Checkbutton(checkbox2_frame, text=option_name[0], variable=option_vars_alergijos[i], bg='white')
    checkbox.grid()
    checkboxes.append(checkbox)

listas = tk.Listbox(langas, width=80, height=20, font=("Arial", 14))
listas.grid(row=0, column=1, rowspan=2, sticky="nsew")

scrollbar = tk.Scrollbar(langas, orient=tk.VERTICAL, command=listas.yview)
scrollbar.grid(row=0, column=2, rowspan=1+2, sticky="ns")
listas.config(yscrollcommand=scrollbar.set)
listas.bind('<Double-Button-1>', parodyti_recepta)

mygtukas_alergijos = tk.Button(langas, text="Pasirinkti", command=pasirinkti_alergijas, font=("Ariel", 11))
mygtukas_alergijos.grid(row=2, column=3, sticky="n")
mygtukas = tk.Button(langas, text="Pasirinkti", command=parodyti, font=("Ariel", 12))
mygtukas.grid(row=2, column=0, sticky="n")
mygtukas_abu = tk.Button(langas, text="Pasirinkau iš abiejų", command=pasirinkti_abu, font=("Ariel", 11))
mygtukas_abu.grid(row=2, column=1, sticky="s")

pasirinktas_t = tk.StringVar()
pasirinktas = tk.Label(langas, textvariable=pasirinktas_t, font=("Ariel", 12))
pasirinktas.grid(row=2, column=1, sticky="sw")
pasirinktas_t_alergijos = tk.StringVar()
pasirinktas_alergijos = tk.Label(langas, textvariable=pasirinktas_t_alergijos, font=("Ariel", 12))
pasirinktas_alergijos.grid(row=2, column=1, sticky="se")

langas.grid_rowconfigure(7, weight=1)
langas.grid_columnconfigure(1, weight=1)

langas.mainloop()