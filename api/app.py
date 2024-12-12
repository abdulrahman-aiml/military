from flask import Flask, render_template, request, redirect, flash
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

# Load the model
with open('api/model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form_page():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Collect form data
        success_rate = request.form["Success Rate"]
        Resilience_Index = request.form["Resilience Index"]
        Communication_Quality = request.form["Communication Quality"]
        Morale_Score = request.form["Morale Score"]
        Casualty_Count = request.form["Casualty Count"]
        Intel_Availability = request.form["Intel Availability"]
        Training_Level = request.form["Training Level"]
        Supply_Level = request.form["Supply Level"]
        Engagement_Frequency = request.form['Engagement Frequency']
        
        # Validate and convert form values
        # Intel_Availability mapping
        if Intel_Availability == 'CMB':
            Intel_Availability = 0
        elif Intel_Availability == 'TRN':
            Intel_Availability = 1
        elif Intel_Availability == 'REC':
            Intel_Availability = 2
        else:
            raise ValueError("Invalid Intel Availability value.")

        # Training_Level mapping
        if Training_Level == 'ARM':
            Training_Level = 0
        elif Training_Level == 'AVI':
            Training_Level = 1
        elif Training_Level == 'UKN':
            Training_Level = 2
        else:
            raise ValueError("Invalid Training Level value.")
        
        # Supply_Level mapping
        if Supply_Level == 'URB':
            Supply_Level = 0
        elif Supply_Level == 'RUR':
            Supply_Level = 1
        elif Supply_Level == 'COS':
            Supply_Level = 2
        else:
            raise ValueError("Invalid Supply Level value.")

        # Engagement_Frequency mapping
        if Engagement_Frequency == 'RAR':
            Engagement_Frequency = 0
        elif Engagement_Frequency == 'FRQ':
            Engagement_Frequency = 1
        elif Engagement_Frequency == 'OCS':
            Engagement_Frequency = 2
        else:
            raise ValueError("Invalid Engagement Frequency value.")

        # Prepare input data for prediction
        t = [[
            float(success_rate), 
            float(Resilience_Index), 
            float(Communication_Quality),
            float(Morale_Score), 
            float(Casualty_Count), 
            float(Engagement_Frequency),
            float(Intel_Availability), 
            float(Supply_Level), 
            float(Training_Level)
        ]]

        # Make prediction
        output = model.predict(t)

        # Handle output and render appropriate template
        if output[0] == 'Successful':
            return render_template('submit.html', prediction_value='The Mission is Successful')
        elif output[0] == 'Ongoing':
            return render_template('submit.html', prediction_value='The Mission is Ongoing')
        elif output[0] == 'Failed':
            return render_template('submit.html', prediction_value='The Mission is Failed')
        else:
            raise ValueError("Invalid prediction result.")
    
    except Exception as e:
        # If an error occurs, flash an error message and redirect to the form
        flash(f"An error occurred: {str(e)}")
        return redirect('/form')

if __name__ == '__main__':
    # Set a secret key for flash messages
    app.secret_key = os.urandom(24)
    app.run(debug=True)
