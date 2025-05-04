#!/usr/bin/env python3
from openai import OpenAI
import os
import argparse
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

def main():
    parser = argparse.ArgumentParser(description='Generate a cover letter based on job description and credentials')
    
    # Add arguments
    parser.add_argument('--job-file', type=str, help='Path to file containing job description')
    parser.add_argument('--job-description', type=str, help='Job description text')
    parser.add_argument('--name', type=str, required=True, help='Your full name')
    parser.add_argument('--email', type=str, required=True, help='Your email address')
    parser.add_argument('--phone', type=str, required=True, help='Your phone number')
    parser.add_argument('--experience', type=str, required=True, help='Your relevant experience')
    parser.add_argument('--skills', type=str, required=True, help='Your skills')
    parser.add_argument('--education', type=str, required=True, help='Your education')
    parser.add_argument('--output-file', type=str, help='Path to save the generated cover letter')
    
    args = parser.parse_args()
    
    # Get job description from file or command line
    job_description = ""
    if args.job_file:
        with open(args.job_file, 'r') as file:
            job_description = file.read()
    elif args.job_description:
        job_description = args.job_description
    else:
        print("Please provide a job description either via --job-file or --job-description")
        return
    
    # Prepare credentials dictionary
    credentials = {
        "name": args.name,
        "email": args.email,
        "phone": args.phone,
        "experience": args.experience,
        "skills": args.skills,
        "education": args.education
    }
    
    # Generate cover letter
    print("Generating cover letter...")
    cover_letter = generate_cover_letter(job_description, credentials)
    
    # Save to file if output file is specified
    if args.output_file:
        with open(args.output_file, 'w') as file:
            file.write(cover_letter)
        print(f"Cover letter saved to {args.output_file}")
    
    # Print the generated cover letter
    print("\n=== GENERATED COVER LETTER ===\n")
    print(cover_letter)

if __name__ == "__main__":
    main()
