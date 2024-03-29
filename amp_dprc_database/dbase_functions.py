import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")

from amp_dprc_database.sf_cap_db_v2 import get_dbase_session,\
    Student, Employee, Course, Enrollment,\
    CourseIlearnID, myDPRCStudentEnrollemet, myDPRCRawCourseList,\
    CaptionStudentCoursesView, DroppedCoursesDiffView,\
    ScrapediLearnVideos, CourseIlearnTable
import sqlalchemy.orm.exc as db_error
import sqlalchemy.exc as core_db_error
import datetime, traceback


session = get_dbase_session()



def add_student(student_id, student_first_name, student_last_name, student_email, captioning_active, transcripts_only):
    try:
        session.query(Student).filter(Student.student_id==student_id).one()
        print("already found student")
    except db_error.NoResultFound:
        new_student = Student(student_id=student_id,
                                 student_first_name=student_first_name,
                                 student_last_name=student_last_name,
                                 student_email=student_email,
                                 captioning_active=captioning_active,
                                 transcripts_only=transcripts_only)

        try:
            session.add(new_student)
            print("Adding New Student ", student_id)
            session.commit()
        except:
            session.rollback()
            print("Something went wrong with the instructor")





def get_all_enrolled_courses():
    all_enrolled = []
    all_enrolled_query = session.query(Student).all()

    for each_student in all_enrolled_query:

        for each_course in each_student.courses_enrolled:
            if each_course.student_enrolled == True:
                all_enrolled.append(each_course)
    return all_enrolled


def get_all_courses(semester):
    all_courses = session.query(Course).filter_by(semester=semester).all()
    session.commit()
    return all_courses


def get_all_students_ids():
    query = session.query(Student).all()

    student_ids = []
    for each_student in query:
        student_ids.append(each_student.student_id)
    return student_ids


def check_or_commit_instructor(instructor_data):

    try:
        instructor_query = session.query(Employee).filter(Employee.employee_id==instructor_data["instructor_id"]).one()
        print("already found instructor")
    except db_error.NoResultFound:
        new_instructor = Employee(employee_id=instructor_data["instructor_id"],
                                        employee_first_name=instructor_data["instructor_first_name"],
                                        employee_last_name=instructor_data["instructor_last_name"],
                                        employee_email=instructor_data["instructor_email"],
                                        employee_phone=instructor_data["instructor_phone"])

        try:
            session.add(new_instructor)
            session.commit()
        except:
            session.rollback()
            print("Something went wrong with the instructor")


def check_or_commit_course(course_data):

    try:
        course_query = session.query(Course).filter(Course.course_gen_id==course_data["course_gen_id"]).one()
        print("already found course")

    except db_error.NoResultFound:
        new_course = Course(course_gen_id=course_data["course_gen_id"],
                            course_name=course_data["course_name"],
                            course_section=course_data["course_section"],
                            employee_id=course_data["course_instructor_id"],
                            semester=course_data["semester"],
                            course_online=course_data["course_online"],
                            import_date=datetime.datetime.utcnow()
                            )

        try:
            session.add(new_course)
            session.commit()
            print("saving course")
        except:
            session.rollback()
            print("Something went wrong with the course", traceback.print_exc())

def check_or_update_enrollement(student_id, course_gen_id, enrolled_status):

    try:
        # print(type(course_gen_id), type(student_id))
        #
        # course_check = session.query(Course).filter_by(course_gen_id=course_gen_id).one()
        #
        # student_check = session.query(Student).filter_by(student_id=student_id).one()
        #
        #course_id = course_check.id

        try:

            enrollement_check = session.query(Enrollment).filter_by(student_id=student_id,course_id=course_gen_id).one()
            enrollement_check.student_enrolled = enrolled_status
            session.commit()

        except db_error.NoResultFound:

            enrollement_commit = Enrollment(course_id=course_gen_id,
                                             student_id=student_id,
                                             student_enrolled=enrolled_status)
            session.add(enrollement_commit)
            session.commit()



    except db_error.NoResultFound:

        print(traceback.print_exc(),"course or student doesn't exist")
        pass


def commit_ilearn_id(course_id_pair):

    for each_pair in course_id_pair:
        print(each_pair)

        try:
            session.query(CourseIlearnTable).filter_by(course_gen_id=each_pair[1]).one()
            print("Already there ", each_pair[0])
        except db_error.NoResultFound:

            course_ilearn_id_commit = CourseIlearnTable(ilearn_page_id=each_pair[0], course_gen_id=each_pair[1])
            session.add(course_ilearn_id_commit)
            print("adding new id", each_pair[0], each_pair[1])



    session.commit()





