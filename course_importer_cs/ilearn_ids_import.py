import csv
import amp_dprc_dbase.dbase_functions as db

csv_link = "C:\\Users\\913678186\\Box\\SF State Python Projects\\DPRC AMP\\course_importer_cs\\courseids.csv"

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


    db.commit_ilearn_id(course_id_list)



add_ilearn_course_ids("sp19")