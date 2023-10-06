import datetime


class SwapOption:
    def __init__(self, cid: str, raw: list[str]):
        self.conflict = None
        self.cid = cid
        splits = raw[0].replace("Tauschoption:", "").strip().split(" ")

        date_splits = splits[0].split(".")

        year = int("20" + date_splits[0])  # todo make changable
        month = int(date_splits[1])
        day = int(date_splits[2])

        self.date = datetime.date(year, month, day)

        time_splits = splits[1].split("-")

        start_splits = time_splits[0].split(":")
        self.start = datetime.time(int(start_splits[0]), int(start_splits[1]))

        end_splits = time_splits[1].split(":")
        self.end = datetime.time(int(end_splits[0]), int(end_splits[1]))

        self.size = int(raw[1].replace("Pers.: ", "").strip())
        self.group = raw[2].replace("Grp: ", "").strip()
        if len(raw) > 3:
            self.conflict = raw[3]

    def __str__(self):
        return f"SwapOption(cid: {self.cid}, date: {self.date}, start: {self.start}, end: {self.end}, size: {self.size}, group: {self.group}, conflict: {self.conflict})"


class Course:
    def __init__(self, raw: dict[str, str], attendance_points: int, swap_options: list[SwapOption]):
        self.cid = raw["Cid"]
        self.subject = raw["Typ"]
        self.title = raw["Titel"]
        self.module = raw["Md"]
        self.teacher = raw["Doz"]
        self.room = raw["Raum / m / g"]

        date_splits = raw["Dat. / m"].split(".")
        year = int("20" + date_splits[2])
        month = int(date_splits[1])
        day = int(date_splits[0])

        self.date = datetime.date(year, month, day)

        start_splits = raw["von"].split(":")
        self.start = datetime.time(int(start_splits[0]), int(start_splits[1]))

        end_splits = raw["bis"].split(":")
        self.end = datetime.time(int(end_splits[0]), int(end_splits[1]))

        self.groups = raw["Gruppen"]
        self.attendance_points = attendance_points
        self.swap_options = swap_options

    def __str__(self):
        # Create a formatted string representation of the Course object
        course_str = f"Course ID: {self.cid}\n"
        course_str += f"Subject: {self.subject}\n"
        course_str += f"Title: {self.title}\n"
        course_str += f"Module: {self.module}\n"
        course_str += f"Teacher: {self.teacher}\n"
        course_str += f"Room: {self.room}\n"
        course_str += f"Date: {self.date}\n"
        course_str += f"Start Time: {self.start}\n"
        course_str += f"End Time: {self.end}\n"
        course_str += f"Groups: {self.groups}\n"
        course_str += f"Attendance Points: {self.attendance_points}\n"
        course_str += "Swap Options:\n"

        if self.swap_options is None:
            return course_str
        for option in self.swap_options:
            course_str += f"  - {option}\n"

        return course_str

    def __repr__(self):
        return self.__str__()
