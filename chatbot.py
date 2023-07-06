import openai
openai.api_key = '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'
messages = [ {"role": "system", "content":
            "You are a intelligent assistant."} ]

def ai_response(message):
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply