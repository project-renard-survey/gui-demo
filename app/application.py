import locale
import logging
from PyQt5 import QtWidgets, QtGui
import app
from app.mainwindow import MainWindow


log = logging.getLogger(__name__)


class Application(QtWidgets.QApplication):

    def __init__(self, args, main_widget=None):
        log.debug('init app')
        super().__init__(args)

        # Initialize application metadata
        locale.setlocale(locale.LC_ALL, '')
        self.setOrganizationName(app.ORG_NAME)
        self.setOrganizationDomain(app.ORG_DOMAIN)
        self.setApplicationDisplayName(app.APP_NAME)
        self.setApplicationName(app.APP_NAME)
        self.setApplicationVersion(app.APP_VERSION)

        # Gui Styles and Fonts
        self.setStyle('fusion')
        font_db = QtGui.QFontDatabase()
        font_db.addApplicationFont(':/fonts/Roboto-Regular.ttf')
        app_font = QtGui.QFont("Roboto Regular")
        app_font.setStyleStrategy(QtGui.QFont.PreferAntialias | QtGui.QFont.PreferQuality)
        app_font.setHintingPreference(QtGui.QFont.PreferNoHinting)
        self.setFont(app_font)

        # Initialize main window
        self.ui = main_widget() if main_widget else MainWindow()
        self.ui.show()

        # Shortcuts
        self.ui.debug_shortcut = QtWidgets.QShortcut('Ctrl+D', self.ui, self.on_ctrl_d)

    def on_ctrl_d(self):
        """Toogle Debug"""
        debug = app.settings.value('debug', False, bool)
        app.settings.setValue('debug', not debug)
        app.settings.sync()
        self.ui.statusbar.showMessage('Debug set to "{}"'.format(debug), 2000)