from confluent_kafka import Producer
import json, time, random
from datetime import datetime

p = Producer({"bootstrap.servers": "redpanda:9092"}) # producer qui se conecte à redpanda


priorites = ['basse', 'moyenne', 'haute']
types = ['Devis', 'Analyse', 'Panne']
demandes = ['Bonjour, demande 1, merci pour votre retour', 'Bonjour, demande 2. Bien cordialement', 'Bonjour, demande 3. Merci bien']


n = 1
while True:
    ticket = {
        "ticket_id": n,
        "created_at": datetime.now().isoformat(),
        "client_id": random.randint(1, 9999),
        "priorite": random.choice(priorites),
        "types": random.choice(types),
        "demandes": random.choice(demandes)
    }
    
    p.produce("client_tickets", json.dumps(ticket).encode('utf-8')) 
    p.poll(0)
    
    n += 1
    time.sleep(0.5)
    

