# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
from canvasapi import Canvas
import json
from lib.file import read_start, read_course
from model.AssignmentDate import AssignmentDate
from model.Comment import Comment
from model.Result import *
from lib.config import actual_date, API_URL, NOT_GRADED
from model.Submission import Submission


def get_submitted_at(item):
    return item[1].submitted_at


def submissionBuilder(a_student, a_assignment, a_canvas_submission, a_assignment_date):
    local_comment = ""
    if a_canvas_submission.score is not None:
        if a_canvas_submission.grade == 'complete':
            # print("Grade", canvas_submission.grade, canvas_submission.score, canvas_submission.assignment_id)
            score = 1.0
        elif a_canvas_submission.grade == 'incomplete':
            # print("Grade", canvas_submission.grade, canvas_submission.score, canvas_submission.assignment_id)
            score = 0.5
        else:
            score = round(a_canvas_submission.score, 2)
        graded = True
    else:
        if not a_canvas_submission.submitted_at:
            # no actual submission
            return
        else:
            score = 0
            if not a_canvas_submission.grader_id:
                graded = False
            else:
                graded = True

    if a_canvas_submission.submitted_at:
        submitted_at = get_date_time_obj(a_canvas_submission.submitted_at)
    else:
        # l_assignment = course.find_assignment(a_assignment.id)
        submitted_at = a_assignment.assignment_date

    # maak een submission en voeg de commentaren toe
    l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                            a_assignment.name, submitted_at, graded, score, a_assignment.points)
    canvas_comments = a_canvas_submission.submission_comments
    if len(local_comment) > 0:
        l_submission.comments.append(Comment(0, "", submitted_at, local_comment))
    for canvas_comment in canvas_comments:
        l_submission.comments.append(
            Comment(canvas_comment['author_id'], canvas_comment['author_name'], get_date_time_obj(canvas_comment['created_at']), canvas_comment['comment']))
    return l_submission



course_config_start = read_start()
course = read_course(course_config_start.course_file_name)
# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config_start.course_id)
# print("Course(canvas_course.id, canvas_course.name, actual_date)")
results = Result(canvas_course.id, canvas_course.name, actual_date, 0, 0)
# kopieer de groepen en studenten vanuit de configuratie
# print("course.studentGroups")
results.students = course.students


# assignments to groups and roles
# print("canvas_course.get_assignments(include=['overrides'])")
canvas_assignments = canvas_course.get_assignments(include=['overrides'])
# print("for canvas_assignment in canvas_assignments")
for canvas_assignment in canvas_assignments:
    assignment_group = course.find_assignment_group(canvas_assignment.assignment_group_id)
    if assignment_group:
        # print("Processing G {0:8} - {1}".format(assignment_group.id, assignment_group.name))
        assignment = course.find_assignment_by_group(assignment_group.id, canvas_assignment.id)
        if assignment:
            print("Processing Assignment {0:6} - {1} {2}".format(assignment.id, assignment_group.name, assignment.name))
            if assignment.unlock_date:
                if assignment.unlock_date > results.actual_date:
                    continue
            if canvas_assignment.overrides:
                for override in canvas_assignment.overrides:
                    assignment_date = AssignmentDate(override.id, override.due_at, override.lock_at)
            else:
                assignment_date = AssignmentDate(canvas_assignment.id, canvas_assignment.due_at, canvas_assignment.lock_at)

            canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments'])
            for canvas_submission in canvas_submissions:
                student = results.find_student(canvas_submission.user_id)
                if student:
                    # voeg een submission toe aan een van de perspectieven
                    l_submission = submissionBuilder(student, assignment, canvas_submission, assignment_date)
                    if l_submission:
                        l_perspective = course.find_perspective_by_assignment_group(l_submission.assignment_group_id)
                        if l_perspective:
                            this_perspective = student.get_perspective(l_perspective.name)
                            if this_perspective:
                                this_perspective.submissions.append(l_submission)
                                results.submission_count += 1
                                if not l_submission.graded:
                                    results.not_graded_count += 1

# for group in results.studentGroups:
#     for student in group.students:
#         for perspective in student.perspectives:
#             perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_at)

with open(course_config_start.results_file_name, 'w') as f:
    dict_result = results.to_json([])
    json.dump(dict_result, f, indent=2)