def get_all_course_ilearn_ids(semester):
    missing_ids = 0
    ilearn_id_query = session.query(Course).filter(Course.semester==semester).all()
    ilearn_ids = []
    for each in ilearn_id_query:

        try:
            print(each.course_gen_id)
            print(each.course_gen_id, each.ilearn_page_id.ilearn_page_id, len(each.students_enrolled))
            if each.ilearn_page_id is not None:
                ilearn_ids.append((each.course_gen_id, each.ilearn_page_id.ilearn_page_id, len(each.students_enrolled)))
            else:
                continue
        except AttributeError:
            missing_ids += 1
            pass
    print(missing_ids)
    return ilearn_ids


def clear_myDPRC_enroll_data():

    try:
        session.execute('TRUNCATE TABLE studentenrollement RESTART IDENTITY;')

    except:
        session.rollback()
        print("Delete OP Failed")


def clear_myDPRC_course_data():

    try:
        session.execute('TRUNCATE TABLE rawcourselist RESTART IDENTITY;')

    except:
        session.rollback()
        print("Delete OP Failed")


def commit_myDPRC_student_enrollement(student_id, course_id):


    myDPRC_enrollement = myDPRCStudentEnrollemet(student_id=student_id, course_reg_number=course_id)
    session.add(myDPRC_enrollement)
    session.commit()


def commit_myDPRC_course_data(course_regestration_number,
                              term_code,
                              subject_code,
                              course_number,
                              section_number,
                              class_title,
                              instructor_name,
                              instructor_email,
                              instructor_id):



    course = myDPRCRawCourseList(course_regestration_number=course_regestration_number,
                                 term_code=term_code,
                                 subject_code=subject_code,
                                 course_number=course_number,
                                 section_number=section_number,
                                 class_title=class_title,
                                 instructor_name=instructor_name,
                                 instructor_email=instructor_email,
                                 instructor_id=instructor_id)



    session.add(course)
    print("committing", class_title)
    session.commit()


def refresh_instructor_table():
    query = session.query(CaptionStudentCoursesView).all()
    for each in query:
            if len(each.instructor_id) == 9:
                try:
                    check_if_instructor_exists = session.query(Employee).filter(Employee.employee_id==each.instructor_id).one()

                except db_error.NoResultFound:

                    new_instructor = Employee(employee_id=each.instructor_id,
                                              employee_first_name=each.instructor_name.split(" ", 1)[0],
                                              employee_last_name=each.instructor_name.split(" ", 1)[1],
                                              employee_email=each.instructor_email,
                                              employee_phone=""
                                                )
                    session.add(new_instructor)
                    session.commit()
            else:
                continue


def add_courses_to_course_table(semester):

    query = session.query(CaptionStudentCoursesView).all()
    print(query)
    for each in query:
        print(each.course_gen_key)
        if len(each.instructor_id) == 9:


            check_if_course_exists = session.query(Course.course_gen_id).filter(Course.course_gen_id == each.course_gen_key).scalar()
            if not check_if_course_exists:
                print("course doesn't exist, adding")
                new_course = Course(course_gen_id=each.course_gen_key,
                                    course_name="{}{}{}".format(each.subject_code, " ", each.course_number),
                                    course_section=each.section_number,
                                    employee_id=each.instructor_id,
                                    semester=semester,
                                    import_date=datetime.datetime.utcnow(),
                                    course_regestration_number=each.course_reg_number)
                session.add(new_course)
                session.commit()
        else:
            continue


