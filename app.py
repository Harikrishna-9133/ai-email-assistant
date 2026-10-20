
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from streamlit_mic_recorder import speech_to_text

load_dotenv()

st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="centered",
)

# Initialize state before creating widgets.
defaults = {
    "email_input": "",
    "last_voice_text": "",
    "generated_email": "",
    "email_editor": "",
    "generation_error": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def clear_instructions():
    """Runs before Streamlit recreates the widgets."""
    st.session_state["email_input"] = ""
    st.session_state["last_voice_text"] = ""
    st.session_state["generated_email"] = ""
    st.session_state["generation_error"] = ""








def generate_email_stream(instructions, email_type, tone, output_area):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from .env")

    client = genai.Client(
        api_key=api_key,
        http_options={"timeout": 120000},
    )

    prompt = f"""
Write a complete email.

Type: {email_type}
Tone: {tone}
Instructions: {instructions}

Include a subject, greeting, two short paragraphs, and a polite closing.
Use placeholders for missing details. Do not invent personal information.
Return the complete email, not just the subject.
"""

    parts = []

    stream = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=prompt,
        stream=True,
        generation_config={
            "max_output_tokens": 500,
            "thinking_level": "minimal",
        },
    )

    for event in stream:
        if event.event_type == "step.delta" and event.delta.type == "text":
            chunk = event.delta.text or ""
            if chunk:
                parts.append(chunk)
                output_area.markdown("".join(parts) + " ▌")

    result = "".join(parts).strip()

    if not result:
        raise RuntimeError("Gemini returned no email text.")

    lines = result.splitlines()
    subject_index = next(
        (
            i for i, line in enumerate(lines)
            if line.strip().lower().startswith(("subject:", "**subject:**"))
        ),
        -1,
    )

    if subject_index == -1:
        raise RuntimeError("The generated email has no subject line.")

    body = "\n".join(lines[subject_index + 1:]).strip()
    if len(body) < 50:
        raise RuntimeError("The generated email body is incomplete.")

    output_area.markdown(result)
    return result







# App heading
st.title("📧 AI Email Assistant")
st.write("Create emails using your keyboard or voice.")

email_type = st.selectbox(
    "Email type",
    [
        "Job Application",
        "Follow-up",
        "Leave Request",
        "Thank You",
        "Meeting Request",
        "General Email",
    ],
)

tone = st.selectbox(
    "Choose the tone",
    ["Professional", "Formal", "Friendly", "Concise"],
)

st.divider()

# Voice input must be processed BEFORE the text-area widget.
st.subheader("🎙️ Speak your instructions")
st.caption("Start recording, speak clearly, then stop recording.")

try:
    voice_text = speech_to_text(
        language="en",
        start_prompt="🎙️ Start recording",
        stop_prompt="⏹️ Stop recording",
        just_once=True,
        use_container_width=True,
        key="voice_input",
    )

    if voice_text and voice_text.strip():
        recognized = voice_text.strip()

        if recognized != st.session_state["last_voice_text"]:
            existing = st.session_state["email_input"].strip()

            st.session_state["email_input"] = (
                f"{existing}\n{recognized}"
                if existing
                else recognized
            )

            st.session_state["last_voice_text"] = recognized
            st.rerun()

except Exception as exc:
    st.error(f"Voice recognition failed: {exc}")
    st.info(
        "Check your browser's microphone permission and try again."
    )

st.divider()

# Text widget
st.subheader("✍️ Email instructions")

st.text_area(
    "Type or review your instructions",
    key="email_input",
    height=140,
    placeholder=(
        "Example: Write an email to HR applying "
        "for an AI Developer internship as a fresher."
    ),
)

# Generate email



# Generate Email with retry support

generate_clicked = st.button(
    "✨ Generate Email",
    type="primary",
    use_container_width=True,
)

retry_clicked = False

if st.session_state["generation_error"]:
    retry_clicked = st.button(
        "🔄 Retry Generation",
        use_container_width=True,
    )

if generate_clicked or retry_clicked:
    instructions = st.session_state["email_input"].strip()

    if not instructions:
        st.warning("Please type or speak your instructions.")

    else:
        st.session_state["generated_email"] = ""
        st.session_state["email_editor"] = ""
        st.session_state["generation_error"] = ""

        st.subheader("✉️ Your email")
        live_output = st.empty()

        try:
            with st.spinner(
                "⏳ Connecting to Gemini and generating your email..."
            ):
                result = generate_email_stream(
                    instructions,
                    email_type,
                    tone,
                    live_output,
                )

            # Save the complete response.
            st.session_state["generated_email"] = result
            st.session_state["email_editor"] = result

            st.success("Email generated successfully!")

        except Exception as exc:
            live_output.empty()

            error_message = str(exc)
            st.session_state["generation_error"] = error_message

            st.error(
                "We couldn't generate your email this time."
            )
            st.caption(
                "Please check your connection and try again. "
                "If the problem continues, check your Gemini API "
                "quota and model availability."
            )
            st.warning(f"Technical details: {error_message}")



# Display generated email in an editable field.
if st.session_state["generated_email"]:
    st.divider()
    st.subheader("✉️ Your generated email")

    st.text_area(
        "Review and edit your email",
        key="email_editor",
        height=350,
    )

    st.download_button(
        "⬇️ Download email as TXT",
        data=st.session_state["email_editor"],
        file_name="generated_email.txt",
        mime="text/plain",
        use_container_width=True,
    )

# Clear button uses a callback to avoid session-state errors.
st.divider()

st.button(
    "🗑️ Clear instructions",
    on_click=clear_instructions,
    use_container_width=True,
)
