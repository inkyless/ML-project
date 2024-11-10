import numpy as np
import pandas as pd
from sklearn.preprocessing import  MultiLabelBinarizer, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import root_mean_squared_error,r2_score,mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from ast import literal_eval
from transformers import MultiLabelBinarizerTransformer
import pickle

#Referensi dari notebook sebelumnya coba implementasi ke dalam satu file

def clean_dataset(dataset,column_name):
    outlier_highend =dataset[(dataset[column_name]>180)].index
    outlier_lowend =dataset[(dataset[column_name]<50)].index
    dataset.drop(outlier_highend,inplace=True)
    dataset.drop(outlier_lowend,inplace=True)
    return dataset

def split_train_predict(dataset):
    genre_data = dataset['genre'].tolist()
    genres = [literal_eval(item) for item in genre_data]
    duration = dataset["duration"]
    score = dataset["score"]
    used_dataset = pd.DataFrame({"duration":duration,"score":score})
    used_dataset["genre"] = genres

    X = used_dataset[["genre","duration"]]
    y = used_dataset["score"]

    X_train, X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
    scaler = StandardScaler()
    minmax = MinMaxScaler()
    mlb_transformer = MultiLabelBinarizerTransformer()

    preprocessor = ColumnTransformer(transformers=[
        ("mlb",mlb_transformer,"genre"),
        ("duration",scaler,["duration"])
    ], remainder='drop')

    tree = DecisionTreeRegressor(max_depth=7,max_features=3,max_leaf_nodes=30,
                                 min_samples_leaf=7,min_weight_fraction_leaf=0.1,splitter="best")
    
    pipeline = Pipeline(steps=[
        ("preprocessor",preprocessor),
        ("model",tree)
    ])

    pipeline.fit(X_train,y_train)
    # prediction = pipeline.predict(test_df[["genre","duration"]])
    # print("Mean Absolute Error : ", mean_absolute_error(test_df["score"],prediction))
    # print("Root Mean Squared Error", root_mean_squared_error(test_df["score"],prediction))
    # print("Mean Squared Error", np.power(root_mean_squared_error(test_df["score"],prediction),2))
    # print("R2 Score : ", r2_score(test_df["score"],prediction))
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
    cleaned_dataset = clean_dataset(dataset,"duration")
    pipeline = split_train_predict(cleaned_dataset)
    genres = ["Action","Drama"]
    duration = 120
    print(test_prediction(pipeline,genres,duration))
    with open("model.pkl","wb") as file:
        pickle.dump(pipeline,file)
    
if __name__ == "__main__":
    main()
    


