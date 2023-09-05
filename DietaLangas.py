import tkinter as tk
import sqlite3
import tkinter.font as tkFont

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

def atnaujinti(recipes):
    listas.delete(0, tk.END)
    for receptas in recipes:
        recepto_pav = receptas[0]
        listas.insert(tk.END, f"Pavadinimas: {recepto_pav}, Paruošimo laikas: {receptas[1]} min")

def parodyti_recepta(event):
    selected_index = listas.curselection()
    if selected_index:
        selected_recipe = recipes[selected_index[0]]
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = selected_recipe

        isokantis = tk.Toplevel(langas)
        isokantis.title("Recepto Informacija")
        isokantis.geometry("1200x600")
        fontas = tkFont.Font(size=12)
        text_widget = tk.Text(isokantis, wrap=tk.WORD, font=fontas)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        details_text = f"Pavadinimas: {pavadinimas}\nParuošimo laikas: {paruosimo_laikas} min\n" \
                       f"Porcijos dydis: {porcijos}\nIngredientai:\n {ingredientai}\nInstrukcija:\n {instrukcija}" \
                       f"\nNuotrauka: {nuotrauka}"
        text_widget.insert(tk.END, details_text)
        text_widget.tag_configure("bold", font=(fontas.actual("family"), fontas.actual("size"), "bold"))
        text_widget.tag_add("bold", "1.0", "1.13")
        text_widget.tag_add("bold", "2.0", "2.17")
        text_widget.tag_add("bold", "3.0", "3.15")
        text_widget.tag_add("bold", "4.0", "4.16")
        text_widget.tag_add("bold", "15.0", "15.15")

def pasirinkti():
    pasirinkta_dieta = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    if not pasirinkta_dieta:
        pasirinktas_t.set("Pasirinkite bent vieną")
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
        conn.close()

        atnaujinti(recipes)

def alergijos():
    global recipes
    conn = sqlite3.connect('Receptai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pavadinimas FROM alergijos')
    options = cursor.fetchall()
    conn.close()
    return options

def pasirinkti_alergijas():
    pasirinktos_alergijos = [options[i][0] for i, var in enumerate(option_vars_alergijos) if var.get()]
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

        atnaujinti(recipes)

langas = tk.Tk()
langas.title("Pasirinkite patiekalą")

options = duomenys()
option_vars = [tk.BooleanVar() for _ in options]

checkboxes = []
for i, option_name in enumerate(options):
    checkbox = tk.Checkbutton(langas, text=option_name[0], variable=option_vars[i])
    checkbox.pack(anchor='w')
    checkboxes.append(checkbox)

mygtukas = tk.Button(langas, text="Pasirinkti", command=pasirinkti, font=("Ariel", 11))
mygtukas.pack()

pasirinktas_t = tk.StringVar()
pasirinktas = tk.Label(langas, textvariable=pasirinktas_t)
pasirinktas.pack()

listas = tk.Listbox(langas, width=80, height=10, font=("Arial", 14))
listas.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(langas, orient=tk.VERTICAL, command=listas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listas.config(yscrollcommand=scrollbar.set)


listas.bind('<Double-Button-1>', parodyti_recepta)


options_alergijos = alergijos()
option_vars_alergijos = [tk.BooleanVar() for _ in options_alergijos]

checkboxes_alergijos = []
for i, option_name in enumerate(options_alergijos):
    checkbox = tk.Checkbutton(langas, text=option_name[0], variable=option_vars_alergijos[i])
    checkbox.pack(anchor='w')
    checkboxes_alergijos.append(checkbox)

mygtukas_alergijos = tk.Button(langas, text="Pasirinkti su alergijomis", command=pasirinkti_alergijas, font=("Ariel", 11))
mygtukas_alergijos.pack()

pasirinktas_t_alergijos = tk.StringVar()
pasirinktas_alergijos = tk.Label(langas, textvariable=pasirinktas_t_alergijos)
pasirinktas_alergijos.pack()

langas.mainloop()