import tkinter as tk
import sqlite3
import tkinter.font as tkFont

def duomenys():
    connection = sqlite3.connect("Receptai.db")
    cursor = connection.cursor()
    cursor.execute("SELECT pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka FROM receptai")
    data = cursor.fetchall()
    connection.close()
    return data


def atnaujinti():
    data = duomenys()
    listas.delete(0, tk.END)
    for item in data:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = item
        listas.insert(tk.END, f"{pavadinimas} - {paruosimo_laikas}min.")
        listas.item_data.append(item)


def parodyti(event):
    selected_text = listas.get(listas.curselection())
    for item in listas.item_data:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = item
        if selected_text.startswith(pavadinimas):
            isokantis = tk.Toplevel(Langas)
            isokantis.title("Recepto Informacija")
            isokantis.geometry("1200x600")
            fontas = tkFont.Font(size=12)
            text_widget = tk.Text(isokantis, wrap=tk.WORD, font=fontas)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            details_text = f"Pavadinimas: {pavadinimas}\nParuošimo laikas: {paruosimo_laikas}min\n" \
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
            break

#Sutvarkyti paieska

def pasirinkti():
    parodyti(None)

def ieskoti_recepto():
    search = paieska.get().strip()
    data = duomenys()
    listas.delete(0, tk.END)
    for item in data:
        pavadinimas, paruosimo_laikas, porcijos, ingredientai, instrukcija, nuotrauka = item
        if search.lower() in pavadinimas.lower():
            listas.insert(tk.END, f"{pavadinimas} - {paruosimo_laikas}min.")
            listas.item_data.append(item)

Langas = tk.Tk()
Langas.title("Receptai")

listas = tk.Listbox(Langas, width=50, height=10, font=("Arial", 14))
listas.pack()

pa_migtukas = tk.Button(Langas, text="Pasirinkti", command=pasirinkti, padx=10, pady=5, font=("Arial", 11, "bold"))
pa_migtukas.pack(side=tk.LEFT)

paieskos_m = tk.Button(Langas, text="Ieškoti", command=ieskoti_recepto, padx=10, pady=5, font=("Arial", 11, "bold"))
paieskos_m.pack(side=tk.RIGHT)

paieska = tk.Entry(Langas, width=30, font=("Arial", 14))
paieska.bind("<Return>", lambda event=None: ieskoti_recepto())
paieska.pack(side=tk.RIGHT)

listas.item_data = []
listas.bind("<Double-Button-1>", parodyti)
atnaujinti()

Langas.mainloop()