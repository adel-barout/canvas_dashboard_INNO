from lib.lib_date import date_to_day


def student_total(a_perspective):
    cum_score = 0
    for submission_sequence in a_perspective.submission_sequences:
        cum_score += submission_sequence.get_score()
    return cum_score


def add_total(totals, total):
    totals.append(total)


def get_submitted_at(item):
    return item.submitted_at


def count_student(a_instances, a_course, a_student_totals, a_student):
    peil = a_student.progress
    # print(a_student.name, peil)
    a_student_totals['actual_progress']['overall'][peil] += 1
    for l_perspective in a_student.perspectives.values():
        add_total(a_student_totals['perspectives'][l_perspective.name]['count'], int(student_total(l_perspective)))
    if a_course.level_moments is not None:
        for peil_label in a_course.level_moments.moments:
            if a_instances.is_instance_of("inno_courses"):
                submission = a_student.get_peilmoment_submission_by_query([peil_label, "overall"])
            else:
                submission = a_student.get_peilmoment_submission_by_query([peil_label])
            if submission is not None:
                a_student_totals["level_moments"][peil_label]['overall'][int(submission.score)] += 1
            else:
                a_student_totals["level_moments"][peil_label]['overall'][-1] += 1


def check_for_late(a_instances, a_course, a_student_totals, a_student, a_submission, a_perspective, a_actual_day):
    if not a_submission.graded:
        # print("BT81", a_student.name, a_student.coach)
        if a_student.coach > 0:
            # print("BT82", a_student.name, a_student.coach)
            if a_perspective == 'team':
                l_selector = a_course.find_teacher(a_student.coach).initials
            elif a_instances.is_instance_of("prop_courses"):
                group = a_course.find_student_group(a_student.group_id)
                l_selector = group.name
            else:
                l_selector = a_student.role
        else:
            if a_instances.is_instance_of("inno_courses"):
                l_selector = a_student.role
            else:
                # print("BT83 Group id", a_student.group_id)
                group = a_course.find_student_group(a_student.group_id)
                l_selector = group.name
        late_days = a_actual_day - a_submission.submitted_day
        # print("BT85", a_perspective, l_selector)
        a_student_totals['perspectives'][a_perspective]['list'][l_selector].append(a_submission.to_json())
        if late_days <= 7:
            a_student_totals['perspectives'][a_perspective]['pending'][l_selector] += 1
        elif 7 < late_days <= 14:
            a_student_totals['perspectives'][a_perspective]['late'][l_selector] += 1
        else:
            a_student_totals['perspectives'][a_perspective]['to_late'][l_selector] += 1
        add_total(a_student_totals['late']['count'], late_days)


def build_totals(a_instances, a_start, a_course, a_results, a_student_totals):
    for l_student in a_results.students:
        count_student(a_instances, a_course, a_student_totals, l_student)
        for l_perspective in l_student.perspectives.values():
            for submission_sequence in l_perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    check_for_late(a_instances, a_course, a_student_totals, l_student, submission, l_perspective.name, a_results.actual_day)

