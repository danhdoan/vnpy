# ======================================
# vnpy/trader/ui/mainwindow.py
# ====================================== 

#
# init_dock
# 
# BRIAN: 交易 - Transaction
# BRIAN: 行情 - Quote
# BRIAN: 委托 - Commission
# BRIAN: 活动 - Activity
# BRIAN: 成交 - Closing
# BRIAN: 日志 - Log
# BRIAN: 资金 - Fund
# BRIAN: 持仓 - Open Position

#
# init_menu
# 
# BRIAN: 系统 - System
# BRIAN: 连接 - Connect
# BRIAN: 退出 - Exit
# BRIAN: 功能 - Features
# BRIAN: 配置 - Configurations
# BRIAN: 帮助 - Help
# BRIANL 查询合约 - Query Contract
# BRIAN: 代码编辑 - Code Editor
# BRIAN: 还原窗口 - Restore Window
# BRIAN: 测试邮件 - Test Mail
# BRIAN: 社区论坛 - Community Forum
# BRIAN: 关于 - About

#
# init_toolbar
#
# BRIAN: 工具栏 - Toolbar 

#
# closeEvent
#
# BRIAN: 退出 - Exit
# BRIAN: 确认退出 - Confirm Exit


# ======================================
# vnpy/trader/ui/widget.py
# ======================================

#
# BaseMonitor
#

#
# init_menu
#
# BRIAN: 调整列宽 - Adjust column width
# BRIAN: 保存数据 - Save Data

#
# save_csv
#
# BRIAN: 保存数据 - Save Data


#
# TickMonitor
#
# BRIAN: 代码 - Symbol
# BRIAN: 交易所 - Exchange
# BRIAN: 名称 - Name
# BRIAN: 最新价 - Last Price
# BRIAN: 成交量 - Volumn
# BRIAN: 开盘价 - Open Price
# BRIAN: 最高价 - High Price
# BRIAN: 最低价 - Low Price
# BRIAN: 买1价 - Buy 1 Price
# BRIAN: 买1量 - Buy 1 Volumn
# BRIAN: 卖1价 - Sell 1 Price
# BRIAN: 卖1量 - Sell 1 Volumn
# BRIAN: 时间 - Datetime
# BRIAN: 接口 - Gateway


#
# LogMonitor
# 
# BRIAN: 时间 - Datetime
# BRIAN: 信息 - Information
# BRIAN: 接口 - Gateway


#
# TradeMonitor
#
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


#
# OrderMonitor
#
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

#
# init_ui
#
# BRIAN: 双击单元格撤单 - Double-click the cell to cancel the order


#
# PositionMonitor
#
# BRIAN: 代码 - Symbol
# BRIAN: 交易所 - Exchange
# BRIAN: 方向 - Direction
# BRIAN: 数量 - Volume
# BRIAN: 昨仓 - Yesterday
# BRIAN: 冻结 - Frozen
# BRIAN: 均价 - Avg. Price
# BRIAN: 已成交 - Profit/Loss
# BRIAN: 接口 - Gateway


#
# AccountMonitor
#
# BRIAN: 账号 - Account ID
# BRIAN: 余额 - Balance
# BRIAN: 冻结 - Frozen
# BRIAN: 可用 - Available
# BRIAN: 接口 - Gateway


#
# ConnectDialog
#

#
# init_ui
#
# BRIAN: 连接 - Connect
# BRIAN: 密码 - Password


#
# TradingWidget
#

#
# init_ui
#
# BRIAN: 委托 - Send
# BRIAN: 全撤 - Cancel All
# BRIAN: 交易所 - Exchange
# BRIAN: 代码 - Symbol
# BRIAN: 名称 - Name
# BRIAN: 方向 - Direction
# BRIAN: 开平 - Offset
# BRIAN: 类型 - Type
# BRIAN: 价格 - Price
# BRIAN: 数量 - Volume
# BRIAN: 接口 - Gateway


#
# send_order
#
# BRIAN: 委托失败 - Send failed
# BRIAN: 请输入合约代码 - Please enter the contract code
# BRIAN: 委托失败 - Send failed
# BRIAN: 请输入委托数量 - Please enter the number of orders


