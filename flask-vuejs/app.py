from flask import Flask, render_template, jsonify, request
from datetime import datetime


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
      block_start_string='{%',
      block_end_string='%}',
      variable_start_string='((',
      variable_end_string='))',
      comment_start_string='{#',
      comment_end_string='#}',
    ))

app = CustomFlask(__name__)

#pages


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/example')
def example():
    message = "Hello Flask!"
    return render_template('example.html', message=message)

@app.route('/result_summary')
def result_summary():
    return render_template('example.html', message=message)




if __name__ == '__main__':
    app.run(debug=True)
