import csv
import itertools
from amp_dprc_database.dbase_functions import add_student
students = r"C:\Users\DanielPC\Desktop\Servers\amp_dprc_db_server\course_importer_myDPRC\students.csv"

with open(students) as course_enrollement:

    csv_reader = csv.reader(course_enrollement)
    csv_reader = itertools.islice(csv_reader, 1, None)
    for row in csv_reader:

        student_id = row[3]
        student_first_name = row[1]
        student_last_name = row[0]
        student_email = row[6]
        captioning_active = True
        transcripts_only = False

        if student_id != "":
            add_student(student_id, student_first_name, student_last_name, student_email, captioning_active, transcripts_only)