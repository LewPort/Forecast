from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from urllib.request import urlopen
import sys, json

version = '1.0'

class GUI(QMainWindow):

    def __init__(self):

        super(GUI, self).__init__()
        self.init_UI()
        self.create_mainframe()
        self.create_main_grid()
        self.create_upper_grid()
        self.create_hourly_grid()
        self.create_favourites_grid()
        self.create_menu_bar()
        self.create_favourites_groupbox()
        self.create_time_slider()
        self.create_weather_display()
        self.create_location_search_bar()
        self.create_favourites_bar()
        self.populate_favourites_list()
        self.favourites_box_functionality()


    def init_UI(self):
        self.setFixedSize(900, 400)
        self.setWindowTitle('4Cast - Extremely Advanced Meteorological Conditions Prediction System (' + version +')')
        #self.mainframe.setWindowTitle('Continuously Updating Meteorological Forecast Internet Relayed System Technology')
        self.show()

    def create_menu_bar(self):
        menubar = self.menuBar()
        apimenu = menubar.addMenu('&API')
        apiitem = apimenu.addAction('&Change Wunderground API Key')
        apiitem.triggered.connect(api_window.api_change_window)


    def create_mainframe(self):
        self.mainframe = qtw.QWidget()
        self.setCentralWidget(self.mainframe)

    def create_main_grid(self):
        self.maingrid = qtw.QGridLayout()
        self.mainframe.setLayout(self.maingrid)

    def create_upper_grid(self):
        self.uppergrid = qtw.QGridLayout()
        self.maingrid.addLayout(self.uppergrid, 0, 0)

    def create_hourly_grid(self):
        self.hourlygrid = qtw.QGridLayout()
        self.maingrid.addLayout(self.hourlygrid, 1, 0)

    def create_location_search_bar(self):
        self.locinput = qtw.QLineEdit()
        self.locinput.setFixedWidth(300)
        self.locinput.returnPressed.connect(lambda: self.update_display_location(self.get_searchbar_location().replace(' ', '_')))
        self.locbutton = qtw.QPushButton('Get Forecast')
        self.locbutton.setFixedWidth(110)
        self.locbutton.clicked.connect(lambda: self.update_display_location(self.get_searchbar_location().replace(' ', '_')))
        self.uppergrid.addWidget(self.locinput, 0, 0)
        self.uppergrid.addWidget(self.locbutton, 0, 1)

    def create_favourites_bar(self):
        self.addtofavs = qtw.QPushButton('+')
        self.addtofavs.setFixedWidth(50)
        self.addtofavs.clicked.connect(self.add_to_favourites_list)
        self.removefromfavs = qtw.QPushButton('-')
        self.removefromfavs.setFixedWidth(50)
        self.removefromfavs.clicked.connect(self.remove_selected_item_from_favourites_list)
        self.favouritescombobox = qtw.QComboBox()
        self.favouritescombobox.setFixedWidth(300)

        self.favourites_grid.addWidget(self.addtofavs, 0, 1)
        self.favourites_grid.addWidget(self.removefromfavs, 0, 2)
        self.favourites_grid.addWidget(self.favouritescombobox, 0, 3)

    def create_favourites_grid(self):
        self.favourites_grid = qtw.QGridLayout()

    def create_favourites_groupbox(self):
        self.favourites_groupbox = qtw.QGroupBox('Favourites')
        self.favourites_groupbox.setLayout(self.favourites_grid)
        self.uppergrid.addWidget(self.favourites_groupbox, 0, 2)

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
        return location

    def no_connection_message(self, location):
        self.statsdisplay.setText('ERROR\n'
                                  'Could not find location \'' + location + '\'.\n'
                                  'Posssible connection issues, or location not recognised.\n'
                                  'Please try again.')
        self.kill_slider_function()


    def update_display_location(self, location):
        self.reset_weather_text_display()
        self.reset_slider()
        try:
            program.get_json(location)
        except:
            self.no_connection_message(location)
            return None

        try:
            self.get_conditions_report()
        except:
            self.no_connection_message(location)
            return None

        self.time_slider_function()
        self.display_radar_image()
        self.display_weather_report(0)


    def populate_favourites_list(self):
        self.favouritescombobox.clear()
        for i in program.favourites:
            self.favouritescombobox.addItem(i)

    def add_to_favourites_list(self):
        program.favourites.append(self.get_searchbar_location())
        program.favourites_json_save()
        self.populate_favourites_list()

    def remove_selected_item_from_favourites_list(self):
        program.favourites.remove(self.get_favourites_list_selected_item())
        program.favourites_json_save()
        self.populate_favourites_list()

    def get_favourites_list_selected_item(self):
        return self.favouritescombobox.currentText()

    def get_weather_from_favourites_combobox(self):
        self.update_display_location(self.get_favourites_list_selected_item().replace(' ', '_'))

    def favourites_box_functionality(self):
        self.favouritescombobox.activated.connect(self.get_weather_from_favourites_combobox)

    def do_fuck_all(self):
        pass

class API_Window():

    def __init__(self):

        self.api_key = self.get_current_api_key()

    def api_change_window(self):
        self.api_window = qtw.QWidget()
        self.api_window.setFixedSize(200, 100)
        self.api_window.setWindowTitle('Change API Key')

        api_window_vbox = qtw.QVBoxLayout()
        api_window_hbox = qtw.QHBoxLayout()

        self.api_entry = qtw.QLineEdit(self.get_current_api_key())
        api_ok = qtw.QPushButton('Ok')
        api_cancel = qtw.QPushButton('Cancel')

        api_window_vbox.addWidget(self.api_entry)
        api_window_vbox.addLayout(api_window_hbox)
        api_window_hbox.addWidget(api_ok)
        api_window_hbox.addWidget(api_cancel)

        api_ok.clicked.connect(self.ok_button)
        api_cancel.clicked.connect(self.cancel_button)

        self.api_window.setLayout(api_window_vbox)

        self.api_window.show()

    def cancel_button(self):
        self.api_window.close()

    def ok_button(self):
        self.save_api_key()
        self.api_window.close()

    def save_api_key(self):
        self.api_key = self.api_entry.text()
        with open('apikey.json', 'w') as self.api_key_json:
            json.dump(self.api_key, self.api_key_json)


    def get_current_api_key(self):
        try:
            with open('apikey.json', 'r') as self.api_key_json:
                api_key = json.load(self.api_key_json)
        except:
            api_key = 'API Key Here'

        return api_key


class Program():

    def __init__(self):
        try:
            with open('favlocations.json', 'r') as self.favlocations:
                self.favourites = json.load(self.favlocations)
        except:
            self.favourites = []
            self.favourites_json_save()


    def favourites_json_save(self):
        with open('favlocations.json', 'w') as self.favlocations:
            json.dump(self.favourites, self.favlocations)

    def get_json(self, location):
        url = 'http://api.wunderground.com/api/' + api_window.api_key + '/conditions/hourly10day/satellite/q/' + location + '.json'
        print(url)
        url = urlopen(url).read().decode('utf8')
        self.api = json.loads(url)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qtw = QtWidgets
    program = Program()
    api_window = API_Window()
    gui = GUI()
    sys.exit(app.exec_())
