from typing import Callable, Dict
from pathlib import Path

from PyQt5 import QtWidgets, Qsci, QtGui

from vnpy.event import EventEngine
from ..engine import MainEngine


class CodeEditor(QtWidgets.QMainWindow):
    """"""
    NEW_FILE_NAME: str = "Untitled"

    _instance: "CodeEditor" = None

    def __new__(cls, *args, **kwargs):
        """"""
        if not cls._instance:
            cls._instance = QtWidgets.QMainWindow.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, main_engine: MainEngine = None, event_engine: EventEngine = None):
        """"""
        super().__init__()

        self.new_file_count: int = 0
        self.editor_path_map: Dict[Qsci.QsciScintilla, str] = {}

        self.init_ui()

    def init_ui(self) -> None:
        """"""
        # BRIAN: 策略编辑器 - Strategy Editor
        self.setWindowTitle("Strategy Editor")

        self.init_menu()
        self.init_central()

    def init_central(self) -> None:
        """"""
        self.tab = QtWidgets.QTabWidget()
        self.tab.currentChanged.connect(self.update_path_label)

        self.path_label = QtWidgets.QLabel()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.tab)
        vbox.addWidget(self.path_label)

        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)

    def init_menu(self) -> None:
        """"""
        bar = self.menuBar()

        # BRIAN: 文件 - File
        file_menu = bar.addMenu("File")
        # BRIAN: 新建文件 - New File
        self.add_menu_action(file_menu, "New File", self.new_file, "Ctrl+N")
        # BRIAN: 打开文件 - Open File
        self.add_menu_action(file_menu, "Open File", self.open_file, "Ctrl+O")
        # BRIAN: 关闭文件 - Close File
        self.add_menu_action(file_menu, "Close File", self.close_editor, "Ctrl+W")
        file_menu.addSeparator()
        # BRIAN: 保存 - Save
        self.add_menu_action(file_menu, "Save", self.save_file, "Ctrl+S")
        # BRIAN: 另存为 - Save as...
        self.add_menu_action(
            file_menu,
            "Save as...",
            self.save_file_as,
            "Ctrl+Shift+S"
        )
        file_menu.addSeparator()
        # BRIAN: 退出 - Close
        self.add_menu_action(file_menu, "Close", self.close)

        # BRIAN: 编辑 - Edit
        edit_menu = bar.addMenu("Edit")
        # BRIAN: 撤销 - Revoke
        self.add_menu_action(edit_menu, "Revoke", self.undo, "Ctrl+Z")
        # BRIAN: 恢复 - Restore
        self.add_menu_action(edit_menu, "Restore", self.redo, "Ctrl+Y")
        edit_menu.addSeparator()
        # BRIAN: 复制 - Copy
        self.add_menu_action(edit_menu, "Copy", self.copy, "Ctrl+C")
        # BRIAN: 粘贴 - Paste
        self.add_menu_action(edit_menu, "Paste", self.paste, "Ctrl+P")
        # BRIAN: 剪切 - Cut
        self.add_menu_action(edit_menu, "Cut", self.cut, "Ctrl+X")
        edit_menu.addSeparator()
        # BRIAN: 查找 - Find
        self.add_menu_action(edit_menu, "Find", self.find, "Ctrl+F")
        # BRIAN: 替换 - Replace
        self.add_menu_action(edit_menu, "Replace", self.replace, "Ctrl+H")

    def add_menu_action(
        self,
        menu: QtWidgets.QMenu,
        action_name: str,
        func: Callable,
        shortcut: str = "",
    ) -> None:
        """"""
        action = QtWidgets.QAction(action_name, self)
        action.triggered.connect(func)
        menu.addAction(action)

        if shortcut:
            sequence = QtGui.QKeySequence(shortcut)
            action.setShortcut(sequence)

    def new_editor(self) -> Qsci.QsciScintilla:
        """"""
        # Create editor object
        editor = Qsci.QsciScintilla()

        # Set editor font
        font = QtGui.QFont()
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(10)

        editor.setFont(font)
        editor.setMarginsFont(font)

        # Set margin for line numbers
        font_metrics = QtGui.QFontMetrics(font)
        editor.setMarginWidth(0, font_metrics.width("00000") + 6)
        editor.setMarginLineNumbers(0, True)
        editor.setMarginsBackgroundColor(QtGui.QColor("#cccccc"))

        # Set brace matching
        editor.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)

        # Hide horizontal scroll bar
        editor.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # Set current line color
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QtGui.QColor("#ffe4e4"))

        # Set Python lexer
        lexer = Qsci.QsciLexerPython()
        lexer.setDefaultFont(font)
        editor.setLexer(lexer)

        # Add minimum editor size
        editor.setMinimumSize(600, 450)

        # Enable auto complete
        editor.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        editor.setAutoCompletionThreshold(2)
        editor.setAutoCompletionCaseSensitivity(False)
        editor.setAutoCompletionReplaceWord(False)

        # Use space indentation
        editor.setIndentationsUseTabs(False)
        editor.setTabWidth(4)
        editor.setIndentationGuides(True)

        # Enable folding
        editor.setFolding(True)

        return editor

    def open_editor(self, file_path: str = "") -> None:
        """"""
        # Show editor tab if file already opened
        if file_path:
            file_path = str(Path(file_path))

            for editor, path in self.editor_path_map.items():
                if file_path == path:
                    editor.show()
                    return

        # Otherwise create new editor
        editor = self.new_editor()

        if file_path:
            buf = open(file_path, encoding="UTF8").read()
            editor.setText(buf)
            file_name = Path(file_path).name

            self.editor_path_map[editor] = file_path
        else:
            self.new_file_count += 1
            file_name = f"{self.NEW_FILE_NAME}-{self.new_file_count}"

            self.editor_path_map[editor] = file_name

        i = self.tab.addTab(editor, file_name)
        self.tab.setCurrentIndex(i)

        self.path_label.setText(file_path)

    def close_editor(self) -> None:
        """"""
        i = self.tab.currentIndex()

        # Close editor if last file closed
        if not i:
            self.close()
        # Otherwise only close current tab
        else:
            self.save_file()

            editor = self.get_active_editor()
            self.editor_path_map.pop(editor)

            self.tab.removeTab(i)

    def open_file(self) -> None:
        """"""
        # BRIAN: 打开文件 - Open File
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "Python(*.py)")

        if file_path:
            self.open_editor(file_path)

    def new_file(self) -> None:
        """"""
        self.open_editor("")

    def save_file(self) -> None:
        """"""
        editor = self.get_active_editor()
        file_path = self.editor_path_map[editor]

        if self.NEW_FILE_NAME in file_path:
            # BRIAN: 保存 - Save
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save", "", "Python(*.py)")

        self.save_editor_text(editor, file_path)

    def save_file_as(self) -> None:
        """"""
        editor = self.get_active_editor()

        # BRIAN: 保存 - Save
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", "", "Python(*.py)")

        self.save_editor_text(editor, file_path)

    def save_editor_text(self, editor: Qsci.QsciScintilla, file_path: str) -> None:
        """"""
        if file_path:
            self.editor_path_map[editor] = file_path

            i = self.tab.currentIndex()
            file_name = Path(file_path).name
            self.tab.setTabText(i, file_name)

            with open(file_path, "w", encoding="UTF8") as f:
                f.write(editor.text())

        self.update_path_label()

    def copy(self) -> None:
        """"""
        self.get_active_editor().copy()

    def paste(self) -> None:
        """"""
        self.get_active_editor().paste()

    def undo(self) -> None:
        """"""
        self.get_active_editor().undo()

    def redo(self) -> None:
        """"""
        self.get_active_editor().redo()

    def cut(self) -> None:
        """"""
        self.get_active_editor().cut()

    def find(self) -> None:
        """"""
        dialog = FindDialog(
            self.get_active_editor(),
            False
        )
        dialog.exec_()

    def replace(self) -> None:
        """"""
        dialog = FindDialog(
            self.get_active_editor(),
            True
        )
        dialog.exec_()

    def get_active_editor(self) -> Qsci.QsciScintilla:
        """"""
        return self.tab.currentWidget()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """"""
        for editor, path in self.editor_path_map.items():
            # BRIAN: 退出保存 - Save and Exit
            # BRIAN: 是否要保存 - Save?
            i = QtWidgets.QMessageBox.question(
                self,
                "Save and Exit",
                f"Save {path}?",
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Save
            )

            if i == QtWidgets.QMessageBox.Save:
                if self.NEW_FILE_NAME in path:
                    # BRIAN: 保存 - Save
                    path, _ = QtWidgets.QFileDialog.getSaveFileName(
                        self, "Save", "", "Python(*.py)")

                if path:
                    self.save_editor_text(editor, path)
            elif i == QtWidgets.QMessageBox.Cancel:
                break

        event.accept()

    def show(self) -> None:
        """"""
        if not self.tab.count():
            self.open_editor()

        self.showMaximized()

    def update_path_label(self) -> None:
        """"""
        editor = self.get_active_editor()
        path = self.editor_path_map[editor]
        self.path_label.setText(path)


