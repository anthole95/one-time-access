from flask import Flask, request, render_template, url_for, abort
import uuid

app = Flask(__name__)

text_storage = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_text = request.form['text']
        unique_id = str(uuid.uuid4())
        text_storage[unique_id] = user_text
        full_link = url_for('get_text', unique_id=unique_id, _external=True)
        # HTML for the response with "Return" and "Close" buttons
        response_html = f'''
        <p>Generated link: <a href="{full_link}">{full_link}</a></p>
        <p><a href="{url_for('index')}"><button>Return</button></a></p>
        '''
        response = make_response(response_html)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return render_template('index.html')

@app.route('/get/<unique_id>', methods=['GET'])
def get_text(unique_id):
    if unique_id in text_storage:
        user_text = text_storage.pop(unique_id)
        response = make_response(user_text)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        abort(404)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