#
# ContractManager
#
# BRIAN: 本地代码 - Native Symbol
# BRIAN: 代码 - Symbol 
# BRIAN: 交易所 - Exchange
# BRIAN: 名称 - Name 
# BRIAN: 合约分类 - Contract Classification
# BRIAN: 合约乘数 - Contract multiplier
# BRIAN: 价格跳动 - Price Tick
# BRIAN: 最小委托量 - Min Volume
# BRIAN: 交易接口 - Trading Gateway

#
# init_ui
#
# BRIAN: 合约查询 - Contract Inquiry
# BRIAN: 输入合约代码或者交易所 - Enter contract code or exchange
# BRIAN: 留空则查询所有合约 - Leave blank to query all contracts
# BRIAN: 查询 - Inquire

#
# AboutDialog
#

#
# init_ui
#
# BRIAN: 关于 - About


#
# GlobalDialog
#

#
# init_ui
#
# BRIAN: 全局配置 - Global Configuration
# BRIAN: 确定 - Apply

#
# update_setting
#
# BRIAN: 注意 - Note
# BRIAN: 全局配置的修改需要重启 - Changes to global configuration require restart
# BRIAN: 后才会生效 - to take effect


# ======================================
# vnpy/trader/constant.py
# ======================================

#
# Direction
#
# BRIAN: 多 - Long
# BRIAN: 空 - Short
# BRIAN: 净 - Net

#
# Offset
#
# BRIAN: 开 - Open
# BRIAN: 平 - Close
# BRIAN: 平今 - Close Today
# BRIAN: 平昨 - Close Yesterday

#
# Status
#
# BRIAN: 提交中 - Submitting
# BRIAN: 未成交 - Not Traded
# BRIAN: 部分成交 - Part Traded
# BRIAN: 全部成交 - All Traded
# BRIAN: 已撤销 - Canceled
# BRIAN: 拒单 - Rejected

#
# Product
#
# BRIAN: 股票 - Equity
# BRIAN: 期货 - Futures
# BRIAN: 期权 - Option
# BRIAN: 指数 - Index
# BRIAN: 外汇 - Forex
# BRIAN: 现货 - Spot
# BRIAN: 债券 - Bond
# BRIAN: 权证 - Warrant
# BRIAN: 价差 - Spread
# BRIAN: 基金 - Fund

#
# OrderType
#
# BRIAN: 限价 - Limit
# BRIAN: 市价 - Market

#
# OptionType
#
# <TO_CONFIRM>
# BRIAN: 看涨期权 - Call
# BRIAN: 看跌期权 - Put


# ======================================
# vnpy/trader/ui/editor.py
# ======================================

#
# init_ui
#
# BRIAN: 策略编辑器 - Strategy Editor

#
# init_menu
#
# BRIAN: 文件 - File
# BRIAN: 新建文件 - New File
# BRIAN: 打开文件 - Open File
# BRIAN: 关闭文件 - Close File
# BRIAN: 保存 - Save
# BRIAN: 另存为 - Save as...
# BRIAN: 退出 - Close
# BRIAN: 编辑 - Edit
# BRIAN: 撤销 - Revoke
# BRIAN: 恢复 - Restore
# BRIAN: 复制 - Copy
# BRIAN: 粘贴 - Paste
# BRIAN: 剪切 - Cut
# BRIAN: 查找 - Find
# BRIAN: 替换 - Replace

#
# open_file
#
# BRIAN: 打开文件 - Open File

#
# save_file
#
# BRIAN: 保存 - Save

#
# save_file_as
#
# BRIAN: 保存 - Save

#
# closeEvent
#
# BRIAN: 退出保存 - Save and Exit
# BRIAN: 是否要保存 - Save?
# BRIAN: 保存 - Save


#
# FindDialog
#

#
# init_ui
#
# BRIAN: 查找 - Find
# BRIAN: 替换 - Replace
# BRIAN: 大小写 - Case sensitive
# BRIAN: 全词匹配 - Whole word
# BRIAN: 选中区域 - In selection
# BRIAN: 替换 - Replace


