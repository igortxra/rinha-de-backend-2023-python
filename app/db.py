from pymongo import ASCENDING, MongoClient

DB_URI = "mongodb://root:root@db:27017/person_db?authSource=admin"

client = MongoClient(DB_URI)
db = client.person_db
collection = db.pessoas

collection.create_index([
    ("apelido", ASCENDING),
    ("nome", ASCENDING),
    ("stack", ASCENDING)
])

collection.create_index("apelido")
