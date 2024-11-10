from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

model = pickle.load(open("svm_model.pkl","rb"))

@app.route('/',methods=["GET"])
def home():
    title = "Get Recommendation Movie Score with Genres and Duration"        
    return render_template("page.html",message = title)
    
@app.route("/result",methods=["POST"])
def result():
    genre = request.form.getlist('genre')
    duration = (request.form.get("duration"))
    genres_string = (','.join(genre))
    title = "Error Message"
    try:
        duration = int(duration)
        if duration<60 or duration>180 : 
            return render_template("page.html", error="Input between 1-3 hours in range",message = title,)
        if len(genre)==0:
            return render_template("page.html", error="Please input at least a genre", message = title)
        if len(genre)==0 or len(genre)>3:
            return render_template("page.html", error="Input 3 genres at max", message = title)
    except ValueError:
        return render_template("page.html", error="Input Numerical Value Only", message = title)
    
    input_data = pd.DataFrame({"genre":[genre],"duration":[duration]})
    prediction = model.predict(input_data)
    predict_value = round(float(prediction[0]),2)
    title = "Prediction Result"
    return render_template("page.html", predicted_result=predict_value, message = title,
                           input_choice="You have tried to make a film of {} minutes with genre(s) of {}".format(duration,genres_string))

if __name__ == "__main__":
    app.run(debug=True)
