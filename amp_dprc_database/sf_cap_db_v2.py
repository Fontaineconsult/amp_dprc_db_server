from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text, Table, Time, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import sqlalchemy.exc
from sqlalchemy.schema import CreateSchema
Base = declarative_base()
import traceback
import yaml, os




def load_config():
    __path__ = os.path.join(os.path.dirname(__file__), "database_vars.yaml").replace('/','//')
    with open(__path__, 'r') as config:
        try:
            return yaml.load(config)
        except:
            print("Error Loading Config File")
            return None


class PermissionType(Base):

    __tablename__ ='permission_type'

    user_id = Column(String, primary_key=True)
    permission_type = Column(String)



class CourseIlearnID(Base):

    __tablename__ = 'course_ilearn_id'

    id = Column(Integer, primary_key=True)
    course_gen_id = Column(String)
    ilearn_page_id = Column(String)


class Enrollment(Base):

    __tablename__ = 'enrollment'

    course_id = Column(String, ForeignKey("course.course_gen_id"), primary_key=True)
    student_id = Column(String, ForeignKey("student.student_id"), primary_key=True)
    student_enrolled = Column(Boolean)
    last_updated = Column(DateTime, default=datetime.utcnow())
    student_requests_captioning = Column(Boolean, default=False)
    student = relationship("Student")
    course = relationship("Course")
    accomm_added_date = Column(DateTime)


class Employee(Base):

    __tablename__ = 'employee'

    employee_id = Column(String, primary_key=True)
    employee_first_name = Column(String)
    employee_last_name = Column(String)
    employee_email = Column(String)
    employee_phone = Column(String)
    permission_type = Column(String)
    courses_instructing = relationship('Course', backref='employee')
    related_organizations = relationship('CampusOrganizationAssignment')

class CampusOrganization(Base):

    __tablename__ = 'campus_organization'
    id = Column(Integer, primary_key=True)
    organization_name = Column(String, unique=True)
    organization_location = Column(String)
    organization_contact = Column(String)
    comments = Column(String)


class CampusOrganizationAssignment(Base):

    __tablename__ = 'campus_association_assignment'
    id = Column(Integer, primary_key=True)
    campus_org_id = Column(Integer, ForeignKey('campus_organization.id'))
    campus_org = relationship(CampusOrganization)
    employee_id = Column(String, ForeignKey('employee.employee_id'))
    employee = relationship(Employee)


class Course(Base):

    __tablename__ = 'course'


    course_gen_id = Column(String,  primary_key=True)
    course_name = Column(String)
    course_title = Column(String)
    course_section = Column(String)
    course_location = Column(String) # location is reserved word
    employee_id = Column(String, ForeignKey('employee.employee_id'))  ##! Rename to employee_id
    course_instructor = relationship(Employee)
    students_enrolled = relationship(Enrollment,
                                     back_populates="course") # needs a linking table many to many relationship
    semester = Column(String)
    course_online = Column(Boolean)
    no_students_enrolled = Column(Boolean)
    contact_email_sent = Column(Boolean)
    contact_email_sent_date = Column(DateTime)
    student_requests_captions_email_sent = Column(Boolean)
    student_requests_captions_email_sent_date = Column(DateTime)
    no_student_enrolled_email_sent = Column(Boolean)
    course_comments = Column(String)
    activate_ilearn_video_notification_sent = Column(String)
    ilearn_page_id = relationship(CourseIlearnID,
                                  foreign_keys=[course_gen_id],
                                  primaryjoin='CourseIlearnID.course_gen_id == Course.course_gen_id',
                                  lazy='joined')
    import_date = Column(DateTime, default=datetime.utcnow)
    course_regestration_number = Column(String)
    instructor_requests_captioning = Column(Boolean)



class CaptioningRequester(Base):

    __tablename__ = 'captioning_requester'
    # This is the in point to the application
    id = Column(Integer,  primary_key=True)
    campus_association_id = Column(Integer, ForeignKey('campus_association_assignment.id'), unique=True)
    campus_association = relationship(CampusOrganizationAssignment)
    course_id = Column(String, ForeignKey('course.course_gen_id'), unique=True)
    course = relationship(Course)


class Student(Base):

    __tablename__ = 'student'

    student_id = Column(String, primary_key=True)
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
    id = Column(Integer,  primary_key=True)
    media_type = Column(String)
    title = Column(String)
    length = Column(String)
    source_url = Column(String, unique=True)
    captioned_url = Column(String)
    at_catalog_number = Column(String)
    comments = Column(String)
    date_added = Column(DateTime, default=datetime.utcnow)


class CaptioningJob(Base):

    __tablename__ = "captioning_job"
    id = Column(Integer,  primary_key=True)
    requester_id = Column(Integer, ForeignKey("captioning_requester.id"))
    requester = relationship(CaptioningRequester)
    request_date = Column(DateTime, default=datetime.utcnow)
    show_date = Column(DateTime, default=None)
    delivered_date = Column(DateTime, default=None)
    media_id = Column(Integer, ForeignKey("captioning_media.id"))
    media = relationship(CaptioningMedia)
    output_format = Column(String)
    comments = Column(String)
    delivery_location = Column(String)
    transcripts_only = Column(String)
    job_status = Column(String)
    captioning_provider = Column(String)
    priority = Column(Boolean, default=False)
    rush_service_used = Column(Boolean, default=False)
    request_method = Column(String) # by scanner or by form
    ast_job_id = Column(Integer, ForeignKey('automatic_sync_job.id'), default=None)


