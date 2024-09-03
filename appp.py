from flask import Flask, jsonify
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin

app = Flask(__name__)

class TimeStoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stories = []
        self.in_story = False
        self.title = ''
        self.link = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h2' and len(self.stories) < 6:
            self.in_story = True
        elif tag == 'a' and self.in_story:
            for attr in attrs:
                if attr[0] == 'href':
                    self.link = attr[1]

    def handle_data(self, data):
        if self.in_story:
            self.title = data.strip()

    def handle_endtag(self, tag):
        if tag == 'h2' and self.in_story:
            full_link = urljoin('https://time.com', self.link)
            self.stories.append({
                'title': self.title,
                'link': full_link
            })
            self.in_story = False
            self.title = ''
            self.link = ''

@app.route('/')
def index():
    return "Welcome to the Time Stories API. Use the '/getTimeStories' endpoint to fetch stories."

@app.route('/getTimeStories', methods=['GET'])
def get_time_stories():
    url = 'https://time.com'
    try:
        response = requests.get(url)
        response.raise_for_status()  
        parser = TimeStoryParser()
        parser.feed(response.text)
        return jsonify(parser.stories)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
