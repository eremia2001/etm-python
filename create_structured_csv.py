import csv

def create_structured_csv(data_list, output_csv_path):
    # Starten mit den Basis-Feldnamen für die CSV-Datei
    fieldnames = ["PDS", "ANZ_S"]
    auspr_counter = data_list[0]['auspr_counter']
    # Durchlaufe alle JSON-Einträge, um die Feldnamen (Spalten) für die CSV zu sammeln
    for pds_data in data_list:
        for auspr_name, auspr_list in pds_data['AUSPRAEGUNG'].items():
            for rts_typ in [0, 1, 3, 4, 9]:
                col_name = f"RTS_{auspr_name}.{rts_typ}"
                if col_name not in fieldnames:  # Überprüfe, ob der Spaltenname bereits in der Liste ist
                    fieldnames.append(col_name)
                if rts_typ in [3, 4]:
                    for suffix in ["MW_A_PR", "MW_M_PR", "MW_A_PW", "MW_M_PW"]:
                        new_col_name = f"{col_name}.{suffix}"
                        if new_col_name not in fieldnames:  
                            fieldnames.append(new_col_name)


    # Öffne (oder erstelle) die CSV-Datei zum Schreiben
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_outfile:
        writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)
        writer.writeheader()

        for pds_data in data_list:
            row = {"PDS": pds_data["PDS"], "ANZ_S": pds_data['ANZ_S']}
            counter = 1
            for auspr_name, auspr_list in pds_data['AUSPRAEGUNG'].items():
                for auspr_data in auspr_list:
                    # Überprüfe, ob der Wert von AUSPR2 "ETM_NR" ist
                    if auspr_data["AUSPR2"] == "ETM_NR":
                        rts = int(auspr_data["RTS_TYP1"])  # Konvertiere den Wert in einen Integer
                        col_name = f"RTS_{auspr_name}.{rts}"
                        row[col_name] = auspr_data["ANZ_UG"]
                        # Wenn der Typ 3 oder 4 ist, füge die Werte für die vier zusätzlichen Spalten hinzu
                        if rts in [3, 4]:
                            for suffix in ["MW_A_PR", "MW_M_PR", "MW_A_PW", "MW_M_PW"]:
                                # Ersetze Komma durch Punkt und speichere den Wert in der CSV-Datei
                                value = auspr_data[suffix]
                                row[f"{col_name}.{suffix}"] = value
                counter +=1
            writer.writerow(row)

    return output_csv_path
