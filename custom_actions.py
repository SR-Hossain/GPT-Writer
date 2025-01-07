from clients import Gemini


def ai_prompt(text):
    return Gemini().generate_response(text)


def rephrase(text):
    prompt = f'''Rephrase and improve the following text: \n"{text}"'''
    return Gemini().generate_response(prompt)
