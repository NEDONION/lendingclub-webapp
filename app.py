import streamlit as st
import pandas as pd
import pickle
import boto3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_option('deprecation.showPyplotGlobalUse', False)

def display_wc(wc):
	plt.imshow(wc, interpolation='bilinear')
	plt.axis("off")
	plt.show()
	st.pyplot()

page = st.sidebar.selectbox(
	'',
	('Dashboard', 'Model', 'Team')
	)

if page == 'Dashboard':
	st.title('Sentiment Prediction')
	st.write('This dashboard predicts sentiment of Reddit posts in "r/movies" subreddit using our Machine Learning model')
	st.markdown(' --- ')

	db_client = boto3.client('dynamodb', region_name='us-east-1')
	resp = db_client.scan(TableName='reddit')
	d = []
	pos = 0
	neg = 0
	postext = ""
	negtext = ""
	for item in resp['Items']:
		d.append({
			'selftext': item['selftext']['S'], 
			'sentiment': item['sentiment']['S']})
		if item['sentiment']['S'] == 'positive':
			pos += 1
			postext += item['selftext']['S'] + " " 
		else:
			neg += 1 
			negtext += item['selftext']['S'] + " "
	df = pd.DataFrame(d)
	st.bar_chart(df['sentiment'].value_counts())
	
	with st.container():
		col1, col2 = st.columns(2)
		with col1:
			st.metric(label="Positive", value=pos)
		with col2:
			st.metric(label="Negative", value=neg)
	st.markdown(' --- ')

	st.subheader('Word Cloud')
	col1, col2 = st.columns(2)
	with col1:
		poswc = WordCloud(max_words=50).generate(postext)
		display_wc(poswc)
		st.text('Top 50 Positive Sentiment Posts')
	with col2:
		negwc = WordCloud(max_words=50).generate(negtext)
		display_wc(negwc)
		st.text('Top 50 Negative Sentiment Posts')
	st.markdown(' --- ')

	st.subheader('Sample Posts and Sentiment Prediction')
	with st.expander('See sample'):
		for index, row in df.sample(5).iterrows():
			st.markdown(' --- ')
			st.write(row['selftext'])
			if row['sentiment'] == 'positive':
				st.success('Positive')
			else:
				st.error('Negative')

elif page == 'Model':
	st.title('Our Sentiment Model')
	st.markdown(' --- ')
	# df = pd.read_csv("IMDB_movie_reviews_train.csv")
	# X = df.loc[:,['review']]
	# X_docs = [doc for doc in X.review]
	# vect = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=2000)
	# a = vect.fit_transform(X_docs)
	# feature_names = vect.get_feature_names()
	# dense = a.todense().tolist()
	# df = pd.DataFrame(dense, columns=feature_names)
	# wc = WordCloud(background_color="white", max_words=50).generate_from_frequencies(df.T.sum(axis=1))  
	# display_wc(wc)
	st.image('tfidf_wordcloud.png')
	st.text('Word Cloud Showing TfIdf Vectorizer of Our Sentiment Model')
	st.markdown(' --- ')

	st.subheader("Test Sentiment Model")
	text = st.text_area(label="Movie Review Text")
	if st.button("Predict Sentiment"):
		with st.spinner('Wait! Our model is predicting sentiment...'):
			# write your code to predict the sentiment using your model and vectorizer file
			s3_client = boto3.client('s3')
			model = pickle.loads(s3_client.get_object(Bucket='yhegde-model-files', Key='sentiment.model')['Body'].read())		
			vect = pickle.loads(s3_client.get_object(Bucket='yhegde-model-files', Key='sentiment.vect')['Body'].read())	
			X = vect.transform([text])
			pred = model.predict(X)[0]
			st.write('Predicted sentiment is: ')
			if pred == 'positive':
				st.success(pred)
			else:
				st.error(pred)
			st.balloons()

elif page == 'Team':
	st.title('About Us')
	st.markdown(' --- ')
	st.write('description about your team')
	st.subheader('Team')
	col1, col2 = st.columns(2)
	with col1:
		st.image('unnamed.jpg')
	with col2: 
		st.write('Member 1 bio')
	col1, col2 = st.columns(2)
	with col1:
		st.image('unnamed.jpg')
	with col2: 
		st.write('Member 2 bio')




