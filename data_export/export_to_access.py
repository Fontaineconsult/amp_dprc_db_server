import amp_dprc_dbase.dbase_functions as dbase_functions
import xlwt

all_courses = dbase_functions.get_all_courses("sp19")

print(all_courses)

all_rows = []

class CourseRow:

    def __init__(self, student_id,
                 student_first_name,
                 student_last_name,
                 student_email,
                 course,
                 section,
                 status,
                 instructor_first_name,
                 instructor_last_name,
                 instructor_id,
                 instructor_phone,
                 instructor_email,
                 course_gen_key):

        self.student_id = {'col': 0, 'value': student_id, 'column_name': "Student_ID"}
        self.student_first_name = {'col': 1, 'value': student_first_name, 'column_name': "Student_First_Name"}
        self.student_last_name = {'col': 2, 'value': student_last_name, 'column_name': "Student_Last_Name"}
        self.student_email = {'col': 3, 'value': student_email, 'column_name': "Student_Email"}
        self.course = {'col': 4, 'value': course,  'column_name': "Course"}
        self.section = {'col': 5, 'value': section, 'column_name': "Section"}
        self.status = {'col': 6, 'value': "Enrolled" if status is True else "Dropped", 'column_name': "Status"}
        self.instructor_first_name = {'col': 7, 'value': instructor_first_name, 'column_name': "Instructor_First_Name"}
        self.instructor_last_name = {'col': 8, 'value': instructor_last_name, 'column_name': "Instructor_Last_Name"}
        self.instructor_id = {'col': 9, 'value': instructor_id,  'column_name': "Instructor_ID"}
        self.instructor_phone = {'col': 10, 'value': instructor_phone, 'column_name': "Instructor_Phone"}
        self.instructor_email = {'col': 11, 'value': instructor_email, 'column_name': "Instructor_Email"}
        self.course_gen_key = {'col': 12, 'value': course_gen_key, 'column_name': "Course_Gen_key"}

def build_course_rows():

    for course in all_courses:

        for enrolled in course.students_enrolled:

            all_rows.append(CourseRow(enrolled.student.student_id,
                                       enrolled.student.student_first_name,
                                       enrolled.student.student_last_name,
                                       enrolled.student.student_email,
                                       course.course_name,
                                       course.course_section,
                                       enrolled.student_enrolled,
                                       course.course_instructor.instructor_first_name,
                                       course.course_instructor.instructor_last_name,
                                       course.course_instructor.instructor_id,
                                       course.course_instructor.instructor_phone,
                                       course.course_instructor.instructor_email,
                                       course.course_gen_id))

        print(all_rows)


def make_excel_document():

    current_row = 0

    wb = xlwt.Workbook()
    ws = wb.add_sheet("Current_Enrollment")

    for attr, value in all_rows[0].__dict__.items():
        ws.write(current_row, value['col'], value['column_name'])
    current_row += 1

    for course_class in all_rows:

        for attr, value in course_class.__dict__.items():
            print(attr, value)
            ws.write(current_row, value['col'], value['value'])
        current_row += 1


    wb.save("courses.xls")




build_course_rows()
make_excel_document()