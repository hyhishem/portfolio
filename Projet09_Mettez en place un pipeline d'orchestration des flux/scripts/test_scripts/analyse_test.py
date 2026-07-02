import pandas as pd
import sys


try:
  df_CA = pd.read_csv("CA.csv")
  df_CA_par_bouteille = pd.read_csv("CA_par_bouteille.csv")
  df_prem = pd.read_csv("Premiums.csv")
  df_ord = pd.read_csv("Ordinaires.csv")
except Exception as e:
  with open("rapport_test.txt", "a", encoding="utf-8") as f:
      f.write("ERREUR LECTURE FICHIER\n")
      f.write(f"Message : {str(e)}\n")
  sys.exit(1)


################
#CA
##########


# Initialisation du rapport
rapport = []
rapport.append("")
rapport.append("-" * 50)
rapport.append("=== Résultats ===")
rapport.append(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
rapport.append(f"CA : {df_CA.iloc[0,0]:.2f} € ")
rapport.append(f"-> Nombre de bouteilles premiums : {len(df_prem)}")
rapport.append(f"-> Nombre de bouteilles ordinaires : {len(df_ord)}")
rapport.append(f"-> Total (ordinaires + premiums) : {len(df_ord)+len(df_prem)}")

rapport.append("")



# Ecriture du rapport
with open("rapport_test.txt", "a", encoding="utf-8") as f:
  f.write("\n ".join(rapport))
