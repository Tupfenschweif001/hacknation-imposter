import os
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def play_mp3(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Audio file not found: {path}")

    # macOS: afplay
    if shutil.which("afplay"):
        subprocess.run(["afplay", path], check=True)
        return

    # Linux: mpg123 or ffplay fallback
    if shutil.which("mpg123"):
        subprocess.run(["mpg123", path], check=True)
        return

    if shutil.which("ffplay"):
        subprocess.run(["ffplay", "-nodisp", "-autoexit", path], check=True)
        return

    raise RuntimeError("No supported audio player found. Install 'mpg123' or 'ffplay'.")


def fetch_twiml(url, data=None):
    if data is None:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode("utf-8")

    encoded = urllib.parse.urlencode(data).encode("utf-8")
    with urllib.request.urlopen(url, data=encoded) as resp:
        return resp.read().decode("utf-8")


def play_remote_audio(url, base_url=None):
    # Local file path support (absolute or relative)
    local_candidate = url
    if not os.path.isabs(local_candidate):
        local_candidate = os.path.join(os.getcwd(), local_candidate)

    if os.path.isfile(local_candidate):
        play_mp3(local_candidate)
        return

    if url.startswith("file://"):
        local_path = urllib.request.url2pathname(url.replace("file://", ""))
        play_mp3(local_path)
        return

    # Relative URL from TwiML -> try local file first, then resolve against base_url
    if url.startswith("/"):
        local_from_root = os.path.join(os.getcwd(), url.lstrip("/"))
        if os.path.isfile(local_from_root):
            play_mp3(local_from_root)
            return
        if base_url:
            url = f"{base_url}{url}"

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name
    urllib.request.urlretrieve(url, tmp_path)
    try:
        play_mp3(tmp_path)
    finally:
        os.remove(tmp_path)


def handle_twiml(twiml, base_url):
    root = ET.fromstring(twiml)
    namespace = "{http://www.twilio.com/docs/voice/twiml}"

    def strip_ns(tag):
        return tag.replace(namespace, "")

    for node in root:
        tag = strip_ns(node.tag)
        if tag == "Say":
            text = (node.text or "").strip()
            if text:
                print(f"Assistant: {text}")
        elif tag == "Play":
            url = (node.text or "").strip()
            if url:
                print(f"Assistant (audio): {url}")
            play_remote_audio(url, base_url=base_url)
        elif tag == "Gather":
            prompt = None
            for child in node:
                child_tag = strip_ns(child.tag)
                if child_tag == "Say":
                    prompt = (child.text or "").strip()
                    if prompt:
                        print(f"Assistant: {prompt}")
            return {"action": node.attrib.get("action", "/gather"), "prompt": prompt}

    return None


def main():
    print("CLI Twilio Simulator")
    print("--------------------")

    base_url = input("Base URL (e.g. http://127.0.0.1:5001): ").strip().rstrip("/")
    start_url = f"{base_url}/start_conversation"

    call_sid = "SIMULATED_CALL_SID"
    twiml = fetch_twiml(start_url, data={"CallSid": call_sid})

    while True:
        gather_info = handle_twiml(twiml, base_url)
        if not gather_info:
            print("Call ended.")
            break

        user_text = input("You: ").strip()
        if user_text.lower() in {"q", "quit", "exit"}:
            print("Call ended by user.")
            break

        action_url = gather_info["action"]
        if not action_url.startswith("http"):
            action_url = f"{base_url}{action_url}"

        twiml = fetch_twiml(
            action_url,
            data={
                "CallSid": call_sid,
                "SpeechResult": user_text,
            },
        )


if __name__ == "__main__":
    main()
