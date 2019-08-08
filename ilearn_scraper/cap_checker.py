import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")

from ilearn_scraper.moodle_core_objects import IlearnCoursePage
from amp_dprc_database.dbase_functions import get_all_course_ilearn_ids
from ilearn_scraper.request_functions import open_iLearn_connection

from ilearn_scraper.temp_workarounds import fix_mediasite_links as fix
from amp_dprc_database.dbase_functions import add_scraped_videos
import requests, json


def cap_checker_function():
    open_iLearn_connection()

    ilearn_page_ids = get_all_course_ilearn_ids("fa19")


    if ilearn_page_ids is not None:

        for page_id in ilearn_page_ids:

            ilearn_page = IlearnCoursePage(page_id[1])
            print(ilearn_page)

            course_section_content = ilearn_page.get_all_content()


            # check_or_commit_course(page_id[1], ilearn_page.course_name, page_id[0], "sp19", page_id[2]) //depreciated

            for section in course_section_content:
                for resource in section['resources']:
                    if resource['service_type'] == 'captioning':
                        cap_status_request = requests.get("https://amp.sfsu.edu/api/captioning/refresh-cap-status",
                                                          params={"url": resource['link']},
                                                          verify=False)
                        print(cap_status_request.content)

                        cap_status = json.loads(cap_status_request.content)

                        # commit_ilearn_video_content(resource['title'], fix.fix_mediasite_link(resource['link']), page_id[1], cap_status["cap-state"], section['section']) //depreciated
                        add_scraped_videos(resource['title'], fix.fix_mediasite_link(resource['link']), page_id[1], cap_status["cap-state"], page_id[0], section['section'])


def cap_check_single(page_id, course_gen_id):

    open_iLearn_connection()

    ilearn_page = IlearnCoursePage(page_id)
    print(ilearn_page)

    course_section_content = ilearn_page.get_all_content()
    print("ALL SECTIONS", course_section_content)

    for section in course_section_content:
        print("SECTION", section)
        for resource in section['resources']:
            if resource['service_type'] == 'captioning':

                cap_status_request = requests.get("https://amp.sfsu.edu/api/captioning/refresh-cap-status",
                                                  params={"url": resource['link']},
                                                  verify=False)

                cap_status = json.loads(cap_status_request.content)

                add_scraped_videos(resource['title'], fix.fix_mediasite_link(resource['link']), page_id, cap_status["cap-state"], course_gen_id, section['section'])
                pass




if __name__ == '__main__':
    cap_checker_function()
