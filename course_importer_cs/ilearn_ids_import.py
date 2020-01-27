import csv
import amp_dprc_database.dbase_functions as db

csv_link = "C:\\Users\\913678186\\Box\\Servers\\amp_dprc_db_server\\course_importer_cs\\courses.csv"

def add_ilearn_course_ids(semester):

    course_id_list = []

    with open(csv_link) as ilearn_ids:
        csv_reader = csv.reader(ilearn_ids, delimiter=',')
        for row in csv_reader:
            ilearn_id = str(row[0])
            try:


                course_area = row[1].split()[0]
                course_number = row[1].split()[1][1:]
                fixed_course_name = "{}{}".format(course_area, course_number)



                course_gen_id = "{}{}".format(semester, str(fixed_course_name)
                                              .replace(" ","")
                                              .replace("-","")
                                              .replace("_","")
                                              .replace(":",""))

                print(course_gen_id)

                course_id_list.append((ilearn_id, course_gen_id))



            except:
                pass

    print(course_id_list)
    db.commit_ilearn_id(course_id_list)



add_ilearn_course_ids("sp20")