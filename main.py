import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QTableWidget, QTableWidgetItem, QTextEdit, QLabel, QHBoxLayout, QInputDialog, QHeaderView, QSpinBox
)
from PyQt5.QtGui import QFont

class RotationalGameplayApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sims 2 Rotational Gameplay Tracker")
        self.setGeometry(100, 100, 1200, 1000)  # Start with a specific window size

        self.families = []
        self.load_data()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create font
        font = QFont("ITC Benguiat Gothic", 14)

        # Create family input
        self.family_input = QLineEdit(self)
        self.family_input.setPlaceholderText("Enter family name")
        self.family_input.setFont(font)
        layout.addWidget(self.family_input)

        # Create add family button with style
        button_style = """
                    QPushButton {
                        color: rgb(10, 18, 101);
                        background-color: rgb(174,189,255); /* Blue color similar to Sims 2 */
                        border: 3px solid rgb(10, 18, 101); /* Border color */
                        border-radius: 10px;
                        padding: 10px 20px;
                    }
                    QPushButton:hover {
                        background-color: rgb(155,167,255);  /* Darker shade when hovered */
                    }
                """

        self.add_family_button = QPushButton("Add Family", self)
        self.add_family_button.setStyleSheet(button_style)
        self.add_family_button.setFont(font)
        self.add_family_button.clicked.connect(self.add_family)
        layout.addWidget(self.add_family_button)

        # Create input for number of days per turn
        self.days_input = QSpinBox(self)
        self.days_input.setRange(1, 100)
        self.days_input.setValue(4)  # Default value
        self.days_input.setFont(font)
        layout.addWidget(QLabel("Set number of days per turn:"))
        layout.addWidget(self.days_input)

        # Create table to display families
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Family", "Days Played", "Family Members", "Actions"])
        self.table.setColumnWidth(2, 500)
        self.table.setColumnWidth(3, 400)
        layout.addWidget(self.table)

        # Create text edit widget for additional information
        self.info_display = QTextEdit(self)
        self.info_display.setReadOnly(True)
        self.info_display.setFont(font)
        self.info_display.setStyleSheet(
            "background-color: rgb(174,189,255); color: rgb(10, 18, 101); border: 3px solid rgb(10, 18, 101); padding: 10px 20px; border-radius: 10px;")
        self.info_display.setLineWrapMode(QTextEdit.NoWrap)
        layout.addWidget(self.info_display)

        # Initial update of table
        self.update_table()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set the main window background color
        self.setStyleSheet("background-color: rgb(174,189,255);")

    def add_family(self):
        family_name = self.family_input.text()
        if family_name:
            self.families.append({"name": family_name, "days_played": 0, "members": []})
            self.family_input.clear()
            self.update_table()
            self.save_data()
            self.info_display.append(f"Added family: {family_name}")

    def add_family_member(self, family_index):
        family_name = self.families[family_index]["name"]
        member_name, ok = QInputDialog.getText(self, 'Add Family Member',
                                               f'Enter the name of the new member for {family_name}:')
        if ok and member_name:
            self.families[family_index]["members"].append(member_name)
            self.update_table()
            self.save_data()
            self.info_display.append(f"Added member: {member_name} to family: {family_name}")

    def remove_family_member(self, family_index):
        family_name = self.families[family_index]["name"]
        members = self.families[family_index]["members"]
        if not members:
            self.info_display.append(f"No members to remove in family: {family_name}")
            return

        member_name, ok = QInputDialog.getItem(self, 'Remove Family Member',
                                               f'Select the member to remove from {family_name}:', members, 0, False)
        if ok and member_name:
            self.families[family_index]["members"].remove(member_name)
            self.update_table()
            self.save_data()
            self.info_display.append(f"Removed member: {member_name} from family: {family_name}")

    def increment_days_played(self, family_index):
        days_to_add = self.days_input.value()
        self.families[family_index]["days_played"] += days_to_add
        self.update_table()
        self.save_data()
        family_name = self.families[family_index]["name"]
        self.info_display.append(f"Incremented days played for {family_name} by {days_to_add} days")

    def update_table(self):
        self.table.setRowCount(len(self.families))
        for row, family in enumerate(self.families):
            self.table.setItem(row, 0, QTableWidgetItem(family["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(family["days_played"])))
            members = ", ".join(family.get("members", []))
            self.table.setItem(row, 2, QTableWidgetItem(members))

            # Add buttons to manage family members
            buttons_layout = QHBoxLayout()
            add_member_button = QPushButton("Add Member")
            remove_member_button = QPushButton("Remove Member")
            played_button = QPushButton("Played")

            button_style = """
                QPushButton {
                    color: rgb(10, 18, 101);
                    background-color: rgb(174,189,255);
                    border: 3px solid rgb(10, 18, 101);
                    border-radius: 10px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: rgb(155,167,255);
                }
            """
            add_member_button.setStyleSheet(button_style)
            remove_member_button.setStyleSheet(button_style)
            played_button.setStyleSheet(button_style)

            add_member_button.clicked.connect(lambda checked, index=row: self.add_family_member(index))
            remove_member_button.clicked.connect(lambda checked, index=row: self.remove_family_member(index))
            played_button.clicked.connect(lambda checked, index=row: self.increment_days_played(index))

            buttons_layout.addWidget(add_member_button)
            buttons_layout.addWidget(remove_member_button)
            buttons_layout.addWidget(played_button)

            buttons_widget = QWidget()
            buttons_widget.setLayout(buttons_layout)
            self.table.setCellWidget(row, 3, buttons_widget)

    def load_data(self):
        try:
            with open("families.json", "r") as file:
                self.families = json.load(file)
            for family in self.families:
                if "members" not in family:
                    family["members"] = []
        except (FileNotFoundError, json.JSONDecodeError):
            self.families = []

    def save_data(self):
        with open("families.json", "w") as file:
            json.dump(self.families, file, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RotationalGameplayApp()
    window.show()
    sys.exit(app.exec_())
