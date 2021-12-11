import streamlit as st
import pandas as pd
from joblib import dump,load
from sklearn import metrics
from sklearn.metrics import confusion_matrix,plot_confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
import boto3
import json
import matplotlib.pyplot as plt
import graphviz as graphviz


st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
    st.markdown("<h1 style='text-align: center;'>Connect to AWS Service</h1>", unsafe_allow_html=True)
    # st.header('Connect to AWS Service')
    st.markdown("<h3 style='color:#F63366;'><b>Introduction<b></h3>", unsafe_allow_html=True)
    st.write('''
             At **Borrow Faster**, we provide an unsafe network transmission method for users to enter AWS Token to connect the AWS for demo.
             
             - Enter your account information (region time, dynamoDB table name, etc).
             - Enter your predict output column name.
             - Enter your AWS Token.
             - Your predicted result in the DynamoDB table will be generated below.
             
             ''')

    
    st.markdown("<h3 style='color:#F63366;'><b>Workflow<b></h3>", unsafe_allow_html=True)
    # graph.edge(' LambdaFunc1 Upload Test Data to Dynamodb Table', 'Fetch Data')
    # graph.edge('Fetch Data', 'S3 Bucket Test Data')
    # Create a graphlib graph object
    st.graphviz_chart('''
    digraph {
        { 
            node [shape=box style=filled]
            "S3 Bucket Test Data"[fillcolor=lightsalmon2]
            "LambdaFunc1 
        Upload Test Data to Dynamodb Table"[fillcolor=cornsilk2]
            "S3 Bucket
        FeaturePipeline+Predict Model"[fillcolor=lightsalmon2]
            "Dynamodb Table
        LendingClub"[fillcolor=aquamarine2]
            "LambdaFunc2
        MakePredictions & Insert Output to Dynamodb Table"[fillcolor=cornsilk2]
        
        }
        "S3 Bucket Test Data" -> "LambdaFunc1 
        Upload Test Data to Dynamodb Table"
        
        "LambdaFunc1 
        Upload Test Data to Dynamodb Table" -> "Dynamodb Table
        LendingClub"
        
        "S3 Bucket
        FeaturePipeline+Predict Model" -> "LambdaFunc2
        MakePredictions & Insert Output to Dynamodb Table"
        
        "LambdaFunc2
        MakePredictions & Insert Output to Dynamodb Table" -> "Dynamodb Table
        LendingClub"
        
        "Dynamodb Table
        LendingClub" -> "LambdaFunc2
        MakePredictions & Insert Output to Dynamodb Table"
    }
''')
    
    
    st.markdown(" --- ")
    #lin_svc=pickle.load(open('linear_svc_model','rb'))
    #vect=pickle.load(open('feature_transform','rb'))

    region_name = st.selectbox(
     'Region Time',
     ('us-east-1','others'))
    st.write('You selected:', region_name)
    if region_name == 'others':
        st.error("Wrong Region Time")
        
    
    s3_bucket = st.text_input('S3 Bucket Name')

    if not s3_bucket:
        st.error("Missing S3 Bucket Name")
    else:
        st.write('You selected:', s3_bucket)

    db_table = st.text_input('DynamoDB Table Name')
    if not db_table:
        st.error("Missing DynamoDB Table Name")
    else:
        st.write('You selected:', db_table)
    
    predict_column = st.text_input('Predict Output Column Name')
    if not predict_column:
        st.error("Missing Predict Output Column Name")
    else:
        st.write('You selected:', predict_column)
    
    paras = { 
    'db_table':db_table,
    'region_name': region_name,
    's3_bucket': s3_bucket,
    'predict_column': predict_column
}
    
    awstoken = st.text_area('Enter AWS Token: ')
    if not awstoken:
        st.error("Missing AWS Token")
    
    if st.button('Click to connect'):
        st.markdown(" --- ")
        
        def readKeys(text):
            lines = text.split("\n")
            key_id = lines[0].split("=")[1]
            access_key = lines[1].split("=")[1]
            session_token = lines[2].split("=")[1]
            return key_id, access_key, session_token

        key_id, access_key, session_token = readKeys(awstoken)


        client = boto3.client('s3', 
                    aws_access_key_id = key_id,
                    aws_secret_access_key = access_key,
                    aws_session_token = session_token,
                    region_name = paras['region_name'])


        db_client = boto3.client('dynamodb', 
                                aws_access_key_id = key_id,
                                aws_secret_access_key = access_key,
                                aws_session_token = session_token,
                                region_name=paras['region_name'])

        resp = db_client.scan(TableName=paras['db_table'])
        d = []
        nfp = 0
        fp = 0
        unknown = 0
        # st.write(resp['Items'])

        for rec_data in resp['Items']:
            d.append({
            'credit_policy': rec_data['credit_policy']['S'],
            'purpose': rec_data['purpose']['S'],
            'int_rate': rec_data['int_rate']['S'],
            'installment': rec_data['installment']['S'],
            'log_annual_inc': rec_data['log_annual_inc']['S'],
            'dti': rec_data['dti']['S'],
            'fico': rec_data['fico']['S'],
            'days_with_cr_line': rec_data['days_with_cr_line']['S'],
            'revol_bal': rec_data['revol_bal']['S'],
            'revol_util': rec_data['revol_util']['S'],
            'inq_last_6mths': rec_data['inq_last_6mths']['S'],
            'delinq_2yrs': rec_data['delinq_2yrs']['S'],
            'pub_rec': rec_data['pub_rec']['S'],
            predict_column: rec_data[predict_column]['N']
            })
            if rec_data[predict_column]['N']:
                if rec_data[predict_column]['N'] == '0':
                    fp += 1
                elif rec_data[predict_column]['N'] == '1':
                    nfp += 1 
                else:
                    unknown += 1
            elif rec_data[predict_column]['S']:
                if rec_data[predict_column]['S'] == '0':
                    fp += 1
                elif rec_data[predict_column]['S'] == '1':
                    nfp += 1 
                else:
                    unknown += 1
            else:
                st.error("AWS Still Running. Please wait...")
        
        df_2 = pd.DataFrame(d)
        df_show = df_2.head()
        st.write(df_show)
        
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="fully_paid", value=fp)
            with col2:
                st.metric(label="not_fully_paid", value=nfp)
            with col3:
                st.metric(label="unknown", value=unknown)
        
        
        col4, col5 = st.columns(2)
        
        with col4:

            fully_paid = df_2[df_2[predict_column]=='0']['credit_policy'].value_counts()
            not_fully_paid = df_2[df_2[predict_column]=='1']['credit_policy'].value_counts()
            st.write('Loan Payment(Result) Distribution by Credit Policy')
            df = pd.DataFrame([fully_paid,not_fully_paid])
            df.index = ('fully_paid','not_fully_paid')
            st.bar_chart(df)

        with col5:
            fully_paid = df_2[df_2[predict_column]=='0']['purpose'].value_counts()
            not_fully_paid = df_2[df_2[predict_column]=='1']['purpose'].value_counts()
            st.write('Loan Payment(Result) Distribution by Purpose')
            df = pd.DataFrame([fully_paid,not_fully_paid])
            df.index = ('fully_paid','not_fully_paid')
            st.bar_chart(df)


        #histogram['dti','log_annual_inc','revol_bal','fico','int_rate']
        cols = ['dti','log_annual_inc','revol_bal','fico','int_rate']
        # data[cols] = data[cols].apply(pd.to_numeric, errors='coerce', axis=1)
        df_2[cols] = df_2[cols].apply(pd.to_numeric)


        col6, col7 = st.columns(2)
        with col6:
            st.write('Dti and Log_annual_inc Histogram')
            df_3 = pd.DataFrame(df_2, columns =['dti','log_annual_inc'])
            df_3.hist()
            plt.show()
            st.pyplot()

        with col7:
            st.write('Fico score and Int_rate Histogram')
            df_4 = pd.DataFrame(df_2, columns =['fico','int_rate'])
            df_4.hist()
            plt.show()
            st.pyplot()