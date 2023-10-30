import math
import random
import sys
import time
from threading import Lock, Thread

from gepetto.corbaserver import Client as ViewerClient
from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory
from PythonQt import QtCore
from PythonQt.QtGui import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    mainWindow,
)

from hpp.environments import Buggy

lockDisplay = Lock()
lockProblem = Lock()
displayed = True
runTime = 180000
fps = 24


class IAThread(Thread):
    ir_ = None
    initConfig_ = None

    def __init__(self, iaRobot):
        Thread.__init__(self)
        self.ir_ = iaRobot
        with lockProblem:
            iaRobot.client.problem.selectProblem("default")
            iaRobot.client.problem.selectSteeringMethod("ReedsShepp")
            self.initConfig_ = iaRobot.client.robot.getCurrentConfig()
            iaRobot.client.robot.setJointBounds("base_joint_xy", [0, 16, -4, 4])
            iaRobot.client.problem.setInitialConfig(self.initConfig_)
            iaRobot.client.problem.addGoalConfig([10.0, 0.0, 1.0, 0.0, 0.0, 0.0])

    def run(self):
        global displayed
        while (
            gameWidget.remainTime.minute() != 0 or gameWidget.remainTime.second() != 0
        ):
            with lockDisplay, lockProblem:
                iaRobot.client.problem.selectProblem("default")
                value = random.randint(0, 1)
                if value == 0 or gameWidget.lastPath_ == -1:
                    self.ir_.client.problem.clearPathOptimizers()
                    self.ir_.client.problem.resetRoadmap()
                    self.ir_.client.problem.solve()
                elif value == 1:
                    if gameWidget.lastPath_ == 0:
                        optimize = 0
                    else:
                        optimize = random.randint(0, gameWidget.lastPath_)
                    self.ir_.client.problem.addPathOptimizer("RandomShortcut")
                    self.ir_.client.problem.optimizePath(optimize)
                displayed = False
            time.sleep(2)


class Car:
    def setMove(self, direction):
        pass

    def turn(self, angle):
        pass

    def update(self, direction):
        pass

    def reset(self):
        pass

    def check(self, xPosition, yPosition):
        pass


class PlayerCar(Car):
    def __init__(self, playerRobot):
        self.speed = 1.25
        self.angleWheel = 0.0
        self.angleCar = 0.0
        self.angleCarSave = 0.0
        self.rightIndex = playerRobot.rankInConfiguration["wheel_frontright_joint"]
        self.leftIndex = playerRobot.rankInConfiguration["wheel_frontleft_joint"]
        self.limit = playerRobot.client.robot.getJointBounds("wheel_frontleft_joint")
        self.pr = playerRobot
        self.position = playerRobot.client.robot.getCurrentConfig()
        self.pr.client.problem.selectProblem("player")
        self.pr.client.problem.setInitialConfig(self.position)

    def move(self, direction):
        newP = self.position[::]
        speed = self.speed / fps * direction
        self.angleCarSave = self.angleCar
        self.angleCar += self.angleWheel * speed
        newP[2] = math.cos(self.angleCar)
        newP[3] = math.sin(self.angleCar)
        newP[0] = newP[0] + newP[2] * speed
        newP[1] = newP[1] + newP[3] * speed
        return newP

    def turn(self, angle):
        with lockProblem:
            self.pr.client.problem.selectProblem("player")
            pos = self.position
            if angle < 2:
                pos[self.rightIndex] = self.limit[angle]
                pos[self.leftIndex] = self.limit[angle]
            else:
                pos[self.rightIndex] = 0
                pos[self.leftIndex] = 0
            if self.pr.client.robot.isConfigValid(pos)[0]:
                self.position = pos[::]
                pv(self.position)
                self.angleWheel = self.limit[angle] if (angle < 2) else 0

    def update(self, direction):
        with lockProblem:
            self.pr.client.problem.selectProblem("player")
            newP = self.position[::]
            if direction != 0:
                newP = self.move(direction)
            if self.pr.client.robot.isConfigValid(newP)[0]:
                self.position = newP[::]
                pv(self.position)
            else:
                self.angleCar = self.angleCarSave

    def reset(self):
        with lockProblem:
            self.angleWheel = 0
            self.angleCar = 0
            self.pr.client.problem.selectProblem("player")
            self.position = self.pr.client.problem.getInitialConfig()
            pv(self.position)

    def check(self, xLimit, yLimit):
        return (
            True
            if (
                xLimit[0] <= self.position[0]
                and yLimit[0] <= self.position[1] <= yLimit[1]
            )
            else False
        )


