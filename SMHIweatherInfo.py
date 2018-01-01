import requests
import json
from datetime import datetime
import logging

class SMHI(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon
        self.host = 'https://opendata-download-metfcst.smhi.se'
        self.Logger = logging.basicConfig(filename='SMHI_Errorlog.txt', level=logging.ERROR)
        self.update()


    def update(self):
        try:
            self.r = requests.get(self.host + \
                                '/api/category/pmp3g/version/2/geotype/point/lon/{0}/lat/{1}/data.json'\
                                .format(self.lat, self.lon))

            if self.r.status_code != requests.codes.ok:
                raise Exception("Status code from response not Ok.")

            self.parsedJSON = json.loads(self.r.text)
            self.lastUpdated = datetime.strptime(self.parsedJSON['approvedTime'],\
                                                '%Y-%m-%dT%H:%M:%SZ')
            self.temp = self.parsedJSON['timeSeries'][0]['parameters'][11]['values']
            self.tempUnit = self.parsedJSON['timeSeries'][0]['parameters'][11]['unit']

        except Exception:
            logging.exception('Message')
            exit(1)

if __name__ == '__main__':
    smhi_info = SMHI(21.4047,65)
