from typing import Tuple, Dict
from functools import partial
from datetime import datetime

from vnpy.trader.ui import QtWidgets, QtCore
from vnpy.trader.engine import MainEngine, EventEngine
from vnpy.trader.constant import Interval, Exchange

from ..engine import APP_NAME, ManagerEngine


class ManagerWidget(QtWidgets.QWidget):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__()

        self.engine: ManagerEngine = main_engine.get_engine(APP_NAME)

        self.tree_items: Dict[Tuple, QtWidgets.QTreeWidgetItem] = {}

        self.init_ui()

    def init_ui(self) -> None:
        """"""
        # BRIAN: 数据管理 - Data Management
        self.setWindowTitle("Data Management")

        self.init_tree()
        self.init_table()

        # BRIAN: 刷新 - Refresh
        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_tree)

        # BRIAN: 导入数据 - Import Data
        import_button = QtWidgets.QPushButton("Import Data")
        import_button.clicked.connect(self.import_data)

        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(refresh_button)
        hbox1.addStretch()
        hbox1.addWidget(import_button)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.tree)
        hbox2.addWidget(self.table)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def init_tree(self) -> None:
        """"""
        # BRIAN: 数据 - Data
        # BRIAN: 本地代码 - Native Symbol
        # BRIAN: 代码 - Symbol
        # BRIAN: 交易所 - Exchange
        # BRIAN: 数据量 - Amount of Data
        # BRIAN: 开始时间 - Start time
        # BRIAN: 结束时间 - End time
        labels = [
            "Data",
            "Native Symbol",
            "Symbol",
            "Exchange",
            "Amount of Data",
            "Start time",
            "End time",
            "",
            ""
        ]

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(len(labels))
        self.tree.setHeaderLabels(labels)

        root = QtWidgets.QTreeWidgetItem(self.tree)
        # BRIAN: K线数据 - K-line data
        root.setText(0, "K-line data")
        root.setExpanded(True)

        self.minute_child = QtWidgets.QTreeWidgetItem()
        # BRIAN: 分钟线 - Minute line        
        self.minute_child.setText(0, "Minute line")
        root.addChild(self.minute_child)

        self.hour_child = QtWidgets.QTreeWidgetItem()
        # BRIAN: 小时线 - Hour line
        self.hour_child.setText(0, "Hour line")
        root.addChild(self.hour_child)

        self.daily_child = QtWidgets.QTreeWidgetItem()
        # BRIAN: 日线 - Daily line
        self.daily_child.setText(0, "Daily line")
        root.addChild(self.daily_child)

    def init_table(self) -> None:
        """"""
        # BRIAN: 时间 - Time
        # BRIAN: 开盘价 - Open price
        # BRIAN: 最高价 - Highest price
        # BRIAN: 最低价 - Lowest price
        # BRIAN: 收盘价 - Close price
        # BRIAN: 成交量 - Volume
        # BRIAN: 持仓量 - Open interest
        labels = [
            "Time",
            "Open price",
            "Highest price",
            "Lowest price",
            "Close price",
            "Volume",
            "Open interest"
        ]

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(len(labels))
        self.table.setHorizontalHeaderLabels(labels)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

    def refresh_tree(self) -> None:
        """"""
        data = self.engine.get_bar_data_available()

        for d in data:
            key = (d["symbol"], d["exchange"], d["interval"])
            item = self.tree_items.get(key, None)

            if not item:
                item = QtWidgets.QTreeWidgetItem()
                self.tree_items[key] = item

                item.setText(1, ".".join([d["symbol"], d["exchange"]]))
                item.setText(2, d["symbol"])
                item.setText(3, d["exchange"])

                if d["interval"] == Interval.MINUTE.value:
                    self.minute_child.addChild(item)
                elif d["interval"] == Interval.HOUR.value:
                    self.hour_child.addChild(item)
                else:
                    self.daily_child.addChild(item)

                # BRIAN: 导出 - Export
                output_button = QtWidgets.QPushButton("Export")
                output_func = partial(
                    self.output_data,
                    d["symbol"],
                    Exchange(d["exchange"]),
                    Interval(d["interval"]),
                    d["start"],
                    d["end"]
                )
                output_button.clicked.connect(output_func)

                # BRIAN: 查看 - Show
                show_button = QtWidgets.QPushButton("Show")
                show_func = partial(
                    self.show_data,
                    d["symbol"],
                    Exchange(d["exchange"]),
                    Interval(d["interval"]),
                    d["start"],
                    d["end"]
                )
                show_button.clicked.connect(show_func)

                self.tree.setItemWidget(item, 7, show_button)
                self.tree.setItemWidget(item, 8, output_button)

            item.setText(4, str(d["count"]))
            item.setText(5, d["start"].strftime("%Y-%m-%d %H:%M:%S"))
            item.setText(6, d["end"].strftime("%Y-%m-%d %H:%M:%S"))

        self.minute_child.setExpanded(True)
        self.hour_child.setExpanded(True)
        self.daily_child.setExpanded(True)

    def import_data(self) -> None:
        """"""
        dialog = ImportDialog()
        n = dialog.exec_()
        if n != dialog.Accepted:
            return

        file_path = dialog.file_edit.text()
        symbol = dialog.symbol_edit.text()
        exchange = dialog.exchange_combo.currentData()
        interval = dialog.interval_combo.currentData()
        datetime_head = dialog.datetime_edit.text()
        open_head = dialog.open_edit.text()
        low_head = dialog.low_edit.text()
        high_head = dialog.high_edit.text()
        close_head = dialog.close_edit.text()
        volume_head = dialog.volume_edit.text()
        open_interest_head = dialog.open_interest_edit.text()
        datetime_format = dialog.format_edit.text()

        start, end, count = self.engine.import_data_from_csv(
            file_path,
            symbol,
            exchange,
            interval,
            datetime_head,
            open_head,
            high_head,
            low_head,
            close_head,
            volume_head,
            open_interest_head,
            datetime_format
        )

        # BRIAN: CSV载入成功 - CSV loaded successfully
        # BRIAN: 代码 - Symbol
        # BRIAN: 交易所 - Exchange
        # BRIAN: 周期 - Interval
        # BRIAN: 起始 - Start
        # BRIAN: 结束 - End
        # BRIAN: 总数量 - Total amount
        msg = f"\
        CSV loaded successfully\n\
        Symbol: {symbol}\n\
        Exchange: {exchange.value}\n\
        Interval: {interval.value}\n\
        Start: {start}\n\
        End: {end}\n\
        Total amount: {count}\n\
        "

        # BRIAN: 载入成功 - Loaded successfully
        QtWidgets.QMessageBox.information(self, "Loaded successfully!", msg)

    def output_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> None:
        """"""
        # Get output date range
        dialog = DateRangeDialog(start, end)
        n = dialog.exec_()
        if n != dialog.Accepted:
            return
        start, end = dialog.get_date_range()

        # Get output file path
        # BRIAN: 导出数据 - Export data
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export data",
            "",
            "CSV(*.csv)"
        )
        if not path:
            return

        result = self.engine.output_data_to_csv(
            path,
            symbol,
            exchange,
            interval,
            start,
            end
        )

        # BRIAN: 导出失败 - Export failed
        # BRIAN: 该文件已在其他程序中打开，请关闭相关程序后再尝试导出数据
        # The file is already open in another program, 
        # please close the program before trying to export the data
        if not result:
            QtWidgets.QMessageBox.warning(
                self,
                "Export failed!",
                "The file is already open in another program, " + \
                "please close the program before trying to export the data"
            )

    def show_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> None:
        """"""
        # Get output date range
        dialog = DateRangeDialog(start, end)
        n = dialog.exec_()
        if n != dialog.Accepted:
            return
        start, end = dialog.get_date_range()

        bars = self.engine.load_bar_data(
            symbol,
            exchange,
            interval,
            start,
            end
        )

        self.table.setRowCount(0)
        self.table.setRowCount(len(bars))

        for row, bar in enumerate(bars):
            self.table.setItem(row, 0, DataCell(bar.datetime.strftime("%Y-%m-%d %H:%M:%S")))
            self.table.setItem(row, 1, DataCell(str(bar.open_price)))
            self.table.setItem(row, 2, DataCell(str(bar.high_price)))
            self.table.setItem(row, 3, DataCell(str(bar.low_price)))
            self.table.setItem(row, 4, DataCell(str(bar.close_price)))
            self.table.setItem(row, 5, DataCell(str(bar.volume)))
            self.table.setItem(row, 6, DataCell(str(bar.open_interest)))

    def show(self) -> None:
        """"""
        self.showMaximized()