class IACar(Car):
    def __init__(self, iaRobot):
        self.maxLength = -1.0
        self.currentLength = 0.0
        self.speed = 1.25
        self.ir = iaRobot
        self.hasLock = False

    def move(self, direction):
        return

    def turn(self, angle):
        return

    def update(self, direction):
        global displayed
        if not displayed:
            if not self.hasLock:
                if not lockDisplay.acquire(False):
                    return
                self.hasLock = True
            with lockProblem:
                self.ir.client.problem.selectProblem("default")
                length = 0
                if self.maxLength == -1.0:
                    gameWidget.lastPath_ += 1
                    self.maxLength = self.ir.client.problem.pathLength(
                        gameWidget.lastPath_
                    )
                if self.currentLength + self.speed > self.maxLength:
                    self.currentLength = 0
                    self.maxLength = -1.0
                    length = self.maxLength
                    lockDisplay.release()
                    displayed = True
                    print("AAAAAAAAA")
                else:
                    self.currentLength += self.speed / fps
                    length = self.currentLength
                gameWidget.iaCurrentTime = gameWidget.iaCurrentTime.addMSecs(
                    1.0 / fps * 1000
                )
                config = self.ir.client.problem.configAtParam(
                    gameWidget.lastPath_, length
                )
                self.position = config[::]
                iv(config)

    def check(self, xLimit, yLimit):
        return (
            True
            if (
                xLimit[0] <= self.position[0]
                and yLimit[0] <= self.position[1] <= yLimit[1]
            )
            else False
        )

    def reset(self):
        global displayed
        with lockProblem:
            self.maxLength = -1.0
            self.currentLength = 0
            self.ir.client.problem.selectProblem("default")
            self.position = self.ir.client.problem.getInitialConfig()
            self.hasLock = False
            iv(self.position)
            lockDisplay.release()
            displayed = True


class GameWidget(QDockWidget):
    player = None
    ia = None
    moveDirection_ = 0

    labelOG = None
    igWidget = None
    ogWidget = None
    labelRemain = None
    labelIA = None
    labelBest = None
    labelCurrent = None

    iaTime = None
    iaCurrentTime = None
    remainTime = None
    currentTime = None
    bestTime = None

    runLaunched = False
    currentLength_ = 0.0
    maxLength_ = -1.0
    lastPath_ = -1

    def __init__(self, mainWindow, iaRobot, playerRobot):
        super(GameWidget, self).__init__("Buggy game", mainWindow)
        self.player = PlayerCar(playerRobot)
        self.ia = IACar(iaRobot)
        self.createOGWidget()
        self.createIGWidget()
        self.createWidget()

    def createOGWidget(self):
        self.ogWidget = QWidget()
        ogLayout = QHBoxLayout()
        self.labelOG_ = QLabel(
            "Press start button to launch the game. (You play on the right side)"
        )
        ogLayout.addWidget(self.labelOG_)
        self.ogWidget.setLayout(ogLayout)

    def createIGWidget(self):
        self.igWidget = QWidget()
        igLayout = QHBoxLayout()
        self.labelRemain = QLabel("", self.igWidget)
        self.labelIA = QLabel("", self.igWidget)
        self.labelBest = QLabel("", self.igWidget)
        self.labelCurrent = QLabel("", self.igWidget)
        igLayout.addWidget(self.labelRemain)
        igLayout.addWidget(self.labelIA)
        igLayout.addWidget(self.labelBest)
        igLayout.addWidget(self.labelCurrent)
        self.igWidget.setLayout(igLayout)
        self.igWidget.setVisible(False)

    def createWidget(self):
        widget = QWidget()
        layout = QHBoxLayout()
        self.button = QPushButton(widget)
        self.button.setText("Start !")
        self.button.setMaximumWidth(150)
        self.button.connect("clicked()", launch)
        layout.addWidget(self.button)
        widget.setLayout(layout)
        layout.addWidget(self.ogWidget)
        layout.addWidget(self.igWidget)
        self.setWidget(widget)
        self.setFocusPolicy(2)

    def keyPressEvent(self, event):
        if event.key() == 0x01000012:
            self.runLaunched = True
            self.player.turn(1)
        elif event.key() == 0x01000014:
            self.runLaunched = True
            self.player.turn(0)
        elif event.key() == 0x01000013:
            self.runLaunched = True
            self.moveDirection_ = 1
        elif event.key() == 0x01000015:
            self.runLaunched = True
            self.moveDirection_ = -1
        elif event.key() == 0x20:
            self.runLaunched = False
            self.player.reset()
            self.currentTime = QtCore.QTimer(0, 0)

    def keyReleaseEvent(self, event):
        if event.key() == 0x01000012 or event.key() == 0x01000014:
            self.player.turn(2)
        if event.key() == 0x01000013 or event.key() == 0x01000015:
            self.moveDirection_ = 0

    def update(self):
        self.player.update(self.moveDirection_)
        self.ia.update(0)
        self.remainTime = self.remainTime.addMSecs(-1.0 / fps * 1000)
        self.labelRemain.setText("Time remain : " + self.remainTime.toString("mm:ss"))
        if self.player.check([9.0, 9.0], [-4, 4]):
            self.runLaunched = False
            if self.currentTime < self.bestTime:
                self.bestTime = self.currentTime.addMSecs(0)
                self.labelBest.setText(
                    "Your best : " + self.bestTime.toString("mm:ss:zz")
                )
            self.currentTime = QtCore.QTime(0, 0)
            self.player.reset()
        if not displayed and self.ia.check([9.0, 9.0], [-4, 4]):
            print(self.iaCurrentTime)
            print(self.iaTime)
            print(self.iaCurrentTime < self.iaTime)
            print()
            if self.iaCurrentTime < self.iaTime:
                self.iaTime = self.iaCurrentTime.addMSecs(0)
                self.labelIA.setText("IA's time : " + self.iaTime.toString("mm:ss:zz"))
            self.iaCurrentTime = QtCore.QTime(0, 0)
            self.ia.reset()
        if self.runLaunched:
            self.currentTime = self.currentTime.addMSecs(1.0 / fps * 1000)
            self.labelCurrent.setText(
                "Current run : " + self.currentTime.toString("mm:ss:zz")
            )

    def start(self):
        self.iaTime = QtCore.QTime(0, (runTime / 1000) / 60)
        self.iaCurrentTime = QtCore.QTime(0, 0)
        self.remainTime = QtCore.QTime(0, (runTime / 1000) / 60)
        self.currentTime = QtCore.QTime(0, 0)
        self.bestTime = QtCore.QTime(0, (runTime / 1000) / 60)
        self.labelRemain.setText("Time remain : " + self.remainTime.toString("mm:ss"))
        self.labelIA.setText("IA's time : --:--:--")
        self.labelBest.setText("Your best : --:--:--")
        self.labelCurrent.setText(
            "Current run : " + self.currentTime.toString("mm:ss:zz")
        )
        self.button.disconnect("clicked()", launch)
        self.button.setText("Stop !")
        self.button.connect("clicked()", end)

    def end(self):
        if self.iaTime > self.bestTime:
            self.labelOG_.setText(
                "Congratulations, you won with a "
                + self.bestTime.toString("mm:ss:zz")
                + " seconds time !"
            )
        elif self.iaTime < self.bestTime:
            self.labelOG_.setText(
                "Maybe next time, IA won with a "
                + self.iaTime.toString("mm:ss:zz")
                + " seconds time !"
            )
        else:
            self.labelOG_.setText("It's a tie !")
        updateTimer.stop()
        self.igWidget.setVisible(False)
        self.ogWidget.setVisible(True)
        self.button.disconnect("clicked()", end)
        self.button.setText("Start !")
        self.button.connect("clicked()", launch)


