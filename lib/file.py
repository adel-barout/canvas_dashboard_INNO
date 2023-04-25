import json

from model.Course import Course
from model.CourseConfig import CourseConfig
from model.CourseConfigStart import CourseConfigStart
from model.Student import Student
from model.Submission import Submission

course_config_start_file = "course_config_start.json"

def read_course_config_start():
    with open(course_config_start_file, mode='r', encoding="utf-8") as file_config_start:
        data = json.load(file_config_start)
        course_config_start = CourseConfigStart.from_dict(data)
        return course_config_start

def read_course_config(course_config_file_name):
    print("read_course_config",course_config_file_name)
    with open(course_config_file_name, mode='r', encoding="utf-8") as course_config_file:
        data = json.load(course_config_file)
        course_config = CourseConfig.from_dict(data)
        return course_config

# def read_course(course_result_file_name):
#     with open(course_result_file_name, mode='r', encoding="utf-8") as file_result:
#         data = json.load(file_result)
#         course = CourseConfig.from_dict(data)
#         return course

def read_course_results(course_result_file_name):
    print("read_course_results",course_result_file_name)
    with open(course_result_file_name, mode='r', encoding="utf-8") as file_result:
        data = json.load(file_result)
        course = Course.from_dict(data)
        return course

def read_late_json():
    f = open('late.json')
    late_list = []
    data = json.load(f)
    for late_json in data:
        late = Submission.from_dict(late_json)
        late_list.append(late)
    # Closing file
    f.close()
    return late_list

def read_student_json():
    f = open('student_results.json')
    students = []
    data = json.load(f)
    for student_json in data['student_groups']:
        student = Student.from_dict(student_json)
        students.append(student)
    # Closing file
    f.close()
    return students