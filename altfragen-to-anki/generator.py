import openai
import config
import time

def generate_anwsers(question: str, count: int, prev_anwsers: dict[int, tuple[str, bool]], retry = False) -> list[str]:
    if retry:
        time.sleep(5)
    request = f"Bitte generiere {count} falsche Antworten zu folgender Frage: \n {question.strip()} \nEs gibt bereits folgende Antworten: \n"

    for prev in prev_anwsers.values():
        request += prev[0].strip() + "\n"


    request += "\nIncludiere keine Hinweise wie 'Falsche Antwort', 'Richtige Antwort', 'Antwort' oder ähnliches. \n Bitte orientiere dich immer an den voerherigen Antworten. Nutze | als Delimiter."
    print(request)

    if count <= 0:
        return []

    openai.api_key = config.openai_secret
    openai.organization = "org-gj2MzWVuHUdDbND5jI9AlXNE"
    openai.Model.list()
    
    generated_anwsers = []

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": request}
            ]
        )
        print(completion)
        results = completion.choices[0].message
        if results == None:
            results = completion.choices[0].messages
            for result in results:
                generated_anwsers.append(result.content)
        else:
            content: str = results.content
            generated_anwsers = generated_anwsers + content.split("|")
    except Exception as e:
        print(e)
    except openai.error.OpenAIError:
        if retry:
            return []
        return generate_anwsers(question, count, prev_anwsers, retry=True)

    return generated_anwsers
    
