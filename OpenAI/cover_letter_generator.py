from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

def generate_cover_letter(job_description, credentials):
    """
    Generate a cover letter based on job description and personal credentials
    using the o4-mini model
    
    Args:
        job_description (str): The job description text
        credentials (dict): Dictionary containing personal information like name, experience, skills, etc.
        
    Returns:
        str: Generated cover letter
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Prepare the prompt with job description and credentials
    prompt = f"""
    Generate a professional cover letter based on the following:
    
    JOB DESCRIPTION:
    {job_description}
    
    MY CREDENTIALS:
    Name: {credentials.get('name', '')}
    Email: {credentials.get('email', '')}
    Phone: {credentials.get('phone', '')}
    Experience: {credentials.get('experience', '')}
    Skills: {credentials.get('skills', '')}

    Education: {credentials.get('education', '')}
    Past Experience: {credentials.get('previous_experience', '')}

    The cover letter should be professional, highlight relevant skills and experience,
    and explain why I am a good fit for this position.
    """
    
    # Call the OpenAI API to generate the cover letter
    response = client.chat.completions.create(
        model="o4-mini",  # Using o4-mini model as requested
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract and return the generated cover letter
    return response.choices[0].message.content

if __name__ == "__main__":
    # Example usage
    job_description = """
    Software Engineer - Python
    
    We are looking for a skilled Python developer to join our team. The ideal candidate 
    will have experience with web frameworks, API development, and database integration.
    Responsibilities include designing, coding, and testing new features, collaborating 
    with cross-functional teams, and maintaining existing codebase.
    
    Requirements:
    - 3+ years of Python programming experience
    - Experience with web frameworks (Django, Flask)
    - Knowledge of RESTful APIs
    - Database experience (SQL, NoSQL)
    - Strong problem-solving skills
    """
    
    credentials = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "experience": "4 years of Python development, including Django and Flask frameworks",
        "skills": "Python, Django, Flask, RESTful APIs, SQL, MongoDB, Git, AWS",
        "education": "Bachelor's in Computer Science"
    }
    
    # Generate cover letter
    cover_letter = generate_cover_letter(job_description, credentials)
    
    # Print the generated cover letter
    print("\n=== GENERATED COVER LETTER ===\n")
    print(cover_letter)
