import os
import anthropic

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024


class LlmClient:
    def __init__(self, api_key=None):
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def send(self, messages, tools=None, system=None):
        kwargs = {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        if system:
            kwargs["system"] = system
        return self.client.messages.create(**kwargs)