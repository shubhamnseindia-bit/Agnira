from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/fleetowner')
def fleetowner():
    return render_template('fleetowner.html')

@app.route('/freight-calculator')
def freight_calculator():
    return render_template('freightcalculator.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 
