import pandas as pd
import sys

################
#Jointure
##########

try:
  df = pd.read_csv("jointure.csv")
  dfcms = pd.read_csv("cms_clean.csv")
  dferp = pd.read_csv("erp_clean.csv")
except Exception as e:
  with open("rapport_test.txt", "a", encoding="utf-8") as f:
      f.write("ERREUR LECTURE FICHIER\n")
      f.write(f"Message : {str(e)}\n")
  sys.exit(1)




# Initialisation du rapport
rapport = []
rapport.append("")
rapport.append("-" * 50)
rapport.append("=== Fichier jointure ===")
rapport.append(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
rapport.append(f"Nombre de lignes lues : {len(df)}")
rapport.append("Colonnes presentes : " + ", ".join(df.columns.tolist()))


# 1. Verification doublons sur id
doublons = df[df.duplicated(subset=["id_web"], keep=False)]
nb_doublons_cms = len(doublons)

doublons = df[df.duplicated(subset=["product_id"], keep=False)]
nb_doublons_erp = len(doublons)



if nb_doublons_cms+ nb_doublons_erp > 0:
  rapport.append("ECHEC - DOUBLONS DETECTES")
  rapport.append(f"-> Nombre de product_id en doublon : {nb_doublons_erp}")
  rapport.append(f"-> Nombre de id_web en doublon : {nb_doublons_cms}")
else:
  rapport.append("Aucun doublon sur les id")

rapport.append("")

# 2. Verification valeurs manquantes
missing_id_web = df["id_web"].isna().sum()
missing_product_id  = df["product_id"].isna().sum()
missing_total      = missing_id_web + missing_product_id

rapport.append("VERIFICATION VALEURS MANQUANTES")
rapport.append(f"-> id_web manquants       : {missing_id_web}")
rapport.append(f"-> product_id manquants  : {missing_product_id}")
rapport.append(f"-> Total manquants        : {missing_total}")

if missing_total > 0:
  rapport.append("ECHEC - VALEURS MANQUANTES DETECTEES")
else:
  rapport.append("OK - Aucune valeur manquante sur id_web et product_id")


rapport.append("")


# 3. Coherence de volumetrie
rapport.append("VOLUMETRIE DES DONNEES ")
rapport.append(f"Nombre de lignes ERP avant jointure     : {len(dferp):,}")
rapport.append(f"Nombre de lignes CMS avant jointure     : {len(dfcms):,}")
rapport.append(f"Nombre de lignes après jointure         : {len(df):,}")



if len(df) > max(len(dferp), len(dfcms)):
    rapport.append("ECHEC - La jointure a créé plus de lignes que la plus grande source") 
    
if len(df) < 0.95 * min(len(dferp), len(dfcms)):
    rapport.append(f" ECHEC - Perte importante de lignes")
else:
    rapport.append(f"OK - La volumétrie des données après les jointures est cohérente ")


rapport.append("")



# Ecriture du rapport
with open("rapport_test.txt", "a", encoding="utf-8") as f:
  f.write("\n ".join(rapport))
