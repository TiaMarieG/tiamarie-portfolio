import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

NAV_LINKS = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"}
    
]

@app.context_processor
def inject_nav_links():
    return dict(nav_links=NAV_LINKS)


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

    education = [
        {"school": "Green River College", "degree": "BAS in Software Engineering", "year": "2026"},
        {"school": "Green River College", "degree": "AAS in Software Engineering", "year": "2024"}
    ]
    
    return render_template('index.html', title="Tia Marie Gordon", url=os.getenv("URL"), work_experience=work_experience, education=education)

@app.route('/hobbies')
def hobbies():
    hobbies_list = [
        {"name": "Gaming", "image": "/static/img/hobbies/World_of_Warcraft.png"},
        {"name": "Cross-Stitching", "image": "/static/img/hobbies/Dragon-X-Stitch.jpg"},
        {"name": "Legos", "image": "/static/img/hobbies/DD_Lego.jpg"},
        {"name": "Reading", "image": "/static/img/hobbies/books.webp"},
        {"name": "Web Development", "image": "/static/img/hobbies/web-dev.jpg"}
    ]
        
    return render_template(
        'hobbies.html',
        title="Hobbies",
        hobbies=hobbies_list
    )