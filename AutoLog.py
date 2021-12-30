import time
import dateutil
import gui
import pandas as pd
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

version = '0.0.2'
name = 'test'

# Read CSV
input_table = pd.read_csv(f'data/{name}.csv')

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)

# Set label attribute here
add_success_label = ui.label


def view_table(input_ui):
    # Specify table dimensions
    n_rows = len(input_table.index)
    n_cols = len(input_table.columns)
    input_ui.display_table.setColumnCount(n_cols)
    input_ui.display_table.setRowCount(n_rows)
    # Load data
    for i in range(n_rows):
        for j in range(n_cols):
            input_ui.display_table.setItem(i, j, QTableWidgetItem(str(input_table.iat[i, j])))
    # Update dimensions
    input_ui.display_table.resizeColumnsToContents()
    input_ui.display_table.resizeRowsToContents()


def add_entry(values):
    input_table.loc[len(input_table)] = values
    view_table(ui)
    save_csv()


def show_add_success():
    add_success_label.show()
    time.sleep(3)
    add_success_label.hide()


def save_csv():
    input_table.to_csv(f'data/{name}.csv', index_label=False)


view_table(ui)
add_success_label.hide()
# Update name.csv and save
ui.actionSave.triggered.connect(lambda: save_csv())
# Add record
ui.addEntryButton.clicked.connect(lambda: add_entry([
    str(dateutil.parser.parse(ui.date_box.date().toString()).date().strftime('%-m/%-d/%y')),
    ui.miles_box.toPlainText(), ui.cat_drop.currentText(), ui.part_drop.currentText(),
    ui.product_box.toPlainText(), ui.cost_box.toPlainText(), ui.notes_box.toPlainText()
]))

MainWindow.show()
sys.exit(app.exec_())
