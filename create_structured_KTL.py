import json
import csv


def create_structured_ktl(data_list, output_csv_path):
    # CSV-Datei vorbereiten
    csv_columns = ["PDS", "ANZ_S"]
    auspr_keys = set()  # Ein Set wird verwendet, um doppelte Einträge zu vermeiden.

    # Alle Schlüssel (z.B. D579, D573, ...) sammeln
    for entry in data_list:
        for auspr_list in entry["AUSPRAEGUNG"].values():
            for auspr in auspr_list:
                # Überprüfen, ob AUSPR2 nicht "ETM_NR" ist, bevor es zum Set hinzugefügt wird.
                if auspr["AUSPR2"] != "ETM_NR":
                    auspr_keys.add(auspr["AUSPR2"])

    # Die gesammelten AUSPR2-Werte werden zu den Spaltennamen hinzugefügt.
    for key in sorted(auspr_keys):
        csv_columns.extend([key, f"{key}.MW_A_PR", f"{key}.MW_M_PR", f"{key}.MW_A_PW", f"{key}.MW_M_PW"])

    # CSV-Datei schreiben
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()  # Die Spaltennamen werden als Kopfzeile geschrieben.
        
        for entry in data_list:
            row = {"PDS": entry["PDS"], "ANZ_S": entry["ANZ_S"]}  # Grundlegende Daten werden initialisiert.
            
            for auspr_list in entry["AUSPRAEGUNG"].values():
                for auspr in auspr_list:
                    # Überprüfen, ob AUSPR2 nicht "ETM_NR" ist, bevor weitere Aktionen durchgeführt werden.
                    if auspr["AUSPR2"] != "ETM_NR":
                        row[auspr["AUSPR2"]] = int(auspr["ANZ_UG"])
                        # Die vier zusätzlichen Eigenschaften werden gelesen und zur Zeile hinzugefügt.
                        row[f"{auspr['AUSPR2']}.MW_A_PR"] = auspr["MW_A_PR"]  # Wenn der Wert nicht vorhanden ist, wird ein leerer String gesetzt.
                        row[f"{auspr['AUSPR2']}.MW_M_PR"] = auspr["MW_M_PR"]
                        row[f"{auspr['AUSPR2']}.MW_A_PW"] = auspr["MW_A_PW"]
                        row[f"{auspr['AUSPR2']}.MW_M_PW"] = auspr["MW_M_PW"]
            
            # Die zusammengestellte Zeile wird in die CSV-Datei geschrieben.
            writer.writerow(row)
    return output_csv_path