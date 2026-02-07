from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY"
)

response = client.conversational_ai.agents.create(
    name="My conversational agent",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "You are a helpful assistant that can answer questions and help with tasks.",
            }
        }
    }
)