class DataCell(QtWidgets.QTableWidgetItem):
    """"""

    def __init__(self, text: str = ""):
        super().__init__(text)

        self.setTextAlignment(QtCore.Qt.AlignCenter)


class DateRangeDialog(QtWidgets.QDialog):
    """"""

    def __init__(self, start: datetime, end: datetime, parent=None):
        """"""
        super().__init__(parent)

        # BRIAN: 选择数据区间 - Select data interval 
        self.setWindowTitle("Select data interval")

        self.start_edit = QtWidgets.QDateEdit(
            QtCore.QDate(
                start.year,
                start.month,
                start.day
            )
        )
        self.end_edit = QtWidgets.QDateEdit(
            QtCore.QDate(
                end.year,
                end.month,
                end.day
            )
        )

        # BRIAN: 确定 - Apply
        button = QtWidgets.QPushButton("Apply")
        button.clicked.connect(self.accept)

        form = QtWidgets.QFormLayout()
        # BRIAN: 开始时间 - Start time
        form.addRow("Start time", self.start_edit)
        # BRIAN: 结束时间 - End time
        form.addRow("End time", self.end_edit)
        form.addRow(button)

        self.setLayout(form)

    def get_date_range(self) -> Tuple[datetime, datetime]:
        """"""
        start = self.start_edit.date().toPyDate()
        end = self.end_edit.date().toPyDate()
        return start, end


