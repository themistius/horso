import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QTabWidget, QPushButton, QComboBox
from database import DatabaseHandler
from TJK_races_scraper import race

class HorseRacingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_handler = DatabaseHandler('data/horse_racing.db')
        self.init_ui()
        self.column_names = []
        
    def init_ui(self):
        self.setWindowTitle("Horse Racing App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        fetch_button = QPushButton("Show races")
        fetch_button.clicked.connect(self.show_data)
        layout.addWidget(fetch_button)

        update_button = QPushButton("Update races")
        update_button.clicked.connect(self.scrape_data)
        layout.addWidget(update_button)

        # Create a QTabWidget for filtering data
        self.tab_widget = QTabWidget(self)

        # Dynamically add city tabs and race time tabs
        self.add_dynamic_tabs()

        # Add a QTableWidget for displaying race data
        self.data_table = QTableWidget()
        layout.addWidget(self.tab_widget)

        # Add the tab widget to the layout
        layout.addWidget(self.data_table)

        central_widget.setLayout(layout)
        
        self.tab_widget.currentChanged.connect(self.tab_changed)

    def scrape_data(self):
        race()
        self.update_db_list()

    def show_data(self):
        self.update_db_list()

    def update_db_list(self):
        race_data = self.db_handler.fetch_races()
        if race_data:
            self.column_names = list(race_data[0].keys())

            # Add data to each city tab and race time sub-tab
            for i in range(self.tab_widget.count()):
                city_tab = self.tab_widget.widget(i)
                city_name = city_tab.objectName()
                race_times = list(set(race['Race Time'] for race in race_data if race['City'] == city_name))
                self.populate_city_tab(city_tab, race_data, city_name, race_times)

    def add_dynamic_tabs(self):
        # Retrieve city names and race times dynamically
        race_data = self.db_handler.fetch_races()
        city_names = list(set(race['City'] for race in race_data))
        for city_name in city_names:
            city_tab = QWidget(self)
            city_tab.setObjectName(city_name)  # Set the object name as the city name
            self.tab_widget.addTab(city_tab, city_name)

            # Create a QTabWidget for race times within the city tab
            race_time_tab_widget = QTabWidget(city_tab)

            # Add the race time tabs within the city tab
            race_time_tab_widget.addTab(QWidget(), "All Times")
            self.add_race_time_tabs(race_time_tab_widget, city_name)

    def add_race_time_tabs(self, race_time_tab_widget, city_name):
        race_data = self.db_handler.fetch_races()
        if race_data:
            race_times = list(set(race['Race Time'] for race in race_data if race['City'] == city_name))
            for time in race_times:
                race_time_tab = QTableWidget()  # Use QTableWidget here
                race_time_tab_widget.addTab(race_time_tab, time)


    def populate_city_tab(self, city_tab, race_data, city_name, race_times):
        city_layout = QVBoxLayout()
        city_tab.setLayout(city_layout)

        for race_time in race_times:
            # Add a QTableWidget for each race time sub-tab
            race_time_table_widget = QTableWidget()
            city_layout.addWidget(race_time_table_widget)

            # Populate the tables with data
            city_table_data = [race for race in race_data if race['City'] == city_name]
            race_time_table_data = [race for race in city_table_data if race['Race Time'] == race_time]

            self.populate_table(race_time_table_widget, race_time_table_data)        
   
    def tab_changed(self, index):
        if index >= 0:
            city_tab = self.tab_widget.widget(index)
            city_name = city_tab.objectName()
            race_data = self.db_handler.fetch_races()
            race_time_tab_widget = city_tab.findChild(QTableWidget)
            if race_time_tab_widget:
                for i in range(race_time_tab_widget.columnCount()):
                    race_time_tab = race_time_tab_widget.cellWidget(i, 0)
                    race_time = race_time_tab_widget.tabText(i)
                    race_time_table_data = [race for race in race_data if race['City'] == city_name and race['Race Time'] == race_time]
                    self.populate_table(race_time_tab, race_time_table_data)

    def populate_table(self, table_widget, table_data):
        if not table_data:
            return

        self.column_names = list(table_data[0].keys())
        table_widget.setColumnCount(len(self.column_names))
        table_widget.setHorizontalHeaderLabels(self.column_names)
        table_widget.setRowCount(len(table_data))

        for row_index, race in enumerate(table_data):
            for col_index, key in enumerate(self.column_names):
                item = QTableWidgetItem(str(race[key]))
                table_widget.setItem(row_index, col_index, item)

def main():
    app = QApplication(sys.argv)
    window = HorseRacingApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
