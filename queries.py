from pymongo import MongoClient

first_pipeline = [
    {"$match": {"predictions": "anomaly"}},
    {
        "$group": {
            "_id": "$to_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

df6 = query6('DataManagement-Project', 'AfterTreatment')
print(df6)


def query7(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    pipeline = [
        {"$match": {"predictions": "normal"}},
        {
            "$group": {
                "_id": "$to_ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    result = list(collection.aggregate(pipeline))
    return result

df7 = query7('DataManagement-Project', 'AfterTreatment')
print(df7)

def query4(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    pipeline = [
        {"$match": {"predictions": "anomaly"}},
        {
            "$group": {
                "_id": "$from_ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    result = list(collection.aggregate(pipeline))
    print(result)

df4 = query4('DataManagement-Project', 'AfterTreatment')
print(df4)

def query3(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    pipeline = [
        {
            "$group": {
                "_id": "$to_ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]

    result = list(collection.aggregate(pipeline))
    print(result)

df3 = query3('DataManagement-Project', 'AfterTreatment')
print(df3)

def query5(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    pipeline = [
        {"$match": {"predictions": "normal"}},
        {
            "$group": {
                "_id": "$from_ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    result = list(collection.aggregate(pipeline))
    print(result)

df5 = query5('DataManagement-Project', 'AfterTreatment')
print(df5)

import pandas as pd
from pymongo import MongoClient

def query1(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    pipeline = [
        {
            "$group": {
                "_id": {
                    "predictions": "$predictions",
                    "protocol_type": "$protocol_type",
                    "service": "$service",
                    "flag": "$flag"
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {
            "$group": {
                "_id": "$_id.predictions",
                "most_common": {
                    "$first": {
                        "protocol_type": "$_id.protocol_type",
                        "service": "$_id.service",
                        "flag": "$_id.flag",
                        "count": "$count"
                    }
                }
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "predictions": "$_id",
                    "protocol_type": "$most_common.protocol_type",
                    "service": "$most_common.service",
                    "flag": "$most_common.flag",
                    "count": "$most_common.count"
                }
            }
        }
    ]

    result = list(collection.aggregate(pipeline))
    print(result)

df1 = query1('DataManagement-Project', 'AfterTreatment')
print(df1)

def query2(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    pipeline = [
        {
            "$group": {
                "_id": "$from_ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]

    result = list(collection.aggregate(pipeline))
    print(result)

def get_ip_communication_count(db_name, collection_name, connection_string='mongodb://localhost:27017/'):
    # Connexion à MongoDB
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    # Exécution de l'agrégation
    pipeline = [
        {
            "$group": {
                "_id": {"from_ip": "$from_ip", "to_ip": "$to_ip"},
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "from_ip": "$_id.from_ip",
                "to_ip": "$_id.to_ip",
                "count": "$count"
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]

    result = list(collection.aggregate(pipeline))
    print(result)

df = get_ip_communication_count(db_name, collection_name)
print(df)

def execute_request(pipeline, collection):
    return list(collection.aggregate(pipeline))


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['DataManagement-Project']
    collection = db['AfterTreatment']