class ImportDialog(QtWidgets.QDialog):
    """"""

    def __init__(self, parent=None):
        """"""
        super().__init__()

        # BRIAN: 从CSV文件导入数据 - Importing data from a CSV file
        self.setWindowTitle("Importing data from a CSV file")
        self.setFixedWidth(300)

        self.setWindowFlags(
            (self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
            & ~QtCore.Qt.WindowMaximizeButtonHint)

        # BRIAN: 选择文件 - Select file
        file_button = QtWidgets.QPushButton("Select file")
        file_button.clicked.connect(self.select_file)

        # BRIAN: 确定 - Apply
        load_button = QtWidgets.QPushButton("Apply")
        load_button.clicked.connect(self.accept)

        self.file_edit = QtWidgets.QLineEdit()
        self.symbol_edit = QtWidgets.QLineEdit()

        self.exchange_combo = QtWidgets.QComboBox()
        for i in Exchange:
            self.exchange_combo.addItem(str(i.name), i)

        self.interval_combo = QtWidgets.QComboBox()
        for i in Interval:
            self.interval_combo.addItem(str(i.name), i)

        self.datetime_edit = QtWidgets.QLineEdit("datetime")
        self.open_edit = QtWidgets.QLineEdit("open")
        self.high_edit = QtWidgets.QLineEdit("high")
        self.low_edit = QtWidgets.QLineEdit("low")
        self.close_edit = QtWidgets.QLineEdit("close")
        self.volume_edit = QtWidgets.QLineEdit("volume")
        self.open_interest_edit = QtWidgets.QLineEdit("open_interest")

        self.format_edit = QtWidgets.QLineEdit("%Y-%m-%d %H:%M:%S")

        # BRIAN: 合约信息 - Contract information
        info_label = QtWidgets.QLabel("Contract information")
        info_label.setAlignment(QtCore.Qt.AlignCenter)

        # BRIAN: 表头信息 - Header information
        head_label = QtWidgets.QLabel("Header information")
        head_label.setAlignment(QtCore.Qt.AlignCenter)

        # BRIAN: 格式信息 - Format information
        format_label = QtWidgets.QLabel("Format information")
        format_label.setAlignment(QtCore.Qt.AlignCenter)

        form = QtWidgets.QFormLayout()
        form.addRow(file_button, self.file_edit)
        form.addRow(QtWidgets.QLabel())
        form.addRow(info_label)
        # BRIAN: 代码 - Symbol
        form.addRow("Symbol", self.symbol_edit)
        # BRIAN: 交易所 - Exchange
        form.addRow("Exchange", self.exchange_combo)
        # BRIAN: 周期 - Interval
        form.addRow("Interval", self.interval_combo)
        form.addRow(QtWidgets.QLabel())
        form.addRow(head_label)
        # BRIAN: 时间戳 - Datetime
        form.addRow("Datetime", self.datetime_edit)
        # BRIAN: 开盘价 - Open price
        form.addRow("Open price", self.open_edit)
        # BRIAN: 最高价 - Highest price
        form.addRow("Highest price", self.high_edit)
        # BRIAN: 最低价 - Lowest price
        form.addRow("Lowest price", self.low_edit)
        # BRIAN: 收盘价 - Close price
        form.addRow("Lowest price", self.close_edit)
        # BRIAN: 成交量 - Volume
        form.addRow("Volume", self.volume_edit)
        # BRIAN: 持仓量 - Open interest
        form.addRow("Open interest", self.open_interest_edit)
        form.addRow(QtWidgets.QLabel())
        form.addRow(format_label)
        # BRIAN: 时间格式 - Time format
        form.addRow("Time format", self.format_edit)
        form.addRow(QtWidgets.QLabel())
        form.addRow(load_button)

        self.setLayout(form)

    def select_file(self):
        """"""
        result: str = QtWidgets.QFileDialog.getOpenFileName(
            self, filter="CSV (*.csv)")
        filename = result[0]
        if filename:
            self.file_edit.setText(filename)
