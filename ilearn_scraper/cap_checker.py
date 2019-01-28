from ilearn_scraper.moodle_core_objects import IlearnCoursePage
from amp_dprc_dbase.dbase_functions import get_all_course_ilearn_ids
from ilearn_scraper.request_functions import open_iLearn_connection
from aws_server.aws_dbase_functions import commit_ilearn_video_content, check_or_commit_course
import requests, json


open_iLearn_connection()

ilearn_page_ids = get_all_course_ilearn_ids("sp19")


if ilearn_page_ids is not None:

    for page_id in ilearn_page_ids:

        ilearn_page = IlearnCoursePage(page_id[1])
        print(ilearn_page)

        course_section_content = ilearn_page.get_all_content()


        check_or_commit_course(page_id[1], ilearn_page.course_name, page_id[0], "sp19")

        for section in course_section_content:
            for resource in section['resources']:
                if resource['service_type'] == 'captioning':
                    cap_status_request = requests.get("https://amp.sfsu.edu/api/captioning/refresh-cap-status",
                                                      params={"url": resource['link']},
                                                      verify=False)
                    print(cap_status_request.content)

                    cap_status = json.loads(cap_status_request.content)

                    commit_ilearn_video_content(resource['title'], resource['link'], page_id[1], cap_status["cap-state"])


