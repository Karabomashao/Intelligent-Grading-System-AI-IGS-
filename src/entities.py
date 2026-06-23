from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MarkAllocation:
    value: int


@dataclass
class Option:
    label: str
    text: str


@dataclass
class SubQuestion:
    number: str
    text: str = ""
    options: List[Option] = field(default_factory=list)
    marks: Optional[MarkAllocation] = None
    children: List["SubQuestion"] = field(default_factory=list)
    parent: Optional["SubQuestion"] = None

    def add_option(self, option: Option):
        self.options.append(option)

    def set_marks(self, marks: MarkAllocation):
        self.marks = marks

    def add_child(self, child: "SubQuestion"):
        child.parent = self
        self.children.append(child)

    def append_text(self, extra_text: str):
        if self.text:
            self.text += " " + extra_text
        else:
            self.text = extra_text


@dataclass
class Question:
    number: str
    subquestions: List[SubQuestion] = field(default_factory=list)

    def add_subquestion(self, subq: SubQuestion):
        self.subquestions.append(subq)


@dataclass
class Section:
    name: str
    questions: List[Question] = field(default_factory=list)

    def add_question(self, question: Question):
        self.questions.append(question)


@dataclass
class Document:
    sections: List[Section] = field(default_factory=list)

    def add_section(self, section: Section):
        self.sections.append(section)