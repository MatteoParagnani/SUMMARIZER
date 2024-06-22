from flask import Flask, request, render_template_string, redirect, url_for, render_template
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud
from matplotlib import pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)



def riassumi(testo):
    parole = word_tokenize(testo, language='italian')
    stop_words = set(stopwords.words('italian'))
    frasi = sent_tokenize(testo, language='italian')
    parole = [x.lower() for x in parole if (x.lower() not in stop_words and x.isalpha())]  
    lemmatizer = WordNetLemmatizer()   
    parole = [lemmatizer.lemmatize(x) for x in parole]                                      
    
    wc = WordCloud().generate(' '.join([i for i in parole]))
    plt.imshow(wc)
    freq_dist = FreqDist(parole)
    punteggio_frasi = {}

    for i, sentence in enumerate(frasi):
      sentence_words = word_tokenize(sentence.lower())
      sentence_score = sum([freq_dist[word] for word in sentence_words if word in freq_dist])
      punteggio_frasi[i] = sentence_score
    punteggi_ordinati = sorted(punteggio_frasi.items(), key=lambda x: x[1], reverse=True)
    frasi_selezionate = punteggi_ordinati[:1]

    frasi_selezionate = sorted(frasi_selezionate)
    sommario = ' '.join([frasi[i] for i, _ in frasi_selezionate])
     # ...
    return sommario

@app.route('/', methods=['GET', 'POST'])
def home(): 
    if request.method == 'POST':
        testo = request.form["text"]
        testo = riassumi(testo)
        return render_template('index.html', riassunto=testo)

    return render_template('index.html', riassunto="Il riassunto apparirà qui...")

if __name__ == "__main__":
  app.run(debug=True)