import os
from dotenv import load_dotenv
from groq import Groq
from groq import APIStatusError  # for nicer error messages

load_dotenv()

# Create client (will read GROQ_API_KEY from env by default)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_rca_with_groq(incident_description: str, model: str = "llama3-8b-8192"):
    system_msg = {
        "role": "system",
        "content": (
            "You are an experienced SRE and Root Cause Analysis expert. "
            "Produce a clear RCA using this format:\n\n"
            "1. Problem Summary\n"
            "2. Business / Technical Impact\n"
            "3. Timeline of Events\n"
            "4. Immediate Cause\n"
            "5. Root Cause\n"
            "6. Corrective Actions\n"
            "7. Preventive Actions\n"
        )
    }

    user_msg = {
        "role": "user",
        "content": f"INCIDENT DETAILS:\n{incident_description}"
    }

    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[system_msg, user_msg],
            temperature=0.2
        )

        return chat_completion.choices[0].message["content"]

    except Exception as e:
        print("Unexpected error:", str(e))
        raise

if __name__ == "__main__":
    # Example incident — replace with your real incident text
    incident = """
    On 27-Nov at 14:02 UTC the payment API began returning 503 for 22 minutes.
    Logs show repeated database connection timeouts. DB CPU spiked to 98% because autoscaling
    was disabled due to a recent config change. No failover occurred.
    """

    print("\n===== GENERATED RCA =====\n")
    rca_text = generate_rca_with_groq(incident)
    print(rca_text)