# ======================================
# vnpy/trader/ui/__init__.py
# ======================================
#
# ExceptionDialog
#
#
# init_ui
#
# BRIAN: 触发异常 - Trigger an Exception
# BRIAN: 复制 - Copy
# BRIAN: 求助 - Ask for Help
# BRIAN: 关闭 - Close


# ======================================
# vnpy/trader/engine.py
# ======================================
#
# get_gateway
#
# BRIAN: 找不到底层接口 - Cannot find Gateway
# BRIAN: 找不到引擎 - Engine not found


# ======================================
# vnpy/gateway/ib/ib_gateway.py
# ======================================
#
# IbGateway
#
# BRIAN: TWS地址 - TWS Address
# BRIAN: TWS端口 - TWS Port
# BRIAN: 客户号 - Client Number
# BRIAN: 交易账户 - Transaction Account

#
# connectAck
#
# BRIAN: TWS连接成功 - TWS Connection succeeded

#
# connectionClosed
#
# BRIAN: TWS连接断开 - TWS disconnected

#
# currentTime
#
# BRIAN: 服务器时间 - Server time

#
# error
#
# BRIAN: 信息通知，代码 - Information notification, code
# BRIAN: 内容 - Content


#
# updatePortfolio
#
# BRIAN: 存在不支持的交易所持仓 - Unsupported exchange positions

#
# managedAccounts
#
# BRIAN: 当前使用的交易账号为 - Current trading account is

#
# subscribe
#
# BRIAN: 不支持的交易所 - Unsupported exchange
# BRIAN: 代码解析失败，请检查格式是否正确 - Symbol parsing failed, please check if the format is correct

#
# send_order
#
# BRIAN: 不支持的交易所 - Unsupported exchange
# BRIAN: 不支持的价格类型 - Unsupported price type

#
# load_contract_data
#
# BRIAN: 本地缓存合约信息加载成功 - Local cache contract information loaded successfully


# ======================================
# vnpy/app/datamanager/ui/widget.py
# ======================================
#
# init_ui
#
# BRIAN: 数据管理 - Data Management
# BRIAN: 刷新 - Refresh
# BRIAN: 导入数据 - Import Data

#
# init_tree
#
# BRIAN: 数据 - Data
# BRIAN: 本地代码 - Native Symbol
# BRIAN: 代码 - Symbol
# BRIAN: 交易所 - Exchange
# BRIAN: 数据量 - Amount of Data
# BRIAN: 开始时间 - Start time
# BRIAN: 结束时间 - End time
# BRIAN: K线数据 - K-line data
# BRIAN: 分钟线 - Minute line
# BRIAN: 小时线 - Hour line
# BRIAN: 日线 - Daily line

#
# init_table
# 
# BRIAN: 时间 - Time
# BRIAN: 开盘价 - Open price
# BRIAN: 最高价 - Highest price
# BRIAN: 最低价 - Lowest price
# BRIAN: 收盘价 - Close price
# BRIAN: 成交量 - Volume
# BRIAN: 持仓量 - Open interest

#
# refresh_tree
# 
# BRIAN: 导出 - Export 
# BRIAN: 查看 - Show

#
# import_data
#
# BRIAN: CSV载入成功 - CSV loaded successfully
# BRIAN: 代码 - Symbol
# BRIAN: 交易所 - Exchange
# BRIAN: 周期 - Interval
# BRIAN: 起始 - Start
# BRIAN: 结束 - End
# BRIAN: 总数量 - Total amount
# BRIAN: 载入成功 - Loaded successfully

#
# output_data
#
# BRIAN: 导出数据 - Export data
# BRIAN: 导出失败 - Export failed
# BRIAN: 该文件已在其他程序中打开，请关闭相关程序后再尝试导出数据
# The file is already open in another program, please close the program before trying to export the data

#
# DateRangeDialog
#

#
# __init__
#
# BRIAN: 选择数据区间 - Select data interval 
# BRIAN: 确定 - Apply
# BRIAN: 开始时间 - Start time
# BRIAN: 结束时间 - End time


