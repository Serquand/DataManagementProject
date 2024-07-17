import pandas as pd
import joblib
from pymongo import MongoClient
import random
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

def generate_all_ips(number_of_ip_to_generate):
    from_ips = []
    to_ips = []
    for _ in range(number_of_ip_to_generate):
        from_ip = generate_random_ip(None)
        from_ips.append(from_ip)
        to_ips.append(generate_random_ip(from_ip))
    return {"from_ips": from_ips, "to_ips": to_ips}

def generate_random_ip(exclude_ip: str | None) -> str:
    list_ips = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
    if exclude_ip is None:
        return list_ips[random.randint(0, 3)]
    else:
        while True:
            chosen_ip = list_ips[random.randint(0, 3)]
            if chosen_ip != exclude_ip:
                return chosen_ip

def treat_data(data):
    model = joblib.load('best_model.joblib')
    preprocessor = joblib.load('best_preprocessor.joblib')
    df = pd.DataFrame(data)
    X_new = preprocessor.transform(df)
    predictions = model.predict(X_new)
    predicted_labels = ['anomaly' if x == -1 else 'normal' for x in predictions]
    df['predictions'] = predicted_labels
    ips = generate_all_ips(len(predictions))
    df["from_ip"] = ips["from_ips"]
    df["to_ip"] = ips["to_ips"]
    return df

def load_data_from_db(db):
    collection = db['BeforeTreatment']
    return list(collection.find())

def store_data_to_mongodb(db, data_to_store):
    collection = db['AfterTreatment']
    data_dict = data_to_store.to_dict('records')
    collection.insert_many(data_dict)

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['DataManagement-Project']

    data = load_data_from_db(db)
    data_to_store = treat_data(data)
    store_data_to_mongodb(db, data_to_store)

    client.close()