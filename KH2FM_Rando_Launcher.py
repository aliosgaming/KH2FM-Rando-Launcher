import sys
import subprocess
import configparser
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QMessageBox
from PySide6.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('KH2FM Rando Launcher')
        self.setWindowIcon(QIcon(self.resource_path('theGrid.ico')))
        self.initUI()
        self.loadConfig()

    def initUI(self):
        self.setGeometry(100, 100, 600, 300)

        main_layout = QVBoxLayout()

        self.text_boxes = []
        
        layout = QHBoxLayout()
        text_box = QLineEdit(self)
        button = QPushButton(f'KHTracker', self)
        button.clicked.connect(lambda checked, index=0: self.showDialog(index))
        layout.addWidget(text_box)
        layout.addWidget(button)
        main_layout.addLayout(layout)
        self.text_boxes.append(text_box)

        layout = QHBoxLayout()
        text_box = QLineEdit(self)
        button = QPushButton(f'Seed Generator', self)
        button.clicked.connect(lambda checked, index=1: self.showDialog(index))
        layout.addWidget(text_box)
        layout.addWidget(button)
        main_layout.addLayout(layout)
        self.text_boxes.append(text_box)
        
        layout = QHBoxLayout()
        text_box = QLineEdit(self)
        button = QPushButton(f'Mods Manager', self)
        button.clicked.connect(lambda checked, index=2: self.showDialog(index))
        layout.addWidget(text_box)
        layout.addWidget(button)
        main_layout.addLayout(layout)
        self.text_boxes.append(text_box)
        
        layout = QHBoxLayout()
        text_box = QLineEdit(self)
        button = QPushButton(f'Livesplit', self)
        button.clicked.connect(lambda checked, index=3: self.showDialog(index))
        layout.addWidget(text_box)
        layout.addWidget(button)
        main_layout.addLayout(layout)
        self.text_boxes.append(text_box)

        self.export_button = QPushButton('Run', self)
        self.export_button.clicked.connect(self.launchPrograms)
        main_layout.addWidget(self.export_button)

        self.setLayout(main_layout)

    def showDialog(self, index):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if dialog.exec():
            selected_directory = dialog.selectedFiles()[0]
            self.text_boxes[index].setText(selected_directory)
            self.saveConfig(index, selected_directory)

    def launchPrograms(self):
        directories = [text_box.text() for text_box in self.text_boxes if text_box.text()]
        if not directories:
            QMessageBox.warning(self, 'No Directories Selected', 'Please select at least one directory.')
            return
        
        exe_dir = ''
        final_status = ''
        try:
            for directory in directories:
                if os.path.isfile(directory):
                    exe_dir = os.path.dirname(directory)
                    os.startfile(directory, cwd=exe_dir)
                      
                    final_status += '\n' + os.path.basename(directory)
                else:
                    raise Exception(f'Cannot access file at \"{directory}\"')
            QMessageBox.information(self, 'Success', f'Launching: {final_status}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while launching the programs: {e}')
    
    def loadConfig(self):
        config = configparser.ConfigParser()
        
        if not os.path.isfile('kh2fmLauncherConfig.ini'):
            config['Settings'] = {
            'tracker': '',
            'seed_gen': '',
            'mods_manager': '',
            'livesplit': ''
            }
            with open('kh2fmLauncherConfig.ini', 'w') as configfile:
                config.write(configfile)
        
        config.read('kh2fmLauncherConfig.ini')
        self.text_boxes[0].setText(config.get('Settings', 'tracker'))
        self.text_boxes[1].setText(config.get('Settings', 'seed_gen'))
        self.text_boxes[2].setText(config.get('Settings', 'mods_manager'))
        self.text_boxes[3].setText(config.get('Settings', 'livesplit'))
        
    
    def saveConfig(self, index, file):
        config = configparser.ConfigParser()
        
        config.read('kh2fmLauncherConfig.ini')
        
        if index == 0:
            config.set('Settings', 'tracker', file)
        if index == 1:
            config.set('Settings', 'seed_gen', file)
        if index == 2:
            config.set('Settings', 'mods_manager', file)
        if index == 3:
            config.set('Settings', 'livesplit', file)
        
        with open('kh2fmLauncherConfig.ini', 'w') as configfile:
            config.write(configfile)
        
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())