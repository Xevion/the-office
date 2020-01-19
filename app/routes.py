from app import app
from flask import send_from_directory, redirect, url_for, render_template

@app.route('/')
def index():
    return 'WIP'