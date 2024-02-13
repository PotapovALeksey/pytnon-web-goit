from .table import Table
from dataclasses import dataclass
from random import randint, seed


@dataclass
class Subject:
    name: str
    teacher_id: int


class Subjects(Table):
    def __init__(self):
        super().__init__(
            "subjects",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "teacher_id": "INTEGER NOT NULL",
                "name": "VARCHAR(30) UNIQUE NOT NULL",
                "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            ("FOREIGN KEY (teacher_id) REFERENCES teachers (id)",),
        )

    def generate_data(self):
        seed()

        self.insert(Subject(teacher_id=randint(1, 5), name="Figma").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="Redis").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="MySQL").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="HTTPS").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="CSS").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="HTML").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="JS").__dict__)
        self.insert(Subject(teacher_id=randint(1, 5), name="PYTHON").__dict__)
