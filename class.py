import requests
import json
from html.parser import HTMLParser

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
            self.stories.append({
                'title': self.title,
                'link': 'https://time.com' + self.link
            })
            self.in_story = False
            self.title = ''
            self.link = ''

def get_time_stories():
    url = 'https://time.com'
    response = requests.get(url)
    parser = TimeStoryParser()
    parser.feed(response.text)
    return json.dumps(parser.stories)

if __name__ == '__main__':
    print(get_time_stories())