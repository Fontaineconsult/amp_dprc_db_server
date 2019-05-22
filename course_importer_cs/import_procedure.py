import sys

sys.path.append("/home/daniel/dev/py36-venv/dev")

import amp_dprc_database.dbase_functions as db
from course_importer_cs.course_importer_classes import CourseList
import os

file_path_link = "C:\\Users\\913678186\\Box\\SF State Python Projects\\DPRC AMP\\course_importer\\courses.xlsx"
csv_link = "C:\\Users\\913678186\\Box\\SF State Python Projects\\DPRC AMP\\course_importer\\courseidsold.csv"

def create_courses_object(semester, file_path):

    captioning_students = db.get_all_students_ids()
    current_course_list = []

    if os.path.exists(file_path):

        all_courses = CourseList(file_path, semester)

        for student_course_object in all_courses.student_course_list:
            if student_course_object.student_id in captioning_students:
                current_course_list.append(student_course_object)

    return current_course_list


def course_constructor(semester):

    cap_students_courses = create_courses_object(semester, file_path_link)

    for student in cap_students_courses:

        for course in student.courses:

            check_instructors(course)
            check_course(course)
            update_enrollement(student.student_id, course.course_gen_id, course.student_enrolled)


def check_instructors(course):

    instructor_first_name = course.instructor_name.split(",")[0]
    instructor_last_name = course.instructor_name.split(",")[1]

    db.check_or_commit_instructor({"instructor_id": course.instructor_id,
                                   "instructor_first_name": instructor_first_name,
                                   "instructor_last_name": instructor_last_name,
                                   "instructor_email": course.instructor_email,
                                   "instructor_phone": course.instructor_phone})


def check_course(course):

    db.check_or_commit_course({"course_gen_id": course.course_gen_id,
                               "course_name": course.course_code,
                               "course_section": course.course_section,
                               "course_instructor_id": course.instructor_id,
                               "semester": course.semester,
                               "course_online": course.course_online})


def update_enrollement(student_id, course_gen_id, enrolled):

    db.check_or_update_enrollement(student_id, course_gen_id, enrolled)




