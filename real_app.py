# Import Streamlit to build the web app
import streamlit as st

# Import pandas for data loading and cleaning
import pandas as pd

# Import matplotlib for charts
import matplotlib.pyplot as plt

# Import Plotly Express for creating interactive charts (hover, zoom, modern visuals)
import plotly.express as px


# -------------------------------
# APP TITLE
# -------------------------------

st.title("📊 Job Market Analyzer")

st.markdown("Analyze real job posting data to explore salary trends, job roles, locations, and in-demand skills.")


# -------------------------------
# LOAD DATA
# -------------------------------

# Load smaller cleaned dataset for deployment
df = pd.read_csv("data/clean_jobs_sample.csv")


# -------------------------------
# CLEAN DATA
# -------------------------------

df = df.drop(columns=[
    'Unnamed: 0',
    'index',
    'job_id',
    'thumbnail',
    'commute_time',
    'description_tokens'
], errors="ignore")

df['location'] = df['location'].fillna('Unknown')




# -------------------------------
# CLEAN JOB TITLES
# -------------------------------

def clean_title(title):
    title = title.lower()

    if 'data analyst' in title:
        return 'Data Analyst'
    elif 'data scientist' in title:
        return 'Data Scientist'
    elif 'data engineer' in title:
        return 'Data Engineer'
    elif 'machine learning' in title or 'ml engineer' in title:
        return 'ML Engineer'
    else:
        return 'Other'


df['clean_title'] = df['title'].apply(clean_title)


# -------------------------------
# EXTRACT SKILLS
# -------------------------------

skills = ['python', 'sql', 'excel', 'tableau', 'power bi', 'aws']

for skill in skills:
    df[skill] = df['description'].str.contains(skill, case=False, na=False)


# -------------------------------
# SIDEBAR FILTER
# -------------------------------

st.sidebar.header("Filter Options")

role_filter = st.sidebar.selectbox(
    "Select Job Role",
    ["All"] + sorted(df["clean_title"].unique())
)

if role_filter != "All":
    filtered_df = df[df["clean_title"] == role_filter]
else:
    filtered_df = df



col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Average Salary", f"${filtered_df['clean_salary'].mean():,.0f}")
col3.metric("Top Role", filtered_df['clean_title'].value_counts().idxmax())


# -------------------------------
# DATA PREVIEW
# -------------------------------

st.markdown("### 📋 Cleaned Dataset Preview")
st.markdown("This table shows a sample of the cleaned job postings used for the dashboard.")

preview_columns = [
    "title", "company_name", "location",
    "clean_salary", "clean_title",
    "python", "sql", "excel", "tableau", "power bi", "aws"
]

st.dataframe(filtered_df[preview_columns].head(20))

st.markdown("---")


# -------------------------------
# JOB ROLE DISTRIBUTION
# -------------------------------

st.markdown("### 📊 Job Role Distribution")
st.markdown("This chart shows which job roles appear most often in the dataset.")

role_counts = filtered_df["clean_title"].value_counts().reset_index()
role_counts.columns = ["Job Role", "Number of Jobs"]

fig1 = px.bar(
    role_counts,
    x="Job Role",
    y="Number of Jobs",
    
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")


# -------------------------------
# SALARY BY ROLE
# -------------------------------

# Average Salary by Role (Interactive)
st.markdown("### 💰 Average Salary by Job Role")
st.markdown("This chart compares average salary across job categories using the cleaned salary column.")

salary_by_role = (
    filtered_df.groupby("clean_title")["clean_salary"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    salary_by_role,
    x="clean_title",
    y="clean_salary",
    labels={"clean_title": "Job Role", "clean_salary": "Average Salary"},
    
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")


# -------------------------------
# SKILL DEMAND
# -------------------------------

st.markdown("### 🧠 In-Demand Skills")
st.markdown("This chart counts how often key skills appear in job descriptions.")

skill_counts = {skill: filtered_df[skill].sum() for skill in skills}

skill_df = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Count"])
# Capitalize skill names for better UI
skill_df["Skill"] = skill_df["Skill"].str.title()

# Fix common formatting
skill_df["Skill"] = skill_df["Skill"].replace({
    "Sql": "SQL",
    "Aws": "AWS",
    "Power Bi": "Power BI"
})

fig3 = px.bar(
    skill_df,
    x="Skill",
    y="Count",
    
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# -------------------------------
# TOP LOCATIONS
# -------------------------------

st.markdown("### 📍 Top Job Locations")
st.markdown("This chart shows the most common job locations in the cleaned dataset.")

location_counts = (
    filtered_df["location"]
    .value_counts()
    .head(10)
    .reset_index()
)

location_counts.columns = ["Location", "Count"]

fig4 = px.bar(
    location_counts,
    x="Location",
    y="Count",
    
)

st.plotly_chart(fig4, use_container_width=True)