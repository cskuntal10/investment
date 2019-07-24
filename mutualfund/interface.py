import tkinter as tk

from core import get_investment_suggestions, invest
from consts import  MF_DETAILS

class InvestMenu(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root,  *args, **kwargs)

        label_scheme = tk.Label(self, text="Scheme")
        label_amount = tk.Label(self, text="Amount")
        label_scheme.grid(row=0, column=0, ipadx=5, pady=5, sticky=tk.W + tk.N)
        label_amount.grid(row=1, column=0, ipadx=5, pady=5, sticky=tk.W + tk.N)

        self.schem_options = tk.StringVar(self)
        OPTIONS = list(MF_DETAILS.keys())
        self.schem_options.set(OPTIONS[0])
        self.entry_scheme = tk.OptionMenu(self, self.schem_options, *OPTIONS)
        self.entry_amount = tk.Entry(self)

        self.entry_scheme.grid(row=0, column=1, ipadx=5, pady=5, sticky=tk.W + tk.N)
        self.entry_amount.grid(row=1, column=1, ipadx=5, pady=5, sticky=tk.W + tk.N)

        MyButton1 = tk.Button(self, text="Submit", width=10, command=self.invest)
        MyButton1.grid(row=2, column=1)

    def invest(self):
        fund=self.schem_options.get()
        amount=self.entry_amount.get()
        invest(fund,amount)
        print("Invested today")


class SuggestionMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        suggestions = get_investment_suggestions()
        table_header = ['date', 'fund', 'nav', 'units', 'amount', 'yday_nav', 'nav_change(%)', 'index_today']
        if suggestions:
            title_label = tk.Label(self, borderwidth=1, relief="solid", text = 'Last Investment Details', width=62)
            title_label.grid(row=0, column=0, columnspan=5, sticky=tk.W)
            today_label = tk.Label(self, borderwidth=1, relief="solid", text='Today Change', width=37)
            today_label.grid(row=0, column=5, columnspan=3, sticky=tk.W)
            for row in range(len(table_header)):
                header_label = tk.Label(self, borderwidth=1, relief="solid", text = table_header[row].upper(), width=12, anchor='w')
                header_label.grid(row=1, column=row, sticky=tk.W)

            num_rows = len(suggestions)
            num_cols = len(list(suggestions[0].keys()))
            for row in range(num_rows):
                for column in range(num_cols):
                    label = tk.Label(self, borderwidth=1, relief="solid", text=suggestions[row].get(table_header[column]), width=12, anchor='w')
                    label.grid(row=row+2, column=column, sticky=tk.N)


def _main_window():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.geometry("1000x500")
    root.title('Money Guru')
    return root


def start_ui():
    root=_main_window()
    invest_menu = InvestMenu(root, borderwidth=2, relief="solid")
    suggest_menu = SuggestionMenu(root, borderwidth=1, relief="solid")
    invest_menu.grid(padx=10, pady=20)
    suggest_menu.grid(padx=10, pady=20)
    root.mainloop()