#
# ImportDialog
#

#
# __init__
#
# BRIAN: 从CSV文件导入数据 - Importing data from a CSV file
# BRIAN: 选择文件 - Select file
# BRIAN: 确定 - Apply
# BRIAN: 合约信息 - Contract information
# BRIAN: 表头信息 - Header information
# BRIAN: 格式信息 - Format information
# BRIAN: 代码 - Symbol
# BRIAN: 交易所 - Exchange 
# BRIAN: 周期 - Interval
# BRIAN: 时间戳 - Datetime
# BRIAN: 开盘价 - Open price
# BRIAN: 最高价 - Highest price
# BRIAN: 最低价 - Lowest price
# BRIAN: 收盘价 - Close price
# BRIAN: 成交量 - Volume
# BRIAN: 持仓量 - Open interest
# BRIAN: 时间格式 - Time format


# ======================================
# vnpy/gateway/ctp/ui/ctp_gateway.py
# ======================================
# BRIAN: 请选择开平方向 - Please choose Offset type
# BRIAN:  - 
# BRIAN:  - 
# BRIAN:  - 
# BRIAN:  - 
# BRIAN:  - 
# BRIAN:  - 


# ======================================
# vnpy/app/cta_strategy/ui/widget.py
# ======================================

#
# CtaManager
#

#
# init_ui
#
# BRIAN: CTA策略 - CTA Strategy
# BRIAN: 添加策略 - Add Strategy
# BRIAN: 全部初始化 - Initialize All
# BRIAN: 全部启动 - Start All
# BRIAN: 全部停止 - Stop All
# BRIAN: 清空日志 - Clear Log


#
# StrategyManager
#

#
# init_ui
#
# BRIAN: 初始化 - Initialize
# BRIAN: 启动 - Start
# BRIAN: 停止 - Stop
# BRIAN: 编辑 - Edit
# BRIAN: 移除 - Remove


#
# StopOrderMonitor
#
# BRIAN: 停止委托号 - Stop Order ID
# BRIAN: 限价委托号 - Limit Order ID
# BRIAN: 本地代码 - Native Symbol
# BRIAN: 方向 - Direction
# BRIAN: 开平 - Offset
# BRIAN: 价格 - Price
# BRIAN: 数量 - Volume
# BRIAN: 状态 - Status
# BRIAN: 锁仓 - Lock
# BRIAN: 策略名 - Strategy Name

#
# LogMonitor
#
# BRIAN: 时间 - Datetime
# BRIAN: 信息 - Information

#
# SettingEditor
#

#
# init_ui
#
# BRIAN: 添加策略 - Add Strategy
# BRIAN: 添加 - Add to
# BRIAN: 参数编辑 - Parameter Editing
# BRIAN: 确定 - Apply


# ======================================
# vnpy/app/cta_strategy/engine.py
# ======================================

#
# CtaEngine
#
#
# init_engine
#
# BRIAN: CTA策略引擎初始化成功 - 
# CTA policy engine initialized successfully

#
# init_rqdata
#
# BRIAN: RQData数据接口初始化成功 - 
# RQData data interface initialized successfully

#
# cancel_server_order
#
# BRIAN: 撤单失败，找不到委托 - 
# Order cancellation failed, no order found

#
# send_order
#
# BRIAN: 委托失败，找不到合约 - 
# Order failed, no contract found

#
# call_strategy_func
#
# BRIAN: 触发异常已停止 - Trigger exception stopped

#
# add_strategy
#
# BRIAN: 创建策略失败，存在重名 - 
# Creating policy failed with duplicate name
# BRIAN: 创建策略失败，找不到策略类 -
# Failed to create policy, no policy class found

#
# _init_strategy
#
# BRIAN: 已经完成初始化，禁止重复操作 - 
# initialization is completed and repeated operations are prohibited
# BRIAN: 开始执行初始化 - Start initialization
# BRIAN: 行情订阅失败，找不到合约 - 
# Quote subscription failed, no contract found
# BRIAN: 初始化完成 - loading finished

