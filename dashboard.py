import pandas as pd
import streamlit as st

df1 = pd.read_excel('R03731s.xlsx')
df2 = pd.read_excel('Neonatology Report 10-28-2021draft.xlsx')

df1_cols = ['STAR#', 'LLeRA#', 'IRB#', 'ShortTitle',
 'Nickname', 'PI', 'IRB Status', 'IRB Expiration Date']
df2_cols = ['STAR#', 'Regulatory / Coordinator', 'Inclusion', 'Exclusion',
 '# Subject Approved', 'Consented', 'Active', 'Questions and Comments', 'Study Status Updates']

df = df1[df1_cols].merge(df2[df2_cols])

df = df.astype(str)
df['LLeRA#'] = df['LLeRA#'].astype('string').str.split('.').str[0]
df['IRB#'] = df['IRB#'].astype('string').str.split('.').str[0]
df['IRB Expiration Date'] = df['IRB Expiration Date'].str.split(' ').str[0]

# sidebar
st.sidebar.write('Filter Studies By PI')
filter_PI = st.sidebar.selectbox(label = 'Select PI', options = df['PI'].sort_values().unique())

# main
st.title('NICU Clinical Trials Dashboard')
st.header('Studies for {}'.format(filter_PI))
df = df.query('PI == @filter_PI')

study_title = st.selectbox(label = 'Select Study Short Title', options = df['ShortTitle'])

data = df.loc[df['ShortTitle'] == study_title]

col1, col2, col3 = st.columns(3)
col1.metric("IRB Status", data['IRB Status'].values[0])
col2.metric("STAR #", data['STAR#'].values[0])
col3.metric("LLeRA #", data['LLeRA#'].values[0])

col4, col5, col6 = st.columns(3)
col4.metric('IRB #', data['IRB#'].values[0])
# col5 blank
col6.metric('IRB Renewal Date Due', data['IRB Expiration Date'].values[0])

col7, col8, col9= st.columns(3)
col7.metric('Subjects Approved', data['# Subject Approved'].values[0].split('.')[0])
col8.metric('Consented', data['Consented'].values[0].split('.')[0])
col9.metric('Active', data['Active'].values[0].split('.')[0])

with st.container():
    st.subheader('Inclusion Criteria')
    st.write(data['Inclusion'].values[0])

with st.container():
    st.subheader('Exclusion Criteria')
    st.write(data['Exclusion'].values[0])

with st.expander('Click here to see questions and comments'):
    st.write(data['Questions and Comments'].values[0])

with st.expander('Click here to see study status updates'):
    st.write(data['Study Status Updates'].values[0])


