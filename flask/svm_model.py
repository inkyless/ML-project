import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler, MinMaxScaler
from sklearn.metrics import root_mean_squared_error,r2_score,mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from ast import literal_eval
from transformers import MultiLabelBinarizerTransformer
import pickle
from sklearn.tree import DecisionTreeRegressor

def clean_dataset(dataset,column_name):
    outlier_highend =dataset[(dataset[column_name]>180)].index
    outlier_lowend =dataset[(dataset[column_name]<50)].index
    dataset.drop(outlier_highend,inplace=True)
    dataset.drop(outlier_lowend,inplace=True)
    return dataset

def train_svm_model(data_path):
    genre_data = data_path['genre'].tolist()
    genres = [literal_eval(item) for item in genre_data]
    duration = data_path["duration"]
    score = data_path["score"]
    used_dataset = pd.DataFrame({"duration":duration,"score":score})
    used_dataset["genre"] = genres

    X = used_dataset[["genre","duration"]]
    y = used_dataset["score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    minmax = MinMaxScaler()
    mlb_transformer = MultiLabelBinarizerTransformer()

    preprocessor = ColumnTransformer(transformers=[
        ("mlb",mlb_transformer,"genre"),
        ("duration",scaler,["duration"])
    ], remainder='drop')

    svr = SVR(kernel="rbf",C=10,epsilon=0.5,gamma=0.1)
    
    pipeline = Pipeline(steps=[
        ("preprocessor",preprocessor),
        ("model",svr)
    ])
    
    pipeline.fit(X_train,y_train)
    prediction = pipeline.predict(X_test)
    print("Mean Absolute Error : ", mean_absolute_error(y_test,prediction))
    print("Root Mean Squared Error", root_mean_squared_error(y_test,prediction))
    print("Mean Squared Error", np.power(root_mean_squared_error(y_test,prediction),2))
    print("R2 Score : ", r2_score(y_test,prediction))
    return pipeline

def test_prediction(pipeline,genres,duration):
    test_features = {
    "genre" : genres,
    "duration" : duration
    }
    input_data = pd.DataFrame([test_features])
    test_prediction = pipeline.predict(input_data)
    return test_prediction[0]

def main():
    dataset = pd.read_csv("final_dataset.csv")
    pipeline = train_svm_model(dataset)
    genres = ["Action","Drama"]
    duration = 120
    print(test_prediction(pipeline,genres,duration))
    with open("svm_model.pkl","wb") as file:
        pickle.dump(pipeline,file)
    
if __name__ == "__main__":
    main()
