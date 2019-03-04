
import re

def fix_mediasite_link(input_string):
    regex = re.compile("(https://ilearn.support.at.sfsu.edu/ay1819/mod/mediasite/content_launch.php\?id=([0-9]{0,7})&a=0&frameset&inpopup=1)")
    start_string_url = "https://ilearn.support.at.sfsu.edu/ay1819/mod/mediasite/view.php?id="
    media_site_id = regex.match(input_string)
    if media_site_id is not None:
        return "{}{}".format(start_string_url, media_site_id.group(2))

    else:
        return input_string



