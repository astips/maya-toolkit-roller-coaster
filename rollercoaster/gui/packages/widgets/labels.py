# -*- coding: utf-8 -*-

import os
import re
import string
from QtSide import QtWidgets, QtGui, QtCore
from ..color import Color


class ColorfulBGLabel(QtWidgets.QLabel):
    toggled = QtCore.pyqtSignal()

    def __init__(self, parent=None, wh=(40, 16), text='', basic=(75, 75, 75, 255), color=(255, 255, 255, 255)):
        super(ColorfulBGLabel, self).__init__(parent)
        self.state = False

        self.wh = wh
        self.text = text
        self.basic = basic
        self.color = color

        self.__style()

    def __style(self):
        self.setMinimumSize(QtCore.QSize(self.wh[0], self.wh[1]))
        self.setMaximumSize(QtCore.QSize(250, 40))

        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setMouseTracking(True)
        self.setText(self.text)
        self.setStyleSheet(
            "background-color: rgb({0}, {1}, {2}, {3});".format(self.basic[0], self.basic[1],
                                                                self.basic[2], self.basic[3])
        )

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def on(self):
        self.state = True
        self.setStyleSheet(
            "background-color: rgb({0}, {1}, {2}, {3});".format(self.color[0], self.color[1],
                                                                self.color[2], self.color[3])
        )

    def off(self):
        self.state = False
        self.setStyleSheet(
            "background-color: rgb({0}, {1}, {2}, {3});".format(self.basic[0], self.basic[1],
                                                                self.basic[2], self.basic[3])
        )

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()

    def mousePressEvent(self, event):
        self.toggle()
        self.toggled.emit()
        event.accept()


class ColorfulTextLabel(QtWidgets.QLabel):
    toggled = QtCore.pyqtSignal()

    def __init__(self, parent=None, wh=(40, 16), text='', bgc_color=(10, 10, 10, 30),
                 off_color=(75, 75, 75, 255), on_color=(255, 255, 255, 255)):
        super(ColorfulTextLabel, self).__init__(parent)

        self.state = False

        self.wh = wh
        self.text = text
        self.bgc_color = bgc_color
        self.off_color = off_color
        self.on_color = on_color

        self.__style()

    def __style(self):
        self.setMinimumSize(QtCore.QSize(self.wh[0], self.wh[1]))
        self.setMaximumSize(QtCore.QSize(250, 40))

        font = QtGui.QFont()
        font.setBold(True)
        # font.setPointSize(9)
        self.setFont(font)
        self.setMouseTracking(True)
        self.setText(self.text)
        self.setStyleSheet(
            "background-color: rgb({0}, {1}, {2}, {3});color: rgb({4}, {5}, {6}, {7});".format(
                self.bgc_color[0], self.bgc_color[1], self.bgc_color[2], self.bgc_color[3],
                self.off_color[0], self.off_color[1], self.off_color[2], self.off_color[3]
            )
        )

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def on(self):
        self.state = True
        self.setStyleSheet(
            "background-color: rgb({0}, {1}, {2}, {3});color: rgb({4}, {5}, {6}, {7});".format(
                self.bgc_color[0], self.bgc_color[1], self.bgc_color[2], self.bgc_color[3],
                self.on_color[0], self.on_color[1], self.on_color[2], self.on_color[3]
            )
        )

    def off(self):
        self.state = False
        self.setStyleSheet(
            "background-color: rgb({0}, {1}, {2}, {3});color: rgb({4}, {5}, {6}, {7});".format(
                self.bgc_color[0], self.bgc_color[1], self.bgc_color[2], self.bgc_color[3],
                self.off_color[0], self.off_color[1], self.off_color[2], self.off_color[3]
            )
        )

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()

    def mousePressEvent(self, event):
        self.toggle()
        self.toggled.emit()
        event.accept()


