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

    __tablename__ = 'current_ilearn_ids'

    id = Column(Integer, primary_key=True)
    course_gen_id = Column(String)
    ilearn_page_id = Column(String)


class CourseIlearnTable(Base):

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
    student_requests_captioning = Column(Boolean)
    student = relationship("Student")
    course = relationship("Course")
    accomm_added_date = Column(DateTime)


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)


class Employee(Base):

    __tablename__ = 'employee'

    employee_id = Column(String, primary_key=True)
    employee_first_name = Column(String)
    employee_last_name = Column(String)
    employee_email = Column(String)
    employee_phone = Column(String)
    permission_type = Column(String, default='user')
    # courses_instructing = relationship('Course', backref='employee')
    # related_organizations = relationship('CampusOrganizationAssignment')

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
    course_instructor = relationship(Employee, lazy="joined", innerjoin=True)
    students_enrolled = relationship(Enrollment,
                                     lazy="joined", innerjoin=True,
                                     back_populates="course") # needs a linking table many to many relationship
    semester = Column(String)
    ilearn_video_service_requested = Column(Boolean, default=False)
    ilearn_video_service_requested_date = Column(DateTime)
    course_online = Column(Boolean, default=True)
    no_students_enrolled = Column(Boolean, default=False)
    contact_email_sent = Column(Boolean, default=False)
    no_student_enrolled_email_sent = Column(Boolean, default=False)
    course_comments = Column(String)
    activate_ilearn_video_notification_sent = Column(String)
    ilearn_page_id = relationship(CourseIlearnID,
                                  foreign_keys=[course_gen_id],
                                  primaryjoin='CourseIlearnID.course_gen_id == Course.course_gen_id',
                                  lazy='joined')
    import_date = Column(DateTime)
    course_regestration_number = Column(String)
    instructor_requests_captioning = Column(Boolean, default=False)
    contact_email_sent_date = Column(DateTime)
    student_requests_captions_email_sent = Column(Boolean, default=False)
    student_requests_captions_email_sent_date = Column(DateTime)
    ignore_course_ilearn_videos = Column(Boolean, default=False)




class CaptioningRequester(Base):

    __tablename__ = 'captioning_requester'
    # This is the in point to the application
    id = Column(Integer,  primary_key=True)
    campus_association_id = Column(Integer, ForeignKey('campus_association_assignment.id'), unique=True)
    campus_association = relationship(CampusOrganizationAssignment)
    course_id = Column(String, ForeignKey('course.course_gen_id'), unique=True)
    course = relationship(Course)


class CaptioningRequesterOptimizedView(Base):

    __tablename__ = 'captioning_requester_view'
    # This is the in point to the application
    id = Column(Integer,  primary_key=True)
    campus_association_id = Column(Integer, ForeignKey('campus_association_assignment.id'), unique=True)
    course_id = Column(String, ForeignKey('course.course_gen_id'), unique=True)
    employee_id = Column(String)
    org_employee_id = Column(String)
    campus_org_id = Column(Integer)
    semester = Column(String)



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


class S3FileStorage(Base):

    __tablename__ = "s3_file_storage"
    id = Column(Integer, primary_key=True)
    source_url = Column(String)
    key = Column(String)
    object_url = Column(String)
    object_uuid = Column(String)
    date_added = Column(DateTime, default=datetime.utcnow())
    file_name = Column(String)
    mime_type = Column(String)
    sha_256_hash = Column(String)


class S3CaptionStorage(Base):
    __tablename__ = "s3_caption_storage"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    object_url = Column(String)
    object_uuid = Column(String)
    date_added = Column(DateTime, default=datetime.utcnow())
    file_name = Column(String)
    mime_type = Column(String)


class CaptioningMedia(Base):

    __tablename__ = "captioning_media"
    id = Column(Integer,  primary_key=True)
    media_type = Column(String)
    title = Column(String)
    length = Column(String)
    source_url = Column(String, unique=True)
    captioned_url = Column(String)
    primary_caption_resource_id = Column(Integer)
    at_catalog_number = Column(String)
    comments = Column(String)
    sha_256_hash = Column(String)
    date_added = Column(DateTime, default=datetime.utcnow)
    media_objects = relationship("MediaObjectAssignments", back_populates="captioning_media")
    captioned_resources = relationship("CaptionedResources")

class MediaObjectAssignments(Base):

    __tablename__ = "media_object_assignments"
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("captioning_media.id"))
    captioning_media = relationship(CaptioningMedia, back_populates="media_objects")
    s3_file_key = Column(Integer, ForeignKey("s3_file_storage.id"))
    s3_caption_key = Column(Integer, ForeignKey("s3_caption_storage.id"))
    associated_files = relationship(S3FileStorage)
    associated_captions = relationship(S3CaptionStorage)


class CaptioningRequest(Base):

    __tablename__ = 'captioning_request'
    id = Column(Integer,  primary_key=True)
    requester_id = Column(Integer, ForeignKey('captioning_requester.id'))
    requester = relationship(CaptioningRequester)
    media_id = Column(Integer, ForeignKey('captioning_media.id'))
    media = relationship(CaptioningMedia)
    delivery_format = Column(String)
    employee_id = Column(String, ForeignKey('employee.employee_id'))


class AstStatus(Base):

    __tablename__ = "automatic_sync_job_status"

    id = Column(Integer, primary_key=True)
    added_date = Column(DateTime, default=datetime.utcnow)
    job_id = Column(Integer, ForeignKey("automatic_sync_job.id"))
    ast_id = Column(String)
    ast_type = Column(String)
    ast_result = Column(String)
    ast_status = Column(String)
    ast_error_detail = Column(String)


