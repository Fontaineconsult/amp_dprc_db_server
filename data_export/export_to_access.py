import amp_dprc_dbase.dbase_functions as dbase_functions
import xlwt

all_courses = dbase_functions.get_all_courses("sp19")

print(all_courses)



for each in all_courses:
    print(each.students_enrolled, each.course_gen_id)
    for enrolled in each.students_enrolled:
        print(each.course_gen_id, enrolled.student_enrolled, enrolled.student.student_id, each.ilearn_page_id.ilearn_page_id)





def make_excel_document():

    current_row = 0

    wb = xlwt.Workbook()
    ws = wb.add_sheet("Current_Enrollment")

    for each in all_courses:
        print(each.students_enrolled)


        for enrolled in each.students_enrolled:
            print(enrolled.student_enrolled, enrolled.student.student_id)

    ws.write(0,0, "TESSTTT")


    wb.save("courses.xls")








#
# student_id
# student_name
# student_email
# descr = None
# course
# section
# status
# instructor_name
# instructor_id
# instructor_phone
# instructor_email
# facil_id
# mtg_start
# mtg_end
# meetings
# diagnosis
# description
# acad_plan
# descr = None
# birthdate = None
