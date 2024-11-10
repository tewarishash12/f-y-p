from flask import Flask, request, render_template, redirect, url_for, session
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Importing pickle files
model = pickle.load(open('Models\\classifier.pkl', 'rb'))
ferti = pickle.load(open('Models\\fertilizer.pkl', 'rb'))


@app.route('/')
def index():
    result = session.get('result')  # Retrieve result from session
    session.pop('result', None)  # Clear result from session
    return render_template("Fertilizer_Rec.html", x=result)  # Pass result to template


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve input values from form 
        temp = request.form.get('temp')
        humi = request.form.get('humid')
        mois = request.form.get('mois')
        soil = request.form.get('soil')
        crop = request.form.get('crop')
        nitro = request.form.get('nitro')
        pota = request.form.get('pota')
        phosp = request.form.get('phos')

        # Check if any of the inputs are missing or not numeric
        inputs = [temp, humi, mois, soil, crop, nitro, pota, phosp]
        if None in inputs or not all(val.isdigit() for val in inputs):
            session['result'] = 'Invalid input. Please provide numeric values for all fields.'
            return redirect(url_for('index'))

        # Convert values to integers
        input_values = [int(val) for val in inputs]

        # Make prediction using the loaded model
        prediction = model.predict([input_values])

        # Retrieve the result from the fertilizer mapping
        res = str(ferti.classes_[prediction[0]])

        # Store the result in the session and redirect to index
        session['result'] = res
        return redirect(url_for('index'))

    except Exception as e:
        # Handle any errors that occur during the process
        session['result'] = f"Error: {str(e)}"
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8002)
