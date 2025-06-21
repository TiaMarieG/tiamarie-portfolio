import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    work_experience = [
        {
            "company": "Nintendo",
            "position": "Customer Support",
            "description": "Assisted customers with technical issues."
        },
        {
            "company": "Best Buy",
            "position": "Inventory Specialist",
            "description": "Compared stock to online inventory to ensure acccuracy."
        },
        {
            "company": "Green River College",
            "position": "Full Stack Developer Intern",
            "description": "Worked with professors to update tools and resources they used to manage their classes."
        }
    ]
    
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), work_experience=work_experience)