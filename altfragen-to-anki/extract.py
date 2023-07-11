import re

mc_regex = r"((?:^|(?<=\n))(?:[0-9]\.(?! Frage))|(?:^|(?<=\n))[A-Ea-e]\))"
anwser_regex = r"Antwort:\s{0,10}(.)"

letters = ["A)", "B)", "C)", "D)", "E)", "F)", "G)", "H)"]
letters_to_index = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
}

def test_and_add(mc_dict: dict[int, tuple[str, bool]], mc: str, qi: int):
    if re.match(r"^\s*$", mc) != None:
        return
    mc_dict[qi] = (mc, False)

def extract_mc_questions(text: str) -> dict[int, tuple[str, bool]]:
    mcQuestions = re.split(mc_regex, text)[1:]
    if len(mcQuestions) < 2:
        return {}
    mc_dict: dict[int, tuple[str, bool]] = {}
    print(text)

    for i in range(0, len(mcQuestions), 2):
        qi = mcQuestions[i]
        mc = mcQuestions[i+1]

        qi = qi.replace(")", "").replace(".", "")
        qi = letters_to_index[qi]

        if "Fach:" in mc:
            mc = mc.split("Fach:")[0]
            test_and_add(mc_dict, mc, qi)
            break
        if "Antwort:" in mc:
            mc = mc.split("Antwort:")[0]
            test_and_add(mc_dict, mc, qi)
            break
        test_and_add(mc_dict, mc, qi)
        

    print(mc_dict)


    return mc_dict



def extract_correct_anwser(anwser_line: str) -> int:
    print(anwser_line)
    match = re.match(anwser_regex, anwser_line)
    
    if match == None:
        print(anwser_line)
        print("anwser not found")
        return -1

    if (len(match.groups()) < 1):
        print(anwser_line)
        print("anwser not found")
        return -1
    anwser = match.group(1).capitalize()
    try:
        return letters_to_index[anwser]
    except:
        return -1
