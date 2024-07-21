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
    {"$match": {"predictions": "normal"}},
    {
        "$group": {
            "_id": "$from_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}},
]

fifth_pipeline = [
    {
        "$group": {
            "_id": "$to_ip",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"count": -1}}
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

def display_result(results, sentence):
    print("\n--------------------------------\n")
    print(sentence)
    for result in results:
        print("IP: " + result["_id"] + ". Number of request: " + str(result["count"]))
    print("\n--------------------------------\n")

def display_cross_table(results, sentence):
    print("\n--------------------------------\n")
    print(sentence)
    for result in results:
        print(result["from_ip"] + " -> " + result["to_ip"] + " => "+ str(result["count"]))
    print("\n--------------------------------\n")

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['DataManagement-Project']
    collection = db['AfterTreatment']

    display_result(execute_request(first_pipeline, collection), "Number of anomly requests recieved per IP adress :")
    display_result(execute_request(second_pipeline, collection), "Number of normal requests revieved per IP adress :")
    display_result(execute_request(third_pipeline, collection), "Number of anomaly requests sent per IP adress :")
    display_result(execute_request(fourth_pipeline, collection), "Number of normal requests sent per IP adress :")
    display_result(execute_request(fifth_pipeline, collection), "Number of recieved requests per IP adress :")
    display_result(execute_request(sixth_pipeline, collection), "Number of requests sent per IP adress :")
    display_cross_table(execute_request(seventh_pipeline, collection), "Table of requests between IP adresses :")