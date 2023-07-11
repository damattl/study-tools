import re
import generator
import extract

from os import makedirs, path, listdir
from os.path import isfile, join


def convert_file_to_anki(filename: str, combined_output: bool = False, use_gpt = False, input_dir = "./altfragen/"):
    with open(f'{input_dir}{filename}') as f:
        text = f.read()

    questions = re.split(r"_{10,}", text)
    questions = questions[1 : len(questions)]

    question_anwser_dict: dict[str, str] = {}
    tries = 0

    for question in questions:
        print("________________")
        splits = question.split("\n")

        anwser = question
        anwserIndex = len(splits)

        breakAtNextBlankLine = False
        lastLine = len(splits)

        mcs = extract.extract_mc_questions(question)
        splits_by_question_start = re.split(extract.mc_regex, question)
        prompt = splits_by_question_start[0].strip()

    
        if len(mcs) == 0 and re.match(r"^[0-9]{0,3}\.\s?Frage:?\s*\n|$", prompt) != None:
            continue

        firstQuestionIndex = -1
        for j, split in enumerate(splits):
            match = re.match(extract.mc_regex, split)
            if firstQuestionIndex is -1 and  match != None:
                firstQuestionIndex = j
            if (breakAtNextBlankLine and split == ""):
                lastLine = j
                break;
            if "Antwort:" in split:
                anwserIndex = j
                answerSplits = split.split("Antwort:")
                if (len(answerSplits) <= 1):
                    continue
                
                splits[j] = "Antwort:" + answerSplits[1]
                continue
            if "Kommentar:" in split:
                breakAtNextBlankLine = True

        correct_anwser = -1
        if anwserIndex < len(splits):
            correct_anwser = extract.extract_correct_anwser(splits[anwserIndex])
        print(correct_anwser)

        mcs_l = len(mcs)

        if use_gpt:
            gpt_anwsers = generator.generate_anwsers(prompt, 5 - len(mcs), prev_anwsers=mcs)

            print(f"GPT Anwsers: {gpt_anwsers}")
            
            usedAnswers = 0
            for i in range(5):
                if usedAnswers >= len(gpt_anwsers):
                    break
                if mcs.get(i) is not None:
                    continue


                mcs[i] = (gpt_anwsers[usedAnswers], True)
                usedAnswers += 1


        mcPartQuestion = ""
        for key, value in mcs.items():
            mcPartQuestion += f"{extract.letters[key]} {value[0].strip()}\n"


        mcPartAnwser = ""
        for key, value in mcs.items():
            generated = "(ChatGPT)" if value[1] else ""
            mcPartAnwser += f"{extract.letters[key]} {value[0].strip()} {generated}\n"
            
    
                
        anwser = "\n".join([*splits[0:firstQuestionIndex], mcPartAnwser, *splits[anwserIndex:lastLine]]).replace('"', "'")
        question = "\n".join([*splits[0:firstQuestionIndex], mcPartQuestion]).replace('"', "'")

        

        print(question)
        print(anwser)

        question_anwser_dict[question] = anwser
        #if mcs_l < 5:
         #   tries += 1

        #if tries > 2:
         #   exit()

    makedirs("output", exist_ok=True)
    filename_parts = filename.split("-")
    gpt_mode = "-gpt" if use_gpt else "-no-gpt"
    gpt_cat = "-GPT" if use_gpt else ""

    if (combined_output):
        output_path = f"output/ankis{gpt_mode}-combined.txt"
        if not path.exists(output_path):
            with open(output_path, 'w'): pass
        with open(output_path, "r+") as file:
            if file.read() == "": 
                file.write('#deck column:3\n')
            for key, value in question_anwser_dict.items():
                file.write(f'"{key}";"{value}";"Medizin::2.Lernspirale::Modul {filename_parts[1]}::Altfragen{gpt_cat}::{filename_parts[0]}"\n')
    else:
        with open(f"output/ankis{gpt_mode}-{filename.split('.')[0]}.txt", "w") as file:
            file.write('#deck column:3\n')
            for key, value in question_anwser_dict.items():
                file.write(f'"{key}";"{value}";"Medizin::2.Lernspirale::Modul {filename_parts[1]}::Altfragen{gpt_cat}::{filename_parts[0]}"\n')




def convert_all_files_in_folder(combined_output: bool = True, use_gpt = False, input_dir = "./altfragen/"):
    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    for file in files:
        convert_file_to_anki(file, combined_output, use_gpt, input_dir)