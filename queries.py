from pymongo import MongoClient

first_pipeline = [
    {"$match": {"predictions": "anomaly"}},
    {
        "$group": {
            "_id": "$to_ip",
            "count": {"$sum": 1 }
        }
    },
    {"$sort": {"count": -1}},
]

second_pipeline = [
    {"$match": {"predictions": "normal"}},
    {
        "$group": {
            "_id": "$to_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}},
]

third_pipeline = [
    {"$match": {"predictions": "anomaly"}},
    {
        "$group": {
            "_id": "$from_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}},
]

fourth_pipeline = [
    {
        "$group": {
            "_id": "$to_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}}
]

fifth_pipeline = [
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

sixth_pipeline = [
    {
        "$group": {
            "_id": "$from_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}}
]

seventh_pipeline = [
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

def execute_request(pipeline, collection):
    return list(collection.aggregate(pipeline))

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['DataManagement-Project']
    collection = db['AfterTreatment']

    first_result = execute_request(first_pipeline, collection)
    second_result = execute_request(second_pipeline, collection)
    third_result = execute_request(third_pipeline, collection)
    fourth_result = execute_request(fourth_pipeline, collection)
    fifth_result = execute_request(fifth_pipeline, collection)
    sixth_result = execute_request(sixth_pipeline, collection)
    seventh_result = execute_request(seventh_pipeline, collection)

    print("First :", str(first_result))
    print("\nSecond :", str(second_result))
    print("\nThird :", str(third_result))
    print("\nFourth :", str(fourth_result))
    print("\nFifth :", str(fifth_result))
    print("\nSixth :", str(sixth_result))
    print("\nSeventh :", str(seventh_result))
