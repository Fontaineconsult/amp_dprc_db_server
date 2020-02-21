from amp_dprc_database.sf_cap_db_v2 import CaptioningMedia, get_dbase_session
from datetime import datetime
import csv


session = get_dbase_session()


with open('Caption_Media.csv') as media:
    csv_reader = csv.reader(media)

    for each in csv_reader:

        if each[5] is not '':
            print(each[4])
            test = session.query(CaptioningMedia).filter_by(source_url=each[4]).all()

            if len(test) == 0:



                video = CaptioningMedia(title=each[2],
                                        length=each[3],
                                        source_url=each[4],
                                        captioned_url=each[5],
                                        date_added=datetime.strptime(each[9], "%m/%d/%Y"))
                session.add(video)
                session.commit()
