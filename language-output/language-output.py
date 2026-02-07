import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

load_dotenv(override=True)

client = ElevenLabs(api_key=os.getenv("meinapitoken"))
api_key = os.getenv("meinapitoken")
a = "The connection is finally working!" #change this to the LLM response
voice_1 = "9BWtsMINqrJLrRacOk9x"

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

    client = ElevenLabs(api_key=api_key)
    print("Generating dialogue...")
    dialogue_bytes = b""

    print(f"Generating voice: {voice_1}")
    response = client.text_to_speech.convert(
        text=a,
        voice_id=voice_1,
        output_format="mp3_44100_128",
        model_id="eleven_multilingual_v2"
    )

    print("Playing full dialogue...")
    with open("output.mp3", "wb") as f:
        for chunk in response:
            f.write(chunk)

except Exception as e:
    print(f"An error occurred: {e}")