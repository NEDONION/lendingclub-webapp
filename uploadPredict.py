import streamlit as st
import pandas as pd
from joblib import dump,load
import pickle
import time
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


def app():

    st.header('标题1')
    st.write('''
             At **Borrow Faster**, we are dedicated to offering the most effective evaluation model to help business, applicants estimate their eligibility for loan applications. We make full use of four supervised machine learning techniques(**Logistic Regression**, **Naive Bayers**, **K-Nearest Neighbors**, and **Decision Tree**) to learn how to best make predictions.
             ''')

  
    @st.cache(allow_output_mutation=True)
    def openModel(path):
        model  = pickle.load(open(path, 'rb'))
        return model
    
    nb = openModel('model/lc_nb.model')
    lr = openModel('model/lc_lr.model')
    knn = openModel('model/lc_knn.model')
    svc = openModel('model/lc_svc.model')
    dt = openModel('model/lc_dt.model')
    # xgb = openXgb()
    pipeline = openModel('model/feature.pipeline')
    
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
        
        # 判定数据集合法
        if len(df.columns) > 13:
            st.error("More than 13 columns")
            st.stop()
        elif len(df.columns) < 13:
            st.error("Less than 13 columns")
            st.stop()
        else:
            st.success("Correct number of columns")
        
        @st.cache(allow_output_mutation=True)
        def showReport(df):
            pr = df.profile_report()
            return pr
        
        with st.expander("REPORT", expanded=True):
            my_bar = st.progress(0)
            pr = showReport(df)
            st_profile_report(pr)
            
            for percent_complete in range(100):
                time.sleep(0.02)
                my_bar.progress(percent_complete + 1)
                
            my_bar.empty()
        
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
            lr_pred = lr.predict(lc_X_tr)
            nb_pred = nb.predict(lc_X_tr)
            
            df['knn_predict'] = knn_pred
            df['dt_predict'] = dt_pred
            df['lr_predict'] = lr_pred
            df['nb_predict'] = nb_pred
            
            @st.cache(allow_output_mutation=True)
            def posAndNeg(pred):
                fp = nfp = 0
                for i in pred:
                    if i == 0:
                        fp += 1
                    else:
                        nfp += 1
                return fp, nfp
            
            st.markdown("<h5 style='color:#F63366;'><b>KNN Model<b></h5>", unsafe_allow_html=True)
            
            knn_fp, knn_nfp = posAndNeg(knn_pred)
            # knn_fp = len(df[df['knn_predict'] == 0])
            # knn_nfp = len(df[df['knn_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=knn_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=knn_nfp)
            
            st.markdown(" --- ")
            
            st.markdown("<h5 style='color:#F63366;'><b>Decision Tree Model<b></h5>", unsafe_allow_html=True)
            
            dt_fp, dt_nfp = posAndNeg(dt_pred)
            # dt_fp = len(df[df['dt_predict'] == 0])
            # dt_nfp = len(df[df['dt_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=dt_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=dt_nfp)
                    
            st.markdown(" --- ")
            
            st.markdown("<h5 style='color:#F63366;'><b>Logistic Regression Model<b></h5>", unsafe_allow_html=True)
            
            lr_fp, lr_nfp = posAndNeg(lr_pred)
            # jq_fp = len(df[df['model_predict'] == 0])
            # jq_nfp = len(df[df['model_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=lr_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=lr_nfp)
            
            st.markdown(" --- ")
            
            st.markdown("<h5 style='color:#F63366;'><b>Naive Bayers Model<b></h5>", unsafe_allow_html=True)
            
            nb_fp, nb_nfp = posAndNeg(nb_pred)
            # nb_fp = len(df[df['nb_predict'] == 0])
            # nb_nfp = len(df[df['nb_predict'] == 1])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="fully_paid", value=nb_fp)
                with col2:
                    st.metric(label="not_fully_paid", value=nb_nfp)