import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config("HR Attrition Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})
    return df

df = load_data()

st.title("Employee Attrition and HR Insights Dashboard")

# KPI Metrics
attr_rate = df["AttritionFlag"].mean() * 100
avg_tenure = df["YearsAtCompany"].mean()
avg_income = df["MonthlyIncome"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("Attrition Rate", f"{attr_rate:.1f}%")
c2.metric("Avg Tenure (Years)", f"{avg_tenure:.1f}")
c3.metric("Avg Monthly Income", f"$ {avg_income:,.0f}")

st.markdown("---")

# 1. Attrition Count by Department
fig1 = px.histogram(df, x="Department", color="Attrition", barmode="group",
                    title="Attrition Count by Department")
st.plotly_chart(fig1, use_container_width=True)

# 2. Age Distribution by Attrition
fig2 = px.histogram(df, x="Age", color="Attrition", nbins=20,
                    title="Age Distribution by Attrition Status")
st.plotly_chart(fig2, use_container_width=True)

# 3. Job Role vs Attrition Rate
job_rate = df.groupby("JobRole")["AttritionFlag"].mean().reset_index()
job_rate["AttritionRate"] = job_rate["AttritionFlag"] * 100
fig3 = px.bar(job_rate, x="JobRole", y="AttritionRate",
              title="Attrition Rate by Job Role", labels={"AttritionRate": "Rate (%)"})
st.plotly_chart(fig3, use_container_width=True)

# 4. Satisfaction vs Attrition (Scatter)
fig4 = px.scatter(df, x="JobSatisfaction", y="EnvironmentSatisfaction",
                  color="Attrition", title="Satisfaction Ratings vs Attrition",
                  labels={"JobSatisfaction": "Job Satisfaction", "EnvironmentSatisfaction": "Environment Satisfaction"})
st.plotly_chart(fig4, use_container_width=True)

# 5. Income vs Years at Company with Attrition
fig5 = px.scatter(df, x="YearsAtCompany", y="MonthlyIncome", color="Attrition",
                  title="Income vs Tenure colored by Attrition")
st.plotly_chart(fig5, use_container_width=True)