class ScrapediLearnVideos(Base):

    __tablename__= 'scraped_ilearn_videos'

    id = Column(Integer, primary_key=True)
    resource_type = Column(String)
    resource_link = Column(String)
    title = Column(String)
    scan_date = Column(DateTime, default=datetime.utcnow)
    video_length = Column(Time) ##! Change to time
    captioned = Column(Boolean)
    captioned_version_id = Column(String)
    indicated_due_date = Column(DateTime)
    submitted_for_processing = Column(Boolean)
    submitted_for_processing_date = Column(DateTime)
    course_ilearn_id = Column(String)
    course_gen_id = Column(String, ForeignKey("course.course_gen_id"))
    course = relationship(Course)
    semester = Column(String)
    page_section = Column(String)
    captioned_version = relationship(CaptioningMedia, foreign_keys=[resource_link],
                                     lazy='joined',
                                     primaryjoin='CaptioningMedia.source_url == ScrapediLearnVideos.resource_link')


class DroppedCoursesDiffView(Base):

    __tablename__ = 'dropped_courses_diff'

    course_id = Column(String, primary_key=True)
    student_id = Column(String, primary_key=True)
    student_enrolled = Column(Boolean)


class AstJob(Base):

    __tablename__ = "automatic_sync_job"
    id = Column(Integer, primary_key=True)
    captioning_status = Column(String)
    ast_id = Column(String)


class AstStatus(Base):

    __tablename__ = "automatic_sync_job_status"

    id = Column(Integer, primary_key=True)
    added_date = Column(DateTime)
    ast_id = Column(String)
    ast_type = Column(String)
    ast_result = Column(String)
    ast_status = Column(String)


class AstResult(Base):

    __tablename__ = "automatic_sync_job_result"
    # not sure what to do with this yet
    id = Column(Integer, primary_key=True)



class myDPRCStudentEnrollemet(Base):

    __tablename__ = 'studentenrollement'

    id = Column(Integer, primary_key=True)
    student_id = Column(String)
    course_reg_number = Column(String)


class myDPRCRawCourseList(Base):

    __tablename__ = 'rawcourselist'

    id = Column(Integer, primary_key=True)
    course_regestration_number = Column(String)
    term_code = Column(String)
    subject_code = Column(String)
    course_number = Column(String)
    section_number = Column(String)
    class_title = Column(String)
    instructor_name = Column(String)
    instructor_email = Column(String)
    instructor_id = Column(String)


class CaptionStudentCoursesView(Base):

    __tablename__ = "current_student_courses"

    student_id = Column(String, primary_key=True)
    student_first_name = Column(String)
    student_last_name = Column(String)
    student_email = Column(String)
    student_requests = Column(String)
    captioning_active = Column(Boolean)
    transcripts_only = Column(Boolean)
    subject_code = Column(String)
    course_number = Column(String)
    section_number = Column(String)
    class_title = Column(String)
    instructor_id = Column(String)
    instructor_name = Column(String)
    instructor_email = Column(String)
    course_gen_key = Column(String, primary_key=True)
    course_reg_number = Column(String)


def get_dbase_session():
    config = load_config()
    database = "postgresql://{}:{}@{}/{}".format(config['username'],
                                             config['password'],
                                             config['server'],
                                             config['config'])

    try:
        engine = create_engine(database,
                               connect_args={'options': '-csearch_path={}'.format("main_1")},
                               client_encoding='utf8')
        Base.metadata.create_all(engine)

        DBsession = sessionmaker(bind=engine)
        session = DBsession()
        print("Database Connected")
        return session
    except:
        print(traceback.print_exc())
        pass

if __name__ == '__main__':

    config = load_config()
    database = "postgresql://{}:{}@{}/{}".format(config['username'],
                                                 config['password'],
                                                 config['server'],
                                                 config['database'])

    try:

        engine = create_engine(database,
                               connect_args={'options': '-csearch_path={}'.format("main_1"), 'sslmode': 'verify-ca',
                                             'connect_timeout': 3, "sslrootcert": "C:\\Users\\913678186\\Box\\Servers\\amp_dprc_db_server\\ssl\\root.crt",
                                             "sslkey": "C:\\Users\\913678186\\Box\\Servers\\amp_dprc_db_server\\ssl\\postgresql\\postgresql.key",
                                             "sslcert": "C:\\Users\\913678186\\Box\\Servers\\amp_dprc_db_server\\ssl\\postgresql\\postgresql.crt"
                                             },
                               client_encoding='utf8')
        engine.execute(CreateSchema("main_1"))
        Base.metadata.create_all(engine)
        print("Built Db")
    except:
        pass

