from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (StructType, StructField, IntegerType, StringType)
import json

#Création de la session Spark

spark =(
    SparkSession.builder 
    .appName("Redpanda_Tickets_stream") 
    .master("spark://spark-master:7077") 
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.3") 
    .getOrCreate()
)


# Schéma 
schema = StructType([
    StructField("ticket_id", IntegerType(), True),
    StructField("created_at", StringType(), True),  
    StructField("client_id", IntegerType(), True),
    StructField("priorite", StringType(), True),
    StructField("types", StringType(), True),
    StructField("demandes", StringType(), True)
])

# Lecture streaming depuis Redpanda 
df =(
    spark.readStream 
    .format("kafka") 
    .option("kafka.bootstrap.servers", "redpanda:9092") 
    .option("subscribe", "client_tickets") 
    .option("startingOffsets", "earliest") 
    .load()
)

# Conversion du message brut en str
df_json = df.selectExpr("CAST(value AS STRING) AS message")

# Parsing JSON
df_parsed = df_json.select(
    from_json(col("message"), schema).alias("data")
).select(
    col("data.ticket_id"),
    col("data.created_at"),
    col("data.client_id"),
    col("data.priorite"),
    col("data.types"),
    col("data.demandes")
)


# Fonction pour sauvegarder les données dans un fichier JSON
def sauvegarder_tickets(donnees, numero_batch):
    lignes = donnees.collect()
    if lignes:
        with open("/app/output/tickets.json", "a", encoding="utf-8") as f:
            for ligne in lignes:
                donnees_dict = ligne.asDict()
                f.write(json.dumps(donnees_dict, ensure_ascii=False) + "\n")
        
        #Nombre par types        
        donnees_par_types= donnees.groupBy("types").count()
        lignes_transform = donnees_par_types.collect()
        
        batch_complet = {
            f"batch_{numero_batch}": [ligne.asDict() for ligne in lignes_transform]
        }
        with open("/app/output/stat.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(batch_complet, ensure_ascii=False) + "\n")   
 
 

# Traitement en continu
query =(
      df_parsed.writeStream 
    .foreachBatch(sauvegarder_tickets) 
    .option("checkpointLocation", "/app/checkpoint") 
    .trigger(processingTime="5 seconds") 
    .start()
)

# Attend et traite les données en continu
query.awaitTermination()
