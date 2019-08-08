import csv
import itertools



from amp_dprc_database import dbase_functions

course_enrollement_csv = r"C:\Users\913678186\Box\Servers\amp_dprc_db_server\course_importer_myDPRC\Courses.txt"
course_list_csv = r"C:\Users\913678186\Box\Servers\amp_dprc_db_server\course_importer_myDPRC\Classlist.txt"





def import_student_enrollement():

    dbase_functions.clear_myDPRC_enroll_data()

    with open(course_enrollement_csv) as course_enrollement:

        csv_reader = csv.reader(course_enrollement, delimiter='\t')
        csv_reader = itertools.islice(csv_reader, 1, None)
        for row in csv_reader:

            print(row[0], row[2])
            dbase_functions.commit_myDPRC_student_enrollement(row[0], row[2])





def import_all_courses():

    count = 0
    dbase_functions.clear_myDPRC_course_data()

    with open(course_list_csv) as course_list:

        csv_reader = csv.reader(course_list, delimiter='\t')
        csv_reader = itertools.islice(csv_reader, 1, None)



        for row in csv_reader:


            count += 1
            term_code = row[0]
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
                                                      term_code,
                                                      subject_code,
                                                      course_number,
                                                      section_number,
                                                      class_title,
                                                      instructor_name,
                                                      instructor_email,
                                                      instructor_id)

    print("THEEE COUNNTTTTTT", count)

def add_items_to_tables():
    dbase_functions.refresh_instructor_table()
    dbase_functions.add_courses_to_course_table('fa19')
    dbase_functions.update_course_enrollement()


import_student_enrollement()
import_all_courses()
add_items_to_tables()