# rca_groq.py
import os
from dotenv import load_dotenv
from groq import Groq
from groq import APIStatusError  # for nicer error messages


def generate_rca_with_groq(incident_description):
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama3-8b-1024",  # UPDATED MODEL
            messages=[
                {"role": "system", "content": "You are an expert in Root Cause Analysis (RCA)."},
                {"role": "user",
                 "content": f"Generate a clear, simple RCA for this incident:\n\n{incident_description}"}
            ],
            temperature=0.3
        )

        return response.choices[0].message["content"]

    except Exception as e:
        print("Unexpected error:", e)
        return None


# Example usage
if __name__ == "__main__":
    incident = """
    Server went down for 45 minutes due to a database connection timeout.
    Impact: Users unable to log in.
    """

    rca = generate_rca_with_groq(incident)
    print("\n--- RCA OUTPUT ---\n")
    print(rca)
