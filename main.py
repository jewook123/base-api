from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_youtube():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        if 'ytInitialPlayerResponse' in str(script_tag):
            script_content = script_tag.string
            if script_content:
                start = script_content.index('{')
                end = script_content.rindex('}') + 1
                json_data = script_content[start:end]
                return json_data

    return 'No YouTube script found in the page.'


if __name__ == '__main__':
    app.run(debug=True)
