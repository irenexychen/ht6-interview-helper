from flask import Flask, render_template
import cv2

app = Flask(__name__)

# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='ElevAIte')

if __name__ == '__main__':
    app.run(debug=True)
