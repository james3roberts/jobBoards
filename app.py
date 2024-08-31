from flask import Flask, render_template, request

app = Flask(__name__) #start the flask app

# Dictionary to store the programming languages and their counts
languages = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_title = request.form['job_title']
        languages_input = request.form['languages']

        # Split the languages by comma and strip any whitespace
        languages_list = [lang.strip() for lang in languages_input.split(',')]
        
        # Update the language counts
        for lang in languages_list:
            if lang in languages:
                languages[lang] += 1
            else:
                languages[lang] = 1
    
    # Sort the languages by count in descending order
    sorted_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
    
    return render_template('index.html', languages=sorted_languages)

if __name__ == '__main__':
    app.run(debug=True)


#to start just type flask run
#if that dont work try export FLASK_APP=app.py
#or export FLASK_ENV=development    to use development mode.
#this is running on http://127.0.000.1:5000   Just hold ctrl and lick the link
#ctrl+c to stop running