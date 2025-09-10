import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
import base64
import os
import plotly.express as px
import pandas as pd
import collections.abc


# Initialize session variables
if "user_data" not in st.session_state:
    st.session_state['user_data'] = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Styling
st.markdown(
    """
    <style>
        h1, h2, h3 {
            font-family: 'Georgia', serif;
            color: white;
        }
        p, .css-18e3th9, .stTextInput, .stPasswordInput, .stButton, .stMarkdown {
            font-family: 'Verdana', sans-serif;
            color: white;
        }
        .stButton > button {
            background: linear-gradient(145deg, #6c757d, #495057); /* Gray gradient */
            color: white;
            font-size: 12px; /* Slightly larger font size */
            padding: 10px 15px; /* More padding for better button size */
            margin: 2px; /* Space between buttons */
            height: 40px; /* Bigger height */
            border: none; /* No border */
            border-radius: 8px; /* Smooth corners */
            cursor: pointer;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2); /* Soft shadow */
            transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease; /* Smooth transition */
        }
        .stButton > button:hover {
            background: linear-gradient(145deg, #495057, #6c757d); /* Hover inverted gradient */
            box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.4); /* Stronger shadow on hover */
            transform: translateY(-3px); /* Button moves up slightly on hover */
        }
        .stButton > button:active {
            background: #495057; /* Solid color when pressed */
            box-shadow: none; /* Remove shadow when active */
            transform: translateY(2px); /* Slightly depressed effect when clicked */
        }
        .stApp {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


#login page styling
st.markdown("""
    <style>
        /* Style the form container */
        .stTextInput, .stPasswordInput {
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 10px;
            
        }
    </style>
    """, unsafe_allow_html=True
)

# Adding a background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_path = "Downloads/image.jpg"  # Replace with your actual image path
if os.path.exists(image_path):
    base64_image = get_base64_of_bin_file(image_path)
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{base64_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning("Background image not found! Please check the file path.")

# Function to send feedback
def send_feedback(feedback):
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_user = "support@aptpath.in"
    smtp_password ="kjydtmsbmbqtnydk"
    sender_email = smtp_user
    receiver_email = "praneeth.salapu1@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "User Feedback"
    email_body = f"User Feedback: {feedback}"
    message.attach(MIMEText(email_body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        st.success("Thank you for your feedback! Your message has been sent.")
    except Exception as e:
        st.error(f"Error sending feedback: {e}")

# Sidebar Navigation with Buttons
def sidebar_navigation():
    st.sidebar.title("Navigation")
    if st.sidebar.button("🏠Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("📊Power BI Reports"):
        st.session_state.page = "Power BI Reports"
    if st.sidebar.button("📖Overview"):
        st.session_state.page = "Overview"
    if st.sidebar.button("✍️Feedback"):
        st.session_state.page = "Feedback"
    if st.sidebar.button("🚪Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"

# Function to display Power BI Embed
def display_powerbi_report(report_url, report_title):
    st.subheader(report_title)
    iframe_code = f"""
    <iframe width="100%" height="600" 
        src="{report_url}" 
        frameborder="0" allowFullScreen="true">
    </iframe>
    """
    components.html(iframe_code,  width=1000, height=600)

# Login function
def login_user():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if username in st.session_state['user_data'] and st.session_state['user_data'][username] == hash_password(password):
            st.session_state.logged_in = True
            st.success(f"Welcome back, {username}!")
            st.session_state.page = "Home"
        else:
            st.error("Invalid username or password.")

# Registration function
def register_user():
    st.title("Register New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Register"):
        if new_username in st.session_state['user_data']:
            st.error("Username already exists. Please choose a different username.")
        else:
            st.session_state['user_data'][new_username] = hash_password(new_password)
            st.success("Registration successful! Please log in.")

# Home Page
def home_page():
    st.markdown(
        """
        <h1 style="font-size: 36px; color: white;">Welcome to the Indian GDP and Productivity Analysis Dashboard</h1>
        """, 
        unsafe_allow_html=True
    )

    st.write("""
            This app offers an interactive platform for exploring key economic indicators, visualizing trends, and drawing insights from recent data. 
             

            ### Key Metrics:
            """
    )
    # Sample data for GDP and unemployment rate
    data = {
        'Year': [2019, 2020, 2021, 2022, 2023],
        'GDP': [2.87, 2.72, 3.01, 3.20, 3.45],  # in trillion USD
        'Unemployment Rate': [7.8, 8.5, 8.0, 7.5, 7.2]  # in percentage
    }
    df = pd.DataFrame(data)
    
    # Calculate sum of GDP
    total_gdp = df['GDP'].sum()
    
    # Display smaller GDP Sum Card
    st.markdown(f"""
        <div style="background-color: #3E4A5D; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h4>Total GDP (2019-2023): ${total_gdp} Trillion</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Display Unemployment Rate Graph using Plotly
    fig = px.line(df, x='Year', y='Unemployment Rate', title='Unemployment Rate (2019-2023)', 
                  labels={'Unemployment Rate': 'Unemployment Rate (%)', 'Year': 'Year'})
    
    # Customize the graph layout
    fig.update_layout(
        title_font=dict(size=24),
        xaxis=dict(title='Year', tickmode='linear'),
        yaxis=dict(title='Unemployment Rate (%)'),
        template='plotly_dark',
        width=600,
        height=400
    )
    fig.update_traces(text=df['Unemployment Rate'], textposition='top center')
    st.plotly_chart(fig)

    # Descr

    st.write("""
            

            ### Key Features:
            - **Dynamic Data Visualization**: Dive into data spanning from 2019 to 2023 with dynamic, customizable charts.
            - **Comprehensive Economic Analysis**: Our dashboard covers GDP, inflation rates, employment figures, and other indicators to give you a 
              holistic view of the economic landscape.
            - **Trends and Insights**: Track changes over time, compare yearly and monthly trends, and identify emerging patterns.

        
            ### Get Started:
            Use the navigation options to explore specific indicators, dive deep into trends, or generate customized reports.
            
                     
            ### How to Use This App:
            - Use the **Home** page for a general introduction and explore key metrics and features.
            - Visit **Power BI Reports** to view and interact with detailed economic reports.
            - Explore trends and insights for different regions and indicators to deepen your understanding of economic patterns.
            """)
# About Page
def about_page():
    st.title("Overview About this Project")
    st.write("""
    ### Purpose and Goals
    The Economic Insights Dashboard provides an interactive platform for visualizing and interpreting India's economic data, 
    enabling users to analyze trends, understand sectoral contributions, and gain insights into key economic indicators.

    ### Data Sources:
    Data is sourced from a cleaned and merged dataset for the years 2019-2023. This ensures accuracy and consistency across 
    multiple metrics. Additionally, Power BI is used to present detailed insights through embedded reports.
    """)

    # Features Section
    st.subheader("Key Features:")
    st.write("""
    - **User Authentication**: Secure login and registration with hashed passwords for data protection.
    - **Dynamic Data Visualization**: Interactive graphs and charts created with Plotly.
    - **Power BI Integration**: Embedded Power BI dashboards for detailed economic analysis.
    - **Feedback Mechanism**: Users can submit feedback, which is sent directly to the support team via email.
    - **Navigation System**: Sidebar navigation for easy access to all sections.
    """)

    # Technical Stack Section
    st.subheader("Technical Stack:")
    st.write("""
    - **Frontend**: Built using Streamlit, enhanced with custom CSS for styling.
    - **Backend**:
        - SMTP integration for sending feedback emails.
    - **Data Visualization**: 
        - Power BI for embedding professional reports.
    """)
    st.write("""
    - **The dashboard is built with Streamlit for responsiveness and interactivity, combined with Power BI for embedded visual analytics. 
    This combination ensures a seamless blend of real-time analytics and static reporting.**
    """)

    # Use Cases Section
    st.subheader("Use Cases:")
    st.write("""
    - **Policymakers**: Analyze trends to make informed economic decisions.
    - **Students/Researchers**: Access visualized data for academic research and projects.
    - **General Audience**: Gain a better understanding of India's economic performance and trends.
    """)


# Feedback Page
def feedback_page():
    st.title("Feedback")
    feedback_content = st.text_area("Your Feedback")
    if st.button("Submit Feedback"):
        if feedback_content:
            send_feedback(feedback_content)
        else:
            st.warning("Please enter your feedback.")

# Main App
def app():
    if not st.session_state.logged_in:
        st.sidebar.title("Login/Register")
        login_or_register = st.sidebar.radio("Select Option", ["Login", "Register"])
        if login_or_register == "Login":
            login_user()
        elif login_or_register == "Register":
            register_user()
    else:
        sidebar_navigation()
        if st.session_state.page == "Home":
            home_page()
        elif st.session_state.page == "Power BI Reports":
            # Define the single report URL and title
            report_url = "https://app.powerbi.com/view?r=eyJrIjoiNTZkMWQ5OGMtZmUwMy00Mzc1LTkwMmYtYjgyMTMyYTI1OWQzIiwidCI6IjU2NTlkMDY1LTU4MGMtNGNmMi1hNmRlLWZjNmFkZGNjMDE5NyJ9"
            report_title = "India's GDP Analysis"

            # Display the Power BI report
            display_powerbi_report(report_url, report_title)
        elif st.session_state.page == "Overview":
            about_page()
        elif st.session_state.page == "Feedback":
            feedback_page()

# Run the app
if __name__ == "__main__":
    app()
