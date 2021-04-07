# hlani program

import tkinter as tk
from tkinter import ttk, StringVar, NORMAL, CENTER, N, S, E, W
from tkinter import LEFT, NO, DISABLED, NORMAL, YES
import tkinter.messagebox

import new_student as ns
import prace_s_db
import nastaveni


class slovnik:

    def __init__(self):
        self.seznam_studentu = []
        self.nacti_studenty()
        self.jazyky_studenta = []
        self.akt_jazyk = ""
        self.seznam_ucebnic = []

    def nacti_studenty(self):
        try:
            prace_s_db.overeni_sl()
        except:
            self.seznam_studentu = []
        else:
            self.seznam_studentu = prace_s_db.seznam_studentu()

class slovnikGUI(tk.Frame):

    def __init__(self, parent, slovnik):
        super().__init__(parent)
        self.parent = parent
        self.slovnik = slovnik
        self.parent.title("Slovnik")
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()
        self.zobraz()


    def create_widgets(self):
        self.uzivatel = tk.Label(root, text="", font="Arial 16", fg="red")
        self.uzivatel.grid(row=0, columnspan=3, sticky=W+E)
        self.kdo = tk.LabelFrame(root, text="Kdo jsi", font="Arial 8")
        self.kdo.grid(row=1, column=0, sticky=W)

        self.tree_zaznamy = ttk.Treeview(self.kdo, column=("student"), height=8, selectmode='browse')
        self.tree_zaznamy['show'] = 'headings' # schová první sloupec s identifikátorem
        self.tree_zaznamy.grid(row=2, column=0)
        
        self.tree_zaznamy.heading("#0", text="#")
        self.tree_zaznamy.column("#0", width=0, stretch=NO, anchor='center')

        self.tree_zaznamy.heading("student", text="Student")
        self.tree_zaznamy.column("student", minwidth=0, width=124, stretch=NO, anchor='center')


        self.jazyky = tk.LabelFrame(root, text="Testovat jazyk", font="Arial 8")
        self.jazyky.grid(row=1, column=1, sticky=N)
         # připravené "pole pro RdaioButtony" se seznamem jazyků vybraného studenta, zatím prázdné
        self.j_studenta = tk.Label(self.jazyky, text="", font="Arial 8")






        self.button_NacistStudenta = tk.Button(root, text="Načti studenta", command=self.nacti_studenta, fg="blue", font="Arial 8", width=20)
        self.button_NacistStudenta.grid(row=8, column=0, sticky=W)

        self.button_Konec = tk.Button(root, text="Nový student", command=self.novy_student, fg="blue", font="Arial 8", width=20)
        self.button_Konec.grid(row=9, column=0, sticky=W)

        self.button_Konec = tk.Button(root, text="Konec", command=self.on_close, fg="red", font="Arial 8", width=20)
        self.button_Konec.grid(row=10, column=0, sticky=W)

    def create_widgets_jazyk(self):
        pozice = 1 # pozice řádky v rámci skupiny RadioButtonu
        self.akt_jazyk = StringVar()
        # smaže prvek pro výpis
        # aby se vynuloval a zobrazolo se to jen pro daného studenta a nemotaly se tam předchozí jazyky
        self.jazyky.destroy()
        # a tady se to vytváří znova - "pole pro RadioButtony", buhužel to nehezky přeblikává
        self.jazyky = tk.LabelFrame(root, text="Testovat jazyk", font="Arial 8")
        self.jazyky.grid(row=1, column=1, sticky=N)

        # pokud má student nastavený akt_jazyk, už bude předvybraný
        # self.akt_jazyk = prace_s_db.akt_jazyk_studenta(self.akt_student)

        for jazyk in self.jazyky_studenta:
            self.j_studenta = tk.Radiobutton(self.jazyky, indicatoron=0, text=jazyk, variable=self.akt_jazyk, command=self.nacti_ucebnice, value=jazyk, width = 20)
            self.j_studenta.grid(row=pozice, column=0, sticky=W)
            if jazyk == self.akt_jazyk:
                self.j_studenta.select()
            else:
                self.j_studenta.deselect()
            pozice = pozice + 1

    def create_widgets_ucebnice(self):
        self.ucebnice = tk.LabelFrame(root, text="Učebnice", font="Arial 8")
        self.ucebnice.grid(row=1, column=2, sticky=N)
        self.ucebnice_ListBox = tk.Listbox(self.ucebnice, width=20)
        self.ucebnice_ListBox.bind( "<ButtonRelease-1>", self.nacti_lekce)  # po kliknutí se načtou slovíčka z dané učebnice
        self.ucebnice_ListBox.grid(row=2, column=2, sticky=W)


    def create_ovl_sekce(self):
        self.pole_nastaveni = tk.LabelFrame(root, text="Nastavení", font="Arial 8")
        self.pole_nastaveni.grid(row=1, column=3, sticky=N)
        self.nastav = tk.Label(self.pole_nastaveni, text="", font="Arial 8")

        self.button_Nastaveni = tk.Button(self.pole_nastaveni, text="Nastavení studenta", command=self.nastaveni_stud, fg="blue", font="Arial 8", width=20)
        self.button_Nastaveni.grid(row=2, column=2, sticky=W)





    def nastaveni_stud(self):
        nastaveni.nastav_studenta(self)


    def novy(self):
        self.novy = ns.ulozit_noveho_studenta(self)
        if self.novy == None:
            return
        prace_s_db.pridat_studenta(self.novy)
        self.slovnik.nacti_studenty()
        self.zobraz()
        return


    def novy_student(self):
        """
        Otevře okno pro registraci studenta
        """
        ns.zaloz_studenta(self)


    def nacti_studenta(self):
        """
        Nacte jazyky studenta
        """
        # urci vybranou pozici polozky a z toho pak hodnotu dane polozky
        try:
            self.akt_student = self.tree_zaznamy.item(self.tree_zaznamy.focus())["values"][0]
            self.jazyky_studenta = prace_s_db.jazyky_studenta(self.akt_student)
            self.create_widgets_jazyk()
            self.create_ovl_sekce()
            self.uzivatel["text"] = "Aktuální uživatel je "+self.akt_student
        except :
            tk.messagebox.showwarning("ERROR", "Něco se nezdařilo.")
            return

        

    def nacti_ucebnice(self):
        # print(self.akt_jazyk.get(), end=": ")
        self.seznam_ucebnic = prace_s_db.seznam_ucebnic(self.akt_jazyk.get())
        self.create_widgets_ucebnice()
        for ucebnice in self.seznam_ucebnic:
            self.ucebnice_ListBox.insert(1, ucebnice)
       

    def nacti_lekce(self, event):
        try:
            self.akt_ucebnice = self.seznam_ucebnic[self.ucebnice_ListBox.curselection()[0]]
            print("Učebnice: ", self.akt_ucebnice, end=": ")
            self.seznam_lekci = prace_s_db.seznam_lekci(self.akt_ucebnice)
            print(self.seznam_lekci)
        except:
            tk.messagebox.showwarning("ERROR", "Není vybraná učebnice.")
            return
        



    def zobraz(self):
        for ii in self.tree_zaznamy.get_children():
            self.tree_zaznamy.delete(ii)

        pozice = 0
        for zaznam in self.slovnik.seznam_studentu:
            self.tree_zaznamy.insert("", "end", text=pozice, values=zaznam)
            pozice += 1

    # zavřít
    def on_close(self):
       self.parent.destroy()


    
if __name__ == '__main__':
    root = tk.Tk()
    slovnik = slovnik()
    app = slovnikGUI(root, slovnik)
    app.mainloop()
