from model.Student import Student


class StudentGroup:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.teachers = []
        self.students = []

    def to_json(self, scope):
        return {
            'id': self.id,
            'name': self.name,
            'teachers': self.teachers,
            'students': list(map(lambda s: s.to_json([]), self.students)),
        }

    def __str__(self):
        line = f'StudentGroup({self.id}, {self.name}, {self.teachers})\n'
        for s in self.students:
            line += " s "+str(s)
        return line

    @staticmethod
    def from_dict(data_dict):
        new_student_group = StudentGroup(data_dict['id'], data_dict['name'])
        new_student_group.teachers = data_dict['teachers']
        new_student_group.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        return new_student_group

