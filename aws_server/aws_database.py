from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class iLearn_Course(Base):

    __tablename__ = 'courses'
    course_id = Column(String, primary_key=True)
    course_name = Column(String)
    course_gen_id = Column(String)
    semester = Column(String)
    no_students_enrolled = Column(Boolean)
    date_added = Column(DateTime, default=datetime.utcnow)
    assigned_videos = relationship('iLearn_Video', backref='courses')


class iLearn_Video(Base):

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    resource_type = Column(String)
    resource_link = Column(String)
    title = Column(String)
    scan_date = Column(DateTime, default=datetime.utcnow)
    length = Column(String)
    captioned = Column(Boolean)
    indicated_due_date = Column(DateTime)
    captioned_version_url = Column(String)
    course_id = Column(String, ForeignKey('courses.course_id'))
    course = relationship(iLearn_Course)
    page_section = Column(String)


def get_session():
    engine = create_engine("postgresql://accessdb:accessdb@54.203.102.241/video_link_repo")
    Base.metadata.create_all(engine)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    return session



