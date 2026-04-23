import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Job Market Analyzer")
st.markdown("### 📊 Analyze job trends, salaries, and in-demand skills")

df = pd.read_csv("data/jobs.csv")
# Filter by location
location_filter = st.selectbox("Select Location", df["location"].unique())
filtered_df = df[df["location"] == location_filter]

st.subheader("Dataset Preview")
st.write(filtered_df)
st.markdown("---")

st.subheader("Top Job Roles")
job_counts = df['job_title'].value_counts()
fig1, ax1 = plt.subplots()
job_counts.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Top Locations")
loc_counts = df['location'].value_counts()
fig2, ax2 = plt.subplots()
loc_counts.plot(kind='bar', ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

st.subheader("Average Salary by Role")
salary_avg = df.groupby('job_title')['salary'].mean()
fig3, ax3 = plt.subplots()
salary_avg.plot(kind='bar', ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader("In-Demand Skills")
skills = ['Python', 'SQL', 'Excel', 'Tableau', 'Java', 'AWS']
skill_count = {}

for skill in skills:
    skill_count[skill] = df['description'].str.contains(skill, case=False).sum()

fig4, ax4 = plt.subplots()
ax4.bar(skill_count.keys(), skill_count.values())
st.pyplot(fig4)