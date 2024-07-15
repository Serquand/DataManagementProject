import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset
df = pd.read_csv('dataset/Train_data.csv')
df.ffill(inplace=True)

categorical_columns = ['protocol_type', 'service', 'flag']
numerical_columns = df.drop(categorical_columns + ['class'], axis=1).columns

scalers = {
    'StandardScaler': StandardScaler(),
    'RobustScaler': RobustScaler(),
    'MinMaxScaler': MinMaxScaler()
}

best_model = None
best_report = None
best_params = None
best_accuracy = 0

for scaler_name, scaler in scalers.items():
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', scaler, numerical_columns),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
        ])

    X = preprocessor.fit_transform(df.drop('class', axis=1))
    y = df['class']
    y = y.apply(lambda x: -1 if x == 'anomaly' else 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    contamination_grid = [0.03, 0.04, 0.05]

    for contamination in contamination_grid:
        model = IsolationForest(n_estimators=500, max_samples=0.9, contamination=contamination, max_features=1.0, random_state=42)
        model.fit(X_train)
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, target_names=['anomaly', 'normal'], output_dict=True, zero_division=1)
        accuracy = accuracy_score(y_test, y_pred)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_report = report
            best_params = {
                'scaler': scaler_name,
                'contamination': contamination
            }
print(f"Best parameters: {best_params}")
print("Best Classification Report:")
print(classification_report(y_test, best_model.predict(X_test), target_names=['anomaly', 'normal'], zero_division=1))

# Save the best model and preprocessor
joblib.dump(best_model, 'best_model.joblib')
joblib.dump(preprocessor, 'best_preprocessor.joblib')
