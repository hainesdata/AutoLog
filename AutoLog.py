import sys
import time

import dateutil
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QFileDialog, QMessageBox

import gui

version = '0.0.8'

try:
    recent = pd.read_csv('recent.dat')
    name = recent.loc[0, 'recent:']
except:
    recent_log = pd.DataFrame(columns=['recent:'])
    recent_log['recent:'] = ['table.log']
    recent_log.to_csv('recent.dat', index_label=False)
    name = 'table.log'

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
        input_table = pd.DataFrame(columns=['Date', 'Miles', 'Category', 'Brand', 'Product', 'Part Number', 'Cost', 'Notes'])
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
        ui.miles_box.toPlainText(), ui.cat_drop.currentText(), ui.brand_box.toPlainText(),
        ui.product_box.toPlainText(), ui.pn_box.toPlainText(), ui.cost_box.toPlainText(), ui.notes_box.toPlainText()
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


def validate(values):
    error_raised = False
    if not values[1].isnumeric():
        invalid_mileage()
        error_raised = True
        values[1] = 0
    if not values[6].isnumeric():
        invalid_price()
        error_raised = True
        values[5] = 0
    if error_raised:
        raise SyntaxError()
    return values


def invalid_mileage():
    box = QtWidgets.QMessageBox()
    box.setWindowTitle('Error Adding Entry')
    box.setText(
        'Validation Error 200: The mileage you entered is invalid: make sure you are not using commas, symbols, '
        'spaces, or new lines.')
    box.setIcon(QMessageBox.Critical)
    box.exec_()


def invalid_price():
    box = QtWidgets.QMessageBox()
    box.setWindowTitle('Error Adding Entry')
    box.setText(
        'Validation Error 300: The price you entered is invalid: make sure symbols, commas, spaces, or new lines'
        ' are not used.')
    box.setIcon(QMessageBox.Critical)
    box.exec_()


def add_entry(values):
    try:
        values = validate(values)
    except SyntaxError:
        return
    wrk_table.loc[len(wrk_table)] = values
    view_table(ui)
    save_csv()
    show_add_success()


def show_add_success():
    succ = QMessageBox()
    succ.setIcon(QMessageBox.Information)
    succ.setText('Record successfully added.')
    succ.exec_()


def rmv_entry():
    global wrk_table
    selected = ui.display_table.selectionModel().selectedRows()
    for row in selected:
        queued_row = row.row()
        wrk_table = wrk_table.drop(queued_row.__index__())
    wrk_table = wrk_table.reset_index(drop=True)
    view_table(ui)
    save_csv()


def save_csv():
    wrk_table.to_csv(f'{name}', index_label=False)
    recent_log = pd.DataFrame(columns=['recent:'])
    recent_log['recent:'] = [f'{name}']
    recent_log.to_csv('recent.dat', index_label=False)


def select_file():
    global input_table, name
    (import_name, filetype) = QFileDialog.getOpenFileName()
    name = import_name
    print(name)
    input_table = pd.read_csv(name)
    init()


try:
    init()
    MainWindow.show()
except:
    crit = QMessageBox()
    crit.setText('Critical runtime error: AutoLog must close. Any previously added entries should be saved.')
    crit.setIcon(QMessageBox.Critical)
    crit.exec_()

sys.exit(app.exec_())