def play():
    gameWidget.update()


def end():
    gameWidget.end()


sys.argv = []
gui = ViewerClient()

gui.gui.createWindow("ia")
gui.gui.createWindow("player")
iaRobot = Buggy("buggy_ia")
ips = ProblemSolver(iaRobot)
ivf = ViewerFactory(ips)
ivf.loadObstacleModel("hpp_environments", "scene", "scene_ia")
iv = ivf.createViewer(viewerClient=gui)

iaRobot.client.problem.selectProblem("player")
playerRobot = Buggy("buggy_player")
pps = ProblemSolver(playerRobot)
pvf = ViewerFactory(pps)
pvf.loadObstacleModel("hpp_environments", "scene", "scene_player")
pvf(playerRobot.client.robot.getCurrentConfig())
pv = pvf.createViewer(viewerClient=gui)
gui.gui.addSceneToWindow("buggy_player", 1)
gui.gui.addSceneToWindow("scene_player", 1)
gui.gui.addSceneToWindow("buggy_ia", 0)
gui.gui.addSceneToWindow("scene_ia", 0)

# To launch the game
gameTimer = QtCore.QTimer()
gameTimer.setInterval(runTime)
gameTimer.connect("timeout()", end)
updateTimer = QtCore.QTimer()
updateTimer.setInterval(1.0 / fps * 1000)
updateTimer.connect("timeout()", play)


def launch():
    print("launched")
    t = IAThread(iaRobot)
    updateTimer.setParent(gameWidget)
    updateTimer.start()
    gameTimer.start()
    gui.gui.attachCameraToNode("buggy_player", 1)
    gameWidget.setFocus(True)
    gameWidget.start()
    t.start()
    gameWidget.ogWidget.setVisible(False)
    gameWidget.igWidget.setVisible(True)


# Create widget for the game
gameWidget = GameWidget(mainWindow, iaRobot, playerRobot)
mainWindow.addDockWidget(4, gameWidget)

mainWindow.refresh()
mainWindow.requestApplyCurrentConfiguration()
iaRobot.client.problem.selectProblem("default")
mainWindow.refresh()
mainWindow.requestApplyCurrentConfiguration()
