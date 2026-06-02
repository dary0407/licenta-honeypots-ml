import sqlite3
import pandas as pd

# Calea către copia bazei de date
db_file = "dionaea_copie.sqlite"

try:
    # 1. Ne conectăm la baza de date SQLite
    conn = sqlite3.connect(db_file)
    
    # 2. Executăm o comandă SQL pentru a citi tabelul "connections"
    # Aici Dionaea înregistrează toate scanările de la Nmap
    df = pd.read_sql_query("SELECT * FROM connections", conn)
    
    # Afișăm câteva detalii
    print(f"S-au găsit {len(df)} conexiuni (scanări/atacuri) înregistrate de Dionaea.")
    print("-" * 50)
    
    # Afișăm doar coloanele mai importante ca să încapă pe ecran
    coloane_importante = ['connection_timestamp', 'remote_host', 'local_port', 'connection_protocol']
    
    # Verificăm dacă există aceste coloane (în funcție de versiunea de Dionaea)
    if all(col in df.columns for col in coloane_importante):
        print(df[coloane_importante].tail(15)) # Afișăm ultimele 15 (cele mai recente)
    else:
        print(df.head()) # Afișăm tot dacă structura e ușor diferită
    
    # 3. Salvăm tabelul complet în format CSV pentru Machine Learning
    df.to_csv("dataset_dionaea.csv", index=False)
    print("\n✅ Datele au fost salvate cu succes în 'dataset_dionaea.csv'!")
    
    # Închidem conexiunea
    conn.close()

except Exception as e:
    print(f"A apărut o eroare: {e}")