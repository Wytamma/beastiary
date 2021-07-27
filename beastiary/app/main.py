from os import error
from fastapi import FastAPI
from beastiary.watcher import Watcher
import time

watcher = Watcher()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

    # from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, session

@app.get("/check/{path}")
async def watch(path):
    task = watcher.get(path)
    if not task:
        return {"message": "task not found"}
    if task.done():
        try:
            task.result()
            return {"message": "task ended"}
        except Exception as e:
            return {"message": str(e)} 
    return {"message": "task running"}

@app.get("/watch/{path}")
async def watch(path):
    task = watcher.watch(path)
    print(watcher.tasks)
    return {"message": path}

    # from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, session

# import random
# import logging
# import json
# from datetime import datetime, timezone
# import os

# from .models import Sample, db, Run

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///beastairy.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# @app.route('/')
# def home():
#     number_of_samples = Sample.query.count()
#     return render_template('index.html', number_of_samples=number_of_samples)


# @app.route('/api/runs')
# def runs():
#     runs = Run.query.all()
#     return jsonify([{'filename': r.filename, 'run_id':r.id} for r in runs])


# @app.route('/api/<run_id>/<sample_id>')
# def api(run_id = None, sample_id = -1):
#     print(run_id)
#     samples = Sample.query.filter(Sample.run_id==run_id).filter(Sample.sample_id > sample_id).all()
#     return jsonify([{'sample_id': s.sample_id, 'likelihood':s.data['likelihood']} for s in samples])
