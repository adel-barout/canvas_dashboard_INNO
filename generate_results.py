import sys
from canvasapi import Canvas
import json

from lib.file import read_start, read_course, read_course_instance, read_progress
from lib.lib_attendance import process_attendance
from lib.lib_progress import get_progress, get_overall_progress, get_attendance_progress
from lib.lib_submission import count_graded, add_missed_assignments, read_submissions
from model.ProgressDay import ProgressDay
from model.Result import *
from lib.lib_date import get_actual_date, API_URL, date_to_day


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GR02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR03 - Username", user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)
    if g_actual_date > start.end_date:
        results = Result(start.canvas_course_id, course.name, start.end_date, date_to_day(start.start_date, start.end_date), 0, 0)
    elif g_actual_date < start.start_date:
        results = Result(start.canvas_course_id, course.name, start.start_date, 1, 0, 0)
    else:
        results = Result(start.canvas_course_id, course.name, g_actual_date, date_to_day(start.start_date, g_actual_date), 0, 0)
    for student in course.students:
        print("GR05 -", student.name, student.number)
    results.students = course.students
    for student in results.students:
        print("GR07 -", student.name, student.number)
    read_submissions(canvas_course, start, course, results, True)
    for student in results.students:
        for perspective in student.perspectives.values():
            # Perspective aanvullen met missed Assignments (niets ingeleverd)
            add_missed_assignments(course, results.actual_day, perspective)
    if start.attendance is not None:
        process_attendance(start, course, results)
    else:
        print("GR10 - No attendance")

    # for student in results.students:
    #     print("GR75", student.name)
    # sorteer de attendance en submissions
    for student in results.students:
        if start.attendance is not None:
            student.attendance_perspective.attendance_submissions = sorted(student.attendance_perspective.attendance_submissions, key=lambda s: s.day)
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                submission_sequence.submissions = sorted(submission_sequence.submissions, key=lambda s: s.assignment_day)
            perspective.submission_sequences = sorted(perspective.submission_sequences, key=lambda s: s.get_day())

    results.submission_count, results.not_graded_count = count_graded(results)

    with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    progress_history = read_progress(instances.get_progress_file_name(instances.current_instance))
    progress_day = ProgressDay(results.actual_day, course.perspectives.keys())

    # Bepaal voortgang per perspectief
    for student in results.students:
        if start.attendance is not None:
            get_attendance_progress(course.attendance, results, student.attendance_perspective)
            progress_day.attendance[str(student.attendance_perspective.progress)] += 1
        for perspective in student.perspectives.values():
            # print("GR20 -", student.name, perspective.name)
            get_progress(course, perspective)
            progress_day.perspective[perspective.name][str(perspective.progress)] += 1
    # Bepaal de totaal voortgang
    for student in results.students:
        perspectives = []
        for perspective in student.perspectives.values():
            perspectives.append(perspective.progress)
        progress = get_overall_progress(perspectives)
        # print(student.name, perspectives, progress )
        student.progress = progress
        progress_day.progress[str(progress)] += 1
    progress_history.append_day(progress_day)

    # progress_history = generate_history(results)

    with open(instances.get_progress_file_name(instances.current_instance), 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)

    with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    print("GR99 Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    print("GR01 - generate_results.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")