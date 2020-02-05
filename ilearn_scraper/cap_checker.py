import sys
sys.path.append("/home/daniel/dev/py36-venv/dev")

from ilearn_scraper.moodle_core_objects import IlearnCoursePage
from amp_dprc_database.dbase_functions import get_all_course_ilearn_ids
from ilearn_scraper.request_functions import open_iLearn_connection

from ilearn_scraper.temp_workarounds import fix_mediasite_links as fix
from amp_dprc_database.dbase_functions import add_scraped_videos, add_ilearn_course_name
import requests, json


def cap_checker_function():
    open_iLearn_connection()

    ilearn_page_ids = get_all_course_ilearn_ids("sp20")


    if ilearn_page_ids is not None:

        for page_id in ilearn_page_ids:

            ilearn_page = IlearnCoursePage(page_id[1])
            print(ilearn_page)

            course_section_content = ilearn_page.get_all_content()

            add_ilearn_course_name(ilearn_page.course_name, page_id[0])

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
                        add_scraped_videos(resource['title'], fix.fix_mediasite_link(resource['link']), page_id[1], cap_status["cap-state"], page_id[0], section['section'], "sp20")


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

                print(cap_status_request.content)
                cap_status = json.loads(cap_status_request.content)

                add_scraped_videos(resource['title'], fix.fix_mediasite_link(resource['link']), page_id, cap_status["cap-state"], course_gen_id, section['section'], 'sp20')
                pass





# classes = [("sp20CJ46001", "16646"),
#            ("sp20CJ47001", "17024"),
#            ("sp20CJ47501", "16647"),
#            ("sp20CJ52002", "16738"),
#            ("sp20CAD41002", "14865"),
#            ("sp20CAD62503", "17445"),
#            ("sp20CHEM11528", "15160"),
#            ("sp20CHEM11529", "15174"),
#            ("sp20CHEM11530", "15188"),
#            ("sp20EED61601", "15835"),
#            ("sp20EED64501", "13515"),
#            ("sp20EED70103", "16246"),
#            ("sp20FCS22301", "9038"),
#            ("sp20MATH12405", "13317"),
#            ("sp20PHYS11103", "13866"),
#            ("sp20PHYS11211", "13781"),
#            ("sp20PSY45102", "17462"),
#            ("sp20PSY45201", "11640"),
#            ("sp20PSY69001", "11643"),
#            ("sp20SOC24501", "9258"),
#            ("sp20SPED33002", "13170"),
#            ("sp20SPED63003", "17337"),
#            ("sp20SPED73701", "11811"),
#            ("sp20SPED77401", "13698"),
#            ("sp20SPED78801", "11823"),
#            ("SP20PA71501", "14831"),
#            ("SP20BIOL613GW05", "12116")
#            ]
#
# cap_check_single('15067', 'sp20AFRS46601')



if __name__ == '__main__':
    cap_checker_function()


