import pandas as pd
import joblib
from pymongo import MongoClient
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

def treat_data(data):
    model = joblib.load('best_model.joblib')
    preprocessor = joblib.load('best_preprocessor.joblib')
    df = pd.DataFrame(data)
    X_new = preprocessor.transform(df)
    predictions = model.predict(X_new)
    predicted_labels = ['anomaly' if x == -1 else 'normal' for x in predictions]
    df['predictions'] = predicted_labels
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