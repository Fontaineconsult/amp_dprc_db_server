insert into main_1.employee (employee_id, employee_first_name, employee_last_name, employee_email, employee_phone, permission_type)
select employee_id, employee_first_name, employee_last_name, employee_email, employee_phone, permission_type from main.employee;

---

insert into main_1.course (course_gen_id, course_name, course_title, course_section, course_location, employee_id,semester,course_online, no_students_enrolled, contact_email_sent, no_student_enrolled_email_sent, course_comments, activate_ilearn_video_notification_sent, import_date, course_regestration_number, instructor_requests_captioning)
select course_gen_id, course_name, course_title, course_section, course_location, employee_id,semester,course_online, no_students_enrolled, contact_email_sent, no_student_enrolled_email_sent, course_comments, activate_ilearn_video_notification_sent, import_date, course_regestration_number, instructor_requests_captioning from main.course;

---


INSERT INTO main_1.captioning_media (media_type, title, length, source_url, captioned_url, at_catalog_number, comments, date_added)
SELECT media_type, title, length, source_url, captioned_url, at_catalog_number, comments, date_added from main.captioning_media;

----

INSERT INTO main_1.scraped_ilearn_videos(resource_type, resource_link, title, scan_date,video_length, captioned, captioned_version_id,indicated_due_date,submitted_for_processing,submitted_for_processing_date,course_ilearn_id,course_gen_id,semester,page_section)
SELECT resource_type, resource_link, title, scan_date,video_length, captioned, captioned_version_id,indicated_due_date,submitted_for_processing,submitted_for_processing_date,course_ilearn_id,course_gen_id,semester,page_section from main.scraped_ilearn_videos;

----

INSERT INTO main_1.course_ilearn_id (course_gen_id, ilearn_page_id)
SELECT course_gen_id, ilearn_page_id FROM main.course_ilearn_id;