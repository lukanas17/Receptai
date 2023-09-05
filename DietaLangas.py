import tkinter as tk
import sqlite3


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
    cursor.execute('SELECT r.pavadinimas, r.paruosimo_laikas, r.porcijos, r.ingredientai, r.instrukcija, r.nuotrauka '
                   'FROM receptai AS r '
                   'JOIN receptai_dieta AS rd ON r.id = rd.receptas_id '
                   'JOIN dietos AS d ON rd.dieta_id = d.id '
                   'WHERE d.pavadinimas = ?', (recepto_pav,))
    recepto_d = cursor.fetchall()
    conn.close()
    return recepto_d


def atnaujinti(recipes):
    listas.delete(0, tk.END)
    for receptas in recipes:
        recepto_pav = receptas[0]
        listas.insert(tk.END, f"Pavadinimas: {recepto_pav}, Paruošimo laikas: {receptas[1]} min")


def pasirinkti():
    global listas
    pasirinkta_dieta = [options[i][0] for i, var in enumerate(option_vars) if var.get()]
    if not pasirinkta_dieta:
        pasirinktas_t.set("Pasirinkite bent vieną")
    else:
        conn = sqlite3.connect('Receptai.db')
        cursor = conn.cursor()

        query = """
        SELECT r.pavadinimas, r.paruosimo_laikas
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

        receptu_langas = tk.Toplevel(langas)
        receptu_langas.title("Pasirinkti patiekalai")
        receptu_langas.geometry("800x400")

        listas = tk.Listbox(receptu_langas, width=80, height=10, font=("Arial", 14))
        listas.pack()

        if not recipes:
            listas.destroy()
            receptu_langas.geometry("370x60")
            nera = tk.Label(receptu_langas, text="Nėra receptų tokiam pasirinkimui!",
                            font=("Arial", 12, "bold"))
            uzdaryti = tk.Button(receptu_langas, text="Close", command=receptu_langas.destroy)
            nera.pack()
            uzdaryti.pack()

        else:
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

mygtukas = tk.Button(langas, text="Pasirinkti", command=pasirinkti)
mygtukas.pack()

pasirinktas_t = tk.StringVar()
pasirinktas = tk.Label(langas, textvariable=pasirinktas_t)
pasirinktas.pack()


langas.mainloop()