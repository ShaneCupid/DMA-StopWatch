from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QHBoxLayout, QInputDialog, QFormLayout, QDialog, QShortcut, QFrame
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QKeySequence, QPalette
import sys

class TimeLogger(QWidget):
    def __init__(self):
        super().__init__()

        # Create the timer and time label
        self.timer = QTimer()
        self.time = QTime(0, 0)

        # Create the layout and add the widgets
        self.layout = QVBoxLayout()

        # Create the initial dialog box to get interviewer and interviewee names
        self.interviewer_name, self.interviewee_name = self.get_names()

        # Create the time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("background-color: #2F4F4F; color: #ADD8E6; font-size: 60px;")
        self.time_label.setText(self.time.toString())

        # Create the start, pause, continue, reset and add time buttons
        self.start_button = QPushButton('Start')
        self.start_button.setStyleSheet("background-color: #ADD8E6; color: black; border-radius: 10px; font-family: Sans-serif; font-size: 20px;")
        self.pause_button = QPushButton('Pause')
        self.pause_button.setStyleSheet("background-color: #FFFF00; color: black; border-radius: 10px; font-family: Sans-serif; font-size: 20px;")
        self.continue_button = QPushButton('Continue')
        self.continue_button.setStyleSheet("background-color: #FFC0CB; color: black; border-radius: 10px; font-family: Sans-serif; font-size: 20px;")
        self.reset_button = QPushButton('Reset')
        self.reset_button.setStyleSheet("background-color: #FF69B4; color: black; border-radius: 10px; font-family: Sans-serif; font-size: 20px;")
        self.add_time_button = QPushButton('')  # New button with no text initially
        self.add_time_button.setStyleSheet("background-color: #FFC0CB; color: black; border-radius: 10px; font-family: Sans-serif; font-size: 20px;")

        # Initially hide the pause, continue, reset and add time buttons
        self.pause_button.hide()
        self.continue_button.hide()
        self.reset_button.hide()
        self.add_time_button.hide()

        # Create a horizontal box layout for the start, pause, continue, reset and add time buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.continue_button)
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.add_time_button)  # Add the new button to the layout

        # Add the widgets to the layout
        self.layout.addWidget(self.time_label)
        self.layout.addLayout(self.button_layout)

        # Set the layout
        self.setLayout(self.layout)

        # Connect the buttons to their respective functions
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.continue_button.clicked.connect(self.continue_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.add_time_button.clicked.connect(self.add_time)  # Connect the new button to its function

        # Connect the timer timeout signal to the update_time function
        self.timer.timeout.connect(self.update_time)

        # Create a shortcut for the space bar and connect it to the add_time function
        self.space_shortcut = QShortcut(QKeySequence(' '), self)
        self.space_shortcut.activated.connect(self.add_time)

        # Initialize the question counter
        self.question_counter = 0

    def get_names(self):
        dialog = QDialog()
        dialog.setWindowTitle("Enter Names")
        dialog.setStyleSheet("background-color: #2F4F4F; color: #ADD8E6; font-family: Sans-serif; font-size: 20px;")
        layout = QFormLayout(dialog)

        interviewer_name_edit = QLineEdit(dialog)
        interviewer_name_edit.setPlaceholderText("Interviewer Name")
        interviewer_name_edit.setStyleSheet("background-color: #2F4F4F; color: #ADD8E6; border: none; font-family: Sans-serif; font-size: 20px;")
        interviewee_name_edit = QLineEdit(dialog)
        interviewee_name_edit.setPlaceholderText("Interviewee Name")
        interviewee_name_edit.setStyleSheet("background-color: #2F4F4F; color: #ADD8E6; border: none; font-family: Sans-serif; font-size: 20px;")
        layout.addRow(interviewer_name_edit)
        layout.addRow(interviewee_name_edit)

        ok_button = QPushButton("Proceed", dialog)
        ok_button.setStyleSheet("background-color: #FFC0CB; color: black; border-radius: 10px; font-family: Sans-serif; font-size: 20px;")
        layout.addRow(ok_button)

        ok_button.clicked.connect(dialog.accept)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            interviewer_name = interviewer_name_edit.text()
            interviewee_name = interviewee_name_edit.text()
            if interviewer_name and interviewee_name:
                return interviewer_name, interviewee_name
            else:
                QMessageBox.warning(self, "Warning", "Both fields must be filled.")
                return self.get_names()
        else:
            sys.exit()

    def start_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            self.start_button.hide()
            self.pause_button.show()
            self.reset_button.show()
            self.add_time_button.show()

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.hide()
            self.continue_button.show()

    def continue_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            self.continue_button.hide()
            self.pause_button.show()

    def reset_timer(self):
        self.timer.stop()
        self.time = QTime(0, 0)
        self.time_label.setText(self.time.toString())
        self.start_button.show()
        self.pause_button.hide()
        self.continue_button.hide()
        self.reset_button.hide()
        self.add_time_button.hide()
        self.question_counter = 0
        self.add_time_button.setText('')

    def update_time(self):
        self.time = self.time.addSecs(1)
        self.time_label.setText(self.time.toString())

    def add_time(self):
        self.question_counter += 1
        self.add_time_button.setText(f'Q{self.question_counter}')
        self.write_timestamp_to_file(f'Q{self.question_counter} - {self.time.toString()}')
        print(f'Q{self.question_counter} - {self.time.toString()}')
        self.time_label.setStyleSheet("background-color: #2F4F4F; color: #ADD8E6; font-size: 60px;")

    def write_timestamp_to_file(self, timestamp):
        with open(f'{self.interviewer_name}_{self.interviewee_name}_timestamps.txt', 'a') as f:
            f.write(f'{timestamp}\n')

    def closeEvent(self, event):
        self.timer.stop()
        self.write_timestamp_to_file(f'Q{self.question_counter} - {self.time.toString()}')
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TimeLogger()
    window.setStyleSheet("background-color: #2F4F4F;")
    window.show()

    sys.exit(app.exec_())
