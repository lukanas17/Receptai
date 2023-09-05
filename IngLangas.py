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
        reciptu_list.insert(tk.END, f"{recepto_pav} - {receptas[1]}min")
        reciptu_list.bind('<Double-Button-1>', lambda event, recepto_pav=recepto_pav: parodyti_recepta(recepto_pav))

def parodyti_recepta(recepto_pav):
    selected_index = reciptu_list.curselection()
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
        scrollbar = tk.Scrollbar(isokantis, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

def parodyti():
    global recipes
    pasirinkti_ingredientai = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    if not pasirinkti_ingredientai:
        selected_text.set("Pasirinkti bent vieną ingredientą")
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


langas = tk.Tk()
langas.title("Pasirinkite patiekalą")

options = duomenys()
option_vars = [tk.BooleanVar() for _ in options]

# Create a frame to hold the checkboxes
checkbox_frame = tk.Frame(langas)
checkbox_frame.grid(row=0, column=0, sticky='w')

checkboxes = []
for i, option_name in enumerate(options):
    checkbox = tk.Checkbutton(checkbox_frame, text=option_name[0], variable=option_vars[i])
    checkbox.grid(row=i, column=0, sticky='w')
    checkboxes.append(checkbox)

patvirtinimo_b = tk.Button(langas, text="Pasirinkti", command=parodyti,font=("Ariel", 11))
patvirtinimo_b.grid(row=1, column=0, sticky='w', padx=30, pady=10)

# Create the Listbox widget, but initially, keep it empty
reciptu_list = tk.Listbox(langas, width=60, height=10, font=("Arial", 14))
reciptu_list.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew', )

selected_text = tk.StringVar()
selected_label = tk.Label(langas, textvariable=selected_text, font=("Ariel", 16))
selected_label.grid(row=2, column=0, columnspan=2, pady=10)

# Configure grid weights for proper resizing
langas.grid_rowconfigure(0, weight=1)
langas.grid_rowconfigure(1, weight=1)
langas.grid_columnconfigure(1, weight=1)

langas.mainloop()