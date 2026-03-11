import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew as get_skew

# 1. Page Configuration
st.set_page_config(page_title="AI Resume Dashboard", layout="wide")

# Apply Global Styling for clean plots
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.autolayout': True}) # Ensures titles don't overlap

# 2. Data Loading
@st.cache_data
def load_data():
    try:
        # Assuming the CSV is in the same directory
        df = pd.read_csv("AI_Resume_Screening.csv")
        
        # Pre-processing
        def get_level(years):
            if years <= 2: return "Entry"
            elif years <= 5: return "Mid"
            else: return "Senior"
        
        df['Experience Level'] = df['Experience (Years)'].apply(get_level)
        df['AI Class'] = df['AI Score (0-100)'].apply(lambda x: 'High' if x >= 75 else 'Low')
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

df = load_data()

if df is not None:
    # --- HEADER SECTION ---
    st.title("AI-Driven Resume Screening Dashboard")
    
    st.markdown("""
    This dataset provides a comprehensive overview of applicants' resumes, detailing their qualifications, 
    job roles, number of projects completed, total years of work experience, and specific skills. 
    It also includes the recruiter's decision on hiring or rejection and an AI-based resume ranking score. 
    Analyzing this information offers valuable insights into the qualifications most likely to secure 
    employment and highlights the criteria used by AI screening tools in evaluating candidates. 
    This understanding can aid organizations in refining their recruitment strategies.
    """)

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Global Filters")
    job_list = df["Job Role"].unique().tolist()
    job_filter = st.sidebar.multiselect("Select Job Role", options=job_list, default=job_list)
    
    dec_list = df["Recruiter Decision"].unique().tolist()
    decision_filter = st.sidebar.multiselect("Recruiter Decision", options=dec_list, default=dec_list)

    # Filtering Data
    filtered_df = df[df["Job Role"].isin(job_filter) & df["Recruiter Decision"].isin(decision_filter)]

    # --- METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Applicants", len(filtered_df))
    m2.metric("Avg AI Score", f"{filtered_df['AI Score (0-100)'].mean():.1f}")
    m3.metric("Avg Experience", f"{filtered_df['Experience (Years)'].mean():.1f} Yrs")

    st.markdown("---")

    # --- ROW 1: Experience & Distribution ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Applicant Count by Experience Level")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.countplot(x="Experience Level", data=filtered_df, palette="mako", order=["Entry", "Mid", "Senior"], ax=ax1)
        ax1.set_title('Applicant Count by Experience Level', fontsize=16, fontweight='bold')
        st.pyplot(fig1)

    with col2:
        st.subheader("Distribution of Experience Years")
        skew_val = get_skew(filtered_df["Experience (Years)"])
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_df["Experience (Years)"], kde=True, color="#2a9d8f", ax=ax2)
        ax2.set_title(f"Distribution of Experience Years\nSkewness = {skew_val:.2f}", fontsize=16, fontweight='bold')
        st.pyplot(fig2)

    # --- ROW 2: Correlation & AI Class ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Correlation Heatmap of Numeric Features")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        numeric_df = filtered_df.select_dtypes(include=['int64', 'float64']).drop(columns=['Resume_ID'], errors='ignore')
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax3, fmt=".2f")
        ax3.set_title('Correlation Heatmap of Numeric Features', fontsize=16, fontweight='bold')
        st.pyplot(fig3)

    with col4:
        st.subheader("Hire vs Reject Percentage by AI Class")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.countplot(data=filtered_df, x='AI Class', hue='Recruiter Decision', palette="flare", ax=ax4)
        ax4.set_title("Hire vs Reject Percentage by AI Class", fontsize=16, fontweight='bold')
        st.pyplot(fig4)

    # --- ROW 3: Skills & Education ---
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Top 10 Skills Among Hired Applicants")
        hired_df = filtered_df[filtered_df['Recruiter Decision'] == 'Hire']
        if not hired_df.empty:
            all_skills = hired_df['Skills'].str.split(', ').explode()
            top_skills = all_skills.value_counts().head(10)
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            sns.barplot(y=top_skills.index, x=top_skills.values, palette="GnBu_r", ax=ax5)
            ax5.set_title("Top 10 Skills Among Hired Applicants", fontsize=16, fontweight='bold')
            st.pyplot(fig5)
        else:
            st.info("No 'Hired' candidates to show top skills.")

    with col6:
        st.subheader("Average Experience Required for Hire per Education Level")
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        avg_exp = filtered_df.groupby('Education')['Experience (Years)'].mean().sort_values().reset_index()
        sns.barplot(data=avg_exp, x='Education', y='Experience (Years)', palette="rocket", ax=ax6)
        ax6.set_title('Average Experience Required for Hire per Education Level', fontsize=16, fontweight='bold')
        st.pyplot(fig6)

    # --- INSIGHT SECTION ---
    st.markdown("---")
    st.header("Key Insights")
    
    st.info("""
    * **AI Score Influence:** All candidates with high AI scores got hired, meaning the AI score feature has the highest influence on Recruiter Decisions. The minimum AI score for an accepted applicant is **65**.
    * **Experience Factor:** Hired candidates consistently have more experience than rejected ones across all education levels.
    * **Job Role Performance:** The **Software Engineer** role has the highest hiring percentage at **83.69%**, while other job roles show similar, lower percentages.
    * **Top Skills:** The most influential skills for hired applicants are **Python, SQL, and NLP**.
    * **Certifications:** Applicants with at least one certification have a slightly higher hiring rate (**82.6%**) compared to those without (**77.4%**). However, a large number of applicants without certifications were still hired, indicating certifications are not the primary factor in hiring decisions.
    """)

    # --- SEARCH CANDIDATE DETAILS ---
    st.markdown("---")
    st.subheader("Search Candidate Details")
    search_query = st.text_input("Filter by Skills (e.g. Python, SQL, Java)")
    
    if search_query:
        search_results = filtered_df[filtered_df['Skills'].str.contains(search_query, case=False, na=False)]
    else:
        search_results = filtered_df

    st.dataframe(search_results, use_container_width=True)

else:
    st.error("Missing 'AI_Resume_Screening.csv'. Please upload it to the folder.")