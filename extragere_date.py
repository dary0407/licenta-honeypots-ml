import json
import pandas as pd

# Calea către logul generat de Cowrie
log_file = "cowrie_copie.json"

date_extrase = []

# Deschidem fișierul și îl citim linie cu linie
try:
    with open(log_file, 'r') as f:
        for line in f:
            # Transformăm linia de text într-un dicționar Python
            eveniment = json.loads(line.strip())
            
            # Ne interesează doar evenimentele de tip comandă sau login eșuat
            if eveniment.get('eventid') in ['cowrie.command.input', 'cowrie.login.failed']:
                
                # Extragem doar caracteristicile (features) care ne interesează
                date_extrase.append({
                    'Timestamp': eveniment.get('timestamp'),
                    'IP_Sursa': eveniment.get('src_ip'),
                    'ID_Sesiune': eveniment.get('session'),
                    'Tip_Eveniment': eveniment.get('eventid'),
                    'Input_Atacator': eveniment.get('input') or eveniment.get('password') # prinde și parola și comanda
                })

    # Creăm tabelul de Machine Learning (DataFrame)
    df = pd.DataFrame(date_extrase)
    
    print("S-au extras", len(df), "evenimente.")
    print("-" * 50)
    print(df.head(15)) # Afișăm primele 15 rânduri

    # Salvăm datele pe disk pentru a le folosi la Machine Learning
    df.to_csv("dataset_cowrie.csv", index=False)
    print("Datele au fost salvate cu succes în 'dataset_cowrie.csv'!")

except PermissionError:
    print("Eroare de permisiune! Nu ai dreptul să citești fișierul lui cowrie.")
except Exception as e:
    print(f"A apărut o eroare: {e}")