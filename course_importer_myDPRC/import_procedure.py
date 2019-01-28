import csv
import itertools

from amp_dprc_dbase import dbase_functions


course_enrollement_csv = "C:\\Users\\913678186\\Box\\SF State Python Projects\\DPRC AMP\\course_importer_myDPRC\\Courses.csv"
course_list_csv = "C:\\Users\\913678186\\Box\\SF State Python Projects\\DPRC AMP\\course_importer_myDPRC\\Classlist.csv"


def import_student_enrollement():

    with open(course_enrollement_csv) as course_enrollement:
        csv_reader = csv.reader(course_enrollement, delimiter=',')

        for row in csv_reader:

            dbase_functions.commit_myDPRC_student_enrollement(row[0], row[2])





def import_all_courses():


    dbase_functions.clear_myDPRC_course_data()

    with open(course_list_csv) as course_list:

        csv_reader = csv.reader(course_list, delimiter=',')
        csv_reader = itertools.islice(csv_reader, 1, None)



        for row in csv_reader:

            course_reg_number = row[1]
            subject_code = row[2]
            course_number = row[3]
            section_number = row[4]
            if len(section_number) == 1:
                section_number = "{}{}".format("0",section_number)
            class_title = row[5]
            instructor_name = row[18]

            instructor_email = row[19]
            instructor_id = row[20]

            print(instructor_name, instructor_email, instructor_id)

            dbase_functions.commit_myDPRC_course_data(course_reg_number,
                                                        subject_code,
                                                        course_number,
                                                        section_number,
                                                        class_title,
                                                        instructor_name,
                                                        instructor_email,
                                                        instructor_id)



def add_items_to_tables():
    dbase_functions.refresh_instructor_table()
    dbase_functions.add_courses_to_course_table()
    dbase_functions.update_course_enrollement()



import_all_courses()
add_items_to_tables()