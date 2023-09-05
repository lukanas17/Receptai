import tkinter as tk
import sqlite3
import tkinter.font as tkFont

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


def atnaujinti(recipes):
    reciptu_list.delete(0, tk.END)
    for receptas in recipes:
        recepto_pav = receptas[0]
        reciptu_list.insert(tk.END, f"Pavadinimas: {recepto_pav}, Paruošimo laikas: {receptas[1]} min")
        reciptu_list.bind('<Double-Button-1>', lambda event, recepto_pav=recepto_pav: parodyti_recepta(recepto_pav))

def parodyti_recepta(recepto_pav):
    pasirinkti = receptai(recepto_pav)
    if pasirinkti:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = pasirinkti

        issokantis = tk.Toplevel(langas)
        issokantis.title("Recepto Informacija")
        issokantis.geometry("800x600")
        fontas = tkFont.Font(size=12)
        text_widget = tk.Text(issokantis, wrap=tk.WORD, font=fontas)
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

        # Create a vertical scrollbar and attach it to the Text widget
        scrollbar = tk.Scrollbar(issokantis, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

def patvirtinti():
    global reciptu_list  # Use the global variable
    pasirinkti_ingredientai = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    if not pasirinkti_ingredientai:
        selected_text.set("Pasirinkti bent vieną ingredientą")
    else:
        conn = sqlite3.connect('Receptai.db')
        cursor = conn.cursor()

        query = """
        SELECT r.pavadinimas, r.paruosimo_laikas
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

        patiekalai = tk.Toplevel(langas)
        patiekalai.title("Pasirinkti patiekalai")
        patiekalai.geometry("800x400")

        reciptu_list = tk.Listbox(patiekalai, width=80, height=10, font=("Arial", 14))
        reciptu_list.pack()

        if not recipes:
            reciptu_list.destroy()
            patiekalai.geometry("370x60")
            nera = tk.Label(patiekalai, text="Receptų su tokia ingredientų kombinacija - nėra",
                            font=("Ariel", 12, "bold"))
            uzdaryti = tk.Button(patiekalai, text="Uždaryti", command=patiekalai.destroy)
            nera.pack()
            uzdaryti.pack()

        else:
            # Update the Listbox with the selected recipes
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


patvirtinimo_b = tk.Button(langas, text="Pasirinkau!", command=patvirtinti)
patvirtinimo_b.pack()


selected_text = tk.StringVar()
selected_label = tk.Label(langas, textvariable=selected_text)
selected_label.pack()


langas.mainloop()