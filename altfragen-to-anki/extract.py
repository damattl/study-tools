import re
import ai
from altfrage import Altfrage

mc_regex = re.compile(r"((?:^|(?<=\n)|(?<=^   )|(?<=\n   )|(?<=    ))(?:[0-9]\.(?! Frage))|(?:^|(?<=\n))[A-Ea-e]\))", re.MULTILINE)
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


def extract_important_line_indices(splits: list[str]) -> tuple[int, int, int]:
    anwser_index = len(splits)
    last_line_index = len(splits)
    first_question_index = -1
    for j, split in enumerate(splits):
        if first_question_index == -1:
            matches = re.findall(mc_regex, split)
            if len(matches) > 0:
                first_question_index = j
        if "Antwort:" in split:
            anwser_index = j
            continue
        if "Gedächtnisprotokoll" in split:
            last_line_index = j-1
            break;
    # print(splits)
    return first_question_index, anwser_index, last_line_index


def sanitize_anwser_line(splits: list[str], anwser_index: int): 
    print(splits)
    split = splits[anwser_index]
    answer_splits = split.split("Antwort:")
    if (len(answer_splits) <= 1):
        return
    splits[anwser_index] = "Antwort:" + answer_splits[1]



def extract_all_from_raw_text(text: str, use_gpt: bool = False) -> list[Altfrage]:
    questions = re.split(r"_{12,}", text)
    questions = questions[1 : len(questions)]

    altfragen: list[Altfrage] = []

    for i, question in enumerate(questions):
        print("________________")
        splits = question.split("\n")

        if len(splits) < 2:
            continue

        mcs = extract_mc_questions(question)
        splits_by_question_start = re.split(mc_regex, question)
        prompt = splits_by_question_start[0].strip()

        if len(mcs) == 0 and re.match(r"^[0-9]{0,3}\.\s?Frage:?\s*(?:\n|$)", prompt) != None:
            continue

        first_question_index, anwser_index, last_line_index = extract_important_line_indices(splits)
        sanitize_anwser_line(splits, anwser_index)
        

        # Currently not in use
        correct_anwser = -1
        if anwser_index < len(splits):
            correct_anwser = extract_correct_anwser(splits[anwser_index])
        # print(correct_anwser)

       # mcs_l = len(mcs)

        if use_gpt:
            gpt_anwsers = ai.generate_anwsers(prompt, 5 - len(mcs), prev_anwsers=mcs)

            print(f"GPT Anwsers: {gpt_anwsers}")
            
            usedAnswers = 0
            for i in range(5):
                if usedAnswers >= len(gpt_anwsers):
                    break
                if mcs.get(i) is not None:
                    continue

                mcs[i] = (gpt_anwsers[usedAnswers], True)
                usedAnswers += 1
        

        altfrage = Altfrage.from_indices(mcs, splits, first_question_index, anwser_index, last_line_index)
    
        altfragen.append(altfrage)
        #if mcs_l < 5:
         #   tries += 1

        #if tries > 2:
         #   exit()
    return altfragen
