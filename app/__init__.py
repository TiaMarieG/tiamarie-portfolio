import os
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
from datetime import datetime

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

# Define TimelinePost model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

# Connect and create table if it doesn't exist

mydb.connect()
mydb.create_tables([TimelinePost])

# Navigation links for base layout
NAV_LINKS = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
    {"name": "Timeline", "endpoint": "timeline"}
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
            "description": "Compared stock to online inventory to ensure accuracy."
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

@app.context_processor
def inject_globals():
    return dict(nav_links=NAV_LINKS, now=datetime.now)

# POST endpoint to create a timeline post
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return "Invalid name", 400
    if not email or "@" not in email:
        return "Invalid email", 400
    if not content:
        return "Invalid content", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

# GET endpoint to retrieve all posts, newest first
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

# Timeline form & display page
@app.route('/timeline')
def timeline():
    return render_template('timeline.html')
