import requests
import json
from datetime import datetime
import traceback
import sys


class SMHI(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon
        self.host = 'https://opendata-download-metfcst.smhi.se'
        self.lastUpdated = datetime.strptime('1900-01-01T00:00:00Z',\
                                            '%Y-%m-%dT%H:%M:%SZ')
        self.temp = 0
        self.tempUnit = ''
        self.update()


    def update(self):
        try:
            r = requests.get(self.host + \
                                '/api/category/pmp3g/version/2/geotype/point/' + \
                                'lon/{0}/lat/{1}/data.json'\
                                .format(self.lat, self.lon))

            if r.status_code != requests.codes.ok:
                raise Exception('Status code from response not Ok.\n' + \
                                'HTTP code = {0}'.format(r.status_code))
            1/0
            parsedJSON = json.loads(r.text)
            self.lastUpdated = datetime.strptime(parsedJSON['approvedTime'],\
                                                '%Y-%m-%dT%H:%M:%SZ')
            self.temp = parsedJSON['timeSeries'][0]['parameters'][11]['values'][0]
            self.tempUnit = parsedJSON['timeSeries'][0]['parameters'][11]['unit']

        except Exception:
            self.LogWriter(traceback.format_exc())
            exit(1)

    def LogWriter(self,e):
        fh = open('SMHI_Errorlog.txt','a')
        s = '*-------------------*' + '\n'
        s = s + 'Time: ' + str(datetime.now()) + '\n'
        s = s + str(e)
        s = s + '*-------------------*' + '\n' + '' + '\n' + '' + '\n'
        fh.write(s)
        fh.close()

if __name__ == '__main__':
    smhi_info = SMHI(22.1567,65.5848)
    print(str(smhi_info.temp) + ' ' + smhi_info.tempUnit)
    print(smhi_info.lastUpdated)
