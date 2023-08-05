import openai
import config
import time
import extract
import re


def generate_anwsers(
        question: str,
        count: int,
        prev_anwsers: dict[int, tuple[str, bool]],
        retry=False
) -> list[str]:

    if count <= 0:
        return []
    if retry:
        time.sleep(5)
    request = ""
    if count == 5:
        request = f"Bitte generiere eine richtige und vier falsche Antworten zu folgender Frage: \n {question.strip()} \n"
        request += """Die richtige Antwort bitte zuerst
        \nIncludiere keine Hinweise wie z.B. 'falsch', 'richtig', 'Falsche Antwort',
        'Richtige Antwort', 'Antwort' oder ähnliches.
        \nNutze keine Aufzählungszeichen wie z.B. 1. oder A)
        \nNutze | als Delimiter."""
    else:
        request = f"Bitte generiere {count} falsche Antworten zu folgender Frage: \
        \n {question.strip()} \nEs gibt bereits folgende Antworten: \n"

        for key, value in prev_anwsers.items():
            request += f"{extract.letters[key]} {value[0].strip()}\n"
        request += """\nBerücksichtige die bereits gegebenen Antworten.
        \nIncludiere keine Hinweise wie z.B. 'falsch', 'richtig', 'Falsche Antwort',
        'Richtige Antwort', 'Antwort' oder ähnliches.
        \nNutze keine Aufzählungszeichen wie z.B. 1. oder A).
        \nNutze | als Delimiter."""

    print(request)

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
        if results is None:  # is not in use
            results = completion.choices[0].messages
            for result in results:
                generated_anwsers.append(result.content)
        else:
            content: str = results.content
            generated_anwsers = generated_anwsers + sanitize_gpt(content)
    except openai.error.OpenAIError:
        if retry:
            return []
        return generate_anwsers(question, count, prev_anwsers, retry=True)
    except Exception as e:
        print(e)

    return generated_anwsers
    

def sanitize_gpt(content: str) -> list[str]:
    splits = re.split(r"\n|\|", content)
    for i, split in enumerate(splits):
        splits[i] = re.sub(r"^[0-9]\.|[A-Ea-e]\)", "", split)
    return splits
