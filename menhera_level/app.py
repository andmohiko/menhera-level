import pickle

from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from wordsplit import get_words
from load_model import load_models

app = Flask(__name__)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('style.scss', filters='pyscss', output='style.css')
assets.register('scss_all', scss)

(stopwords, word_vector_dict, rfc) = load_models()


@app.route('/', methods=['GET'])
def get():
		return render_template('index.html', \
			title = 'Form Sample(get)', \
			message = 'ツイートを入力して下さい。')


@app.route('/', methods=['POST'])
def post():
		tweet = request.form['tweet']
		prediction_result = predict(tweet)
		return render_template('index.html', \
			title = 'Form Sample(post)', \
			original_text = tweet, \
			tweet_words = prediction_result[0], \
			prediction = prediction_result[1], \
		)


def predict(tweet):
		# 単語分割
		tweet_words = get_words(tweet, pos_list=["名詞", "動詞", "形容詞"], form="origin", stopwords=stopwords)
		if tweet_words == []:
				return "no words to predict"
		# ベクトル化
		sentence_vector = vectorize(tweet_words)
		# 予測
		y_pred = rfc.predict_proba([sentence_vector])[0][1]
		# 結果
		# メンヘラ度
		return tweet_words, y_pred


def vectorize(word_list):
		sentence_vector = 0
		(_, word_vector_dict, rfc) = load_models()
		for w in word_list:
				if w not in word_vector_dict.keys():
						word_vector_dict = update_word_vector_dict(word)
				sentence_vector += word_vector_dict[w]
		if np.linalg.norm(sentence_vector) == 0:
				return "error: vector size 0"
		return sentence_vector / np.linalg.norm(sentence_vector)


def update_word_vector_dict(word):
		try:
				word_vector_dict[word] = model[word]
		except KeyError:
				word_vector_dict[word] = np.random.rand(300)
		with open('models/word_vector_dict.pickle', 'wb') as f:
				pickle.dump(word_vector_dict, f)
		return word_vector_dict


## おまじない
if __name__ == "__main__":
    app.run(debug=True)
