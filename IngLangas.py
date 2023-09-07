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
    cursor.execute('SELECT pavadinimas FROM ingredientai')
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

# Atnaujinti listboxą


def atnaujinti(recipes):
    reciptu_list.delete(0, tk.END)
    for receptas in recipes:
        recepto_pav = receptas[0]
        reciptu_list.insert(tk.END, f"{recepto_pav} - {receptas[1]}min")
        reciptu_list.bind('<Double-Button-1>', lambda event, recepto_pav=recepto_pav: parodyti_recepta(recepto_pav))

# Ijungti receptą ant jo du kartus paspaudus


def parodyti_recepta(recepto_pav):
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

    selected_index = reciptu_list.curselection()
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

# atidaryti migtuko funkcija


def atidaryti_recepta():
    selected_index = reciptu_list.curselection()
    if selected_index:
        selected_text.set("")
        selected_recipe = reciptu_list.get(selected_index[0])
        selected_recipe_name = selected_recipe.split(" - ")[0]
        parodyti_recepta(selected_recipe_name)
    else:
        selected_text.set("Nieko nepasirinkote")
# Funkcija parodanti receptus pagal pasirinktus checkboxus


def parodyti():
    global recipes
    pasirinkti_ingredientai = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    if not pasirinkti_ingredientai:
        selected_text.set("Pasirinkite bent vieną ingredientą")
    else:
        selected_text.set("")
        conn = sqlite3.connect('Receptai.db')
        cursor = conn.cursor()

        query = """
        SELECT r.pavadinimas, r.paruosimo_laikas, r.porcijos, r.ingredientai, r.instrukcija, r.nuotrauka
        FROM receptai AS r
        JOIN receptai_ingredientai AS ri ON r.id = ri.receptas_id
        JOIN ingredientai AS i ON ri.ingredientas_id = i.id
        WHERE i.pavadinimas IN ({})
        GROUP BY r.pavadinimas, r.paruosimo_laikas
        HAVING COUNT(DISTINCT i.pavadinimas) = ?
        """.format(', '.join(['?'] * len(pasirinkti_ingredientai)))

        cursor.execute(query, pasirinkti_ingredientai + [len(pasirinkti_ingredientai)])
        recipes = cursor.fetchall()
        conn.close()
        if not recipes:
            reciptu_list.delete(0, tk.END)
            selected_text.set("Receptų su tokia ingredientų kombinacija dar nėra")
        else:
            selected_text.set("")
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
checkbox_frame.grid(row=0, column=0, sticky='w')
checkboxes = []
for i, option_name in enumerate(options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option_name[0], variable=option_vars[i], bg='white')
    checkbox.grid(row=i, column=0, sticky='w')
    checkboxes.append(checkbox)

patvirtinimo_b = tk.Button(langas, text="Pasirinkti", command=parodyti, font=("Ariel", 11))
patvirtinimo_b.grid(row=1, column=0, sticky='w', padx=30, pady=10)
patvirtinimo_ba = tk.Button(langas, text="Atidaryti", command=atidaryti_recepta, font=("Ariel", 11))
patvirtinimo_ba.grid(row=2, column=1, sticky='e', padx=50, pady=0)
reciptu_list = tk.Listbox(langas, width=60, height=10, font=("Arial", 14))
reciptu_list.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

scrollbar = tk.Scrollbar(langas, orient=tk.VERTICAL, command=reciptu_list.yview)
scrollbar.grid(row=0, column=2, sticky="sn")

selected_text = tk.StringVar()
selected_label = tk.Label(langas, textvariable=selected_text, font=("Ariel", 16))
selected_label.grid(row=2, column=0, columnspan=2, pady=10)

langas.grid_rowconfigure(0, weight=1)
langas.grid_rowconfigure(1, weight=1)
langas.grid_columnconfigure(1, weight=1)

langas.mainloop()