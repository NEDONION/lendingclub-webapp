import streamlit as st
import pandas as pd
from joblib import dump,load
from sklearn import metrics
from sklearn.metrics import confusion_matrix,plot_confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from io import BytesIO
import boto3
import json

st.header('Lending Club: Predict Whether a Loan Will Go Bad')
st.write('Upload LendingClub Clients Infomation to Make Predictions' )

#lin_svc=pickle.load(open('linear_svc_model','rb'))
#vect=pickle.load(open('feature_transform','rb'))

client=boto3.client('s3',
aws_access_key_id='ASIA42EKXV7EOMFZYTVU'
,aws_secret_access_key='I0T3ecUllwPLWGTCaKArCCE9SMXbJyAlRxlOpGkz'
,aws_session_token='FwoGZXIvYXdzENn//////////wEaDADTXN3zVuqqgAOjpSLBAUndxwQS4POSpXkW3bNVJocQw5TogS/WMgse2vZeTp1VK9rtl0NX7JP7sSwi8KVd2xG2faBB/sPhp3ZS1dKVC5PC3+cw39XB/Pdp3cL926sRUYPpRuWaOHnEgo+QR9F/DZCtNRHCOXmx20PHhuzyoFXHN8wDLCu87f/ZpRiRjJt/D9fQzvLbKUvGx87Zyi9ClQcs0CEl3qompVLmfbh24nETiXxTW1BddXSQJxHqxNi4Vjun48kLgxzhey7j/a74108oh568jQYyLcl2z1Y5eRwXngK4MrZ+LdDPaHfqvrd/b9fggDeuM5yrXqoD3DXpr5sPIIfWuQ=='
	,region_name='us-east-1'
	)

db_client = boto3.client('dynamodb', region_name='us-east-1')
resp = db_client.scan(TableName='LendingClub')
d = []
nfp = 0
fp = 0
# st.write(resp['Items'])

for rec_data in resp['Items']:
	d.append({
	'credit_policy':rec_data['credit_policy']['S'],
	'purpose':rec_data['purpose']['S'],
	'int_rate':rec_data['int_rate']['S'],
	'installment':rec_data['installment']['S'],
	'log_annual_inc':rec_data['log_annual_inc']['S'],
	'dti':rec_data['dti']['S'],
	'fico':rec_data['fico']['S'],
	'days_with_cr_line':rec_data['days_with_cr_line']['S'],
	'revol_bal':rec_data['revol_bal']['S'],
	'revol_util':rec_data['revol_util']['S'],
	'inq_last_6mths':rec_data['inq_last_6mths']['S'],
	'delinq_2yrs':rec_data['delinq_2yrs']['S'],
	'pub_rec':rec_data['pub_rec']['S'],
	'not_fully_paid':rec_data['not_fully_paid']['N'] #Note 'N'
	})
	if rec_data['not_fully_paid']['N'] == '0':
		fp += 1
	# postext += item['selftext']['S'] + " " 
	else:
		nfp += 1 
	# negtext += item['selftext']['S'] + " "
df_2 = pd.DataFrame(d)
st.bar_chart(df_2['not_fully_paid'].value_counts())
 
with st.container():
	col1, col2 = st.columns(2)
	with col1:
		st.metric(label="fully_paid", value=fp)
	with col2:
		st.metric(label="not_fully_paid", value=nfp)





# #read model and pipeline files from S3 directly
resp_1 = client.get_object(Bucket='lc-pipeline-model', Key='feature.pipeline')
pipeline = BytesIO(resp_1['Body'].read())
pipeline=load(pipeline)

resp_2 = client.get_object(Bucket='lc-pipeline-model', Key='lc_xgb.model')
xgb =BytesIO(resp_2['Body'].read())
xgb=load(xgb)

resp_3 = client.get_object(Bucket='lc-pipeline-model', Key='lc_dt.model')
dt =BytesIO(resp_3['Body'].read())
dt=load(dt)

resp_4 = client.get_object(Bucket='lc-pipeline-model', Key='lc_svc.model')
svc =BytesIO(resp_4['Body'].read())
svc=load(svc)


choose_model=st.sidebar.selectbox(
	'Choose A Prediction Model',
	('XGBOOST','Decision Tree','SVM')
	)

uploaded_file = st.file_uploader("Choose a file")


if uploaded_file is not None:
	df = pd.read_csv(uploaded_file)
	st.write("Let's take a look at the raw testing data")
	st.write(df.head(5))
	df=df.iloc[0:100]

	X=df

	lc_X_tr=pipeline.fit_transform(X)

	if choose_model=='XGBOOST':
		model=xgb
	elif choose_model=='Decision Tree':
		model=dt
	else:
		model=svc

	y_test_pred=model.predict(lc_X_tr)

	df['not_fully_paid']=y_test_pred

	st.write('The test result is as follows:')

	st.write(df)


	







