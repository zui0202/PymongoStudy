from pymongo import MongoClient
client = MongoClient('target.example.com')
client.admin.command('copydb',
                     fromdb='source_db_name',
                     todb='target_db_name')

client.admin.command('copydb',
                     fromdb='source_db_name',
                     todb='target_db_name',
                     fromhost='source.example.com')

client = MongoClient('target.example.com',
                     username='administrator',
                     password='pwd')
client.admin.command('copydb',
                     fromdb='source_db_name',
                     todb='target_db_name',
                     fromhost='source.example.com')