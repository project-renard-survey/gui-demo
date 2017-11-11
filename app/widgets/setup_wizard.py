# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

from app.backend.rpc import RpcClient
from app.ui.setup_wizard import Ui_SetupWizard
from PyQt5.QtWidgets import QWizard
from app.ui import resources_rc

log = logging.getLogger(__name__)


class SetupWizard(QWizard, Ui_SetupWizard):

    P1_LICENSE = 0
    P2_CHOOSE_MODE = 1
    P3_CONNECT = 2
    P4_CHOOSE_ACCOUNT = 3
    P5_IMPORT_ACCOUNT = 4
    P6_CREATE_ACCOUNT = 5
    P7_SYNC = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/images/resources/wizard_logo.png'))
        self.setPixmap(QWizard.BannerPixmap, QPixmap(':/images/resources/wizard_banner.png'))

        # Wizard state
        self._connection_tested = False

        # Global connections
        self.currentIdChanged.connect(self.current_id_changed)

        # Page 1 License agreement
        self.page1_license.isComplete = self.page1_license_is_complete
        self.radio_accept_license.clicked.connect(self.page1_license.completeChanged)
        self.radio_decline_icense.clicked.connect(self.page1_license.completeChanged)

        # Page 2 Choose Installation Mode
        self.button_group_choose_mode.buttonClicked.connect(self.next)

        # Page 3 Connect to existing node
        self.page3_connect.isComplete = self.page3_connect_is_complete
        self.button_test_connection.clicked.connect(self.test_connection)
        self.button_reset_connection_form.clicked.connect(self.reset_connection_form)

        # Page 4 Choose Account Create or Import
        self.button_group_choose_account.buttonClicked.connect(self.next)


    @pyqtSlot(int)
    def current_id_changed(self, page_id: int):
        # Hide Next Button on Command Link Pages
        if page_id in (self.P2_CHOOSE_MODE, self.P4_CHOOSE_ACCOUNT):
            self.button(QWizard.NextButton).hide()

    @pyqtSlot()
    def page1_license_is_complete(self):
        return self.radio_accept_license.isChecked()

    @pyqtSlot()
    def page3_connect_is_complete(self):
        # Verify connection to rpc host
        log.debug('Page 3 completion check request')
        return self._connection_tested

    @pyqtSlot()
    def test_connection(self):
        client = RpcClient(
            host=self.edit_rpc_host.text(),
            port=self.edit_rpc_port.text(),
            user=self.edit_rpc_user.text(),
            pwd=self.edit_rpc_password.text(),
            use_ssl=self.cbox_use_ssl.isChecked(),
        )
        try:
            response = client.getinfo()
            assert response['error'] is None
        except Exception as e:
            self.label_test_connection.setText(str(e))
            return

        msg = 'Successfully connected to %s' % response['result']['description']
        self.label_test_connection.setText(msg)
        self.button_test_connection.setDisabled(True)
        self.gbox_connect.setEnabled(False)
        self._connection_tested = True
        self.page3_connect.completeChanged.emit()

    @pyqtSlot()
    def reset_connection_form(self):
        for wgt in self.gbox_connect.children():
            if isinstance(wgt, QtWidgets.QLineEdit):
                wgt.clear()
            if isinstance(wgt, QtWidgets.QCheckBox):
                wgt.setChecked(False)
        self.label_test_connection.setText('Please test the connection to proceed.')
        self.button_test_connection.setEnabled(True)
        self._connection_tested = False
        self.gbox_connect.setEnabled(True)
        self.page3_connect.completeChanged.emit()

    def page2_next_id(self):
        if self.button_connect_node.isChecked():
            return self.P3_CONNECT
        elif self.button_setup_node.isChecked():
            return self.P4_CHOOSE_ACCOUNT

    def nextId(self):
        if self.currentId() == self.P2_CHOOSE_MODE:
            if self.button_connect_node.isChecked():
                return self.P3_CONNECT
            if self.button_setup_node.isChecked():
                return self.P4_CHOOSE_ACCOUNT
        if self.currentId() == self.P4_CHOOSE_ACCOUNT:
            if self.button_account_create.isChecked():
                return self.P6_CREATE_ACCOUNT
            if self.button_account_import.isChecked():
                return self.P5_IMPORT_ACCOUNT
        return super().nextId()


if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets
    from app.helpers import init_logging
    # import app
    # app.init()
    init_logging()
    wrapper = QtWidgets.QApplication(sys.argv)
    wrapper.setStyle('fusion')
    wizard = SetupWizard()
    wizard.show()
    sys.exit(wrapper.exec())