class AstJob(Base):

    __tablename__ = "automatic_sync_job"
    id = Column(Integer, primary_key=True)
    caption_job_id = Column(Integer, ForeignKey('captioning_job.id'))
    captioning_status = Column(String, default="initialized")
    added_date = Column(DateTime, default=datetime.utcnow)
    ast_status = relationship(AstStatus)
    ast_batch_id = Column(String)
    ast_description = Column(String)
    ast_basename = Column(String)
    ast_language = Column(String)
    ast_rush = Column(String)
    ast_have_trans = Column(Boolean, default=False)
    ast_notes = Column(String)
    ast_persistent_note = Column(Integer)
    ast_purchase_order = Column(Integer)
    ast_callback = Column(String)
    ast_status_url = Column(String)
    ast_id = Column(String)
    media_file_id = Column(Integer, ForeignKey('s3_file_storage.id'))
    media_file = relationship(S3FileStorage)


class CaptioningJob(Base):

    __tablename__ = "captioning_job"
    id = Column(Integer,  primary_key=True)
    requester_id = Column(Integer, ForeignKey("captioning_requester.id"), nullable=False)
    requester = relationship(CaptioningRequester, lazy="joined", innerjoin=True)
    semester = Column(String) # ISSUE FIX THIS
    job_request_id = Column(Integer, ForeignKey("captioning_request.id"))
    request_date = Column(DateTime, default=datetime.utcnow)
    show_date = Column(DateTime, default=None)
    delivered_date = Column(DateTime, default=None)
    media_id = Column(Integer, ForeignKey("captioning_media.id"), nullable=False)
    media = relationship(CaptioningMedia, lazy="joined", innerjoin=True)
    output_format = Column(String)
    comments = Column(String)
    delivery_location = Column(String)
    transcripts_only = Column(Boolean, default=False)
    job_status = Column(String, default='Queued')
    captioning_provider = Column(String)
    priority = Column(Boolean, default=False)
    rush_service_used = Column(Boolean, default=False)
    request_method = Column(String) # by scanner or by form
    ast_jobs = relationship(AstJob)
    deleted = Column(Boolean, default=False)



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
    ignore_video = Column(Boolean, default=False)
    invalid_link = Column(Boolean, default=False)
    captioned_version = relationship(CaptioningMedia, foreign_keys=[resource_link],
                                     lazy='joined',
                                     primaryjoin='CaptioningMedia.source_url == ScrapediLearnVideos.resource_link')
    content_hidden = Column(Boolean, default=False)

class DroppedCoursesDiffView(Base):

    __tablename__ = 'dropped_courses_diff'

    course_id = Column(String, primary_key=True)
    student_id = Column(String, primary_key=True)
    student_enrolled = Column(Boolean)



class AstResult(Base):

    __tablename__ = "automatic_sync_job_result"
    # not sure what to do with this yet
    id = Column(Integer, primary_key=True)


class AstAuth(Base):

    __tablename__ = "automatic_sync_auth"

    id = Column(Integer, primary_key=True)
    active_bearer_token = Column(String)
    set_date = Column(DateTime)


class myDPRCStudentEnrollemet(Base):

    __tablename__ = 'studentenrollement'

    id = Column(Integer, primary_key=True)
    student_id = Column(String)
    course_reg_number = Column(String)


class myDPRCRawCourseList(Base):

    __tablename__ = 'rawcourselist'

    id = Column(Integer, primary_key=True)
    course_regestration_number = Column(String)
    subject_code = Column(String)
    course_number = Column(String)
    section_number = Column(String)
    class_title = Column(String)
    instructor_name = Column(String)
    instructor_email = Column(String)
    instructor_id = Column(String)
    term_code = Column(String)


class AmaraResources(Base):

    __tablename__ = 'amara_resources'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    video_id = Column(String)
    captions_uploaded = Column(Boolean, default=False)
    captions_complete = Column(Boolean, default=False)

class CaptionedResources(Base):

    __tablename__ = 'captioned_resources'

    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("captioning_media.id"))
    amara_id = Column(Integer, ForeignKey("amara_resources.id"))
    amara_resource = relationship(AmaraResources)

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





def get_dbase_session(database_var="database"):
    config = load_config()
    database = "postgresql://{}:{}@{}/{}".format(config['username'],
                                             config['password'],
                                             config['server'],
                                             config['database'])

    dev_database = "postgresql://{}:{}@{}/{}".format(config['username'],
                                                     config['password'],
                                                     config['server'],
                                                     config['dev_database'])

    if database_var=="database":

        try:
            engine = create_engine(database,
                                   connect_args={'options': '-csearch_path={}'.format("main_1")},
                                   client_encoding='utf8')
            Base.metadata.create_all(engine)

            DBsession = sessionmaker(bind=engine)
            session = DBsession()
            print("Database Connected", database)
            return session
        except:
            print(traceback.print_exc())
            pass

    else:
        try:
            engine = create_engine(dev_database,
                                   connect_args={'options': '-csearch_path={}'.format("main_1")},
                                   client_encoding='utf8')
            Base.metadata.create_all(engine)

            DBsession = sessionmaker(bind=engine)
            session = DBsession()
            print("Database Connected", database)
            return session
        except:
            print(traceback.print_exc())
            pass


#
# session = get_dbase_session()
# test = session.query(Course.course_gen_id).filter(Course.course_gen_id == "fa20BIOL351GW04").scalar()
# print(test)

if __name__ == '__main__':

    config = load_config()
    database = "postgresql://{}:{}@{}/{}".format(config['username'],
                                                 config['password'],
                                                 config['server'],
                                                 config['database'])

    dev_database = "postgresql://{}:{}@{}/{}".format(config['username'],
                                                 config['password'],
                                                 config['server'],
                                                 config['dev_database'])

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

