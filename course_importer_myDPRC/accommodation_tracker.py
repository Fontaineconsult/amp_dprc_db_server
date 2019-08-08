import csv
import amp_dprc_database.dbase_functions as db




video_accomm = "C:\\Users\\913678186\\Box\\Servers\\amp_dprc_db_server\\course_importer_myDPRC\\export (7).csv"

course_ids = []

def create_course_gen_id(semester):


    with open(video_accomm) as ilearn_ids:
        csv_reader = csv.reader(ilearn_ids, delimiter=',')
        for row in csv_reader:

            try:


                course_area = row[1]
                course_number = row[2]
                course_section = row[3]

                fixed_course_name = "{}{}{}".format(course_area, course_number, course_section)



                course_gen_id = "{}{}".format(semester, str(fixed_course_name)
                                              .replace(" ","")
                                              .replace("-","")
                                              .replace("_","")
                                              .replace(":",""))


                course_ids.append(course_gen_id)








            except:
                pass



create_course_gen_id("fa19")


for course_id in course_ids:
    print(course_id)
    db.update_video_accomm(course_id)