#
# start_strategy
#
# BRIAN: 策略 - Strategy
# BRIAN: 启动失败，请先初始化 - startup failed, please initialize first

# BRIAN: 已经启动，请勿重复操作 - already started, do not repeat

#
# remove_strategy
#
# BRIAN: 策略 - Strategy
# BRIAN: 移除失败，请先停止 - removal failed, please stop first

#
# load_strategy_class_from_module
#
# BRIAN: 策略文件 - Policy file
# BRIAN: 加载失败，触发异常 - loading failed with exception

#
# send_email
#
# BRIAN: CTA策略引擎 - CTA Strategy Engine


# ======================================
# vnpy/app/cta_strategy/base.py
# ======================================

#
# StopOrderStatus
#
# BRIAN: 等待中 - Waiting
# BRIAN: 已撤销 - Canceled
# BRIAN: 已触发 - Trigger

#
# EngineType
#
# BRIAN: 实盘 - Live
# BRIAN: 回测 - Backtesting


# ===================================================
# vnpy/app/cta_strategy/strategies/<NAME>_strategy.py
# ===================================================

#
# <NAME>Strategy
#
# BRIAN: 用Python的交易员 - Trader using Python
# BRIAN: 策略初始化 - Strategy initialized
# BRIAN: 策略启动 - Strategy started
# BRIAN: 策略停止 - Strategy stopped
# BRIAN: 耗时%s毫秒 - Time consumming %s miliseconds
# BRIAN: 测试已全部完成 - Tests are all completed
# BRIAN: 执行市价单测试 - Perform market order test
# BRIAN: 执行限价单测试 - Perform limit order test
# BRIAN: 执行停止单测试 - Perform stop order test
# BRIAN: 执行全部撤单测试 - Perform all cancel Tests


# ===================================================
# vnpy/app/cta_backtester/engine.py
# ===================================================
#
# BacktestingEngine
#
#
# load_data
#
# BRIAN: 开始加载历史数据 - Start loading historical data
# BRIAN: 起始日期必须小于结束日期 - Start date must be less than end date
# BRIAN: 参数优化起始点必须小于终止点 - 
# Parameter optimization start point must be less than end point
# BRIAN: 参数优化步进必须大于0 - Parameter optimization step must be greater than 0

# BRIAN: 加载进度 - Loading progress
# BRIAN: 历史数据加载完成，数据量 - 
# Loading of historical data is complete, the amount of data
# BRIAN: 触发异常，回测终止 - Trigger exception, backtest terminated
# BRIAN: 策略初始化完成 - Policy initialization completed
# BRIAN: 开始回放历史数据 - Start playback of historical data
# BRIAN: 历史数据回放结束 - End of historical data playback
# BRIAN: 开始计算逐日盯市盈亏 - 
# Start calculating daily mark-to-market profit and loss
# BRIAN: 成交记录为空，无法计算 - 
# Transaction record is empty and cannot be calculated
# BRIAN: 逐日盯市盈亏计算完成 - 
# Completion of daily mark-to-market profit and loss calculation
# BRIAN: 开始计算策略统计指标 - Start calculating strategy statistics
# BRIAN: 首个交易日 - Start trading day
# BRIAN: 最后交易日 - End trading day
# BRIAN: 总交易日 - Total trading days
# BRIAN: 盈利交易日 - Profitable trading days
# BRIAN: 亏损交易日 - Lost trading days

# BRIAN: 起始资金 - Starting capital
# BRIAN: 结束资金 - End balance
# BRIAN: 总收益率 - Total return
# BRIAN: 年化收益 - Annual return
# BRIAN: 最大回撤 - Max Drawdown
# BRIAN: 百分比最大回撤 - Max DD percent
# BRIAN: 最长回撤天数 - Max Drawdown duration

# BRIAN: 总盈亏 - Total profit/loss
# BRIAN: 总手续费 - Total commission
# BRIAN: 总滑点 - Total slippage
# BRIAN: 总成交金额 - Total turnover
# BRIAN: 总成交笔数 - Total transactions

