# ai-resume-dashboard
AI-Driven Resume Screening Dataset.
This dataset shows Aplicants's resumes details such as, Education Level, Job Role, no. of Projects, Experience, Skills, Certifications, and Salary Expectation. It also illustrate the recutier decision(hired/rejected) and the  AI-based resume ranking score.

 Resume dataset could give us insight about what qualification are most likely to get you hired. It also help us understand the criteria for AI screening tools to accept or reject an applicants. Through exploratory data analysis, we investigate patterns in candidate qualifications, identify the most common skills among successful applicants, and examine how factors such as experience, certifications, and AI score relate to hiring outcomes.

 By analyzing this dataset, we aim to gain insights into the criteria that may influence automated resume screening systems and recruiter decision-making. These insights can help highlight the qualifications and attributes that increase the likelihood of passing AI screening tools and progressing in the hiring process.
 
## 1. Dataset Overview

Initial exploration included:

Checking dataset structure

Inspecting data types

Identifying missing values

Understanding feature distributions

## 2. Univariate Analysis

Single-variable analysis was used to understand distributions such as:

Education levels

Experience years

AI score distribution

Salary expectations

Hiring decision distribution

This helped detect class imbalance, outliers, and skewed distributions.

## 3. Outlier Detection

Outliers were analyzed in numerical features such as:

Experience

AI Score

Salary Expectation

Boxplots and statistical methods were used to evaluate extreme values.

## 4. Bivariate Analysis

Relationships between variables were explored, including:

AI Score vs Recruiter Decision

Experience vs Hiring Decision

Education vs Hiring Decision

Salary Expectation vs Hiring Decision

These analyses helped identify which factors appear most related to hiring outcomes.

## 5. Multivariate Analysis

Multiple features were analyzed together to detect deeper patterns in hiring decisions.

Examples include:

AI Score combined with experience

Job role and skill combinations

Education level with certifications

## Feature Engineering

To prepare the data for analysis and modeling:

Skills were processed into structured format

New features such as certification count were created

Categorical variables were encoded using dummy variables

All candidate with high AI scores got hired, meaning AI score feature have the haighest influunce in Recruiter Decision. The least AI scored applicant who got accepted is 65 score. Hired candidates consistently have more experience than rejected ones across all education levels. On the hand, Job Role feature, Software Engineer have the haighest hireing percent with 83.69098%, while other job roles show similar percentages. The skills that influnce hiring and most hired applicants have are Python,SQL, and NLP. However, when looking at certificate Applicants with at least one certification have a slightly higher hiring rate 82.6% compared to those with no certifications 77.4% large number of applicants without certifications were still hired, indicating that certifications are not the primary factor in hiring decisions

## AI model 
An initial machine learning model was started to predict the Recruiter Decision.
The goal of the model is to learn patterns from the dataset and determine whether a applicant will likely be hired or rejected based on resume features. 
###NOTE
The model shows high accuracy 96%, but this may be influenced by class imbalance recutier decision(hired/rejected) in the dataset (which I will be working on later). Therefore, accuracy should be interpreted carefully alongside other evaluation metrics.
