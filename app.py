import tkinter as tk
from tkinter import filedialog, Label, Frame, font, Toplevel, Text, Scrollbar
from csvConvert import remove_spaces
from csv_to_json import convert_csv_to_json
from create_structured_csv import create_structured_csv
from create_structured_KTL import create_structured_ktl

def main():
    root = tk.Tk()
    root.title("CSV zu JSON Konverter")

    main_frame = Frame(root, padx=20, pady=20)
    main_frame.pack(padx=10, pady=10, expand=True, fill="both")

    instruction_font = font.Font(size=10, weight="bold")
    instruction_label = Label(main_frame, text="1. Klicken Sie auf den Button, um eine CSV-Datei auszuwählen.\n"
                                               "2. Den Speicherort und Namen auswählen.",
                              font=instruction_font)
    instruction_label.pack(pady=10)

    def show_error(error_message):
        error_window = Toplevel(root)
        error_window.title("Fehlermeldung")
        
        text_area = Text(error_window, wrap="word", height=10, width=50)
        text_area.insert(tk.END, error_message)
        text_area.pack(padx=10, pady=10)

        scrollbar = Scrollbar(error_window, command=text_area.yview)
        scrollbar.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scrollbar.set)

    def open_file(conversion_function):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not file_path:
                raise ValueError("Keine CSV-Datei ausgewählt!")
            
            if not file_path.endswith('.csv'):
                raise ValueError("Bitte wählen Sie eine gültige CSV-Datei aus!")
            
            remove_spaces(file_path)
            data = convert_csv_to_json(file_path,"balbajs2.json")
            
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            
            if not save_path:
                raise ValueError("Kein Speicherort ausgewählt!")
            
            conversion_function(data, save_path)
        except Exception as e:
            show_error(str(e))

    btn_font = font.Font(size=12)
    open_csv_btn = tk.Button(main_frame, text="CSV Datei öffnen (CSV)", command=lambda: open_file(create_structured_csv), font=btn_font, bg="#4CAF50", fg="white", padx=10, pady=5)
    open_csv_btn.pack(pady=20)

    open_ktl_btn = tk.Button(main_frame, text="CSV Datei öffnen (KTL)", command=lambda: open_file(create_structured_ktl), font=btn_font, bg="#4CAF50", fg="white", padx=10, pady=5)
    open_ktl_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
