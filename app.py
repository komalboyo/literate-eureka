import streamlit as st
import openai
import PyPDF2
import json

# Set up OpenAI API key
openai.api_key = "you api key"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to get GPT-4 response
def get_gpt4_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Main Streamlit app
def main():
    st.set_page_config(page_title="AI Career Counselor", page_icon="🎓", layout="wide")
    
    st.title("🚀 AI Career Counselor for Underprivileged Youth")
    st.markdown("Welcome to your personalized career guidance journey! Let's explore your potential together.")

    # Create two columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📋 Personal Information")
        name = st.text_input("Name")
        age = st.selectbox("Age", options=[13, 14, 15, 16, 17, 18])
        gender = st.radio("Gender", options=["Male", "Female", "Other", "Prefer not to say"])
        location = st.text_input("Location")

        st.header("📚 Academic Information")
        grade = st.selectbox("Current Class/Grade", options=["8th", "9th", "10th", "11th", "12th"])
        fav_subjects = st.multiselect("Favorite Subjects", 
                                      options=["Mathematics", "Science", "Social Studies", "Languages", "Arts", "Commerce"],
                                      default=["Mathematics", "Science"])
        other_fav_subject = st.text_input("Other Favorite Subject (if any)")
        
        least_fav_subjects = st.multiselect("Least Favorite Subjects", 
                                            options=["Mathematics", "Science", "Social Studies", "Languages", "Arts", "Commerce"],
                                            default=["Arts"])
        other_least_fav_subject = st.text_input("Other Least Favorite Subject (if any)")
        
        academic_performance = st.select_slider("Academic Performance", 
                                                options=["Below Average", "Average", "Above Average", "Excellent"])

    with col2:
        st.header("🏆 Extracurricular Activities")
        activities = st.multiselect("Participation in Extracurricular Activities",
                                    options=["Sports", "Music", "Dance", "Art", "Drama", "Debate", "Science Clubs"])
        other_activity = st.text_input("Other Activity (if any)")
        participation_level = st.selectbox("Level of Participation", 
                                           options=["School Level", "District Level", "State Level", "National Level"])

        st.header("🧠 Skills and Interests")
        tech_skills = st.multiselect("Technical Skills",
                                     options=["Coding/Programming", "Graphic Design", "Video Editing", "Web Development"])
        other_tech_skill = st.text_input("Other Technical Skill (if any)")
        
        soft_skills = st.multiselect("Soft Skills",
                                     options=["Communication", "Leadership", "Teamwork", "Problem-Solving", "Critical Thinking"])
        other_soft_skill = st.text_input("Other Soft Skill (if any)")
        
        hobbies = st.multiselect("Hobbies and Interests",
                                 options=["Reading", "Writing", "Traveling", "Cooking", "Gardening"])
        other_hobby = st.text_input("Other Hobby (if any)")

    st.header("💼 Career Aspirations")
    career_fields = st.multiselect("Preferred Career Fields",
                                   options=["Engineering", "Medicine", "Business", "Arts and Humanities", "Social Sciences", "Law"])
    other_career_field = st.text_input("Other Career Field (if any)")
    career_reason = st.radio("Reason for Choosing Preferred Career Field",
                             options=["Interest in the subject", "Job Opportunities", "Family Influence", "Other"])
    if career_reason == "Other":
        other_career_reason = st.text_input("Please specify other reason")

    st.header("👨‍👩‍👧‍👦 Family Background")
    parents_education = st.selectbox("Parents' Educational Background",
                                     options=["No Formal Education", "Primary School", "High School", "College/University", "Postgraduate"])
    parents_occupation = st.selectbox("Parents' Occupation",
                                      options=["Self-employed", "Government Job", "Private Sector Job", "Homemaker", "Other"])
    if parents_occupation == "Other":
        other_parents_occupation = st.text_input("Please specify other occupation")

    st.header("💻 Access to Resources")
    tech_access = st.radio("Access to Technology (Computer/Internet)",
                           options=["Regular Access", "Occasional Access", "No Access"])
    guidance_access = st.radio("Access to Career Guidance Resources",
                               options=["Regular Access", "Occasional Access", "No Access"])

    st.header("📝 Additional Information")
    additional_info = st.text_area("Any Other Information You Would Like to Share")

    st.header("📊 Psychometric Test Results")
    pdf_file = st.file_uploader("Upload Psychometric Test Results (PDF)", type="pdf")
    
    if pdf_file is not None:
        psychometric_results = extract_text_from_pdf(pdf_file)
    else:
        psychometric_results = ""

    if st.button("Submit and Get Career Suggestions", key="submit"):
        # Prepare data for GPT-4
        user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "location": location,
            "grade": grade,
            "favorite_subjects": fav_subjects + ([other_fav_subject] if other_fav_subject else []),
            "least_favorite_subjects": least_fav_subjects + ([other_least_fav_subject] if other_least_fav_subject else []),
            "academic_performance": academic_performance,
            "extracurricular_activities": activities + ([other_activity] if other_activity else []),
            "participation_level": participation_level,
            "technical_skills": tech_skills + ([other_tech_skill] if other_tech_skill else []),
            "soft_skills": soft_skills + ([other_soft_skill] if other_soft_skill else []),
            "hobbies": hobbies + ([other_hobby] if other_hobby else []),
            "preferred_career_fields": career_fields + ([other_career_field] if other_career_field else []),
            "career_reason": career_reason,
            "parents_education": parents_education,
            "parents_occupation": parents_occupation,
            "tech_access": tech_access,
            "guidance_access": guidance_access,
            "additional_info": additional_info,
            "psychometric_results": psychometric_results
        }

        # Prepare prompt for GPT-4
        prompt = f"""
        Based on the following information about a student aged 13-18 in India:

        {json.dumps(user_data, indent=2)}

        Please provide a comprehensive career analysis and suggestions. Your response should include:

        1. A brief summary of the student's profile.
        2. 3-4 career suggestions that best match the student's profile, interests, and skills.
        3. For each career suggestion, provide:
           - A brief description of the career
           - A personalized roadmap for pursuing this career path
           - Key resources for learning and skill development
           - Essential requirements (educational, skills, etc.) for this career

        Return your response in the following JSON format:
        {{
            "profile_summary": "Summary of the student's profile",
            "career_suggestions": [
                {{
                    "title": "Career Title",
                    "description": "Brief description of the career",
                    "roadmap": "Personalized roadmap for this career path",
                    "resources": ["Resource 1", "Resource 2", "Resource 3"],
                    "requirements": ["Requirement 1", "Requirement 2", "Requirement 3"]
                }}
            ]
        }}
        """

        with st.spinner("Analyzing your profile and generating career suggestions..."):
            gpt4_response = get_gpt4_response(prompt)
            response_data = json.loads(gpt4_response)

        st.success("Analysis complete! Here are your personalized career suggestions.")

        st.subheader("📊 Your Profile Summary")
        st.write(response_data["profile_summary"])

        st.subheader("🎯 Career Suggestions")
        for career in response_data["career_suggestions"]:
            with st.expander(f"🚀 {career['title']}"):
                st.write(f"**Description:** {career['description']}")
                st.write(f"**Roadmap:** {career['roadmap']}")
                st.write("**Key Resources:**")
                for resource in career['resources']:
                    st.write(f"- {resource}")
                st.write("**Requirements:**")
                for requirement in career['requirements']:
                    st.write(f"- {requirement}")

if __name__ == "__main__":
    main()