import requests
import json
from datetime import datetime
import traceback


class SMHI(object):
    """Just talking to myself."""

    def __init__(self, lat, lon):
        """Initialize all variables and calls the update function.

        Args:
            -lat (str): latitude of the address
            -lon (str): longitude of the address


        """
        self.lat = lat
        self.lon = lon
        self.host = 'https://opendata-download-metfcst.smhi.se'
        self.parsedJSON = None
        self.approvedTime = datetime.strptime(
                                                '1900-01-01T00:00:00Z',
                                                '%Y-%m-%dT%H:%M:%SZ')
        self.validTime = datetime.strptime(
                                            '1900-01-01T00:00:00Z',
                                            '%Y-%m-%dT%H:%M:%SZ')
        self.lastValidTime = datetime.strptime(
                                                '1900-01-01T00:00:00Z',
                                                '%Y-%m-%dT%H:%M:%SZ')
        self.Temperature = -999
        self.Wsymb2 = -999
        self.TemperatureUnit = ''
        self.update()

    def update(self):
        """Getting the new data and parses the JSON string into variables.

        If the request fails, it checks the the last call for data and
        presents the most accurate data.
        Should be called regularly or on request.

        Returns:
            Returns True if the request succeededs or if there are data from
            a previous call. Otherwise it retrurns false.

        """
        try:

            r = requests.get(
                            self.host +
                            '/api/category/pmp3g/version/2/geotype/point/'
                            'lon/{0}/lat/{1}/data.json'
                            .format(self.lat, self.lon))

            if r.status_code == requests.codes.ok:
                self.parsedJSON = json.loads(r.text)

                self.approvedTime = datetime.strptime(
                                            self.parsedJSON['approvedTime'],
                                            '%Y-%m-%dT%H:%M:%SZ')
                self.validTime = datetime.strptime(
                                self.parsedJSON['timeSeries'][0]['validTime'],
                                '%Y-%m-%dT%H:%M:%SZ')

                self.lastValidTime = datetime.strptime(
                        self.parsedJSON['timeSeries']
                        [len(self.parsedJSON['timeSeries'])-1]['validTime'],
                        '%Y-%m-%dT%H:%M:%SZ')

                self.Temperature = self.parsedJSON['timeSeries'][0]['parameters'][11]['values'][0]
                self.TemperatureUnit = self.parsedJSON['timeSeries'][0]['parameters'][11]['unit']
                self.Wsymb2 = self.parsedJSON['timeSeries'][0]['parameters'][18]['values'][0]
            else:
                validTime_old = None

                if self.parsedJSON is not None:
                    for hours in self.parsedJSON['timeSeries']:
                        validTime = datetime.strptime(hours['validTime'],
                                                      '%Y-%m-%dT%H:%M:%SZ')
                        if validTime_old is None:
                            validTime_old = validTime

                        validTimeMax = datetime.now() + ((validTime -
                                                         validTime_old) / 2)
                        validTimeMin = datetime.now() - ((validTime -
                                                         validTime_old) / 2)
                        print(str(validTime)
                              + ', ' + str(validTimeMin)
                              + ', ' + str(validTimeMax))

                        if (validTimeMax > validTime and
                           validTimeMin < validTime):
                            self.validTime = validTime
                            self.Temperature = hours['parameters'][11]['values'][0]
                            self.TemperatureUnit = hours['parameters'][11]['unit']
                            self.Wsymb2 = hours['parameters'][18]['values'][0]

                        validTime_old = validTime
                    self.__LogWriter('Status code from response not Ok.\n'
                                     'HTTP code = {0}'.format(r.status_code))

                    if self.lastValidTime < datetime.now():
                        return False
                else:
                    return False
            return True

        except Exception:
            self.__LogWriter(traceback.format_exc())
            exit(1)

    def __LogWriter(self, e):
        fh = open('SMHI_Errorlog.txt', 'a')
        s = '*-------------------*' + '\n'
        s = s + 'Time: ' + str(datetime.now()) + '\n'
        s = s + str(e)
        s = s + '*-------------------*' + '\n' + '' + '\n' + '' + '\n'
        fh.write(s)
        fh.close()


if __name__ == '__main__':
    smhi_info = SMHI(22.1567, 65.5848)
    print(str(smhi_info.Temperature) + ' ' + smhi_info.TemperatureUnit)
    print(smhi_info.Wsymb2)
    print(smhi_info.approvedTime)
    print(smhi_info.lastValidTime)
    print(smhi_info.validTime)
