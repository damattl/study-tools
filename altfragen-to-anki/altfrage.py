import extract
import cardbuilder


class Altfrage:
    def __init__(self, mcs: dict[int, tuple[str, bool]], question: str, anwser: str):
        self.mcs: dict[int, tuple[str, bool]] = mcs
        self.question: str = question
        self.anwser: str = anwser

    @staticmethod
    def from_indices(
        mcs: dict[int, tuple[str, bool]], 
        splits: list[str], 
        first_question_index: int, 
        anwser_index: int, 
        last_line_index: int
    ):
        return Altfrage(
            mcs,
            "\n".join(splits[0:first_question_index]),
            "\n".join(splits[anwser_index:last_line_index])
        )
    
    def to_anki_card(self, deckname: str):
        front = cardbuilder.generate_front_side(self.mcs, self.question)
        back = cardbuilder.generate_back_side(self.mcs, self.question, self.anwser)
        return f'"{front}";"{back}";"{deckname}"'
