from teamcity import app
from flask import render_template, flash, redirect, session, url_for, request, g

@app.route('/')
@app.route('/index')
def index():
    app.logger.debug('A value for debugging')
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404