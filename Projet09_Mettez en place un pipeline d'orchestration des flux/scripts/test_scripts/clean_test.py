import pandas as pd
import sys

################
#ERP
##########

try:
  df = pd.read_csv("erp_clean.csv")
except Exception as e:
  with open("rapport_test.txt", "a", encoding="utf-8") as f:
      f.write("ERREUR LECTURE FICHIER\n")
      f.write(f"Message : {str(e)}\n")
  sys.exit(1)

# Initialisation du rapport
rapport = []


rapport.append("")
rapport.append("=== RAPPORT TEST  ===")
rapport.append("")
rapport.append("-" * 50)
rapport.append("=== Fichier ERP ===")
rapport.append(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
rapport.append(f"Nombre de lignes lues : {len(df)}")
rapport.append("Colonnes presentes : " + ", ".join(df.columns.tolist()))



# 1. Verification doublons sur product_id
doublons = df[df.duplicated(subset=["product_id"], keep=False)]
nb_doublons = len(doublons)

if nb_doublons > 0:
  rapport.append("ECHEC - DOUBLONS DETECTES")
  rapport.append(f"-> Nombre de lignes concernees : {nb_doublons}")
else:
  rapport.append("Aucun doublon sur product_id")

rapport.append("")

# 2. Verification valeurs manquantes
missing_product_id = df["product_id"].isna().sum()
missing_price      = df["price"].isna().sum()
missing_total      = missing_product_id + missing_price

rapport.append("VERIFICATION VALEURS MANQUANTES")
rapport.append(f"-> product_id manquants  : {missing_product_id}")
rapport.append(f"-> price manquants       : {missing_price}")
rapport.append(f"-> Total manquants       : {missing_total}")


if missing_total > 0:
  rapport.append("ECHEC - VALEURS MANQUANTES DETECTEES")
else:
  rapport.append("OK - Aucune valeur manquante sur product_id et price")








################
#CMS
##########

try:
  df = pd.read_csv("cms_clean.csv")
except Exception as e:
  with open("rapport_test.txt", "a", encoding="utf-8") as f:
      f.write("ERREUR LECTURE FICHIER\n")
      f.write(f"Message : {str(e)}\n")
  sys.exit(1)

# Initialisation du rapport

rapport.append("")
rapport.append("-" * 50)
rapport.append("=== Fichier CMS ===")
rapport.append(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
rapport.append(f"Nombre de lignes lues : {len(df)}")
rapport.append("Colonnes presentes : " + ", ".join(df.columns.tolist()))



# 1. Verification doublons sur id
doublons = df[df.duplicated(subset=["id_web"], keep=False)]
nb_doublons = len(doublons)

if nb_doublons > 0:
  rapport.append("ECHEC - DOUBLONS DETECTES")
  rapport.append(f"-> Nombre de lignes concernees : {nb_doublons}")
else:
  rapport.append("Aucun doublon sur id_web")

rapport.append("")

# 2. Verification valeurs manquantes
missing_id_web = df["id_web"].isna().sum()
missing_total_sales  = df["total_sales"].isna().sum()
missing_total      = missing_id_web + missing_total_sales

rapport.append("VERIFICATION VALEURS MANQUANTES")
rapport.append(f"-> id_web manquants       : {missing_id_web}")
rapport.append(f"-> total_sales manquants  : {missing_total_sales}")
rapport.append(f"-> Total manquants        : {missing_total}")


if missing_total > 0:
  rapport.append("ECHEC - VALEURS MANQUANTES DETECTEES")
else:
  rapport.append("OK - Aucune valeur manquante sur id_web et total_sales")



rapport.append("")




################
#liaison
##########

try:
  df = pd.read_csv("liaison_clean.csv")
except Exception as e:
  with open("rapport_test.txt", "a", encoding="utf-8") as f:
      f.write("ERREUR LECTURE FICHIER\n")
      f.write(f"Message : {str(e)}\n")
  sys.exit(1)

# Initialisation du rapport

rapport.append("")
rapport.append("-" * 50)
rapport.append("=== Fichier Liaison ===")
rapport.append(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
rapport.append(f"Nombre de lignes lues : {len(df)}")
rapport.append("Colonnes presentes : " + ", ".join(df.columns.tolist()))


# 1. Verification doublons sur id
doublons = df[df.duplicated(subset=["id_web"], keep=False)]
nb_doublons_cms = len(doublons)

doublons = df[df.duplicated(subset=["product_id"], keep=False)]
nb_doublons_erp = len(doublons)



if nb_doublons_cms + nb_doublons_erp > 0:
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

# Ecriture du rapport
with open("rapport_test.txt", "a", encoding="utf-8") as f:
  f.write("\n ".join(rapport))
