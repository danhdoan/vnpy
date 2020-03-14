import csv
from datetime import datetime, timedelta

import numpy as np
import pyqtgraph as pg

from vnpy.trader.constant import Interval, Direction, Offset
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import QtCore, QtWidgets, QtGui
from vnpy.trader.ui.widget import BaseMonitor, BaseCell, DirectionCell, EnumCell
from vnpy.trader.ui.editor import CodeEditor
from vnpy.event import Event, EventEngine
from vnpy.chart import ChartWidget, CandleItem, VolumeItem
from vnpy.trader.utility import load_json, save_json

from ..engine import (
    APP_NAME,
    EVENT_BACKTESTER_LOG,
    EVENT_BACKTESTER_BACKTESTING_FINISHED,
    EVENT_BACKTESTER_OPTIMIZATION_FINISHED,
    OptimizationSetting
)


class BacktesterManager(QtWidgets.QWidget):
    """"""

    setting_filename = "cta_backtester_setting.json"

    signal_log = QtCore.pyqtSignal(Event)
    signal_backtesting_finished = QtCore.pyqtSignal(Event)
    signal_optimization_finished = QtCore.pyqtSignal(Event)

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine

        self.backtester_engine = main_engine.get_engine(APP_NAME)
        self.class_names = []
        self.settings = {}

        self.target_display = ""

        self.init_ui()
        self.register_event()
        self.backtester_engine.init_engine()
        self.init_strategy_settings()

    def init_strategy_settings(self):
        """"""
        self.class_names = self.backtester_engine.get_strategy_class_names()

        for class_name in self.class_names:
            setting = self.backtester_engine.get_default_setting(class_name)
            self.settings[class_name] = setting

        self.class_combo.addItems(self.class_names)

    def init_ui(self):
        """"""

        # BRIAN: CTA回测 - CTA Backtest
        self.setWindowTitle("CTA Backtest")

        # Setting Part
        self.class_combo = QtWidgets.QComboBox()

        self.symbol_line = QtWidgets.QLineEdit("IF88.CFFEX")

        self.interval_combo = QtWidgets.QComboBox()
        for inteval in Interval:
            self.interval_combo.addItem(inteval.value)

        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=3 * 365)

        self.start_date_edit = QtWidgets.QDateEdit(
            QtCore.QDate(
                start_dt.year,
                start_dt.month,
                start_dt.day
            )
        )
        self.end_date_edit = QtWidgets.QDateEdit(
            QtCore.QDate.currentDate()
        )

        self.rate_line = QtWidgets.QLineEdit("0.000025")
        self.slippage_line = QtWidgets.QLineEdit("0.2")
        self.size_line = QtWidgets.QLineEdit("300")
        self.pricetick_line = QtWidgets.QLineEdit("0.2")
        self.capital_line = QtWidgets.QLineEdit("1000000")

        self.inverse_combo = QtWidgets.QComboBox()

        # BRIAN: 正向 - Forward
        # BRIAN: 反向 - Reverse
        self.inverse_combo.addItems(["Forward", "Reverse"])

        # BRIAN: 开始回测 - Start backtesting
        backtesting_button = QtWidgets.QPushButton("Start backtesting")
        backtesting_button.clicked.connect(self.start_backtesting)

        # BRIAN: 参数优化 - Parameter Optimization
        optimization_button = QtWidgets.QPushButton("Parameter Optimization")
        optimization_button.clicked.connect(self.start_optimization)

        # BRIAN: 优化结果 - Optimization Results
        self.result_button = QtWidgets.QPushButton("Optimization Results")
        self.result_button.clicked.connect(self.show_optimization_result)
        self.result_button.setEnabled(False)

        # BRIAN: 下载数据 - Download Data
        downloading_button = QtWidgets.QPushButton("Download Data")
        downloading_button.clicked.connect(self.start_downloading)

        # BRIAN: 委托记录 - Order Book
        self.order_button = QtWidgets.QPushButton("Order Book")
        self.order_button.clicked.connect(self.show_backtesting_orders)
        self.order_button.setEnabled(False)

        # BRIAN: 成交记录 - Transaction Record
        self.trade_button = QtWidgets.QPushButton("Transaction Record")
        self.trade_button.clicked.connect(self.show_backtesting_trades)
        self.trade_button.setEnabled(False)

        # BRIAN: 每日盈亏 - Daily Profit/Loss
        self.daily_button = QtWidgets.QPushButton("Daily Profit/Loss")
        self.daily_button.clicked.connect(self.show_daily_results)
        self.daily_button.setEnabled(False)

        # BRIAN: K线图表 - K-line chart
        self.candle_button = QtWidgets.QPushButton("K-line chart")
        self.candle_button.clicked.connect(self.show_candle_chart)
        self.candle_button.setEnabled(False)

        # BRIAN: 代码编辑 - Code Editing
        edit_button = QtWidgets.QPushButton("Code Editing")
        edit_button.clicked.connect(self.edit_strategy_code)

        # BRIAN: 策略重载 - Strategy Reload
        reload_button = QtWidgets.QPushButton("Strategy Reload")
        reload_button.clicked.connect(self.reload_strategy_class)

        for button in [
            backtesting_button,
            optimization_button,
            downloading_button,
            self.result_button,
            self.order_button,
            self.trade_button,
            self.daily_button,
            self.candle_button,
            edit_button,
            reload_button
        ]:
            button.setFixedHeight(button.sizeHint().height() * 2)

        form = QtWidgets.QFormLayout()
        # BRIAN: 交易策略 - Trading Strategy
        form.addRow("Trading Strategy", self.class_combo)
        # BRIAN: 本地代码 - Native Symbol
        form.addRow("Native Symbol", self.symbol_line)
        # BRIAN: K线周期 - K-line Period
        form.addRow("K-line Period", self.interval_combo)
        # BRIAN: 开始日期 - Start Date
        form.addRow("Start Date", self.start_date_edit)
        # BRIAN: 结束日期 - End Date
        form.addRow("End Date", self.end_date_edit)
        # BRIAN: 手续费率 - Commission Rate
        form.addRow("Commission Rate", self.rate_line)
        # BRIAN: 交易滑点 - Trading Slippage
        form.addRow("Trading Slippage", self.slippage_line)
        # BRIAN: 合约乘数 - Contract Multiplier
        form.addRow("Contract Multiplier", self.size_line)
        # BRIAN: 价格跳动 - Price Tick
        form.addRow("Price Tick", self.pricetick_line)
        # BRIAN: 回测资金 - Backtesting Fund
        form.addRow("Backtesting Fund", self.capital_line)
        # BRIAN: 合约模式 - Contract Model
        form.addRow("Contract Model", self.inverse_combo)

        result_grid = QtWidgets.QGridLayout()
        result_grid.addWidget(self.trade_button, 0, 0)
        result_grid.addWidget(self.order_button, 0, 1)
        result_grid.addWidget(self.daily_button, 1, 0)
        result_grid.addWidget(self.candle_button, 1, 1)

        left_vbox = QtWidgets.QVBoxLayout()
        left_vbox.addLayout(form)
        left_vbox.addWidget(backtesting_button)
        left_vbox.addWidget(downloading_button)
        left_vbox.addStretch()
        left_vbox.addLayout(result_grid)
        left_vbox.addStretch()
        left_vbox.addWidget(optimization_button)
        left_vbox.addWidget(self.result_button)
        left_vbox.addStretch()
        left_vbox.addWidget(edit_button)
        left_vbox.addWidget(reload_button)

        # Result part
        self.statistics_monitor = StatisticsMonitor()

        self.log_monitor = QtWidgets.QTextEdit()
        self.log_monitor.setMaximumHeight(400)

        self.chart = BacktesterChart()
        self.chart.setMinimumWidth(1000)

        # BRIAN: 回测成交记录 - Backtesting Transaction Records
        self.trade_dialog = BacktestingResultDialog(
            self.main_engine,
            self.event_engine,
            "Backtesting Transaction Records",
            BacktestingTradeMonitor
        )

        # BRIAN: 回测委托记录 - Backtesting Commission Records
        self.order_dialog = BacktestingResultDialog(
            self.main_engine,
            self.event_engine,
            "Backtesting Commission Records",
            BacktestingOrderMonitor
        )

        # BRIAN: 回测每日盈亏 - Backtesting Daily Profit/Loss
        self.daily_dialog = BacktestingResultDialog(
            self.main_engine,
            self.event_engine,
            "Backtesting Daily Profit/Loss",
            DailyResultMonitor
        )

        # Candle Chart
        self.candle_dialog = CandleChartDialog()

        # Layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.statistics_monitor)
        vbox.addWidget(self.log_monitor)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(left_vbox)
        hbox.addLayout(vbox)
        hbox.addWidget(self.chart)
        self.setLayout(hbox)

        # Code Editor
        self.editor = CodeEditor(self.main_engine, self.event_engine)

        # Load setting
        setting = load_json(self.setting_filename)
        if not setting:
            return

        self.class_combo.setCurrentIndex(
            self.class_combo.findText(setting["class_name"])
        )

        self.symbol_line.setText(setting["vt_symbol"])

        self.interval_combo.setCurrentIndex(
            self.interval_combo.findText(setting["interval"])
        )

        self.rate_line.setText(str(setting["rate"]))
        self.slippage_line.setText(str(setting["slippage"]))
        self.size_line.setText(str(setting["size"]))
        self.pricetick_line.setText(str(setting["pricetick"]))
        self.capital_line.setText(str(setting["capital"]))

        if not setting["inverse"]:
            self.inverse_combo.setCurrentIndex(0)
        else:
            self.inverse_combo.setCurrentIndex(1)

    def register_event(self):
        """"""
        self.signal_log.connect(self.process_log_event)
        self.signal_backtesting_finished.connect(
            self.process_backtesting_finished_event)
        self.signal_optimization_finished.connect(
            self.process_optimization_finished_event)

        self.event_engine.register(EVENT_BACKTESTER_LOG, self.signal_log.emit)
        self.event_engine.register(
            EVENT_BACKTESTER_BACKTESTING_FINISHED, self.signal_backtesting_finished.emit)
        self.event_engine.register(
            EVENT_BACKTESTER_OPTIMIZATION_FINISHED, self.signal_optimization_finished.emit)

    def process_log_event(self, event: Event):
        """"""
        msg = event.data
        self.write_log(msg)

    def write_log(self, msg):
        """"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"{timestamp}\t{msg}"
        self.log_monitor.append(msg)

    def process_backtesting_finished_event(self, event: Event):
        """"""
        statistics = self.backtester_engine.get_result_statistics()
        self.statistics_monitor.set_data(statistics)

        df = self.backtester_engine.get_result_df()
        self.chart.set_data(df)

        self.trade_button.setEnabled(True)
        self.order_button.setEnabled(True)
        self.daily_button.setEnabled(True)
        self.candle_button.setEnabled(True)

    def process_optimization_finished_event(self, event: Event):
        """"""
        # BRIAN: 请点击[优化结果]按钮查看 - 
        # Please click the [Optimization Results] button to view
        self.write_log("Please click the [Optimization Results] button to view")
        self.result_button.setEnabled(True)

    def start_backtesting(self):
        """"""
        class_name = self.class_combo.currentText()
        vt_symbol = self.symbol_line.text()
        interval = self.interval_combo.currentText()
        start = self.start_date_edit.date().toPyDate()
        end = self.end_date_edit.date().toPyDate()
        rate = float(self.rate_line.text())
        slippage = float(self.slippage_line.text())
        size = float(self.size_line.text())
        pricetick = float(self.pricetick_line.text())
        capital = float(self.capital_line.text())

        # BRIAN: 正向 - Forward
        if self.inverse_combo.currentText() == "Forward":
            inverse = False
        else:
            inverse = True

        # Save backtesting parameters
        backtesting_setting = {
            "class_name": class_name,
            "vt_symbol": vt_symbol,
            "interval": interval,
            "rate": rate,
            "slippage": slippage,
            "size": size,
            "pricetick": pricetick,
            "capital": capital,
            "inverse": inverse,
        }
        save_json(self.setting_filename, backtesting_setting)

        # Get strategy setting
        old_setting = self.settings[class_name]
        dialog = BacktestingSettingEditor(class_name, old_setting)
        i = dialog.exec()
        if i != dialog.Accepted:
            return

        new_setting = dialog.get_setting()
        self.settings[class_name] = new_setting

        result = self.backtester_engine.start_backtesting(
            class_name,
            vt_symbol,
            interval,
            start,
            end,
            rate,
            slippage,
            size,
            pricetick,
            capital,
            inverse,
            new_setting
        )

        if result:
            self.statistics_monitor.clear_data()
            self.chart.clear_data()

            self.trade_button.setEnabled(False)
            self.order_button.setEnabled(False)
            self.daily_button.setEnabled(False)
            self.candle_button.setEnabled(False)

            self.trade_dialog.clear_data()
            self.order_dialog.clear_data()
            self.daily_dialog.clear_data()
            self.candle_dialog.clear_data()

    def start_optimization(self):
        """"""
        class_name = self.class_combo.currentText()
        vt_symbol = self.symbol_line.text()
        interval = self.interval_combo.currentText()
        start = self.start_date_edit.date().toPyDate()
        end = self.end_date_edit.date().toPyDate()
        rate = float(self.rate_line.text())
        slippage = float(self.slippage_line.text())
        size = float(self.size_line.text())
        pricetick = float(self.pricetick_line.text())
        capital = float(self.capital_line.text())

        # BRIAN: 正向 - Forward
        if self.inverse_combo.currentText() == "Forward":
            inverse = False
        else:
            inverse = True

        parameters = self.settings[class_name]
        dialog = OptimizationSettingEditor(class_name, parameters)
        i = dialog.exec()
        if i != dialog.Accepted:
            return

        optimization_setting, use_ga = dialog.get_setting()
        self.target_display = dialog.target_display

        self.backtester_engine.start_optimization(
            class_name,
            vt_symbol,
            interval,
            start,
            end,
            rate,
            slippage,
            size,
            pricetick,
            capital,
            inverse,
            optimization_setting,
            use_ga
        )

        self.result_button.setEnabled(False)

    def start_downloading(self):
        """"""
        vt_symbol = self.symbol_line.text()
        interval = self.interval_combo.currentText()
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()

        start = datetime(start_date.year(), start_date.month(), start_date.day())
        end = datetime(end_date.year(), end_date.month(), end_date.day(), 23, 59, 59)

        self.backtester_engine.start_downloading(
            vt_symbol,
            interval,
            start,
            end
        )

    def show_optimization_result(self):
        """"""
        result_values = self.backtester_engine.get_result_values()

        dialog = OptimizationResultMonitor(
            result_values,
            self.target_display
        )
        dialog.exec_()

    def show_backtesting_trades(self):
        """"""
        if not self.trade_dialog.is_updated():
            trades = self.backtester_engine.get_all_trades()
            self.trade_dialog.update_data(trades)

        self.trade_dialog.exec_()

    def show_backtesting_orders(self):
        """"""
        if not self.order_dialog.is_updated():
            orders = self.backtester_engine.get_all_orders()
            self.order_dialog.update_data(orders)

        self.order_dialog.exec_()

    def show_daily_results(self):
        """"""
        if not self.daily_dialog.is_updated():
            results = self.backtester_engine.get_all_daily_results()
            self.daily_dialog.update_data(results)

        self.daily_dialog.exec_()

    def show_candle_chart(self):
        """"""
        if not self.candle_dialog.is_updated():
            history = self.backtester_engine.get_history_data()
            self.candle_dialog.update_history(history)

            trades = self.backtester_engine.get_all_trades()
            self.candle_dialog.update_trades(trades)

        self.candle_dialog.exec_()

    def edit_strategy_code(self):
        """"""
        class_name = self.class_combo.currentText()
        file_path = self.backtester_engine.get_strategy_class_file(class_name)

        self.editor.open_editor(file_path)
        self.editor.show()

    def reload_strategy_class(self):
        """"""
        self.backtester_engine.reload_strategy_class()

        self.class_combo.clear()
        self.init_strategy_settings()

    def show(self):
        """"""
        self.showMaximized()


class StatisticsMonitor(QtWidgets.QTableWidget):
    """"""
    KEY_NAME_MAP = {
        # BRIAN: 首个交易日 - Start Date
        "start_date": "Start Date",
        # BRIAN: 最后交易日 - End Date
        "end_date": "End Date",

        # BRIAN: 总交易日 - Total Days
        "total_days": "Total Days",
        # BRIAN: 盈利交易日 - Profitable Day
        "profit_days": "Profitable Day",
        # BRIAN: 亏损交易日 - Loss Day
        "loss_days": "Loss Day",

        # BRIAN: 起始资金 - Capital
        "capital": "Capital",
        # BRIAN: 结束资金 - End Balance
        "end_balance": "End Balance",

        # BRIAN: 总收益率 - Total Return
        "total_return": "Total Return",
        # BRIAN: 年化收益 - Annual Return
        "annual_return": "Annual Return",
        # BRIAN: 最大回撤 - Max Drawdown
        "max_drawdown": "Max Drawdown",
        # BRIAN: 百分比最大回撤 - Max DD Percent
        "max_ddpercent": "Max DD Percent",

        # BRIAN: 总盈亏 - Total Profit-Loss
        "total_net_pnl": "Total Profit-Loss",
        # BRIAN: 总手续费 - Total Commission
        "total_commission": "Total Commission",
        # BRIAN: 总滑点 - Total Slippage
        "total_slippage": "Total Slippage",
        # BRIAN: 总成交额 - Total Turnover
        "total_turnover": "Total Turnover",
        # BRIAN: 总成交笔数 - Total Transactions
        "total_trade_count": "Total Transactions",

        # BRIAN: 日均盈亏 - Daily Profit/Loss
        "daily_net_pnl": "Daily Profit/Loss",
        # BRIAN: 日均手续费 - Daily Commission
        "daily_commission": "Daily Commission",
        # BRIAN: 日均滑点 - Daily Slippage
        "daily_slippage": "Daily Slippage",
        # BRIAN: 日均成交额 - Daily Turnover
        "daily_turnover": "Daily Turnover",
        # BRIAN: 日均成交笔数 - Daily Transactions
        "daily_trade_count": "Daily Transactions",

        # BRIAN: 日均收益率 - Daily Return
        "daily_return": "Daily Return",
        # BRIAN: 收益标准差 - Daily Standard Deviation
        "return_std": "Daily Standard Deviation",
        # BRIAN: 夏普比率 - Sharpe Ratio
        "sharpe_ratio": "Sharpe Ratio",
        # BRIAN: 收益回撤比 - Return DD Ratio
        "return_drawdown_ratio": "Return DD Ratio"
    }

    def __init__(self):
        """"""
        super().__init__()

        self.cells = {}

        self.init_ui()

    def init_ui(self):
        """"""
        self.setRowCount(len(self.KEY_NAME_MAP))
        self.setVerticalHeaderLabels(list(self.KEY_NAME_MAP.values()))

        self.setColumnCount(1)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.setEditTriggers(self.NoEditTriggers)

        for row, key in enumerate(self.KEY_NAME_MAP.keys()):
            cell = QtWidgets.QTableWidgetItem()
            self.setItem(row, 0, cell)
            self.cells[key] = cell

    def clear_data(self):
        """"""
        for cell in self.cells.values():
            cell.setText("")

    def set_data(self, data: dict):
        """"""
        data["capital"] = f"{data['capital']:,.2f}"
        data["end_balance"] = f"{data['end_balance']:,.2f}"
        data["total_return"] = f"{data['total_return']:,.2f}%"
        data["annual_return"] = f"{data['annual_return']:,.2f}%"
        data["max_drawdown"] = f"{data['max_drawdown']:,.2f}"
        data["max_ddpercent"] = f"{data['max_ddpercent']:,.2f}%"
        data["total_net_pnl"] = f"{data['total_net_pnl']:,.2f}"
        data["total_commission"] = f"{data['total_commission']:,.2f}"
        data["total_slippage"] = f"{data['total_slippage']:,.2f}"
        data["total_turnover"] = f"{data['total_turnover']:,.2f}"
        data["daily_net_pnl"] = f"{data['daily_net_pnl']:,.2f}"
        data["daily_commission"] = f"{data['daily_commission']:,.2f}"
        data["daily_slippage"] = f"{data['daily_slippage']:,.2f}"
        data["daily_turnover"] = f"{data['daily_turnover']:,.2f}"
        data["daily_return"] = f"{data['daily_return']:,.2f}%"
        data["return_std"] = f"{data['return_std']:,.2f}%"
        data["sharpe_ratio"] = f"{data['sharpe_ratio']:,.2f}"
        data["return_drawdown_ratio"] = f"{data['return_drawdown_ratio']:,.2f}"

        for key, cell in self.cells.items():
            value = data.get(key, "")
            cell.setText(str(value))


class BacktestingSettingEditor(QtWidgets.QDialog):
    """
    For creating new strategy and editing strategy parameters.
    """

    def __init__(
        self, class_name: str, parameters: dict
    ):
        """"""
        super(BacktestingSettingEditor, self).__init__()

        self.class_name = class_name
        self.parameters = parameters
        self.edits = {}

        self.init_ui()

    def init_ui(self):
        """"""
        form = QtWidgets.QFormLayout()

        # Add vt_symbol and name edit if add new strategy
        # BRIAN: 策略参数配置 - Policy Parameter Configuration
        self.setWindowTitle(f"Policy Parameter Configuration: {self.class_name}")
        # BRIAN: 确定 - Apply
        button_text = "Apply"
        parameters = self.parameters

        for name, value in parameters.items():
            type_ = type(value)

            edit = QtWidgets.QLineEdit(str(value))
            if type_ is int:
                validator = QtGui.QIntValidator()
                edit.setValidator(validator)
            elif type_ is float:
                validator = QtGui.QDoubleValidator()
                edit.setValidator(validator)

            form.addRow(f"{name} {type_}", edit)

            self.edits[name] = (edit, type_)

        button = QtWidgets.QPushButton(button_text)
        button.clicked.connect(self.accept)
        form.addRow(button)

        self.setLayout(form)

    def get_setting(self):
        """"""
        setting = {}

        for name, tp in self.edits.items():
            edit, type_ = tp
            value_text = edit.text()

            if type_ == bool:
                if value_text == "True":
                    value = True
                else:
                    value = False
            else:
                value = type_(value_text)

            setting[name] = value

        return setting


class BacktesterChart(pg.GraphicsWindow):
    """"""

    def __init__(self):
        """"""
        super().__init__(title="Backtester Chart")

        self.dates = {}

        self.init_ui()

    def init_ui(self):
        """"""
        pg.setConfigOptions(antialias=True)

        # Create plot widgets
        self.balance_plot = self.addPlot(
            # BRIAN: 账户净值 - Account Equity
            title="Account Equity",
            axisItems={"bottom": DateAxis(self.dates, orientation="bottom")}
        )
        self.nextRow()

        self.drawdown_plot = self.addPlot(
            # BRIAN: 净值回撤 - Net Drawdown
            title="Net Drawdown",
            axisItems={"bottom": DateAxis(self.dates, orientation="bottom")}
        )
        self.nextRow()

        self.pnl_plot = self.addPlot(
            # BRIAN: 每日盈亏 - Daily Profit/Loss
            title="Daily Profit/Loss",
            axisItems={"bottom": DateAxis(self.dates, orientation="bottom")}
        )
        self.nextRow()

        # BRIAN: 盈亏分布 - Profit and Loss Distribution
        self.distribution_plot = self.addPlot(title="Profit and Loss Distribution")

        # Add curves and bars on plot widgets
        self.balance_curve = self.balance_plot.plot(
            pen=pg.mkPen("#ffc107", width=3)
        )

        dd_color = "#303f9f"
        self.drawdown_curve = self.drawdown_plot.plot(
            fillLevel=-0.3, brush=dd_color, pen=dd_color
        )

        profit_color = 'r'
        loss_color = 'g'
        self.profit_pnl_bar = pg.BarGraphItem(
            x=[], height=[], width=0.3, brush=profit_color, pen=profit_color
        )
        self.loss_pnl_bar = pg.BarGraphItem(
            x=[], height=[], width=0.3, brush=loss_color, pen=loss_color
        )
        self.pnl_plot.addItem(self.profit_pnl_bar)
        self.pnl_plot.addItem(self.loss_pnl_bar)

        distribution_color = "#6d4c41"
        self.distribution_curve = self.distribution_plot.plot(
            fillLevel=-0.3, brush=distribution_color, pen=distribution_color
        )

    def clear_data(self):
        """"""
        self.balance_curve.setData([], [])
        self.drawdown_curve.setData([], [])
        self.profit_pnl_bar.setOpts(x=[], height=[])
        self.loss_pnl_bar.setOpts(x=[], height=[])
        self.distribution_curve.setData([], [])

    def set_data(self, df):
        """"""
        if df is None:
            return

        count = len(df)

        self.dates.clear()
        for n, date in enumerate(df.index):
            self.dates[n] = date

        # Set data for curve of balance and drawdown
        self.balance_curve.setData(df["balance"])
        self.drawdown_curve.setData(df["drawdown"])

        # Set data for daily pnl bar
        profit_pnl_x = []
        profit_pnl_height = []
        loss_pnl_x = []
        loss_pnl_height = []

        for count, pnl in enumerate(df["net_pnl"]):
            if pnl >= 0:
                profit_pnl_height.append(pnl)
                profit_pnl_x.append(count)
            else:
                loss_pnl_height.append(pnl)
                loss_pnl_x.append(count)

        self.profit_pnl_bar.setOpts(x=profit_pnl_x, height=profit_pnl_height)
        self.loss_pnl_bar.setOpts(x=loss_pnl_x, height=loss_pnl_height)

        # Set data for pnl distribution
        hist, x = np.histogram(df["net_pnl"], bins="auto")
        x = x[:-1]
        self.distribution_curve.setData(x, hist)


class DateAxis(pg.AxisItem):
    """Axis for showing date data"""

    def __init__(self, dates: dict, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.dates = dates

    def tickStrings(self, values, scale, spacing):
        """"""
        strings = []
        for v in values:
            dt = self.dates.get(v, "")
            strings.append(str(dt))
        return strings


class OptimizationSettingEditor(QtWidgets.QDialog):
    """
    For setting up parameters for optimization.
    """
    # BRIAN: 总收益率 - Total Return
    # BRIAN: 夏普比率 - Sharpe Ratio
    # BRIAN: 收益回撤比 - Return DD Ratio
    # BRIAN: 日均盈亏 - Daily Profit/Loss
    DISPLAY_NAME_MAP = {
        "Total Return": "total_return",
        "Sharpe Ratio": "sharpe_ratio",
        "Return DD Ratio": "return_drawdown_ratio",
        "Daily Profit/Loss": "daily_net_pnl"
    }

    def __init__(
        self, class_name: str, parameters: dict
    ):
        """"""
        super().__init__()

        self.class_name = class_name
        self.parameters = parameters
        self.edits = {}

        self.optimization_setting = None
        self.use_ga = False

        self.init_ui()

    def init_ui(self):
        """"""
        QLabel = QtWidgets.QLabel

        self.target_combo = QtWidgets.QComboBox()
        self.target_combo.addItems(list(self.DISPLAY_NAME_MAP.keys()))

        grid = QtWidgets.QGridLayout()
        # BRIAN: 目标 - Target
        grid.addWidget(QLabel("Target"), 0, 0)
        grid.addWidget(self.target_combo, 0, 1, 1, 3)
        # BRIAN 参数 - Parameter
        grid.addWidget(QLabel("Parameter"), 1, 0)
        # BRIAN: 开始 - Start
        grid.addWidget(QLabel("Start"), 1, 1)
        # BRIAN: 步进 - Step
        grid.addWidget(QLabel("Step"), 1, 2)
        # BRIAN: 结束 - End
        grid.addWidget(QLabel("End"), 1, 3)

        # Add vt_symbol and name edit if add new strategy
        # BRIAN: 优化参数配置 - Optimization Parameter Configuration
        self.setWindowTitle(f"Optimization Parameter Configuration: {self.class_name}")

        validator = QtGui.QDoubleValidator()
        row = 2

        for name, value in self.parameters.items():
            type_ = type(value)
            if type_ not in [int, float]:
                continue

            start_edit = QtWidgets.QLineEdit(str(value))
            step_edit = QtWidgets.QLineEdit(str(1))
            end_edit = QtWidgets.QLineEdit(str(value))

            for edit in [start_edit, step_edit, end_edit]:
                edit.setValidator(validator)

            grid.addWidget(QLabel(name), row, 0)
            grid.addWidget(start_edit, row, 1)
            grid.addWidget(step_edit, row, 2)
            grid.addWidget(end_edit, row, 3)

            self.edits[name] = {
                "type": type_,
                "start": start_edit,
                "step": step_edit,
                "end": end_edit
            }

            row += 1

        # BRIAN: 多进程优化 - Multi-process Optimization
        parallel_button = QtWidgets.QPushButton("Multi-process Optimization")
        parallel_button.clicked.connect(self.generate_parallel_setting)
        grid.addWidget(parallel_button, row, 0, 1, 4)

        row += 1
        # BRIAN: 遗传算法优化 - Genetic Algorithm Optimization
        ga_button = QtWidgets.QPushButton("Genetic Algorithm Optimization")
        ga_button.clicked.connect(self.generate_ga_setting)
        grid.addWidget(ga_button, row, 0, 1, 4)

        self.setLayout(grid)

    def generate_ga_setting(self):
        """"""
        self.use_ga = True
        self.generate_setting()

    def generate_parallel_setting(self):
        """"""
        self.use_ga = False
        self.generate_setting()

    def generate_setting(self):
        """"""
        self.optimization_setting = OptimizationSetting()

        self.target_display = self.target_combo.currentText()
        target_name = self.DISPLAY_NAME_MAP[self.target_display]
        self.optimization_setting.set_target(target_name)

        for name, d in self.edits.items():
            type_ = d["type"]
            start_value = type_(d["start"].text())
            step_value = type_(d["step"].text())
            end_value = type_(d["end"].text())

            if start_value == end_value:
                self.optimization_setting.add_parameter(name, start_value)
            else:
                self.optimization_setting.add_parameter(
                    name,
                    start_value,
                    end_value,
                    step_value
                )

        self.accept()

    def get_setting(self):
        """"""
        return self.optimization_setting, self.use_ga


class OptimizationResultMonitor(QtWidgets.QDialog):
    """
    For viewing optimization result.
    """

    def __init__(
        self, result_values: list, target_display: str
    ):
        """"""
        super().__init__()

        self.result_values = result_values
        self.target_display = target_display

        self.init_ui()

    def init_ui(self):
        """"""
        # BRIAN: 参数优化结果 - Parameter Optimization Results
        self.setWindowTitle("Parameter Optimization Results")
        self.resize(1100, 500)

        # Creat table to show result
        table = QtWidgets.QTableWidget()

        table.setColumnCount(2)
        table.setRowCount(len(self.result_values))
        # BRIAN 参数 - Parameter
        table.setHorizontalHeaderLabels(["Parameter", self.target_display])
        table.setEditTriggers(table.NoEditTriggers)
        table.verticalHeader().setVisible(False)

        table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents
        )
        table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch
        )

        for n, tp in enumerate(self.result_values):
            setting, target_value, _ = tp
            setting_cell = QtWidgets.QTableWidgetItem(str(setting))
            target_cell = QtWidgets.QTableWidgetItem(str(target_value))

            setting_cell.setTextAlignment(QtCore.Qt.AlignCenter)
            target_cell.setTextAlignment(QtCore.Qt.AlignCenter)

            table.setItem(n, 0, setting_cell)
            table.setItem(n, 1, target_cell)

        # Create layout
        # BRIAN: 保存 - Save
        button = QtWidgets.QPushButton("Save")
        button.clicked.connect(self.save_csv)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(button)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(table)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def save_csv(self) -> None:
        """
        Save table data into a csv file
        """
        # BRIAN: 保存数据 - Save Data
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Data", "", "CSV(*.csv)")

        if not path:
            return

        with open(path, "w") as f:
            writer = csv.writer(f, lineterminator="\n")

            # BRIAN: 参数 - Parameter
            writer.writerow(["Parameter", self.target_display])

            for tp in self.result_values:
                setting, target_value, _ = tp
                row_data = [str(setting), str(target_value)]
                writer.writerow(row_data)


class BacktestingTradeMonitor(BaseMonitor):
    """
    Monitor for backtesting trade data.
    """
    # BRIAN: 成交号 - Trade ID
    # BRIAN: 委托号 - Order ID
    # BRIAN: 代码 - Symbol
    # BRIAN: 交易所 - Exchange
    # BRIAN: 方向 - Direction
    # BRIAN: 开平 - Offset
    # BRIAN: 价格 - Price
    # BRIAN: 数量 - Volume
    # BRIAN: 时间 - Datetime
    # BRIAN: 接口 - Gateway
    headers = {
        "tradeid": {"display": "Trade ID ", "cell": BaseCell, "update": False},
        "orderid": {"display": "Order ID", "cell": BaseCell, "update": False},
        "symbol": {"display": "Symbol", "cell": BaseCell, "update": False},
        "exchange": {"display": "Exchange", "cell": EnumCell, "update": False},
        "direction": {"display": "Direction", "cell": DirectionCell, "update": False},
        "offset": {"display": "Offset", "cell": EnumCell, "update": False},
        "price": {"display": "Price", "cell": BaseCell, "update": False},
        "volume": {"display": "Volume", "cell": BaseCell, "update": False},
        "datetime": {"display": "Datetime", "cell": BaseCell, "update": False},
        "gateway_name": {"display": "Gateway", "cell": BaseCell, "update": False},
    }


class BacktestingOrderMonitor(BaseMonitor):
    """
    Monitor for backtesting order data.
    """

    # BRIAN: 委托号 - Order ID
    # BRIAN: 代码 - Symbol
    # BRIAN: 交易所 - Exchange
    # BRIAN: 类型 - Type
    # BRIAN: 方向 - Direction
    # BRIAN: 开平 - Offset
    # BRIAN: 价格 - Price
    # BRIAN: 总数量 - Total Volume
    # BRIAN: 已成交 - Traded
    # BRIAN: 状态 - Status
    # BRIAN: 时间 - Datetime
    # BRIAN: 接口 - Gateway
    headers = {
        "orderid": {"display": "Order ID", "cell": BaseCell, "update": False},
        "symbol": {"display": "Symbol", "cell": BaseCell, "update": False},
        "exchange": {"display": "Exchange", "cell": EnumCell, "update": False},
        "type": {"display": "Type", "cell": EnumCell, "update": False},
        "direction": {"display": "Direction", "cell": DirectionCell, "update": False},
        "offset": {"display": "Offset", "cell": EnumCell, "update": False},
        "price": {"display": "Price", "cell": BaseCell, "update": False},
        "volume": {"display": "Total Volume", "cell": BaseCell, "update": False},
        "traded": {"display": "Traded", "cell": BaseCell, "update": False},
        "status": {"display": "Status", "cell": EnumCell, "update": False},
        "datetime": {"display": "Datetime", "cell": BaseCell, "update": False},
        "gateway_name": {"display": "Gateway", "cell": BaseCell, "update": False},
    }


class DailyResultMonitor(BaseMonitor):
    """
    Monitor for backtesting daily result.
    """

    # BRIAN: 日期 - Date
    # BRIAN: 成交笔数 - No. of Transactions
    # BRIAN: 开盘持仓 - Open Position
    # BRIAN: 收盘持仓 - End Position
    # BRIAN: 成交额 - Tunrover
    # BRIAN: 手续费 - Commission
    # BRIAN: 滑点 - Slippage
    # BRIAN: 交易盈亏 - Trading Profit/Loss
    # BRIAN: 持仓盈亏 - Holding Profit/Loss
    # BRIAN: 总盈亏 - Total Profit/Loss
    # BRIAN: 净盈亏 - Net Profit/Loss
    headers = {
        "date": {"display": "Date", "cell": BaseCell, "update": False},
        "trade_count": {"display": "No. of Transactions", "cell": BaseCell, "update": False},
        "start_pos": {"display": "Open Position", "cell": BaseCell, "update": False},
        "end_pos": {"display": "End Position", "cell": BaseCell, "update": False},
        "turnover": {"display": "Tunrover", "cell": BaseCell, "update": False},
        "commission": {"display": "Commission", "cell": BaseCell, "update": False},
        "slippage": {"display": "Slippage", "cell": BaseCell, "update": False},
        "trading_pnl": {"display": "Trading Profit/Loss", "cell": BaseCell, "update": False},
        "holding_pnl": {"display": "Holding Profit/Loss", "cell": BaseCell, "update": False},
        "total_pnl": {"display": "Total Profit/Loss", "cell": BaseCell, "update": False},
        "net_pnl": {"display": "Net Profit/Loss", "cell": BaseCell, "update": False},
    }


class BacktestingResultDialog(QtWidgets.QDialog):
    """
    """

    def __init__(
        self,
        main_engine: MainEngine,
        event_engine: EventEngine,
        title: str,
        table_class: QtWidgets.QTableWidget
    ):
        """"""
        super().__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine
        self.title = title
        self.table_class = table_class

        self.updated = False

        self.init_ui()

    def init_ui(self):
        """"""
        self.setWindowTitle(self.title)
        self.resize(1100, 600)

        self.table = self.table_class(self.main_engine, self.event_engine)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def clear_data(self):
        """"""
        self.updated = False
        self.table.setRowCount(0)

    def update_data(self, data: list):
        """"""
        self.updated = True

        data.reverse()
        for obj in data:
            self.table.insert_new_row(obj)

    def is_updated(self):
        """"""
        return self.updated


class CandleChartDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self):
        """"""
        super().__init__()

        self.dt_ix_map = {}
        self.updated = False
        self.init_ui()

    def init_ui(self):
        """"""
        # BRIAN: 回测K线图表 - Backtest Chart
        self.setWindowTitle("Backtest Chart")
        self.resize(1400, 800)

        # Create chart widget
        self.chart = ChartWidget()
        self.chart.add_plot("candle", hide_x_axis=True)
        self.chart.add_plot("volume", maximum_height=200)
        self.chart.add_item(CandleItem, "candle", "candle")
        self.chart.add_item(VolumeItem, "volume", "volume")
        self.chart.add_cursor()

        # Add scatter item for showing tradings
        self.trade_scatter = pg.ScatterPlotItem()
        candle_plot = self.chart.get_plot("candle")
        candle_plot.addItem(self.trade_scatter)

        # Set layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.chart)
        self.setLayout(vbox)

    def update_history(self, history: list):
        """"""
        self.updated = True
        self.chart.update_history(history)

        for ix, bar in enumerate(history):
            self.dt_ix_map[bar.datetime] = ix

    def update_trades(self, trades: list):
        """"""
        trade_data = []

        for trade in trades:
            ix = self.dt_ix_map[trade.datetime]

            scatter = {
                "pos": (ix, trade.price),
                "data": 1,
                "size": 14,
                "pen": pg.mkPen((255, 255, 255))
            }

            if trade.direction == Direction.LONG:
                scatter_symbol = "t1"   # Up arrow
            else:
                scatter_symbol = "t"    # Down arrow

            if trade.offset == Offset.OPEN:
                scatter_brush = pg.mkBrush((255, 255, 0))   # Yellow
            else:
                scatter_brush = pg.mkBrush((0, 0, 255))     # Blue

            scatter["symbol"] = scatter_symbol
            scatter["brush"] = scatter_brush

            trade_data.append(scatter)

        self.trade_scatter.setData(trade_data)

    def clear_data(self):
        """"""
        self.updated = False
        self.chart.clear_all()

        self.dt_ix_map.clear()
        self.trade_scatter.clear()

    def is_updated(self):
        """"""
        return self.updated
