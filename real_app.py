# Import Streamlit to build the web app
import streamlit as st

# Import pandas for data loading and cleaning
import pandas as pd

# Import matplotlib for charts
import matplotlib.pyplot as plt


# -------------------------------
# APP TITLE
# -------------------------------

st.title("📊 Job Market Analyzer")

st.markdown("Analyze real job posting data to explore salary trends, job roles, locations, and in-demand skills.")


# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("data/gsearch_jobs.csv", encoding="latin1", on_bad_lines="skip")


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
])

df['location'] = df['location'].fillna('Unknown')

df = df[df['salary_standardized'].notnull()]

df['clean_salary'] = df['salary_standardized'].astype(int)

df = df.drop(columns=[
    'salary',
    'salary_pay',
    'salary_rate',
    'salary_avg',
    'salary_min',
    'salary_max',
    'salary_hourly',
    'salary_yearly',
    'salary_standardized'
])


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


# -------------------------------
# DATA PREVIEW
# -------------------------------

st.subheader("Cleaned Dataset Preview")

st.write(filtered_df.head(20))

st.markdown("---")


# -------------------------------
# JOB ROLE DISTRIBUTION
# -------------------------------

st.subheader("Job Role Distribution")

role_counts = filtered_df["clean_title"].value_counts()

fig1, ax1 = plt.subplots()
role_counts.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Job Role")
ax1.set_ylabel("Number of Jobs")
ax1.set_title("Job Role Distribution")
plt.xticks(rotation=45)

st.pyplot(fig1)

st.markdown("---")


# -------------------------------
# SALARY BY ROLE
# -------------------------------

st.subheader("Average Salary by Job Role")

salary_by_role = filtered_df.groupby("clean_title")["clean_salary"].mean().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
salary_by_role.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Job Role")
ax2.set_ylabel("Average Salary")
ax2.set_title("Average Salary by Job Role")
plt.xticks(rotation=45)

st.pyplot(fig2)

st.markdown("---")


# -------------------------------
# SKILL DEMAND
# -------------------------------

st.subheader("In-Demand Skills")

skill_counts = {}

for skill in skills:
    skill_counts[skill] = filtered_df[skill].sum()

fig3, ax3 = plt.subplots()
ax3.bar(skill_counts.keys(), skill_counts.values())
ax3.set_xlabel("Skills")
ax3.set_ylabel("Number of Jobs")
ax3.set_title("In-Demand Skills")

st.pyplot(fig3)

st.markdown("---")


# -------------------------------
# TOP LOCATIONS
# -------------------------------

st.subheader("Top Job Locations")

location_counts = filtered_df["location"].value_counts().head(10)

fig4, ax4 = plt.subplots()
location_counts.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Location")
ax4.set_ylabel("Number of Jobs")
ax4.set_title("Top Job Locations")
plt.xticks(rotation=45)

st.pyplot(fig4)