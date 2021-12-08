import streamlit as st
import pandas as pd
from joblib import dump,load
import pickle
import time

def app():

    st.header('Lending Club: Predict Whether a Loan Will Go Bad')
    st.write('Upload LendingClub Clients Infomation to Make Predictions' )

    @st.cache(allow_output_mutation=True)
    def openSvc():
        svc = pickle.load(open('model/lc_svc.model', 'rb'))
        return svc
    
    @st.cache(allow_output_mutation=True)
    def openPipeline():
        pipeline = pickle.load(open('model/feature.pipeline', 'rb'))
        return pipeline

    @st.cache(allow_output_mutation=True)
    def openDt():
        dt = pickle.load(open('model/lc_dt.model', 'rb'))
        return dt

    @st.cache(allow_output_mutation=True)
    def openXgb():
        xgb = pickle.load(open('model/lc_xgb.model', 'rb'))
        return xgb

    @st.cache(allow_output_mutation=True)
    def openKnn():
        knn = pickle.load(open('model/lc_knn.model', 'rb'))
        return knn
    
    @st.cache(allow_output_mutation=True)
    def openModel():
        model  = pickle.load(open('model/lc.model', 'rb'))
        return model
    
    @st.cache(allow_output_mutation=True)
    def openNb():
        nb  = pickle.load(open('model/lc_nb.model', 'rb'))
        return nb
    
    nb = openNb()
    model = openModel()
    knn = openKnn()
    svc = openSvc()
    dt = openDt()
    # xgb = openXgb()
    pipeline = openPipeline()
    
    # choose_model=st.selectbox(
	# 'Choose A Prediction Model',
	# ('KNN','Decision Tree')
	# )

    uploaded_file = st.file_uploader("Choose a file")

    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Let's take a look at the raw testing data")
        st.write(df.head(5))
        # df = df.iloc[0:100]

        st.markdown(" --- ")
        if st.button("Predict My CSV"):
            
            with st.spinner('Processing...'):
                time.sleep(1)
            st.success('Done!')
            X = df

            lc_X_tr = pipeline.transform(X)

            # if choose_model == 'XGBOOST':
            #     model = xgb
            # if choose_model == 'Decision Tree':
            #     model = dt
            # elif choose_model == 'KNN':
            #     model = knn

            knn_pred = knn.predict(lc_X_tr)
            dt_pred = dt.predict(lc_X_tr)
            model_pred = model.predict(lc_X_tr)
            nb_pred = nb.predict(lc_X_tr)
            
            df['knn_predict'] = knn_pred
            df['dt_predict'] = dt_pred
            df['model_predict'] = model_pred
            df['nb_predict'] = nb_pred
            
            
            st.markdown("<h5 style='color:#F63366;'><b>KNN Model<b></h5>", unsafe_allow_html=True)
            knn_fp = len(df[df['knn_predict'] == 0])
            knn_nfp = len(df[df['knn_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=knn_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=knn_nfp)
            
            st.markdown(" --- ")
            
            st.markdown("<h5 style='color:#F63366;'><b>Decision Tree Model<b></h5>", unsafe_allow_html=True)
            
            dt_fp = len(df[df['dt_predict'] == 0])
            dt_nfp = len(df[df['dt_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=dt_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=dt_nfp)
                    
            st.markdown(" --- ")
            
            st.markdown("<h5 style='color:#F63366;'><b>嘉全 Model<b></h5>", unsafe_allow_html=True)
            
            jq_fp = len(df[df['model_predict'] == 0])
            jq_nfp = len(df[df['model_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=jq_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=jq_nfp)
            
            st.markdown(" --- ")
            
            st.markdown("<h5 style='color:#F63366;'><b>NB Model<b></h5>", unsafe_allow_html=True)
            
            nb_fp = len(df[df['nb_predict'] == 0])
            nb_nfp = len(df[df['nb_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=nb_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=nb_nfp)