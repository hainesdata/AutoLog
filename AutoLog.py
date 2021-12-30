import time
import dateutil
import gui
import pandas as pd
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

version = '0.0.3'
name = 'test'

# Read CSV
input_table = pd.read_csv(f'data/{name}.log')
wrk_table = input_table
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

# Title
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.setWindowTitle(f'AutoLog v{version}')
ui.display_table.setSelectionBehavior(QAbstractItemView.SelectRows)

# Set label attribute here
add_success_label = ui.label


def view_table(input_ui):
    # Specify table dimensions
    n_rows = len(wrk_table.index)
    n_cols = len(wrk_table.columns)
    input_ui.display_table.setColumnCount(n_cols)
    input_ui.display_table.setRowCount(n_rows)
    # Load data
    for i in range(n_rows):
        for j in range(n_cols):
            input_ui.display_table.setItem(i, j, QTableWidgetItem(str(wrk_table.iat[i, j])))
    # Update dimensions
    input_ui.display_table.resizeColumnsToContents()
    input_ui.display_table.resizeRowsToContents()


def add_entry(values):
    wrk_table.loc[len(wrk_table)] = values
    view_table(ui)
    save_csv()


def show_add_success():
    add_success_label.show()
    time.sleep(3)
    add_success_label.hide()


def rmv_entry():
    global wrk_table
    selected = ui.display_table.selectionModel().selectedRows()
    for row in selected:
        queued_row = row.row()
        # ui.display_table.removeRow(queued_row)
        wrk_table = wrk_table.drop(queued_row.__index__())
        wrk_table.reset_index()
    view_table(ui)
    save_csv()


def save_csv():
    wrk_table.to_csv(f'data/{name}.log', index_label=False)


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

# Remove record
ui.addEntryButton_2.clicked.connect(lambda: rmv_entry())

MainWindow.show()
sys.exit(app.exec_())
