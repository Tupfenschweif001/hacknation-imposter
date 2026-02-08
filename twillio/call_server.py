from pathlib import Path
import sys
import os

# Pfad erweitern, damit Module im Root-Verzeichnis gefunden werden
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Gather
from language_output.language_output import talk
from llmcall_method.callgemini import generate_llm_reply, generate_llm_start
from test.random_text import test_tts_twillio

app = Flask(__name__)

history = []

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    audio_dir = Path(__file__).resolve().parents[1] / "language_output"
    return send_from_directory(audio_dir, filename)

def llm_reply(user_text):
    print(f"User sagte: {user_text}") # Debugging
    text = generate_llm_reply(user_text, history)
    history.append(text)
    filename = talk(text)
    if filename:
        return f"/audio/{filename}"
    return None

def llm_start(request_id, title=None, description=None):
    text = generate_llm_start(request_id, title, description)
    print("AI Start Text:", text)
    history.append(text)
    
    # Jetzt bekommen wir einen eindeutigen Dateinamen zurück (z.B. output_39f8a.mp3)
    filename = talk(text)
    
    if filename:
        return f"/audio/{filename}"
    return None


def build_gather(prompt_text=None):
    gather = Gather(
        input='speech dtmf',
        action='/gather',
        language='en-US',
        timeout=10,
        speech_timeout='auto',
        action_on_empty_result=True,
        num_digits=1
    )
    if prompt_text:
        gather.say(prompt_text, language='en-US')
    return gather




@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Start the conversation."""
    request_id = request.values.get("request_id")
    title = request.values.get("title")
    description = request.values.get("description")

    resp = VoiceResponse()
    resp.play(llm_start(request_id, title, description))
    resp.append(build_gather())
    return str(resp)


@app.route("/gather", methods=['GET', 'POST'])
def gather():
    """Process the user reply."""
    resp = VoiceResponse()
    values = request.values

    user_input = values.get('SpeechResult', '').strip().lower()

    if user_input:
        audio_url = llm_reply(user_input)
        resp.play(audio_url)
        resp.append(build_gather())
        return str(resp)


    resp.append(build_gather())
    return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)


