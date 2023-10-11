import csv
import json

def convert_csv_to_json(input_csv_path, output_json_path=None):
    data = []

    with open(input_csv_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            pds = row['PDS']
            auspr = row['AUSPRAEGUNG']
            auspr2 = row['AUSPR2']
            rts_typ1 = row['RTS_TYP1']
            anz_ug = row['ANZ_UG']
            anz_s = row['ANZ_S']
            mw_a_pr = row['MW_A_PR']  # Neue Spalte
            mw_m_pr = row['MW_M_PR']  # Neue Spalte
            mw_a_pw = row['MW_A_PW']  # Neue Spalte
            mw_m_pw = row['MW_M_PW']  # Neue Spalte

            if not rts_typ1 and anz_ug == anz_s:
                continue

            pds_entry = next((item for item in data if item['PDS'] == pds), None)

            if not pds_entry:
                pds_entry = {
                    "auspr_counter": 0, 
                    "PDS": pds,
                    "ANZ_S": anz_s,
                    "AUSPRAEGUNG": {},
                    "MW_A_PR": mw_a_pr,  # Hinzugefügt
                    "MW_M_PR": mw_m_pr,  # Hinzugefügt
                    "MW_A_PW": mw_a_pw,  # Hinzugefügt
                    "MW_M_PW": mw_m_pw   # Hinzugefügt
                }
                data.append(pds_entry)

            if auspr not in pds_entry['AUSPRAEGUNG']:
                pds_entry['AUSPRAEGUNG'][auspr] = []
                pds_entry['auspr_counter'] += 1

            entry = {
                "KRIT_NR": row['KRIT_NR'],
                "LL_UG_NR": row['LL_UG_NR'],
                "AUSPR2": auspr2,
                "RTS_TYP1": rts_typ1,
                "ANZ_UG": anz_ug,
                "MW_A_PR": mw_a_pr,  # Hinzugefügt
                "MW_M_PR": mw_m_pr,  # Hinzugefügt
                "MW_A_PW": mw_a_pw,  # Hinzugefügt
                "MW_M_PW": mw_m_pw   # Hinzugefügt
            }
            pds_entry['AUSPRAEGUNG'][auspr].append(entry)

    # Wenn ein Ausgabepfad für die JSON-Datei angegeben wurde, speichere die Daten in dieser Datei
    if output_json_path:
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    return data
