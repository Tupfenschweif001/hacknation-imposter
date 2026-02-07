from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

def llm_reply(user_text):
    """Placeholder for the LLM reply.
    Expects a public audio URL (MP3/WAV) that Twilio can play.
    """
    # TODO: Replace with your real LLM/TTS call
    return "/test/test_audio.mp3"

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
    app.run(debug=True, port=5001)


