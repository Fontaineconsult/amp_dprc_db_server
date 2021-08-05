import csv
import itertools



from amp_dprc_database import dbase_functions

course_enrollement_csv = r"C:\Users\DanielPC\Desktop\Servers\amp_dprc_db_server\course_importer_myDPRC\Courses.txt"
course_list_csv = r"C:\Users\DanielPC\Desktop\Servers\amp_dprc_db_server\course_importer_myDPRC\Classlist.txt"





def import_student_enrollement(term_code):

    """
    Adds raw student enrollement data to the 'studentenrollement' table. Table is truncated before adding.
    """


    dbase_functions.clear_myDPRC_enroll_data()

    with open(course_enrollement_csv) as course_enrollement:

        csv_reader = csv.reader(course_enrollement, delimiter='\t')
        csv_reader = itertools.islice(csv_reader, 1, None)
        for row in csv_reader:

            print(row[1])
            if row[1] == term_code:
                print(row[0], row[1], row[2])
                dbase_functions.commit_myDPRC_student_enrollement(row[0], row[2])





def import_all_courses(term_code):

    count = 0

    dbase_functions.clear_myDPRC_course_data()

    with open(course_list_csv) as course_list:

        csv_reader = csv.reader(course_list, delimiter='\t')
        csv_reader = itertools.islice(csv_reader, 1, None)

        for row in csv_reader:

            course_term_code = row[0]
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


            if course_term_code == term_code:
                count += 1
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

    print("THE COUNNTTTTTT", count)

def add_items_to_tables(semester):
    dbase_functions.refresh_instructor_table()
    # make sure to run DB migration at beginning of semester
    # update target db in database_vars.yaml it should be this semester
    # Term code must be set in backend under the 'current_enrollement' table def.
    # semester must be set in 'current_student_courses' table def
    dbase_functions.add_courses_to_course_table(semester)
    dbase_functions.update_course_enrollement()



## Make sure these are set correctly
import_student_enrollement('2215')
import_all_courses('2215')
add_items_to_tables('su21')