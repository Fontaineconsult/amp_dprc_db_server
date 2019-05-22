import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")


from aws_server.aws_database import get_session, iLearn_Video, iLearn_Course
from amp_dprc_database.sf_cap_db import Course, get_dbase_session


aws_session = get_session()


def check_or_commit_course(ilearn_page_id, course_name, course_gen_id, semester, enrolled):

    course_check = aws_session.query(iLearn_Course).filter_by(course_gen_id=course_gen_id).first()

    if course_check:

        pass
    else:

        new_course = iLearn_Course(course_id=ilearn_page_id,
                                   course_name=course_name,
                                   course_gen_id=course_gen_id,
                                   semester=semester,
                                   no_students_enrolled=False)
        aws_session.add(new_course)
        aws_session.commit()


def commit_ilearn_video_content(title, link, course_id, caption_state, section):

    resource_check = aws_session.query(iLearn_Video).filter_by(resource_link=link).filter_by(course_id=course_id).first()

    if not resource_check:

        video_resource = iLearn_Video(resource_link=link,
                                      title=title,
                                      course_id=course_id,
                                      captioned=caption_state,
                                      page_section=section)

        aws_session.add(video_resource)
        aws_session.commit()

    else:
        print(resource_check.title, resource_check.captioned, title, caption_state)
        if resource_check.title is None:
            resource_check.title = title
        if resource_check.captioned is None or resource_check.captioned is False:
            resource_check.captioned = caption_state
        else:
            print("already exists")

        aws_session.commit()


def update_video_link_repo_course_enrollment(semester):

    enrollement_check = get_dbase_session().query(Course).filter_by(semester=semester).all()

    for each_course in enrollement_check:

        student_enrolled = []

        print(each_course.students_enrolled)
        for enrollement in each_course.students_enrolled:
            print(enrollement.student_id, enrollement.student_enrolled)
            student_enrolled.append(enrollement.student_enrolled)


            video_link_repo_course = aws_session.query(iLearn_Course).filter_by(course_gen_id = each_course.course_gen_id).first()

            if video_link_repo_course is not None:
                if True in student_enrolled:
                    video_link_repo_course.no_students_enrolled = False
                    aws_session.commit()
                else:

                    video_link_repo_course.no_students_enrolled = True
                    aws_session.commit()



update_video_link_repo_course_enrollment("sp19")