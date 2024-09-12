from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2

@app.route('/contact/')
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/rapport/')
def mongraphique():
    return render_template("graphique.html")

@app.route('/histogramme/')
def monhistogramme():
    return render_template("histogramme.html")


# Route pour extraire les minutes à partir d'une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour récupérer les commits
@app.route('/commits/')
def get_commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/templates/commits'
    response = requests.get(url)
    data = response.json()

    commits_by_minute = {}

    # Parcourir les commits et extraire les minutes
    for commit in data:
        commit_date = commit['commit']['author']['date']
        minutes = extract_minutes(commit_date).json['minutes']
        
        if minutes in commits_by_minute:
            commits_by_minute[minutes] += 1
        else:
            commits_by_minute[minutes] = 1

    return jsonify(commits_by_minute)


  
if __name__ == "__main__":
  app.run(debug=True)
