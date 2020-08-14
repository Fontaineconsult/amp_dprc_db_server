import csv
import amp_dprc_database.dbase_functions as db


"""
myDPRC query must come from Manage Accommodations > List Accommodation Requests 
"""

video_accomm = "C:\\Users\\DanielPC\\Desktop\\Servers\\amp_dprc_db_server\\course_importer_myDPRC\\capcourses.csv"


course_ids = []

def create_course_gen_id(semester):


    with open(video_accomm) as ilearn_ids:
        csv_reader = csv.reader(ilearn_ids)

        for row in csv_reader:
            print(row)



            course_area = row[7]
            course_number = row[8]
            course_section = row[9]

            if len(course_section) == 1:
                course_section = "0" + course_section


            fixed_course_name = "{}{}{}".format(course_area, course_number, course_section)
            course_gen_id = "{}{}".format(semester, str(fixed_course_name)
                                          .replace(" ","")
                                          .replace("-","")
                                          .replace("_","")
                                          .replace(":",""))

            course_ids.append((course_gen_id, row[2], row[15]))




create_course_gen_id("fa20")


db.clear_video_accomm_status()


print(course_ids)
for course in course_ids:
    print(course)
    db.update_video_accomm(course[0], course[1], course[2])