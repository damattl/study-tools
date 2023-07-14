import extract
import cardbuilder

from os import makedirs, path, listdir
from os.path import isfile, join
from altfrage import Altfrage


def get_correct_output_path(filename: str, output_dir: str, combined_output: bool, use_gpt: bool):
    gpt_mode = "-gpt" if use_gpt else "-no-gpt"

    if combined_output:
        return f"{output_dir}/ankis{gpt_mode}-combined.txt"

    return f"{output_dir}/ankis{gpt_mode}-{filename.split('.')[0]}.txt"

def fill_anki_txt_file(altfragen: list[Altfrage], filename: str, output_dir, combined_output: bool, use_gpt: bool):
    makedirs(output_dir, exist_ok=True)
    output_path = get_correct_output_path(filename, output_dir, combined_output, use_gpt)
    deckname = cardbuilder.generate_deck_name(filename, use_gpt)

    print(output_path)
    if not path.exists(output_path):
        print("Does not exist")
        with open(output_path, 'w') as file: 
            file.write('#deck column:3\n')
    
    with open(output_path, 'a') as file:
        for altfrage in altfragen:
            anki_card = altfrage.to_anki_card(deckname)
            file.write(anki_card)
            file.write("\n")
            

def convert_file_to_anki(filename: str, combined_output: bool = False, use_gpt = False, output_dir = "output", input_dir="./altfragen/"):
    if (path.splitext(filename)[1] != ".txt"):
        return
    
    with open(f'{input_dir}{filename}') as f:
        text = f.read()

    altfragen = extract.extract_all_from_raw_text(text, use_gpt)
    print(filename)
    fill_anki_txt_file(altfragen, filename, output_dir, combined_output, use_gpt)


def convert_all_files_in_folder(combined_output: bool = True, use_gpt = False, input_dir="./altfragen/"):
    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    print(files)
    for file in files:
        convert_file_to_anki(file, combined_output, use_gpt=use_gpt, input_dir=input_dir)
    print(files)