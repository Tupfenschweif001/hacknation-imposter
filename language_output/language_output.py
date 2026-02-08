import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
 
def talk(a):
    load_dotenv(override=True)
    client = ElevenLabs(api_key=os.getenv("meinapitoken"))
    api_key = os.getenv("meinapitoken")
    # a = "The connection is finally working!" #change this to the LLM response
    voice_1 = "9BWtsMINqrJLrRacOk9x"
    client = ElevenLabs(api_key=api_key)
    print("Generating dialogue...")
    dialogue_bytes = b""
    if not api_key:
        print("❌ TokenERROR")
        exit()
 
    try:
        audio_stream = client.text_to_speech.stream(
                voice_id=voice_1,
                output_format="mp3_44100_128",
                text=a,
                model_id="eleven_multilingual_v2"
            )
 
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(output_dir, "output.mp3")

        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        
        return "output.mp3"

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
 
 
def newvoice():
    load_dotenv(override=True)
 
    client = ElevenLabs(api_key=os.getenv("meinapitoken"))
    api_key = os.getenv("meinapitoken")
    a = "The connection is finally working!" #change this to the LLM response
    voice_1 = "9BWtsMINqrJLrRacOk9x"
    client = ElevenLabs(api_key=api_key)
    print("Generating dialogue...")
    dialogue_bytes = b""
    if not api_key:
        print("❌ TokenERROR")
        exit()
    try:
        response = client.voices.ivc.create( ############# create a client voice
            name="My Custom Voice",
            description="A friendly voice for my application",
            files=[
                open("audio_sample1.mp3", "rb"),
                open("audio_sample2.mp3", "rb"),
                open("audio_sample3.mp3", "rb")
            ],
            remove_background_noise=True
        )
    except Exception as e:
        print(f"An error occurred: {e}")
 
        #testtest
