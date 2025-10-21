# Import libraries
import streamlit as st
import pandas as pd
import pickle
import warnings
from mapie.regression import MapieRegressor
warnings.filterwarnings('ignore')

st.title('Graduate Admission Predictor 🌟') 

# Display the image
st.image('admission.jpg', width = 400)

st.write("This app uses multiple inputs to predict the probability of admission to graduate school.")

# Load the pre-trained model from the pickle file
dt_pickle = open('reg_admission.pickle', 'rb') 
reg = pickle.load(dt_pickle) 
dt_pickle.close()

# Create a sidebar for input collection
st.sidebar.header('Enter Your Profile Details')

GRE = st.sidebar.number_input('GRE', min_value = 290, max_value = 340, step = 1, value = 320)
TOEFL = st.sidebar.number_input('TOEFL', min_value = 92, max_value = 120, step = 1, value = 110)
CGPA = st.sidebar.number_input('CGPA', min_value = 6.0, max_value = 10.0, step = 0.01, value = 8.5)
Research = st.sidebar.selectbox('Research Experience', options = ['No', 'Yes'])
Rating = st.sidebar.slider('University Rating', min_value = 1, max_value = 5, step = 1, value = 3)
SOP = st.sidebar.slider('Statement of Purpose (SOP)', min_value = 1.0, max_value = 5.0, step = 0.1, value = 3.0)
LOR = st.sidebar.slider('Letter of Recommendation (LOR)', min_value = 1.0, max_value = 5.0, step = 0.1, value = 3.0)
Predict = st.sidebar.button('Predict')


Research_No, Research_Yes = 0, 0
if Research == 'Yes':
    Research_Yes = 1
else:
    Research_No = 1


if Predict:
    user_data = [[GRE, TOEFL, Rating, SOP, LOR, CGPA, Research_No, Research_Yes]]
    prediction = reg.predict(user_data,alpha=0.1)
    st.subheader("**Predicting Admission Chance**")
    st.success('**Predicted Admission Probability: {:.2f}%**'.format(int(prediction[0])*100))
    st.write("With a {:.2f}% confidence level:".format(90))
    st.write("**Prediction Interval:** [{:.2f}%, {:.2f}%]".format(int(prediction[1][0, 0])*100, int(prediction[1][0, 1])*100))


# Showing additional items in tabs
st.subheader("Model Insights")
tab1, tab2, tab3, tab4 = st.tabs(["Feature Importance", "Histogram of Residuals", "Predicted vs Actual", "Coverage Plot"])

# Tab 1: Visualizing Decision Tree
with tab1:
    st.write("### Feature Importance")
    st.image('feature_importance.svg')
    st.caption("Relative importance of features in prediction.")

# Tab 2: Histogram of Residuals
with tab2:
    st.write("### Histogram of Residuals")
    st.image('residuals.svg')
    st.caption("Distribution of residuals to evaluate prediction quality.")

# Tab 3: Predicted vs Actual
with tab3:
    st.write("### Predicted vs Actual")
    st.image('predicted_vs_actual.svg')
    st.caption("Visual comparison of predicted and actual values.")

# Tab 4: Coverage Plot
with tab4:
    st.write("### Coverage Plot")
    st.image('coverage_plot.svg')
    st.caption("Range of predictions with confidence intervals.")


password_guess = st.text_input("What is the Password?")
if password_guess != st.secrets["puneet"]:
    st.stop()