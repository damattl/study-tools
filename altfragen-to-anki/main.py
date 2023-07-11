import re

from os import listdir, makedirs 
from os.path import isfile, join


altfragen_path = "./altfragen/"


def convertFileToAnki(filename: str):
    with open(f'{altfragen_path}{filename}') as f:
        text = f.read()


    questions = re.split(r"_{10,}", text)
    questions = questions[1 : len(questions)]

    question_anwser_dict: dict[str, str] = {}

    for question in questions:
        splits = question.split("\n")


        anwser = question

        
        anwserIndex = len(splits) - 1
        for i, split in enumerate(splits):
            if "Antwort" in split:
                anwserIndex = i
                break
        
        question = "\n".join(splits[0:anwserIndex])


        question_anwser_dict[question] = anwser



    print(question_anwser_dict[next(iter(question_anwser_dict))])


    filename_parts = filename.split("-")

    makedirs("output", exist_ok=True)
    with open(f"output/ankis-{filename.split('.')[0]}.txt", "w") as file:
        file.write('#deck column:3\n')
        for key, value in question_anwser_dict.items():
            file.write(f'"{key}";"{value}";"Medizin::2.Lernspirale::Modul {filename_parts[1]}::Altfragen::{filename_parts[0]}"\n')



files = [f for f in listdir(altfragen_path) if isfile(join(altfragen_path, f))]
for file in files:
    convertFileToAnki(file)
