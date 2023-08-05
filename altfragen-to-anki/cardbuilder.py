import extract


def add_html_mc_anwser(content: str):
    return f"<li>{content}</li>"


def generate_mc_part(mcs: dict[int, tuple[str, bool]], is_for_backside=False) -> str:
    mcs_part = "<br><ul style='list-style-type: none; padding: 0; margin: 0'>"

    if is_for_backside:
        for key, value in mcs.items():
            generated = "(ChatGPT)" if value[1] else ""
            mcs_part += add_html_mc_anwser(f"{extract.letters[key]} {value[0].strip()} {generated}")
    else: 
        for key, value in mcs.items():
            mcs_part += add_html_mc_anwser(f"{extract.letters[key]} {value[0].strip()}")

    mcs_part += "</ul><br>"
    return mcs_part


def generate_front_side(
        mcs: dict[int, tuple[str, bool]], 
        question: str
        ) -> str:
    mc_part = generate_mc_part(mcs)
    content = "<br>".join([question, mc_part]).replace('"', "'").replace("\n", "<br>")
    return f"<div style='text-align: left'>{content}</div>"


def generate_back_side(
        mcs: dict[int, tuple[str, bool]], 
        question: str,
        anwser: str,
        ) -> str:
    mc_part = generate_mc_part(mcs, True)
    content = "<br>".join([question, mc_part, anwser]).replace('"', "'").replace("\n", "<br>")
    return f"<div style='text-align: left'>{content}</div>"


def generate_deck_name(filename: str, use_gpt: bool):
    gpt_cat = "-GPT" if use_gpt else ""
    filename_parts = filename.split("-")
    return f"Medizin::2.Lernspirale::Modul {filename_parts[1]}::Altfragen{gpt_cat}::{filename_parts[0]}"