class TransparentLabel(QtWidgets.QLabel):
    """"""
    def __init__(self, parent=None, fc=QtGui.QColor(255, 255, 255), bc=QtGui.QColor(10, 10, 10)):
        QtWidgets.QLabel.__init__(self, parent)

        self.fc = fc
        self.bc = bc

        self.__style()

    def set_text(self, text, alpha):
        self.setText(text)
        self.__alpha(alpha)

    def __alpha(self, alpha):
        self.fc.setAlpha(alpha)
        self.bc.setAlpha(alpha/1.4)
        self.setStyleSheet(
            'color: {0}; background-color: {1};'.format(
                'rgb(%d, %d, %d, %d)' %self.fc.getRgb(), 'rgb(%d, %d, %d, %d)' %self.bc.getRgb()
            )
        )
        self.show()

    def __style(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


class ToastLabel(QtWidgets.QLabel):
    DEFAULT_DURATION = 500

    def __init__(self, parent=None, front_color=None, background_color=None, *args):
        QtWidgets.QLabel.__init__(self, parent, *args)
        if front_color is None:
            front_color = (255, 255, 255)
        if background_color is None:
            background_color = (0, 0, 0)

        self._alpha = 255

        self.__style()
        self.front_color = QtGui.QColor(front_color[0], front_color[1], front_color[2])
        self.background_color = QtGui.QColor(background_color[0], background_color[1], background_color[2])
        self._message_display_timer = QtCore.QTimer(self)
        self._message_display_timer.timeout.connect(self.display)
        self._message_fadeout_timer = QtCore.QTimer(self)
        self._message_fadeout_timer.timeout.connect(self.fadeout)

    def __style(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(11)
        self.setFont(font)
        self.setMouseTracking(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def align_to(self, widget, padding=50):
        width = self.get_text_width() + padding
        height = self.get_text_height() + padding + 50
        x = widget.width() / 2 - width / 2
        y = (widget.height() - height) / 2
        self.setGeometry(x, y, width, height)

    def text_rect(self):
        text = self.text()
        font = self.font()
        metrics = QtGui.QFontMetricsF(font)
        return metrics.boundingRect(text)

    def get_text_width(self):
        text_width = self.text_rect().width()
        return max(0, text_width)

    def get_text_height(self):
        text_height = self.text_rect().height()
        return max(0, text_height)

    def display(self):
        self._message_fadeout_timer.start(75)

    def fadeout(self):
        alpha = self.alpha()
        if alpha > 0:
            alpha -= 2
            self.setAlpha(alpha)
        else:
            self.hide()
            self._message_fadeout_timer.stop()
            self._message_display_timer.stop()

    def set_text(self, text=None, duration=None):
        if text:
            QtWidgets.QLabel.setText(self, text)
        duration = duration or self.DEFAULT_DURATION
        self.setAlpha(120)
        self._message_display_timer.stop()
        self._message_display_timer.start(duration)
        self.show()
        self.update()
        self.repaint()

    def alpha(self):
        return float(self._alpha)

    def setAlpha(self, value):
        if value < 0:
            value = 0
        self._alpha = value
        color = self.front_color
        background_color = self.background_color
        color = Color.from_color(color)
        color.setAlpha(self._alpha)
        background_color = Color.from_color(background_color)
        background_color.setAlpha(self._alpha/1.4)
        self.setStyleSheet(
            'color: {0}; background-color: {1};'.format(color.to_string(), background_color.to_string())
        )


class CloseLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None, wh=None, pixmap=None, close_icon=None):
        super(CloseLabel, self).__init__(parent)

        if wh is None:
            wh = (25, 25)
        self.wh = wh
        self.pixmap = pixmap
        self.close_icon = close_icon

        self.__style()
        self.close_btn.clicked.connect(self.close_btn.hide)

    def __style(self):
        self.setMinimumSize(QtCore.QSize(self.wh[0], self.wh[1]))
        self.setMaximumSize(QtCore.QSize(self.wh[0], self.wh[1]))
        self.setMouseTracking(True)
        self.setScaledContents(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPixmap(self.pixmap)

        self.close_btn = QtWidgets.QPushButton(self)
        self.close_btn.setFlat(True)
        self.close_btn.setMouseTracking(True)
        self.close_btn.setMinimumSize(QtCore.QSize(int(self.wh[0]/5), int(self.wh[0]/5)))
        self.close_btn.setMaximumSize(QtCore.QSize(int(self.wh[0]/5), int(self.wh[0]/5)))
        self.close_btn.setIcon(self.close_icon)
        self.close_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_btn.setGeometry(
            self.width()-self.close_btn.width(), 0, self.close_btn.width(), self.close_btn.height()
        )
        self.close_btn.hide()

    def mousePressEvent(self, event):
        event.accept()
        self.clicked.emit()

    def mouseMoveEvent(self, event):
        if (event.pos().y() <= int(self.width()/5)) and (event.pos().x() >= self.width()-self.close_btn.width()):
            self.close_btn.show()
        else:
            self.close_btn.hide()

    def leaveEvent(self, event):
        event.accept()
        self.closeButton.hide()


class CloseComboBoxLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None, wh=None, pixmap=None, close_icon=None, image_icon=None):
        super(CloseComboBoxLabel, self).__init__(parent)

        if wh is None:
            wh = (25, 25)
        self.wh = wh
        self.pixmap = pixmap
        self.close_icon = close_icon
        self.image_icon = image_icon
        self.__style()

    def __style(self):
        self.setMinimumSize(QtCore.QSize(self.wh[0], self.wh[1]))
        self.setMaximumSize(QtCore.QSize(self.wh[0], self.wh[1]))
        self.setMouseTracking(False)
        self.setScaledContents(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPixmap(self.pixmap)

        self.close_btn = QtWidgets.QPushButton(self)
        self.close_btn.setFlat(True)
        self.close_btn.setMouseTracking(False)
        self.close_btn.setMinimumSize(QtCore.QSize(int(self.wh[0] / 5), int(self.wh[0] / 5)))
        self.close_btn.setMaximumSize(QtCore.QSize(int(self.wh[0] / 5), int(self.wh[0] / 5)))
        self.close_btn.setIcon(self.close_icon)
        self.close_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.comb_box = QtWidgets.QComboBox(self)
        self.comb_box.setFocusPolicy(QtCore.Qt.TabFocus | QtCore.Qt.ClickFocus)
        self.comb_box.setFrame(False)
        self.comb_box.setIconSize(QtCore.QSize(16, 16))
        self.comb_box.addItem(self.image_icon, '')
        for c in string.hexdigits[0:10]:
            self.comb_box.addItem(self.image_icon, c)

    def resizeEvent(self, event):
        event.accept()
        self.close_btn.setGeometry(
            self.width()-self.close_btn.width(), 0, self.close_btn.width(), self.close_btn.height()
        )
        self.comb_box.setGeometry(0, self.height()*0.8, self.width(), self.height()/5)

    def mousePressEvent(self, event):
        event.accept()
        self.clicked.emit()


class ImageSequenceLabel(QtWidgets.QLabel):
    PERCENT_COLOR = QtGui.QColor(255, 255, 255, 100)
    PERCENT_HEIGHT = 2

    def __init__(self, parent=None, fps=24, timer=5, *args):
        QtWidgets.QLabel.__init__(self, parent, *args)

        self.__style()
        self._fps = fps
        self.timer = timer * 100

        self._filename = None
        self._image_sequence = ImageSequence(self._fps)
        self._image_sequence.frame_changed.connect(self._frame_changed)

        self.player_install = False
        self.player_install_timer = QtCore.QTimer(self.parent())
        self.player_install_timer.setSingleShot(False)
        self.player_install_timer.timeout.connect(self.__start)

    def __style(self):
        self.setMouseTracking(True)
        self.setScaledContents(True)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def is_control_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        return modifiers == QtCore.Qt.ControlModifier

    def current_pixmap(self):
        return QtGui.QPixmap(self._image_sequence.current_filename())

    def set_dir(self, dirname):
        if dirname is None:
            return
        self._image_sequence.set_dir(dirname)
        if self._image_sequence.frames():
            pixmap = self.current_pixmap()
            self.setPixmap(pixmap)

    def enterEvent(self, event):
        self.player_install_timer.start(self.timer)
        event.accept()

    def __start(self):
        self.player_install_timer.stop()
        self.player_install = True
        self._image_sequence.start()

    def leaveEvent(self, event):
        self.player_install_timer.stop()
        if self.player_install:
            self._image_sequence.pause()
        event.accept()

    def mouseMoveEvent(self, event):
        if self.is_control_modifier():
            percent = 1.0 - float(self.width() - event.pos().x()) / float(self.width())
            frame = int(self._image_sequence.duration() * percent)
            self._image_sequence.set_current_frame(frame)
            pixmap = self.current_pixmap()
            self.setPixmap(pixmap)
        else:
            event.ignore()

    def _reset(self):
        self._image_sequence.reset()

    def _stop(self):
        self._image_sequence.stop()

    def _frame_changed(self, filename=None):
        if not self.is_control_modifier():
            self._filename = filename
            pixmap = self.current_pixmap()
            self.setPixmap(pixmap)

    def set_current_frame(self, frame):
        self._image_sequence.set_current_frame(frame)

    def current_filename(self):
        return self._image_sequence.current_filename()

    def paintEvent(self, event):
        QtWidgets.QLabel.paintEvent(self, event)
        if len(self._image_sequence.frames()) <= 1:
            event.ignore()
            return
        painter = QtGui.QPainter()
        painter.begin(self)
        if self.current_filename():
            r = event.rect()
            playhead_position = self._image_sequence.percent() * r.width()
            x = r.x()
            y = self.height() - self.PERCENT_HEIGHT
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QBrush(self.PERCENT_COLOR))
            painter.drawRect(x, y, playhead_position, self.PERCENT_HEIGHT)
        painter.end()
        # return super(ImageSequenceWidget, self).paintEvent(event)


class ImageSequence(QtCore.QObject):
    IMAGE_TYPE = 'jpg'
    frame_changed = QtCore.pyqtSignal()

    def __init__(self, fps=24, *args):
        QtCore.QObject.__init__(self, *args)

        self._fps = fps
        self._timer = None
        self._frame = 0
        self._frames = []
        self._dirname = None
        self._paused = True

    def set_dir(self, dirname):
        def natural_sort_items(items):
            convert = lambda text: (int(text) if text.isdigit() else text)
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            items.sort(key=alphanum_key)

        self._dirname = dirname
        if os.path.isdir(dirname):
            self._frames = [os.path.join(dirname, filename) for filename in os.listdir(dirname) if
                            filename.endswith(self.IMAGE_TYPE)]
            natural_sort_items(self._frames)

    def dirname(self):
        return self._dirname

    def reset(self):
        if not self._timer:
            self._timer = QtCore.QTimer(self.parent())
            self._timer.setSingleShot(False)
            self._timer.timeout.connect(self._frame_changed)

        if not self._paused:
            self._frame = 0
        self._timer.stop()

    def pause(self):
        self._paused = True
        if self._timer:
            self._timer.stop()

    def resume(self):
        if self._paused:
            self._paused = False
            self._timer.start()

    def stop(self):
        self._frame = 0
        if self._timer:
            self._timer.stop()

    def start(self):
        self.reset()
        self._paused = False
        if self._timer:
            self._timer.start(1000.0 / self._fps)

    def switch(self):
        if self._paused:
            self.start()
        else:
            self.pause()

    def frames(self):
        return self._frames

    def _frame_changed(self):
        if not self._frames:
            return
        frame = self._frame
        frame += 1
        self.set_current_frame(frame)

    def percent(self):
        if len(self._frames) == self._frame + 1:
            _percent = 1
        else:
            _percent = float(len(self._frames) + self._frame - 1) / (len(self._frames) - 1) - 1
        return _percent

    def duration(self):
        return len(self._frames)

    def current_filename(self):
        try:
            return self._frames[self.current_frame()]
        except IndexError:
            pass

    def current_frame(self):
        return self._frame

    def set_current_frame(self, frame):
        if frame >= self.duration():
            frame = 0
        self._frame = frame
        self.frame_changed.emit()
