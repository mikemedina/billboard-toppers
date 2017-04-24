from flask import Flask
from flask_ask import Ask, statement, question, session

import bs4 as bs
import urllib.request


class Record():
    def __init__(self, rank, artist, song):
        self.rank = rank
        self.artist = artist
        self.song = song

    def __str__(self):
        return '{} by {}'.format(self.song, self.artist)

url = 'http://www.billboard.com/charts/hot-100'
source = urllib.request.urlopen(url)
soup = bs.BeautifulSoup(source, 'lxml')

app = Flask(__name__)
ask = Ask(app, "/billboard-top-ten")

@ask.launch
def start_skill():
    return share_top_ten()

@ask.intent("YesIntent")
def share_top_ten():
    return statement("Here are the top 10 songs for today: {}".format(stringify_records(get_records())))

@ask.intent("NoIntent")
def no_intent():
    return statement('Alright, bye then!')
 
def get_records():
    records = []
    try:
        for article in soup.find_all('article')[:10]:
            if 'chart-row' in article.get('class'):
                rank = article.find_all('span', class_='chart-row__current-week')[0].text.strip()
                artist = article.find_all(class_='chart-row__artist')[0].text.strip()
                song = article.find_all('h2', class_='chart-row__song')[0].text.strip()

                records.append(Record(rank, artist, song))
    except:
        pass

    return records

def stringify_records(records):
    if not records:
        response = "I'm sorry, I couldn't get any billboard information"
    elif len(records) == 1:
        response = str(records[0])
    else:
        response = ', '.join(str(record) for record in records[:-1])
        response += ', and ' + str(records[-1])

    return response
   
if __name__ == '__main__':
    app.run(debug=True)

