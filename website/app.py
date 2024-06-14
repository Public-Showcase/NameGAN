from flask import Flask, request, render_template, render_template_string
import os

from nameGenerator import generate_new_name
from GPTGeminiGenerator import gerenateNames

app = Flask(__name__)

@app.route('/generate_name', methods=['POST'])
def generate_name():
    # edge cases
    if request.form['start'] == "":
        return render_template('error.html', error_string="Please enter a start character(s)!")

    start = request.form['start'] # get the start character from the HTML form
    start = start.lower() # convert to lowercase
    names = []
    for i in range(5):
        try:
            names.append(generate_new_name(start=start).capitalize()[:-1])
        except:
            names.append("Error!")
    
    return render_template('result.html', names=names)

@app.route('/gptGeneratePage', methods=['POST'])
def redirectToGPTPage():
    return render_template('gptGeneratePage.html', names=0)

@app.route('/gptGenerate', methods=['POST'])
def GPTGenerate():
    startChar = request.form['startChar']
    religion = request.form['religion']
    gender = request.form['gender']
    originCountry = request.form['originCountry']

    names = gerenateNames([startChar, religion, gender, originCountry])
    return render_template('result.html', names=names)
    # return render_template('gptGeneratePage.html', names=names)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 8080)))
