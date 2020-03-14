import os
import importlib
import traceback
from datetime import datetime
from threading import Thread
from pathlib import Path
from inspect import getfile

from vnpy.event import Event, EventEngine
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.constant import Interval
from vnpy.trader.utility import extract_vt_symbol
from vnpy.trader.object import HistoryRequest
from vnpy.trader.rqdata import rqdata_client
from vnpy.trader.database import database_manager
from vnpy.app.cta_strategy import (
    CtaTemplate,
    BacktestingEngine,
    OptimizationSetting
)

APP_NAME = "CtaBacktester"

EVENT_BACKTESTER_LOG = "eBacktesterLog"
EVENT_BACKTESTER_BACKTESTING_FINISHED = "eBacktesterBacktestingFinished"
EVENT_BACKTESTER_OPTIMIZATION_FINISHED = "eBacktesterOptimizationFinished"


class BacktesterEngine(BaseEngine):
    """
    For running CTA strategy backtesting.
    """

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__(main_engine, event_engine, APP_NAME)

        self.classes = {}
        self.backtesting_engine = None
        self.thread = None

        # Backtesting reuslt
        self.result_df = None
        self.result_statistics = None

        # Optimization result
        self.result_values = None

    def init_engine(self):
        """"""
        # BRIAN: 初始化CTA回测引擎 - Initialize the CTA Backtest engine
        self.write_log("Initialize the CTA Backtest engine")

        self.backtesting_engine = BacktestingEngine()
        # Redirect log from backtesting engine outside.
        self.backtesting_engine.output = self.write_log

        self.load_strategy_class()
        # BRIAN: 策略文件加载完成 - Policy file loading is completed
        self.write_log("Policy file loading is completed")

        self.init_rqdata()

    def init_rqdata(self):
        """
        Init RQData client.
        """
        result = rqdata_client.init()
        if result:
            # BRIAN: RQData数据接口初始化成功 - 
            # RQData data interface initialized successfully
            self.write_log("RQData data interface initialized successfully")

    def write_log(self, msg: str):
        """"""
        event = Event(EVENT_BACKTESTER_LOG)
        event.data = msg
        self.event_engine.put(event)

    def load_strategy_class(self):
        """
        Load strategy class from source code.
        """
        app_path = Path(__file__).parent.parent
        path1 = app_path.joinpath("cta_strategy", "strategies")
        self.load_strategy_class_from_folder(
            path1, "vnpy.app.cta_strategy.strategies")

        path2 = Path.cwd().joinpath("strategies")
        self.load_strategy_class_from_folder(path2, "strategies")

    def load_strategy_class_from_folder(self, path: Path, module_name: str = ""):
        """
        Load strategy class from certain folder.
        """
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                # Load python source code file
                if filename.endswith(".py"):
                    strategy_module_name = ".".join(
                        [module_name, filename.replace(".py", "")])
                    self.load_strategy_class_from_module(strategy_module_name)
                # Load compiled pyd binary file
                elif filename.endswith(".pyd"):
                    strategy_module_name = ".".join(
                        [module_name, filename.split(".")[0]])
                    self.load_strategy_class_from_module(strategy_module_name)

    def load_strategy_class_from_module(self, module_name: str):
        """
        Load strategy class from module file.
        """
        try:
            module = importlib.import_module(module_name)

            for name in dir(module):
                value = getattr(module, name)
                if (isinstance(value, type) and issubclass(value, CtaTemplate) and value is not CtaTemplate):
                    self.classes[value.__name__] = value
        except:  # noqa
            # BRIAN: 策略文件 - Policy file
            # BRIAN: 加载失败，触发异常 - Loading failed with exception
            msg = f"Policy file {module_name} loading failed with exception:\n{traceback.format_exc()}"
            self.write_log(msg)

    def reload_strategy_class(self):
        """"""
        self.classes.clear()
        self.load_strategy_class()
        # BRIAN: 策略文件重载刷新完成 - Policy file reload completed
        self.write_log("Policy file reload completed")

    def get_strategy_class_names(self):
        """"""
        return list(self.classes.keys())

    def run_backtesting(
        self,
        class_name: str,
        vt_symbol: str,
        interval: str,
        start: datetime,
        end: datetime,
        rate: float,
        slippage: float,
        size: int,
        pricetick: float,
        capital: int,
        inverse: bool,
        setting: dict
    ):
        """"""
        self.result_df = None
        self.result_statistics = None

        engine = self.backtesting_engine
        engine.clear_data()

        engine.set_parameters(
            vt_symbol=vt_symbol,
            interval=interval,
            start=start,
            end=end,
            rate=rate,
            slippage=slippage,
            size=size,
            pricetick=pricetick,
            capital=capital,
            inverse=inverse
        )

        strategy_class = self.classes[class_name]
        engine.add_strategy(
            strategy_class,
            setting
        )

        engine.load_data()
        engine.run_backtesting()
        self.result_df = engine.calculate_result()
        self.result_statistics = engine.calculate_statistics(output=False)

        # Clear thread object handler.
        self.thread = None

        # Put backtesting done event
        event = Event(EVENT_BACKTESTER_BACKTESTING_FINISHED)
        self.event_engine.put(event)

    def start_backtesting(
        self,
        class_name: str,
        vt_symbol: str,
        interval: str,
        start: datetime,
        end: datetime,
        rate: float,
        slippage: float,
        size: int,
        pricetick: float,
        capital: int,
        inverse: bool,
        setting: dict
    ):
        if self.thread:
            # BRIAN: 已有任务在运行中，请等待完成 - 
            # Task is already running, please wait for completion
            self.write_log("Task is already running, please wait for completion")
            return False

        self.write_log("-" * 40)
        self.thread = Thread(
            target=self.run_backtesting,
            args=(
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
                setting
            )
        )
        self.thread.start()

        return True

    def get_result_df(self):
        """"""
        return self.result_df

    def get_result_statistics(self):
        """"""
        return self.result_statistics

    def get_result_values(self):
        """"""
        return self.result_values

    def get_default_setting(self, class_name: str):
        """"""
        strategy_class = self.classes[class_name]
        return strategy_class.get_class_parameters()

    def run_optimization(
        self,
        class_name: str,
        vt_symbol: str,
        interval: str,
        start: datetime,
        end: datetime,
        rate: float,
        slippage: float,
        size: int,
        pricetick: float,
        capital: int,
        inverse: bool,
        optimization_setting: OptimizationSetting,
        use_ga: bool
    ):
        """"""
        if use_ga:
            # BRIAN: 开始遗传算法参数优化 - 
            # Start genetic algorithm parameter optimization
            self.write_log("Start genetic algorithm parameter optimization")
        else:
            # BRIAN: 开始多进程参数优化 - 
            # Start multi-process parameter optimization
            self.write_log("Start multi-process parameter optimization")

        self.result_values = None

        engine = self.backtesting_engine
        engine.clear_data()

        engine.set_parameters(
            vt_symbol=vt_symbol,
            interval=interval,
            start=start,
            end=end,
            rate=rate,
            slippage=slippage,
            size=size,
            pricetick=pricetick,
            capital=capital,
            inverse=inverse
        )

        strategy_class = self.classes[class_name]
        engine.add_strategy(
            strategy_class,
            {}
        )

        if use_ga:
            self.result_values = engine.run_ga_optimization(
                optimization_setting,
                output=False
            )
        else:
            self.result_values = engine.run_optimization(
                optimization_setting,
                output=False
            )

        # Clear thread object handler.
        self.thread = None
        # BRIAN: 多进程参数优化完成 - 
        # Multi-process parameter optimization completed
        self.write_log("Multi-process parameter optimization completed")

        # Put optimization done event
        event = Event(EVENT_BACKTESTER_OPTIMIZATION_FINISHED)
        self.event_engine.put(event)

    def start_optimization(
        self,
        class_name: str,
        vt_symbol: str,
        interval: str,
        start: datetime,
        end: datetime,
        rate: float,
        slippage: float,
        size: int,
        pricetick: float,
        capital: int,
        inverse: bool,
        optimization_setting: OptimizationSetting,
        use_ga: bool
    ):
        if self.thread:
            # BRIAN: 已有任务在运行中，请等待完成 - 
            # Task already is running, please wait for completion
            self.write_log("Task is already running, please wait for completion")
            return False

        self.write_log("-" * 40)
        self.thread = Thread(
            target=self.run_optimization,
            args=(
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
        )
        self.thread.start()

        return True

    def run_downloading(
        self,
        vt_symbol: str,
        interval: str,
        start: datetime,
        end: datetime
    ):
        """
        Query bar data from RQData.
        """
        # BRIAN: 开始下载历史数据 - Start downloading historical data 
        self.write_log(f"{vt_symbol}-{interval} start downloading historical data")

        symbol, exchange = extract_vt_symbol(vt_symbol)

        req = HistoryRequest(
            symbol=symbol,
            exchange=exchange,
            interval=Interval(interval),
            start=start,
            end=end
        )

        contract = self.main_engine.get_contract(vt_symbol)

        try:
            # If history data provided in gateway, then query
            if contract and contract.history_data:
                data = self.main_engine.query_history(
                    req, contract.gateway_name
                )
            # Otherwise use RQData to query data
            else:
                data = rqdata_client.query_history(req)

            if data:
                database_manager.save_bar_data(data)
                # BRIAN: 历史数据下载完成 - historical data download completed
                self.write_log(f"{vt_symbol}-{interval} historical data download completed")
            else:
                # BRIAN: 数据下载失败，无法获取 - Data download failed and cannot be obtained
                self.write_log(f"Data download failed and cannot be obtained {vt_symbol} historical data")
        except Exception:
            # BRIAN: 数据下载失败，触发异常 - Data download failed with exception
            msg = f"Data download failed with exception:\n{traceback.format_exc()}"
            self.write_log(msg)

        # Clear thread object handler.
        self.thread = None

    def start_downloading(
        self,
        vt_symbol: str,
        interval: str,
        start: datetime,
        end: datetime
    ):
        if self.thread:
            # BRIAN: 已有任务在运行中，请等待完成 - 
            # Task is already running, please wait for completion
            self.write_log("Task is already running, please wait for completion")
            return False

        self.write_log("-" * 40)
        self.thread = Thread(
            target=self.run_downloading,
            args=(
                vt_symbol,
                interval,
                start,
                end
            )
        )
        self.thread.start()

        return True

    def get_all_trades(self):
        """"""
        return self.backtesting_engine.get_all_trades()

    def get_all_orders(self):
        """"""
        return self.backtesting_engine.get_all_orders()

    def get_all_daily_results(self):
        """"""
        return self.backtesting_engine.get_all_daily_results()

    def get_history_data(self):
        """"""
        return self.backtesting_engine.history_data

    def get_strategy_class_file(self, class_name: str):
        """"""
        strategy_class = self.classes[class_name]
        file_path = getfile(strategy_class)
        return file_path