# BRIAN: 日均盈亏 - Daily avg. profit and loss
# BRIAN: 日均手续费 - Daily avg. commission
# BRIAN: 日均滑点 - Daily slippage
# BRIAN: 日均成交金额 - Daily avg. turnover
# BRIAN: 日均成交笔数 - Daily avg. transactions

# BRIAN: 日均收益率 - Daily avg. return
# BRIAN: 收益标准差 - Standard deviation of returns
# BRIAN: 收益回撤比 - Return DD ratio

# BRIAN: 策略统计指标计算完成 - Computation of strategy statistics indicators

# BRIAN: 优化参数组合为空，请检查 - Optimization parameter combination is empty, please check

# BRIAN: 参数 - Parameter
# BRIAN: 目标 - Target
# BRIAN: 优化参数组合为空，请检查 - 
# Optimization parameter combination is empty, please check
# BRIAN: 优化目标未设置，请检查 - Optimization target is not set, please check

# BRIAN: 参数优化空间 - Parameter optimization space
# BRIAN: 每代族群总数 - Total population per generation
# BRIAN: 优良筛选个数 - Excellent screening number
# BRIAN: 迭代次数 - Number of iterations
# BRIAN: 交叉概率 - Cross probability
# BRIAN: 突变概率 - Mutation probability
# BRIAN: 遗传算法优化完成，耗时{cost}秒 -





# ===================================================
# vnpy/app/cta_backtester/engine.py
# ===================================================
#
# BacktesterEngine
#

#
# init_engine
#
# BRIAN: 初始化CTA回测引擎 - Initialize the CTA Backtest engine
# BRIAN: 策略文件加载完成 - Policy file loading is completed

#
# init_rqdata
#
# BRIAN: RQData数据接口初始化成功 - 
# RQData data interface initialized successfully

#
# load_strategy_class_from_module
#
# BRIAN: 策略文件 - Policy file
# BRIAN: 加载失败，触发异常 - Loading failed with exception

#
# reload_strategy_class
#
# BRIAN: 策略文件重载刷新完成 - Policy file reload completed

#
# start_backtesting
#
# BRIAN: 已有任务在运行中，请等待完成 - 
# Task is already running, please wait for completion

#
# run_optimization
#
# BRIAN: 开始遗传算法参数优化 - 
# Start genetic algorithm parameter optimization

# BRIAN: 开始多进程参数优化 - 
# Start multi-process parameter optimization

# BRIAN: 多进程参数优化完成 - 
# Multi-process parameter optimization completed

#
# start_optimization
#
# BRIAN: 已有任务在运行中，请等待完成 - 
# Task already is running, please wait for completion

#
# run_downloading
#
# BRIAN: 开始下载历史数据 - Start downloading historical data
# BRIAN: 历史数据下载完成 - Historical data download completed
# BRIAN: 数据下载失败，无法获取 - Data download failed and cannot be obtained
# BRIAN: 的历史数据 - Historical data
# BRIAN: 数据下载失败，触发异常 - Data download failed with exception

#
# start_downloading
#
# BRIAN: 已有任务在运行中，请等待完成 - 
# Task is already running, please wait for completion


# ===================================================
# vnpy/app/cta_backtester/ui/widget.py
# ===================================================

#
# BacktesterManager
#
#
# init_ui
#
# BRIAN: CTA回测 - CTA Backtest
# BRIAN: 正向 - Forward
# BRIAN: 反向 - Reverse
# BRIAN: 开始回测 - Start backtesting
# BRIAN: 参数优化 - Parameter Optimization
# BRIAN: 优化结果 - Optimization Results
# BRIAN: 下载数据 - Download Data
# BRIAN: 委托记录 - Order Book
# BRIAN: 成交记录 - Transaction Record
# BRIAN: 每日盈亏 - Daily Profit/Loss
# BRIAN: K线图表 - K-line chart
# BRIAN: 代码编辑 - Code Editing
# BRIAN: 策略重载 - Strategy Reload

