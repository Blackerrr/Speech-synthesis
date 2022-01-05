from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from aip import AipSpeech
from pydub import AudioSegment
from pydub.playback import play
import sys, threading, helloworld


class ExampleApp(QtWidgets.QWidget, helloworld.Ui_Form):
    def __init__(self, filename, client, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.filename = filename
        self.client = client
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_clicked)
        self.Index = [5003, 5118, 106, 110, 111, 103, 5]
        self.textEdit.setText("我叫李明，来自重庆交通大学，学号是6 3 1 8 0 7 0 3 0 1 2 1。")

    def play_music(self):
        song = AudioSegment.from_mp3(self.filename)
        play(song)

    def button_clicked(self):
        print("当前发音人：", self.comboBox.currentText())
        print("当前发音人序号：", self.comboBox.currentIndex())

        print(self.textEdit.toPlainText())
        result = self.client.synthesis(self.textEdit.toPlainText(), 'zh', '1',
                                       {"vol": 9,  # 音量 0-16  默认 5
                                        "spd": 4,  # 语速 0-9   默认 5
                                        "pit": 5,  # 音调 0-9   默认 5
                                        "per": self.Index[self.comboBox.currentIndex()],
                                        # 普通发音人选择 度小美=0(默认)，度小宇=1，，度逍遥（基础）=3，度丫丫=4
                                        # 精品发音人选择：度逍遥（精品）=5003，度小鹿 = 5118，度博文 = 106，
                                        # 度小童 = 110，度小萌 = 111，度米朵 = 103，度小娇 = 5
                                        })

        with open(self.filename, "wb") as f:
            f.write(result)
        t = threading.Thread(target=self.play_music, )
        t.start()


def main():
    APP_ID = '25426975'
    API_KEY = 'besIFO02GHosUHIUdeeYAOLL'
    SECRET_KEY = '4WL6EbLp821uC1oUNKQZLKWWOMot2zGt '

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    outfile = "./audio/speak.mp3"
    app = QApplication(sys.argv)
    form = ExampleApp(outfile, client)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
