import random
from language_output.language_output import talk


def get_random_test_text():
    sentences = [
        "The connection is finally working!",
        "Here is a random test sentence for the demo.",
        "This is a short example response for the TTS pipeline.",
        "Everything looks good so far; let's continue.",
        "Testing the audio generation with a different line."
    ]
    return random.choice(sentences)


if __name__ == "__main__":
    print(get_random_test_text())





def test_tts_twillio():
    return talk(get_random_test_text())