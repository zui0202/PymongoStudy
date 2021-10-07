from pymongo import MongoClient
import urllib.parse
username = urllib.parse.quote_plus('user')
print(username)
password = urllib.parse.quote_plus('pass/word')
print(password)
MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))

from pymongo import MongoClient
client = MongoClient('example.com',
                     username='user',
                     password='password',
                     authSource='the_database',
                     authMechanism='SCRAM-SHA-256')

uri = "mongodb://user:password@example.com/?authSource=the_database&authMechanism=SCRAM-SHA-256"
client = MongoClient(uri)

from pymongo import MongoClient
client = MongoClient('example.com',
                     username='user',
                     password='password',
                     authSource='the_database',
                     authMechanism='SCRAM-SHA-1')

uri = "mongodb://user:password@example.com/?authSource=the_database&authMechanism=SCRAM-SHA-1"
client = MongoClient(uri)

from pymongo import MongoClient
client = MongoClient('example.com',
                     username='user',
                     password='password',
                     authMechanism='MONGODB-CR')

uri = "mongodb://user:password@example.com/?authSource=the_database&authMechanism=MONGODB-CR"
client = MongoClient(uri)

uri = "mongodb://user:password@example.com/default_db?authSource=admin"
client = MongoClient(uri)

# get_database with no "name" argument chooses the DB from the URI
db = MongoClient(uri).get_database()
print(db.name)

from pymongo import MongoClient
client = MongoClient('example.com',
                     username="<X.509 derived username>"
                     authMechanism="MONGODB-X509",
                     tls=True,
                     tlsCertificateKeyFile='/path/to/client.pem',
                     tlsCAFile='/path/to/ca.pem')

uri = "mongodb://<X.509 derived username>@example.com/?authMechanism=MONGODB-X509"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='/path/to/client.pem',
                     tlsCAFile='/path/to/ca.pem')

