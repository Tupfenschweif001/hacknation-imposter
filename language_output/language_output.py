import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path, override=True)

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_TOKEN"))
api_key = os.getenv("ELEVENLABS_API_TOKEN")
voice_1 = "9BWtsMINqrJLrRacOk9x"
client = ElevenLabs(api_key=api_key)
def tts(text_input):
    output_path = Path(__file__).resolve().parent / "output.mp3"
    print("Generating dialogue...")
    dialogue_bytes = b""
    if not api_key:
        print("❌ TokenERROR")
        exit()

    try:

        # response = client.voices.ivc.create( ############# create a client voice
        #     name="My Custom Voice",
        #     description="A friendly voice for my application",
        #     files=[
        #         open("audio_sample1.mp3", "rb"),
        #         open("audio_sample2.mp3", "rb"),
        #         open("audio_sample3.mp3", "rb")
        #     ],
        #     remove_background_noise=True
        # )
        audio_stream = client.text_to_speech.stream(
                voice_id=voice_1,
                output_format="mp3_44100_128",
                text=text_input,
                model_id="eleven_multilingual_v2"
            )

            # Write stream to file manually
        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

    except Exception as e:
        print(f"An error occurred: {e}")

    base_url = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:5001")
    return f"{base_url.rstrip('/')}/audio/output.mp3"