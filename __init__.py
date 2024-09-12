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
@app.route('/commits/')
def get_commits_by_hour():
    try:
        url = 'https://github.com/aminefs/5MCSI_Metriques/blob/main/templates/commits.html'
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch data from GitHub API. Status code: {response.status_code}"}), 500

        commits_by_hour = {}

        # Parcourir les commits et extraire les heures
        for commit in data:
            try:
                commit_date = commit['commit']['author']['date']
                hour = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').hour

                if hour in commits_by_hour:
                    commits_by_hour[hour] += 1
                else:
                    commits_by_hour[hour] = 1
            except KeyError as e:
                return jsonify({"error": f"KeyError - commit structure missing expected fields: {str(e)}"}), 500

        return jsonify(commits_by_hour)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



  
if __name__ == "__main__":
  app.run(debug=True)
