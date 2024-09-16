from flask import Flask, render_template, request, redirect, url_for  # Added redirect and url_for for redirection
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobtracker.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary feature

# Initialize the database
db = SQLAlchemy(app)

# Define the Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each job entry
    title = db.Column(db.String(100), nullable=False)  # Job title
    languages = db.Column(db.String(200), nullable=False)  # Programming languages used

    def __repr__(self):
        return f"<Job {self.title}>"

# Route for adding a job (POST request)
@app.route('/add_job', methods=['POST'])
def add_job():
    job_title = request.form['job_title']
    languages = request.form['languages']
    
    # Create a new Job object and save it to the database
    new_job = Job(title=job_title, languages=languages)
    db.session.add(new_job)
    db.session.commit()
    
    return redirect(url_for('index'))  # Redirect to the index route after adding the job

# Route for displaying the main page (GET request)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_title = request.form['job_title']
        languages_input = request.form['languages']

        # Split the languages by comma and strip any whitespace
        languages_list = [lang.strip() for lang in languages_input.split(',')]
        
        # Update the language counts in the dictionary
        for lang in languages_list:
            if lang in languages:
                languages[lang] += 1
            else:
                languages[lang] = 1
    
    # Retrieve all jobs from the database
    jobs = Job.query.all()

    # Count the frequency of each programming language from the database
    language_count = {}
    for job in jobs:
        for language in job.languages.split(','):
            language = language.strip()
            if language in language_count:
                language_count[language] += 1
            else:
                language_count[language] = 1

    # Sort languages by frequency in descending order
    sorted_languages = dict(sorted(language_count.items(), key=lambda item: item[1], reverse=True))

    return render_template('index.html', languages=sorted_languages)  # Pass sorted languages to the template

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
