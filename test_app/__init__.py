# -*- coding: utf-8 -*-
"""
    flask-fillin-test-app
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/login-form", methods=["GET", "POST"])
def login_form():
    msg = None
    if request.method == "POST":
        if not request.form.get('username'):
            msg = "Missing username"
        if not request.form.get('password'):
            msg = "Missing password"

        if not msg:
            msg = "Welcome " + request.form.get('username')

    return render_template("login_form.html", msg=msg)

@app.route("/hidden-field-form", methods=["GET", "POST"])
def hidden_field_form():
    msg = None
    if request.method == "POST":
        if not request.form.has_key('hidden_field'):
            msg = "Missing the hidden field"
        else:
            msg = "Hidden field received"

    return render_template("hidden_field_form.html", msg=msg)

@app.route("/checkbox-field-form", methods=["GET", "POST"])
def checkbox_field_form():
    msg = None
    if request.method == "POST":
        if request.form.get('checkbox_field', False):
            msg = "Checkbox checked"
        else:
            msg = "Checkbox did not check"

    return render_template("checkbox_field_form.html", msg=msg)

@app.route("/radio-field-form", methods=["GET", "POST"])
def radio_field_form():
    msg = None
    if request.method == "POST":
        radio_value = request.form.get('radio_field', False)
        if radio_value:
            msg = "Selected {}".format(radio_value)
        else:
            msg = "No Radio Value Selected"

    return render_template("radio_field_form.html", msg=msg)

@app.route("/select-field-form", methods=["GET", "POST"])
def select_field_form():
    msg = None
    if request.method == "POST":
        value = request.form.get('select_field', None)
        if request.form.get('select_field', None):
            msg = value
        else:
            msg = "No value selected"

    return render_template("select_field_form.html", msg=msg)

@app.route("/all-fields-form", methods=["GET", "POST"])
def all_fields_form():
    msg = None
    if request.method == "POST":
        if request.form.get('checkbox_field', False):
            msg = "Checkbox checked"
        else:
            msg = "Checkbox did not check"

    return render_template("all_fields_form.html", msg=msg)

@app.route("/empty-field-form", methods=["GET", "POST"])
def empty_field_form():
    msg = None
    if request.method == "POST":
        if request.form['text1'] is not None and request.form['text2'] is not None:
            msg = "No None"
        else:
            msg = "Found None"

    return render_template("empty_field_form.html", msg=msg)

@app.route('/link')
def link():
    return render_template('link.html')

@app.route("/file-form", methods=["GET", "POST"])
def file_form():
    msg = None
    if request.method == "POST":
        if request.form.get('text', False) and request.files.get('file', False):
            msg = "File submitted"
        else:
            msg = "File not submitted"

    return render_template("file_form.html", msg=msg)


if __name__ == "__main__":
    app.run()
