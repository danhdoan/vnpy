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