 Placement Eligibility Streamlit App

An interactive Streamlit application that helps placement teams filter and analyze student readiness based on programming, soft skills, and mock interview performance.


Project Overview

This project simulates a real-world EdTech scenario where placement managers can:

Filter students based on eligibility criteria
Preview student data across multiple tables
View 10 insightful analytics via SQL queries and visualizations

The app is powered by SQLite, Python (OOP), Faker (for synthetic data), and Streamlit for the UI.



Technologies Used

Python 3.8+
Streamlit
SQLite3
Faker – for generating realistic fake data
Pandas / Numpy
Matplotlib / Streamlit built-in charts



 Folder Structure

placement_eligibility_app/
├── data/
│ └── placement.db # SQLite database
├── src/
│ ├── data_generator.py # Generates synthetic data
│ └── db_manager.py # OOP class for DB interaction
├── insights.sql # 10 SQL queries for dashboard insights
├── streamlit_app.py # Main Streamlit app
├── requirements.txt # Python dependencies
└── README.md # Project documentation

 
