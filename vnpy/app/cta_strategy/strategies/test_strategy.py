from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData
)

from time import time


class TestStrategy(CtaTemplate):
    """"""
    # BRIAN: 用Python的交易员 - Trader using Python
    author = "Trader using Python"

    test_trigger = 10

    tick_count = 0
    test_all_done = False

    parameters = ["test_trigger"]
    variables = ["tick_count", "test_all_done"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(TestStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )

        self.test_funcs = [
            self.test_market_order,
            self.test_limit_order,
            self.test_cancel_all,
            self.test_stop_order
        ]
        self.last_tick = None

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        # BRIAN: 策略初始化 - Strategy initialization
        self.write_log("Strategy initialization")

    def on_start(self):
        """
        Callback when strategy is started.
        """
        # BRIAN: 策略启动 - Strategy starts
        self.write_log("Strategy starts")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        # BRIAN: 策略停止 - Strategy stops
        self.write_log("Strategy stops")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        if self.test_all_done:
            return

        self.last_tick = tick

        self.tick_count += 1
        if self.tick_count >= self.test_trigger:
            self.tick_count = 0

            if self.test_funcs:
                test_func = self.test_funcs.pop(0)

                start = time()
                test_func()
                time_cost = (time() - start) * 1000
                # BRIAN: 耗时%s毫秒 - Time consumming %s miliseconds
                self.write_log("Time consumming %s miliseconds" % (time_cost))
            else:
                # BRIAN: 测试已全部完成 - Tests are all completed
                self.write_log("Tests are all completed")
                self.test_all_done = True

        self.put_event()

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        self.put_event()

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        self.put_event()

    def test_market_order(self):
        """"""
        self.buy(self.last_tick.limit_up, 1)
        # BRIAN: 执行市价单测试 - Perform market order test
        self.write_log("Perform market order test")

    def test_limit_order(self):
        """"""
        self.buy(self.last_tick.limit_down, 1)
        # BRIAN: 执行限价单测试 - Perform limit order test
        self.write_log("Perform limit order test")

    def test_stop_order(self):
        """"""
        self.buy(self.last_tick.ask_price_1, 1, True)
        # BRIAN: 执行停止单测试 - Perform stop order test
        self.write_log("Perform stop order test")

    def test_cancel_all(self):
        """"""
        self.cancel_all()
        # BRIAN: 执行全部撤单测试 - Perform all cancel Tests
        self.write_log("Perform all cancel Tests")
