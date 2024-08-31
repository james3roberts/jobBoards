from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Initialize language frequency dictionary
language_frequency = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_job', methods=['POST'])
def add_job():
    job_name = request.form['job_name']
    languages = request.form['languages'].split(',')

    for language in languages:
        language = language.strip().lower()  # Normalize language names
        if language in language_frequency:
            language_frequency[language] += 1
        else:
            language_frequency[language] = 1

    return jsonify(language_frequency)

@app.route('/study_plan')
def study_plan():
    ranked_languages = sorted(language_frequency.items(), key=lambda x: x[1], reverse=True)
    return jsonify(ranked_languages)

if __name__ == '__main__':
    app.run(debug=True)


#to start just type flask run
#if that dont work try export FLASK_APP=app.py
#or export FLASK_ENV=development    to use development mode.