class FindDialog(QtWidgets.QDialog):
    """"""

    def __init__(
        self,
        editor: Qsci.QsciScintilla,
        show_replace: bool = False
    ):
        """"""
        super().__init__()

        self.editor: Qsci.QsciScintilla = editor
        self.show_replace: bool = show_replace
        self.new_task: bool = True

        self.init_ui()

    def init_ui(self) -> None:
        """"""
        # BRIAN: 查找 - Find
        find_label = QtWidgets.QLabel("Find")
        # BRIAN: 替换 - Replace
        replace_label = QtWidgets.QLabel("Replace")

        selected_text = self.editor.selectedText()
        self.find_line = QtWidgets.QLineEdit(selected_text)
        self.find_line.textChanged.connect(self.reset_task)

        self.replace_line = QtWidgets.QLineEdit()

        # BRIAN: 大小写 - Case sensitive
        self.case_check = QtWidgets.QCheckBox("Case sensitive")
        self.case_check.setChecked(True)
        self.case_check.stateChanged.connect(self.reset_task)

        # BRIAN: 全词匹配 - Whole word
        self.whole_check = QtWidgets.QCheckBox("Whole word")
        self.whole_check.stateChanged.connect(self.reset_task)

        # BRIAN: 选中区域 - In selection
        self.selection_check = QtWidgets.QCheckBox("In selection")
        self.selection_check.stateChanged.connect(self.reset_task)

        # BRIAN: 查找 - Find
        find_button = QtWidgets.QPushButton("Find")
        find_button.clicked.connect(self.find_text)

        # BRIAN: 替换 - Replace
        self.replace_button = QtWidgets.QPushButton("Replace")
        self.replace_button.clicked.connect(self.replace_text)
        self.replace_button.setEnabled(False)

        check_hbox = QtWidgets.QHBoxLayout()
        check_hbox.addWidget(self.case_check)
        check_hbox.addStretch()
        check_hbox.addWidget(self.whole_check)
        check_hbox.addStretch()
        check_hbox.addWidget(self.selection_check)
        check_hbox.addStretch()

        button_hbox = QtWidgets.QHBoxLayout()
        button_hbox.addWidget(find_button)
        button_hbox.addWidget(self.replace_button)

        form = QtWidgets.QFormLayout()
        form.addRow(find_label, self.find_line)
        form.addRow(replace_label, self.replace_line)
        form.addRow(check_hbox)
        form.addRow(button_hbox)

        self.setLayout(form)

        if self.show_replace:
            # BRIAN: 替换 - Replace
            self.setWindowTitle("Replace")
        else:
            # BRIAN: 查找 - Find
            self.setWindowTitle("Find")

            replace_label.setVisible(False)
            self.replace_line.setVisible(False)
            self.replace_button.setVisible(False)

    def find_text(self) -> None:
        """"""
        if not self.new_task:
            result = self.editor.findNext()

            if result:
                self.new_task = False
                self.replace_button.setEnabled(True)
                return
            else:
                self.new_task = True

        self.editor.cancelFind()

        if not self.selection_check.isChecked():
            result = self.editor.findFirst(
                self.find_line.text(),
                False,
                self.case_check.isChecked(),
                self.whole_check.isChecked(),
                False,
                line=1,
                index=1
            )

        else:
            result = self.editor.findFirstInSelection(
                self.find_line.text(),
                False,
                self.case_check.isChecked(),
                self.whole_check.isChecked(),
                False
            )

        if result:
            self.new_task = False
            self.replace_button.setEnabled(True)
        else:
            self.new_task = True

    def replace_text(self) -> None:
        """"""
        new_text = self.replace_line.text()

        self.editor.replace(new_text)
        self.editor.findNext()

    def reset_task(self) -> None:
        """"""
        self.new_task = True
        self.replace_button.setEnabled(False)


if __name__ == "__main__":
    from vnpy.trader.ui import create_qapp

    app = create_qapp()
    editor = CodeEditor()
    editor.show()
    app.exec_()
