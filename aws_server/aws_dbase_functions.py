import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")


from aws_server.aws_database import get_session, iLearn_Video, iLearn_Course


session = get_session()


def check_or_commit_course(ilearn_page_id, course_name, course_gen_id, semester):

    course_check = session.query(iLearn_Course).filter_by(course_gen_id=course_gen_id).first()

    if course_check:
        pass
    else:

        new_course = iLearn_Course(course_id=ilearn_page_id,
                                   course_name=course_name,
                                   course_gen_id=course_gen_id,
                                   semester=semester)
        session.add(new_course)
        session.commit()


def commit_ilearn_video_content(title, link, course_id, caption_state):

    resource_check = session.query(iLearn_Video).filter_by(resource_link=link).filter_by(course_id=course_id).first()

    if not resource_check:

        video_resource = iLearn_Video(resource_link=link,
                                      title=title,
                                      course_id=course_id,
                                      captioned=caption_state)

        session.add(video_resource)
        session.commit()

    else:
        print(resource_check.title, resource_check.captioned, title, caption_state)
        if resource_check.title is None:
            resource_check.title = title
        if resource_check.captioned is None or resource_check.captioned is False:
            resource_check.captioned = caption_state
        else:
            print("already exists")

        session.commit()
