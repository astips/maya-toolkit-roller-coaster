# -*- coding: utf-8 -*-

from QtSide import QtWidgets
from ..packages.widgets.labels import ColorfulBGLabel


class OptionWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OptionWidget, self).__init__(parent)
        # self.mode = 'BLEND'  # BLEND / MULTIPLIER
        # self.modify = 'NORMAL'  # NORMAL / L / R / ML / MR / FLIP
        self.option = ['BLEND', 'NORMAL']
        self.setup_ui()
        self.__connect()
        self.label_blend.on()

    def setup_ui(self):
        self.horizontal_layout_main = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout_main.setSpacing(6)
        self.horizontal_layout_main.setContentsMargins(0, 0, 0, 0)

        self.horizontal_layout_mode = QtWidgets.QVBoxLayout()
        self.horizontal_layout_mode.setSpacing(2)
        self.label_blend = ColorfulBGLabel(
            self, wh=(30, 14), text='B', basic=(77, 77, 77, 255), color=(255, 100, 20, 150)
        )
        self.label_blend.setToolTip('Blend Mode')
        self.label_multi = ColorfulBGLabel(
            self, wh=(30, 14), text='+/-', basic=(77, 77, 77, 255), color=(255, 100, 20, 150)
        )
        self.label_multi.setToolTip('Additive Mode')
        self.horizontal_layout_mode.addWidget(self.label_blend)
        self.horizontal_layout_mode.addWidget(self.label_multi)

        self.horizontal_layout_filter = QtWidgets.QHBoxLayout()
        self.horizontal_layout_filter.setSpacing(2)
        self.label_filter_left = ColorfulBGLabel(
            self, wh=(30, 14), text='L', basic=(77, 77, 77, 255), color=(120, 175, 255, 100)
        )
        self.label_filter_left.setToolTip('Filter L : Only apply to L controls')
        self.label_filter_right = ColorfulBGLabel(
            self, wh=(30, 14), text='R', basic=(77, 77, 77, 255), color=(120, 175, 255, 100)
        )
        self.label_filter_right.setToolTip('Filter R : Only apply to R controls')
        self.horizontal_layout_filter.addWidget(self.label_filter_left)
        self.horizontal_layout_filter.addWidget(self.label_filter_right)

        self.horizontal_layout_mirror = QtWidgets.QHBoxLayout()
        self.horizontal_layout_mirror.setSpacing(2)
        self.label_mirror_left = ColorfulBGLabel(
            self, wh=(30, 14), text='ML', basic=(77, 77, 77, 255), color=(120, 175, 255, 100)
        )
        self.label_mirror_left.setToolTip("Mirror From L : Use data's L controls force apply to R controls")
        self.label_mirror_right = ColorfulBGLabel(
            self, wh=(30, 14), text='MR', basic=(77, 77, 77, 255), color=(120, 175, 255, 100)
        )
        self.label_mirror_right.setToolTip("Mirror From R : Use data's R controls force apply to L controls")
        self.horizontal_layout_mirror.addWidget(self.label_mirror_left)
        self.horizontal_layout_mirror.addWidget(self.label_mirror_right)

        self.label_flip = ColorfulBGLabel(
            self, wh=(32, 14), text='FLIP', basic=(77, 77, 77, 255), color=(120, 175, 255, 100)
        )
        self.label_flip.setToolTip('Flip L & R')

        self.horizontal_layout_options = QtWidgets.QHBoxLayout()
        self.horizontal_layout_options.setSpacing(2)
        self.horizontal_layout_options.addLayout(self.horizontal_layout_filter)
        self.horizontal_layout_options.addLayout(self.horizontal_layout_mirror)
        self.horizontal_layout_options.addWidget(self.label_flip)

        self.horizontal_layout_main.addLayout(self.horizontal_layout_mode)
        self.horizontal_layout_main.addLayout(self.horizontal_layout_options)
        self.horizontal_layout_main.setStretch(0, 1)
        self.horizontal_layout_main.setStretch(1, 3)
        self.setLayout(self.horizontal_layout_main)

    def __connect(self):
        self.label_blend.toggled.connect(self.blend)
        self.label_multi.toggled.connect(self.multi)
        self.label_filter_left.toggled.connect(self.left)
        self.label_filter_right.toggled.connect(self.right)
        self.label_mirror_left.toggled.connect(self.mirror_left)
        self.label_mirror_right.toggled.connect(self.mirror_right)
        self.label_flip.toggled.connect(self.flip)

    def blend(self):
        self.label_multi.toggle()
        self.option[0] = 'BLEND' if self.label_blend.state else 'MULTIPLIER'

    def multi(self):
        self.label_blend.toggle()
        self.option[0] = 'BLEND' if self.label_blend.state else 'MULTIPLIER'

    def left(self):
        if self.label_filter_left.state:
            self.label_filter_right.off()
            self.label_mirror_left.off()
            self.label_mirror_right.off()
            self.label_flip.off()
            self.option[1] = 'L'
        else:
            self.option[1] = 'NORMAL'

    def right(self):
        if self.label_filter_right.state:
            self.label_filter_left.off()
            self.label_mirror_left.off()
            self.label_mirror_right.off()
            self.label_flip.off()
            self.option[1] = 'R'
        else:
            self.option[1] = 'NORMAL'

    def mirror_left(self):
        if self.label_mirror_left.state:
            self.label_filter_left.off()
            self.label_filter_right.off()
            self.label_mirror_right.off()
            self.label_flip.off()
            self.option[1] = 'ML'
        else:
            self.option[1] = 'NORMAL'

    def mirror_right(self):
        if self.label_mirror_right.state:
            self.label_filter_left.off()
            self.label_filter_right.off()
            self.label_mirror_left.off()
            self.label_flip.off()
            self.option[1] = 'MR'
        else:
            self.option[1] = 'NORMAL'

    def flip(self):
        if self.label_flip.state:
            self.label_filter_left.off()
            self.label_mirror_left.off()
            self.label_filter_right.off()
            self.label_mirror_right.off()
            self.option[1] = 'FLIP'
        else:
            self.option[1] = 'NORMAL'

    def resizeEvent(self, event):
        event.accept()
        if self.width() >= 310:
            self.horizontal_layout_mode.setDirection(QtWidgets.QBoxLayout.LeftToRight)
            self.horizontal_layout_filter.setDirection(QtWidgets.QBoxLayout.LeftToRight)
            self.horizontal_layout_mirror.setDirection(QtWidgets.QBoxLayout.LeftToRight)

            self.horizontal_layout_options.setStretch(0, 2)
            self.horizontal_layout_options.setStretch(1, 2)
            self.horizontal_layout_options.setStretch(2, 1)
        else:
            self.horizontal_layout_mode.setDirection(QtWidgets.QBoxLayout.TopToBottom)
            self.horizontal_layout_filter.setDirection(QtWidgets.QBoxLayout.TopToBottom)
            self.horizontal_layout_mirror.setDirection(QtWidgets.QBoxLayout.TopToBottom)

            self.horizontal_layout_options.setStretch(0, 1)
            self.horizontal_layout_options.setStretch(1, 1)
            self.horizontal_layout_options.setStretch(2, 1)