def update_course_enrollement():
    courses_to_add = []
    enrolled_ids = []
    current_course_ids_view = []


    current_enrollement = session.query(Enrollment).all()
    current_students_view = session.query(CaptionStudentCoursesView).all()
    print("CURRENT STUDENTS VIEW LENGTH", len(current_students_view))

    def add_new_course_to_enrollement():

        for each in current_enrollement:
            student_id = each.student_id.rstrip()
            print(student_id)

            enrolled_ids.append(( each.course_id, student_id))

        for each in current_students_view:
            student_id = each.student_id.rstrip()
            current_course_ids_view.append((each.course_gen_key, student_id))


    def compare_lists():
        global courses_to_add
        courses_to_add = [i[0] for i in enrolled_ids + current_course_ids_view if i[0] not in enrolled_ids]
        print("COURSES to ADD", courses_to_add)


    def find_course_to_add_to_enroll():
        courses_checked = 0
        print("TOTAL COURSES TO AMTCH", len(current_course_ids_view))
        for each in current_course_ids_view:
            student_id = each[1].rstrip()
            course = (each[0], student_id)

            print("checking course in enroll", course)
            try:

                courses_checked += 1
                session.query(Enrollment).filter_by(course_id=each[0], student_id=student_id).one()
                print("COURSE WAS FOUND", each[0])

            except db_error.NoResultFound:
                print("Course Will be added to enroll", each[0])
                commit_course_to_enroll(course)

        print(courses_checked)

    def commit_course_to_enroll(course):

        try:


            new_enrollement = Enrollment(course_id=course[0],
                                         student_id=course[1],
                                         last_updated=datetime.datetime.utcnow(),
                                         student_enrolled=True)
            session.add(new_enrollement)
            session.commit()
            print("ADDING TO ENROLLMENT",  course[0], course[1])

        except core_db_error.IntegrityError:
            print(traceback.print_exc())
            print("Course/Student Already Exists in enrolled table, IntegrityError", course[0], )
            session.rollback()
        except db_error.FlushError:
            print("Course/Student Already Exists in enrolled table, FlushError")
            session.rollback()

    def drop_enrollment_from_diff_table():
        courses_to_drop = session.query(DroppedCoursesDiffView).all()

        for each_course in courses_to_drop:
            student_id = each_course.student_id
            try:
                drop_check = session.query(Enrollment).filter_by(course_id=each_course.course_id, student_id=student_id).one()
                drop_check.student_enrolled = False
                print("Dropped course", each_course.course_id)
                session.commit()
            except db_error.NoResultFound:
                print("No course to drop for", each_course.course_id)

    # def check_for_drops():
    #     courses_to_drop = []
    #
    #     for each in enrolled_ids:
    #         try:
    #             try:
    #                 enrollement_check = session.query(CaptionStudentCoursesView).filter_by(course_gen_key=each[0]).filter_by(student_id=each[1]).one()
    #
    #             except db_error.MultipleResultsFound:
    #                 pass
    #
    #         except db_error.NoResultFound:
    #
    #             to_be_dropped = session.query(Enrollment).filter_by(course_id=each[0]).filter_by(student_id=each[1]).one()
    #
    #             to_be_dropped.student_enrolled = False
    #             to_be_dropped.last_updated = datetime.datetime.utcnow()
    #             session.commit()
    #
    #
    #             courses_to_drop.append(to_be_dropped.course_id)
    #
    #
    #     print("ENROLLED_IDS", enrolled_ids)
    #     print("CURRENT ENROLLEMENT", current_course_ids_view)
    #     print("COURSES TO ADD", courses_to_add)
    #     print("COURSES THAT WERE DROPPPED", len(courses_to_drop), courses_to_drop)


    add_new_course_to_enrollement()
    compare_lists()
    find_course_to_add_to_enroll()
    drop_enrollment_from_diff_table()


def add_scraped_videos(title, link, course_id, caption_state, course_gen_id, section, semester, scraped_content_hidden):

    scraped_video_check = session.query(ScrapediLearnVideos).filter_by(resource_link=link).filter_by(course_gen_id=course_gen_id).first()

    if not scraped_video_check:
        print("VIDEO DOESNT EXIST")
        video_resource = ScrapediLearnVideos(resource_link=link,
                                             title=title,
                                             course_ilearn_id=course_id,
                                             course_gen_id=course_gen_id,
                                             page_section=section,
                                             semester=semester,
                                             content_hidden=scraped_content_hidden)

        session.add(video_resource)
        session.commit()

    else:
        print(scraped_video_check.title, scraped_video_check.captioned, title, caption_state)
        if scraped_video_check.title is None:
            scraped_video_check.title = title
        # if scraped_video_check.captioned is None or scraped_video_check.captioned is False:
        #     scraped_video_check.captioned = caption_state
        else:
            print("already exists")

        if scraped_video_check.page_section is None:
            scraped_video_check.page_section = section

        if scraped_video_check.content_hidden != scraped_content_hidden:
            scraped_video_check.content_hidden = scraped_content_hidden

        session.commit()


def add_ilearn_course_name(ilearn_course_name, course_gen_id):

    course = session.query(Course).filter_by(course_gen_id=course_gen_id).first()

    if course:

        course.course_title = ilearn_course_name
        session.commit()





def clear_video_accomm_status():

    video_accomm = session.query(Enrollment).all()

    for each in video_accomm:
        each.student_requests_captioning = False

    session.commit()



def update_video_accomm(course_id, student_id, accomm_added_date):



    try:
        video_accomm = session.query(Enrollment).filter_by(course_id=course_id, student_id=student_id).all()

        if len(video_accomm) == 0:
            print("No Course Found for", course_id)

        else:

            for enrollment in video_accomm:
                enrollment.student_requests_captioning = True
                enrollment.accomm_added_date = accomm_added_date


                session.commit()

    except db_error.NoResultFound:

        print("No Course Found", course_id)