# BRIAN: 交易策略 - Trading Strategy
# BRIAN: 本地代码 - Native Symbol
# BRIAN: K线周期 - K-line Period
# BRIAN: 开始日期 - Start Date
# BRIAN: 结束日期 - End Date
# BRIAN: 手续费率 - Commission Rate
# BRIAN: 交易滑点 - Trading Slippage
# BRIAN: 合约乘数 - Contract Multiplier
# BRIAN: 价格跳动 - Price Tick
# BRIAN: 回测资金 - Backtesting Fund
# BRIAN: 合约模式 - Contract Model

# BRIAN: 回测成交记录 - Backtesting Transaction Records
# BRIAN: 回测委托记录 - Backtesting Commission Records
# BRIAN: 回测每日盈亏 - Backtesting Daily Profit/Loss

# BRIAN: 请点击[优化结果]按钮查看 - 
# Please click the [Optimization Results] button to view

# BRIAN: 正向 - Forward

# BRIAN: 首个交易日 - Start Date
# BRIAN: 最后交易日 - End Date
# BRIAN: 总交易日 - Total Days
# BRIAN: 盈利交易日 - Profitable Day
# BRIAN: 亏损交易日 - Loss Day
# BRIAN: 起始资金 - Capital
# BRIAN: 结束资金 - End Balance
# BRIAN: 总收益率 - Total Return
# BRIAN: 年化收益 - Annual Return
# BRIAN: 最大回撤 - Max Drawdown
# BRIAN: 百分比最大回撤 - Max DD Percent
# BRIAN: 总盈亏 - Total Profit-Loss
# BRIAN: 总手续费 - Total Commission
# BRIAN: 总滑点 - Total Slippage
# BRIAN: 总成交额 - Total Turnover
# BRIAN: 总成交笔数 - Total Transactions
# BRIAN: 日均盈亏 - Daily Profit/Loss
# BRIAN: 日均手续费 - Daily Commission
# BRIAN: 日均滑点 - Daily Slippage
# BRIAN: 日均成交额 - Daily Turnover
# BRIAN: 日均成交笔数 - Daily Transactions
# BRIAN: 日均收益率 - Daily Return
# BRIAN: 收益标准差 - Daily Standard Deviation
# BRIAN: 夏普比率 - Sharpe Ratio
# BRIAN: 收益回撤比 - Return DD Ratio

# BRIAN: 策略参数配置 - Policy Parameter Configuration
# BRIAN: 确定 - Apply

# BRIAN: 账户净值 - Account Equity
# BRIAN: 净值回撤 - Net Drawdown
# BRIAN: 每日盈亏 - Daily Profit/Loss
# BRIAN: 盈亏分布 - Profit and Loss Distribution

# BRIAN: 总收益率 - Total Return
# BRIAN: 夏普比率 - Sharpe Ratio
# BRIAN: 收益回撤比 - Return DD Ratio
# BRIAN: 日均盈亏 - Daily Profit/Loss

# BRIAN: 目标 - Target
# BRIAN 参数 - Parameter
# BRIAN: 开始 - Start
# BRIAN: 步进 - Step
# BRIAN: 结束 - End
# BRIAN: 优化参数配置 - Optimization Parameter Configuration

# BRIAN: 多进程优化 - Multi-process Optimization
# BRIAN: 遗传算法优化 - Genetic Algorithm Optimization

# BRIAN: 参数优化结果 - Parameter Optimization Results
# BRIAN 参数 - Parameter
# BRIAN: 保存 - Save
# BRIAN: 保存数据 - Save Data
# BRIAN: 参数 - Parameter

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

# BRIAN: 日期 - Date
# BRIAN: 成交笔数 - No. of Transactions
# BRIAN: 开盘持仓 - Open Positions
# BRIAN: 收盘持仓 - End Positions
# BRIAN: 成交额 - Tunrover
# BRIAN: 手续费 - Commission
# BRIAN: 滑点 - Slippage
# BRIAN: 交易盈亏 - Trading Profit/Loss
# BRIAN: 持仓盈亏 - Holding Profit/Loss
# BRIAN: 总盈亏 - Total Profit/Loss
# BRIAN: 净盈亏 - Net Profit/Loss

# BRIAN: 回测K线图表 - Backtest Chart







# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
# BRIAN:  -
