import litellm

from lab.settings import Settings

SYSTEM_PROMPT = """You are a helpful assistant."""
USER_PROMPT = """Who is Charles Leclerc?"""

settings = Settings()
if not settings.litellm_api_key:
    raise SystemExit("Set LITELLM_API_KEY to your LiteLLM master key or user key.")

litellm.api_base = settings.litellm_base_url
litellm.api_key = settings.litellm_api_key

def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ]

    response = litellm.completion(
        model=settings.model,
        messages=messages,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        top_p=settings.top_p,
        top_k=settings.top_k,
        presence_penalty=settings.presence_penalty,
        repetition_penalty=settings.repetition_penalty,
        extra_body={ # Please disable thinking to get responses in a reasonable time frame
            "chat_template_kwargs": {"enable_thinking": False}
        },  
        stream=True,
    )
    for chunk in response:  # type: ignore[union-attr]
        if isinstance(chunk, litellm.ModelResponseStream): # This is to make the type checker happy
            print(chunk.choices[0].delta.content or "", end="", flush=True)

    print()


if __name__ == "__main__":
    main()
