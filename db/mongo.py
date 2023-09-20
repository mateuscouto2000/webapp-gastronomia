from pymongo import MongoClient
import ssl

client = MongoClient("mongodb+srv://devdivinosabor:oJ3PgTx5nXZQ8OQ8@cluster0.v9y0yig.mongodb.net/?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client["db0"]