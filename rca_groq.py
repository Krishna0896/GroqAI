# rca_groq.py
import os
from dotenv import load_dotenv
from groq import Groq
from groq import APIStatusError  # for nicer error messages

load_dotenv()

# Create client (will read GROQ_API_KEY from env by default)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_rca_with_groq(incident_description: str, model: str = "openai/gpt-oss-20b"):
    """
    Generate a structured RCA using Groq Chat Completions API.

    model: choose a Groq-hosted chat model. Example: "openai/gpt-oss-20b".
    (Change model if you want another available model.)
    """
    # system instruction to set role/format
    system_msg = {
        "role": "system",
        "content": (
            "You are an experienced SRE and root cause analysis specialist. "
            "Produce a concise, factual RCA with this exact structure:\n\n"
            "1. Problem Summary\n"
            "2. Business / Technical Impact\n"
            "3. Timeline of Events\n"
            "4. Immediate Cause\n"
            "5. Root Cause\n"
            "6. Corrective Actions\n"
            "7. Preventive Actions\n\n"
            "Be succinct and use bullet points for timeline and actions."
        )
    }

    user_msg = {
        "role": "user",
        "content": f"INCIDENT DETAILS:\n{incident_description}"
    }

    try:
        # Make chat completion request
        chat_completion = client.chat.completions.create(
            messages=[system_msg, user_msg],
            model=model,
            temperature=0.2,
            max_output_tokens=800  # adjust if you want longer/shorter RCAs
        )

        # Groq's Python SDK returns structured response objects; content usually at:
        choice = chat_completion.choices[0]
        # choice.message.content is usually the generated text (see README)
        generated_text = getattr(choice.message, "content", None) or choice.message.content
        return generated_text

    except APIStatusError as e:
        # show helpful debugging info
        print("APIStatusError:", e.status_code)
        print(e.response)
        raise
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
