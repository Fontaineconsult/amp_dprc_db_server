from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Enrollment(Base):

    __tablename__ = 'enrollment'

    course_id = Column(String, ForeignKey("course.course_gen_id"), primary_key=True)
    student_id = Column(String, ForeignKey("student.student_id"), primary_key=True)
    student_enrolled = Column(Boolean)
    student = relationship("Student")
    course = relationship("Course")


class CourseIlearnID(Base):

    __tablename__ = 'course_ilearn_id'

    id = Column(Integer, primary_key=True)
    course_gen_id = Column(String)
    ilearn_page_id = Column(String)


class Instructor(Base):

    __tablename__ = 'instructor'
    id = Column(Integer, primary_key=True)
    instructor_id = Column(String, unique=True)
    instructor_first_name = Column(String)
    instructor_last_name = Column(String)
    instructor_email = Column(String)
    instructor_phone = Column(String)
    courses_instructing = relationship('Course', backref='instructor')



class Course(Base):

    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    course_gen_id = Column(String, unique=True)
    course_name = Column(String)
    course_section = Column(String)
    course_location = Column(String) # location is reserved word
    course_instructor_id = Column(String, ForeignKey('instructor.instructor_id'))
    course_instructor = relationship(Instructor)
    students_enrolled = relationship(Enrollment,
                                     back_populates="course") # needs a linking table many to many relationship
    semester = Column(String)
    course_online = Column(Boolean)
    no_students_enrolled = Column(Boolean)
    contact_email_sent = Column(Boolean)
    no_student_enrolled_email_sent = Column(Boolean)
    course_comments = Column(String)
    activate_ilearn_video_notification_sent = Column(String)
    ilearn_page_id = relationship(CourseIlearnID,
                                  foreign_keys=[course_gen_id],
                                  primaryjoin='CourseIlearnID.course_gen_id == Course.course_gen_id')
    import_date = Column(DateTime)


class Student(Base):

    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True)
    student_first_name = Column(String)
    student_last_name = Column(String)
    student_email = Column(String)
    student_requests = Column(String)
    captioning_active = Column(Boolean)
    transcripts_only = Column(Boolean)
    courses_enrolled = relationship(Enrollment,
                           back_populates="student")


class CaptioningMedia(Base):

    __tablename__ = "captioning_media"
    id = Column(Integer, primary_key=True)
    media_type = Column(String)
    title = Column(String)
    length = Column(String)
    source_url = Column(String)
    captioned_url = Column(String)
    at_catalog_number = Column(String)
    comments = Column(String)
    date_added = Column(String)


class CourseCaptioningJob(Base):

    __tablename__ = "course_captioning_job"
    id = Column(Integer, primary_key=True)
    course_id = Column(String, ForeignKey("course.course_gen_id"))
    course = relationship(Course)
    request_date = Column(DateTime)
    show_date = Column(DateTime)
    delivered_date = Column(DateTime)
    media_id = Column(Integer, ForeignKey("captioning_media.id"))
    media = relationship(CaptioningMedia)
    output_format = Column(String)
    comments = Column(String)
    delivery_location = Column(String)
    transcripts_only = Column(String)
    job_status = Column(String)
    captioning_provider = Column(String)
    priority = Column(Boolean)
    rush_service_used = Column(Boolean)
    request_method = Column(String) # by scanner or by form
    ast_job_id = Column(Integer, ForeignKey('automatic_sync_job.id'))


class IndividualCaptioningJob(Base):

    __tablename__ = "individual_captioning_job"
    id = Column(Integer, primary_key=True)
    request_date = Column(DateTime)
    show_date = Column(DateTime)
    delivered_date = Column(DateTime)
    media_id = Column(Integer, ForeignKey("captioning_media.id"))
    media = relationship(CaptioningMedia)
    output_format = Column(String)
    comments = Column(String)
    delivery_location = Column(String)
    transcripts_only = Column(String)
    job_status = Column(String)
    captioning_provider = Column(String)
    priority = Column(Boolean)
    rush_service_used = Column(Boolean)
    instructor_id = Column(String, ForeignKey('instructor.instructor_id'))
    instructor = relationship(Instructor)
    ast_job_id = Column(Integer, ForeignKey('automatic_sync_job.id'))


class AstJob(Base):

    __tablename__ = "automatic_sync_job"
    id = Column(Integer, primary_key=True)
    captioning_status = Column(String)





def get_dbase_session():

    engine = create_engine("postgresql://daniel:accessiblevids@localhost/captioning")
    Base.metadata.create_all(engine)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    return session


if __name__ == '__main__':

    engine = create_engine("postgresql://daniel:accessiblevids@localhost/captioning")
    Base.metadata.create_all(engine)