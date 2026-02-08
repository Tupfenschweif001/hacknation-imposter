from pathlib import Path
import sys
import os

from flask import Flask, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Gather

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from test.random_text import test_tts_twillio

app = Flask(__name__)


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    audio_dir = Path(__file__).resolve().parents[1] / "language_output"
    return send_from_directory(audio_dir, filename)

def llm_reply(user_text):
    filename = test_tts_twillio()
    if filename:
        return f"/audio/{filename}"
    return None
    #return "/test/test_audio.mp3"

def llm_start():
    return "/test/test_audio.mp3"


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




@app.route("/start_conversation", methods=['GET', 'POST'])
def start_conversation():
    """Start the conversation."""
    resp = VoiceResponse()
    resp.play(llm_start())
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


