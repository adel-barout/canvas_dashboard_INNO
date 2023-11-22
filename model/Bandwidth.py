class Point:
    def __init__(self, day, lower, upper):
        self.day = day
        self.lower = lower
        self.upper = upper

    def to_json(self):
        return {
            'day': self.day,
            'lower': int(self.lower*100)/100,
            'upper': int(self.upper*100)/100
        }

    def __str__(self):
        return f'Point({self.day}, {self.lower}, {self.upper})'

    @staticmethod
    def from_dict(data_dict):
        return Point(data_dict['day'], data_dict['lower'], data_dict['upper'])


class Bandwidth:
    def __init__(self):
        self.days = []
        self.lowers = []
        self.uppers = []
        self.points = []

    def to_json(self):
        return {
            'days': self.days,
            'lowers': list(map(lambda u: int(u*100)/100, self.lowers)),
            'uppers': list(map(lambda u: int(u*100)/100, self.uppers)),
            'points': list(map(lambda p: p.to_json(), self.points))
        }

    def __str__(self):
        line = f'Bandwidth({self.lowers})'
        for point in self.points:
            line += str(point)
        return line

    def get_progress(self, day, score):
        if score == 0 or day == 0:
            return 0
        try:
            if score < self.points[int(day)].lower:
                return 1
            elif score < self.points[int(day)].upper:
                return 2
            else:
                return 3
        except IndexError:
            if score < self.points[len(self.points)-1].lower:
                return 1
            elif score < self.points[len(self.points)-1].upper:
                return 2
            else:
                return 3

    @staticmethod
    def from_dict(data_dict):
        if data_dict is None:
            return None
        new = Bandwidth()
        new.days = data_dict['days']
        new.lowers = data_dict['lowers']
        new.uppers = data_dict['uppers']
        new.points = list(map(lambda p: Point.from_dict(p), data_dict['points']))
        return new
