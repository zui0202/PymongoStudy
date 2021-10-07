from pymongo import MongoClient
client = MongoClient()
client.drop_database('custom_type_example')
db = client.custom_type_example

'''
from decimal import Decimal
num = Decimal("45.321")
db.test.insert_one({'num': num})
'''

from bson.decimal128 import Decimal128
from bson.codec_options import TypeCodec
class DecimalCodec(TypeCodec):
    python_type = Decimal    # the Python type acted upon by this type codec
    bson_type = Decimal128   # the BSON type acted upon by this type codec
    def transform_python(self, value):
        """Function that transforms a custom type value into a type
                that BSON can encode."""
        return Decimal128(value)
    def transform_bson(self, value):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        return value.to_decimal()
decimal_codec = DecimalCodec()

from bson.codec_options import TypeRegistry
type_registry = TypeRegistry([decimal_codec])

from bson.codec_options import CodecOptions
codec_options = CodecOptions(type_registry=type_registry)
collection = db.get_collection('test', codec_options=codec_options)


collection.insert_one({'num': Decimal("45.321")})
mydoc = collection.find_one()
import pprint
pprint.pprint(mydoc)

vanilla_collection = db.get_collection('test')
pprint.pprint(vanilla_collection.find_one())

class DecimalInt(Decimal):
    def my_method(self):
        """Method implementing some custom logic."""
        return int(self)

# collection.insert_one({'num': DecimalInt("45.321")})

class DecimalIntCodec(DecimalCodec):
    @property
    def python_type(self):
        """The Python type acted upon by this type codec."""
]        return DecimalInt
decimalint_codec = DecimalIntCodec()

type_registry = TypeRegistry([decimal_codec, decimalint_codec])
codec_options = CodecOptions(type_registry=type_registry)
collection = db.get_collection('test', codec_options=codec_options)
collection.drop()
collection.insert_one({'num': DecimalInt("45.321")})
mydoc = collection.find_one()
pprint.pprint(mydoc)

# On Python 3.x.
from bson.binary import Binary
newcoll = db.get_collection('new')
newcoll.insert_one({'_id': 1, 'data': Binary(b"123", subtype=0)})
doc = newcoll.find_one()
type(doc['data'])

# On Python 2.7.x
newcoll = db.get_collection('new')
doc = newcoll.find_one()
type(doc['data'])

def fallback_encoder(value):
    if isinstance(value, Decimal):
        return Decimal128(value)
    return value

type_registry = TypeRegistry(fallback_encoder=fallback_encoder)
codec_options = CodecOptions(type_registry=type_registry)
collection = db.get_collection('test', codec_options=codec_options)
collection.drop()

collection.insert_one({'num': Decimal("45.321")})
mydoc = collection.find_one()
pprint.pprint(mydoc)

class MyStringType(object):
    def __init__(self, value):
        self.__value = value
    def __repr__(self):
        return "MyStringType('%s')" % (self.__value,)

class MyNumberType(object):
    def __init__(self, value):
        self.__value = value
    def __repr__(self):
        return "MyNumberType(%s)" % (self.__value,)

import pickle
from bson.binary import Binary, USER_DEFINED_SUBTYPE
def fallback_pickle_encoder(value):
    return Binary(pickle.dumps(value), USER_DEFINED_SUBTYPE)

class PickledBinaryDecoder(TypeDecoder):
    bson_type = Binary
    def transform_bson(self, value):
        if value.subtype == USER_DEFINED_SUBTYPE:
            return pickle.loads(value)
        return value

codec_options = CodecOptions(type_registry=TypeRegistry(
    [PickledBinaryDecoder()], fallback_encoder=fallback_pickle_encoder))

collection = db.get_collection('test_fe', codec_options=codec_options)
collection.insert_one({'_id': 1, 'str': MyStringType("hello world"),
                       'num': MyNumberType(2)})
mydoc = collection.find_one()
assert isinstance(mydoc['str'], MyStringType)
assert isinstance(mydoc['num'], MyNumberType)