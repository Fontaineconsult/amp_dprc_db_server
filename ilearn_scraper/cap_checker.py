#!/home/daniel/dev/py36-venv/bin/python3
import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")
sys.path.append("C:\\Users\\DanielPC\\Desktop\\Servers\\amp_dprc_db_server")

from ilearn_scraper.moodle_core_objects import IlearnCoursePage
from amp_dprc_database.dbase_functions import get_all_course_ilearn_ids
from ilearn_scraper.request_functions import open_iLearn_connection

from ilearn_scraper.temp_workarounds import fix_mediasite_links as fix
from amp_dprc_database.dbase_functions import add_scraped_videos, add_ilearn_course_name
import requests, json


def cap_checker_function():
    ilearn_connection = open_iLearn_connection()

    if ilearn_connection == False:
        return

    ilearn_page_ids = get_all_course_ilearn_ids("su21")

    if ilearn_page_ids is not None:

        for page_id in ilearn_page_ids:

            ilearn_page = IlearnCoursePage(page_id[1])

            course_section_content = ilearn_page.get_all_content()

            add_ilearn_course_name(ilearn_page.course_name, page_id[0])


            # check_or_commit_course(page_id[1], ilearn_page.course_name, page_id[0], "sp19", page_id[2]) //depreciated

            for section in course_section_content:
                for resource in section['resources']:
                    if resource['service_type'] == 'captioning':
                        # cap_status_request = requests.get("https://amp.sfsu.edu/api/captioning/refresh-cap-status",
                        #                                   params={"url": resource['link']},
                        #                                   verify=False)
                        # cap_status = json.loads(cap_status_request.content)


                        # commit_ilearn_video_content(resource['title'], fix.fix_mediasite_link(resource['link']), page_id[1], cap_status["cap-state"], section['section']) //depreciated
                        add_scraped_videos(resource['title'], fix.fix_mediasite_link(resource['link']), page_id[1], None, page_id[0], section['section'], "su21", resource['hidden'])


def cap_check_single(page_id, course_gen_id):

    open_iLearn_connection()


    ilearn_page = IlearnCoursePage(page_id)


    course_section_content = ilearn_page.get_all_content()


    for section in course_section_content:

        for resource in section['resources']:
            if resource['service_type'] == 'captioning':

                # cap_status_request = requests.get("https://amp.sfsu.edu/api/captioning/refresh-cap-status",
                #                                   params={"url": resource['link']},
                #                                   verify=False)
                # cap_status = False

                add_scraped_videos(resource['title'], fix.fix_mediasite_link(resource['link']), page_id, None, course_gen_id, section['section'], 'su21', resource['hidden'])
                pass


if __name__ == '__main__':
    cap_checker_function()


# cap_check_single("10315", "sp21HIST45001")
