import xlrd


class Course:

    def __init__(self, raw_course, semester):
        ##! Needs a check to warn if column order changes in the excel sheets
        self.course_name = raw_course[3]
        self.course_code = raw_course[4]
        self.course_section = raw_course[5]
        self.location = raw_course[11]
        self.student_enrolled_status = raw_course[6]
        self.student_enrolled = True if self.student_enrolled_status == "Enrolled" else False
        self.instructor_name = raw_course[7]
        self.instructor_id = raw_course[8]
        self.instructor_email = raw_course[10]
        self.instructor_phone = raw_course[9]
        self.course_gen_id = "{}{}{}".format(semester, self.course_code.replace(" ","")
                                             .replace("-","")
                                             .replace("_","")
                                             .replace(":",""),
                                             self.course_section)
        self.course_online = True if self.location == "ONLINE" else False
        self.semester = semester


class Student:

    def __init__(self, raw_courses, semester):

        self.raw_course_list = raw_courses
        self.semester = semester
        self.student_id = self.raw_course_list[0][0]
        self.student_name = self.raw_course_list[0][1]
        self.student_email = self.raw_course_list[0][2]
        self.disability = self.raw_course_list[0][15]
        self.courses = []
        self.build_courses()


    def build_courses(self):
        for each in self.raw_course_list:
            self.courses.append(Course(each, self.semester))


class CourseList:

    def __init__(self, xlsfile, semester):

        self.xlsfile = xlrd.open_workbook(xlsfile).sheet_by_index(0)
        self.headers = []
        self.semester = semester
        self.row_length = self.xlsfile.nrows
        self.rows = list(self.xlsfile.row_values(5))
        self.student_course_list = []
        self.build_headers()
        self.build_students()


    def build_headers(self):
        header_row = self.xlsfile.row(2)

        for each in header_row:
            self.headers.append(each.value)


    def build_students(self):

        temp_rows = []
        current_row_id = None

        for row_num in range(self.row_length):

            row = self.xlsfile.row_values(row_num)
            if row_num > 2:
                if current_row_id is None:
                    current_row_id = row[0]
                else:
                    if current_row_id == row[0]:

                        temp_rows.append(row)

                    elif current_row_id != row[0]:

                        self.student_course_list.append(Student(list(temp_rows), self.semester))

                        temp_rows.clear()

                        current_row_id = row[0]
                        temp_rows.append(row)

                    elif row_num == self.row_length:
                        temp_rows.append(row)

                        self.student_course_list.append(Student(list(temp_rows), self.semester))

