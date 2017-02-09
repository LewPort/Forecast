from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from urllib.request import urlopen
import sys, json

class GUI():

    def __init__(self):
        self.monofont = QtGui.QFont('andale mono', 8)

        self.create_mainframe()
        self.create_main_grid()
        self.create_search_grid()
        self.create_hourly_grid()
        self.create_location_search_bar()
        self.create_weather_display()
        self.create_time_slider()

    def create_mainframe(self):
        self.mainframe = qtw.QWidget()
        self.mainframe.setFixedSize(900, 400)
        self.mainframe.setWindowTitle('Continuously Updating Meteorological Forecast Internet Relayed System Technology')
        self.mainframe.show()

    def create_main_grid(self):
        self.maingrid = qtw.QGridLayout()
        self.mainframe.setLayout(self.maingrid)

    def create_search_grid(self):
        self.searchgrid = qtw.QGridLayout()
        self.maingrid.addLayout(self.searchgrid, 0, 0)

    def create_hourly_grid(self):
        self.hourlygrid = qtw.QGridLayout()
        self.maingrid.addLayout(self.hourlygrid, 1, 0)

    def create_location_search_bar(self):
        self.locinput = qtw.QLineEdit()
        self.locbutton = qtw.QPushButton('Retrieve')
        self.locbutton.clicked.connect(self.update_display_location)
        self.searchgrid.addWidget(self.locinput, 0, 0)
        self.searchgrid.addWidget(self.locbutton, 0, 1)

    def create_weather_display(self):
        self.radardisplay = qtw.QLabel()
        self.statsdisplay = qtw.QLabel()
        self.hourlygrid.addWidget(self.radardisplay, 0,0)
        self.hourlygrid.addWidget(self.statsdisplay, 0, 1)
        self.hourlygrid.setColumnStretch(3, 1)

    def display_weather_report(self, value):
        value += -1
        if value == -1:
            self.statsdisplay.setText(self.get_conditions_report())
        else:
            self.statsdisplay.setText(self.get_hourly_report(value))

    def display_radar_image(self):
        self.get_radar_image() #there was going to be more here but I guess I didn't need it in the end. Mugged it off.

    def reset_weather_text_display(self):
        self.statsdisplay.setText(' ')

    def create_time_slider(self):
        self.timeslider = qtw.QSlider(Qt.Horizontal)
        self.timeslider.setTickPosition(0)
        self.timeslider.setTickInterval(71)
        self.maingrid.addWidget(self.timeslider, 2, 0)

    def time_slider_function(self):
        self.timeslider.setValue(0)
        self.timeslider.valueChanged.connect(lambda: self.display_weather_report(self.timeslider.value()))

    def reset_slider(self):
        self.timeslider.setValue(0)

    def kill_slider_function(self):
        self.timeslider.valueChanged.connect(self.do_fuck_all)
        self.timeslider.valueChanged.disconnect()

    def get_radar_image(self):
        radar_image_url = program.api['satellite']['image_url']
        radar_image_url = urlopen(radar_image_url).read()

        radar_image = QtGui.QImage()
        radar_image.loadFromData(radar_image_url)
        radar_image = QtGui.QPixmap(radar_image)

        return self.radardisplay.setPixmap(radar_image)

    def get_conditions_report(self):
        api = program.api
        city = api['current_observation']['display_location']['full']
        station = api['current_observation']['observation_location']['city']
        lat = api['current_observation']['observation_location']['latitude']
        long = api['current_observation']['observation_location']['longitude']
        elev = api['current_observation']['observation_location']['elevation']

        lastupdate = api['current_observation']['observation_time']
        ctemp = api['current_observation']['temp_c']
        feelslike = api['current_observation']['feelslike_c']
        humidity = api['current_observation']['relative_humidity']
        desc = api['current_observation']['weather']
        windspeed = api['current_observation']['wind_kph']
        winddir = api['current_observation']['wind_degrees']
        gusts = api['current_observation']['wind_gust_kph']
        pressure = api['current_observation']['pressure_mb']
        visibility = api['current_observation']['visibility_km']

        report = ('%s - %s' % (station, city) +
                  '\nElevation: %s (Lat: %s Long: %s)' % (elev, lat, long) +
                  '\n' + lastupdate +

                  # Conditions
                  '\n\nDescription: %s (Visibility: %skm)' % (desc, visibility) +

                  # Temp
                  '\n\nTemp: %s°c (Feels like: %s°c)' % (ctemp, feelslike) +
                  '\nHumidity: ' + humidity +

                  # Wind
                  '\n\nWind: %dkph from %d° (Gusts: %skph)' % (windspeed, winddir, gusts) +
                  '\nPressure: %smb\n\n' % pressure +

                  'Date: Now')

        return report

    def get_hourly_report(self, i):
        api = program.api

        city = api['current_observation']['display_location']['full']
        station = api['current_observation']['observation_location']['city']
        lat = api['current_observation']['observation_location']['latitude']
        long = api['current_observation']['observation_location']['longitude']
        elev = api['current_observation']['observation_location']['elevation']
        lastupdate = api['current_observation']['observation_time']

        hapi = program.api['hourly_forecast'][i]

        date = hapi['FCTTIME']['pretty']
        day = hapi['FCTTIME']['weekday_name']
        condition = hapi['wx']
        windspeed = hapi['wspd']['metric']
        winddir = hapi['wdir']['degrees']
        temp = hapi['temp']['metric']
        humidity = hapi['humidity']
        feelslike = hapi['feelslike']['metric']
        pressure = hapi['mslp']['metric']

        report = ('%s - %s' % (station, city) +
                  '\nElevation: %s (Lat: %s Long: %s)' % (elev, lat, long) +
                  '\n' + lastupdate +

                  # Conditions
                  '\n\nDescription: %s' % condition +

                  # Temp
                  '\n\nTemp: %s°c (Feels like: %s°c)' % (temp, feelslike) +
                  '\nHumidity: %s' % humidity + ' %' +

                  # Wind
                  '\n\nWind: %skph from %s°' % (windspeed, winddir) +
                  '\nPressure: %smb' % pressure +

                    #Date
                  '\n\nDate: %s %s' % (day, date))

        return report

    def get_searchbar_location(self):
        location = self.locinput.text()
        location = location.replace(' ', '_')
        return location

    def update_display_location(self):
        self.reset_weather_text_display()
        self.reset_slider()
        location = self.get_searchbar_location()
        program.get_json(location)
        try:
            self.get_conditions_report()
        except:
            gui.statsdisplay.setText('ERROR\n'
                                     'Could not find location \'' + location +'\'.\n'
                                     'Posssible connection issues, or location not recognised.\n'
                                     'Please try again.')
            self.kill_slider_function()
            return
        self.time_slider_function()
        self.display_radar_image()
        self.display_weather_report(0)

    def do_fuck_all(self):
        pass



class Program():


    def get_json(self, location):
        url = 'http://api.wunderground.com/api/' + api_key + '/conditions/hourly10day/satellite/q/' + location + '.json'
        print(url)
        url = urlopen(url).read().decode('utf8')
        self.api = json.loads(url)

if __name__ == '__main__':
    api_key = '3c06c2fea3463226'
    app = QtWidgets.QApplication(sys.argv)
    qtw = QtWidgets
    program = Program()
    gui = GUI()
    sys.exit(app.exec_())
