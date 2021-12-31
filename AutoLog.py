import sys
import time

import dateutil
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QFileDialog

import gui

version = '0.0.5'

try:
    recent = pd.read_csv('data/recent.dat')
    name = recent.loc[0, 'recent:']
except:
    recent_log = pd.DataFrame(columns=['recent:'])
    recent_log['recent:'] = ['data/table.log']
    recent_log.to_csv('data/recent.dat', index_label=False)
    name = 'data/table.log'


# Read CSV
input_table = None
wrk_table = None
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
add_success_label = None


def init():
    global wrk_table, input_table
    try:
        input_table = pd.read_csv(name)
    except:
        input_table = pd.DataFrame(columns=['Date', 'Miles', 'Category', 'Part', 'Product', 'Cost', 'Notes'])
    # Title
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle(f'AutoLog v{version}')
    ui.display_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    wrk_table = input_table
    wrk_table.Miles = wrk_table.Miles.fillna(0)
    wrk_table.Miles = wrk_table.Miles.astype('int')
    view_table(ui)

    # Set label attribute here
    global add_success_label
    add_success_label = ui.label
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

    # Import file
    ui.actionImport.triggered.connect(lambda: select_file())


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
    wrk_table.to_csv(f'{name}', index_label=False)
    recent_log = pd.DataFrame(columns=['recent:'])
    recent_log['recent:'] = [f'{name}']
    recent_log.to_csv('data/recent.dat', index_label=False)


def select_file():
    global input_table, name
    (import_name, filetype) = QFileDialog.getOpenFileName()
    name = import_name
    print(name)
    input_table = pd.read_csv(name)
    init()


init()
MainWindow.show()
sys.exit(app.exec_())
