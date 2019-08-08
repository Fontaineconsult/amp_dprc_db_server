


CREATE OR REPLACE FUNCTION main_1.track_camp_org_assign() RETURNS TRIGGER as $camp_org_assg$

BEGIN

  IF (TG_OP = 'INSERT') THEN

    INSERT INTO main_1.captioning_requester (campus_org_id) SELECT NEW.id;
    RETURN NEW;

  END IF;

END;

$camp_org_assg$ LANGUAGE plpgsql;

CREATE TRIGGER camp_org_assg

  AFTER INSERT ON main_1.campus_association_assignment
  FOR EACH ROW EXECUTE PROCEDURE main_1.track_camp_org_assign();




CREATE OR REPLACE FUNCTION main_1.track_course_assign() RETURNS TRIGGER as $course_assg$

BEGIN

  IF (TG_OP = 'INSERT') THEN

    INSERT INTO main_1.captioning_requester (course_id) SELECT NEW.course_gen_id;
    RETURN NEW;

  END IF;

END;

$course_assg$ LANGUAGE plpgsql;

CREATE TRIGGER course_assg

  AFTER INSERT ON main_1.course
  FOR EACH ROW EXECUTE PROCEDURE main_1.track_course_assign();



ALTER TABLE main_1.captioning_requester
  ADD CONSTRAINT only_one CHECK (campus_association_id IS NULL AND course_id IS NOT NULL OR campus_association_id IS NOT NULL AND course_id IS NULL);



SELECT studentenrollement.course_reg_number, studentenrollement.student_id,
       rawcourselist.id, rawcourselist.subject_code, rawcourselist.course_number,
       rawcourselist.section_number, rawcourselist.class_title,
       rawcourselist.instructor_name, rawcourselist.instructor_email,
       rawcourselist.instructor_id
FROM main_1.studentenrollement
       JOIN main_1.rawcourselist ON studentenrollement.course_reg_number::text = rawcourselist.course_regestration_number::text;




SELECT student.student_id, student.student_first_name,
       student.student_last_name, student.student_email, student.student_requests,
       student.captioning_active, student.transcripts_only,
       current_enrollement.course_reg_number, current_enrollement.subject_code,
       current_enrollement.course_number, current_enrollement.section_number,
       current_enrollement.class_title, current_enrollement.instructor_id,
       current_enrollement.instructor_name, current_enrollement.instructor_email,
       (('fa19'::text || replace(current_enrollement.subject_code::text, ' '::text, ''::text)) || replace(current_enrollement.course_number::text, ' '::text, ''::text)) || current_enrollement.section_number::text AS course_gen_key
FROM main_1.student
       JOIN main_1.current_enrollement ON student.student_id::text = current_enrollement.student_id::text;


CREATE OR REPLACE VIEW main_1.current_enrollement AS
SELECT studentenrollement.course_reg_number,
       studentenrollement.student_id,
       rawcourselist.id,
       rawcourselist.term_code,
       rawcourselist.subject_code,
       rawcourselist.course_number,
       rawcourselist.section_number,
       rawcourselist.class_title,
       rawcourselist.instructor_name,
       rawcourselist.instructor_email,
       rawcourselist.instructor_id
FROM main_1.studentenrollement
       JOIN main_1.rawcourselist ON studentenrollement.course_reg_number::text = rawcourselist.course_regestration_number::text;

ALTER TABLE main_1.current_enrollement_1
  OWNER TO daniel;


CREATE OR REPLACE VIEW main_1.current_student_courses AS
SELECT student.student_id, student.student_first_name,
       student.student_last_name, student.student_email, student.student_requests,
       student.captioning_active, student.transcripts_only,
       current_enrollement.course_reg_number, current_enrollement.subject_code,
       current_enrollement.course_number, current_enrollement.section_number,
       current_enrollement.class_title, current_enrollement.instructor_id,
       current_enrollement.instructor_name, current_enrollement.instructor_email,
       (('fa19'::text || replace(current_enrollement.subject_code::text, ' '::text, ''::text)) || replace(current_enrollement.course_number::text, ' '::text, ''::text)) || current_enrollement.section_number::text AS course_gen_key
FROM main_1.student
       JOIN main_1.current_enrollement ON student.student_id::text = current_enrollement.student_id::text;

ALTER TABLE main_1.current_student_courses
  OWNER TO daniel;