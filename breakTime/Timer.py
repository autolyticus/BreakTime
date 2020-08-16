import logging

from pprint import pformat

import pendulum

from statemachine import State, StateMachine

from .platforms.adapter import Adapter


class Timer(StateMachine):
    Init = State("Init", initial=True)
    PreWork = State("PreWork")
    Work = State("Work")
    PreBreak = State("PreBreak")
    Break = State("Break")

    waitForUserInput = Init.to(PreWork)
    startWork = PreWork.to(Work)
    notifyImminentBreak = Work.to(PreBreak)
    startBreak = PreBreak.to(Break)
    restart = Break.to(PreWork)

    def __init__(self, workMins, breakMins):
        super().__init__()
        self.workSeconds = workMins * 60
        self.breakSeconds = breakMins * 60
        self.history = []
        self.adapter = Adapter.get()

        self.waitForUserInput()

    def tick(self):
        if self.is_PreWork:
            # If there has been activity in the last 5 seconds, do nothing
            if pendulum.now() >= self.adapter.getLastUserActivityTime().add(seconds=5):
                print("Waiting for user activity...", end="\r")
                return
            # Otherwise time to start work
            self.startWork()
        elif self.is_Work:
            if e := self.getLastEvent("StateChange"):
                # If it has been enough time since work started
                if pendulum.now() >= e["ts"].add(seconds=self.breakSeconds - 15):
                    self.notifyImminentBreak()
                    return
            print(
                f'Work session ongoing at {pendulum.now().strftime("%H:%M:%S")}',
                end="\r",
            )
        elif self.is_PreBreak:
            if e := self.getLastEvent("StateChange"):
                # 15 seconds were left in current work session
                if pendulum.now() >= e["ts"].add(seconds=15):
                    self.startBreak()
                    return
            print(
                f'Work session ongoing at {pendulum.now().strftime("%H:%M:%S")}',
                end="\r",
            )
        elif self.is_Break:
            if e := self.getLastEvent("StateChange"):
                # 15 seconds were left in current work session
                if pendulum.now() >= e["ts"].add(seconds=self.breakSeconds):
                    self.restart()
                    return

    def on_startWork(self):
        print(f'Starting work session at {pendulum.now().strftime("%H:%M:%S")}')
        self.adapter.sendNotification(
            f"Work session - {self.workSeconds / 60} minutes left"
        )

    def on_notifyImminentBreak(self):
        self.adapter.sendNotification("Break in 15 seconds")

    def on_startBreak(self):
        until = pendulum.now().add(seconds=self.breakSeconds)
        print(f'Break until {until.strftime("%H:%M:%S")}')
        self.adapter.sendNotification(
            f'You are obliged to take a break. See you at {until.strftime("%H:%M:%S")}'
        )
        self.adapter.blockInput(self.breakSeconds)  # Does not block the thread
        self.adapter.blockScreen(self.breakSeconds)  # Does not block the thread

    def addToHistory(self, event):
        entry = {"ts": pendulum.now(), **event}
        logging.info(pformat(entry))
        self.history.append(entry)

    def stateChange(self, state):
        stateChangeEvent = {
            "name": "StateChange",
            "prevState": self.current_state,
            "state": state,
        }
        self.addToHistory(stateChangeEvent)
        self.state = state

    def getLastEvent(self, name):
        return list(filter(lambda e: e["name"] == name, self.history))[-1]

    def record(self):
        self.addToHistory({"name": "StateChange", "state": self.current_state_value})

    def on_enter_PreWork(self):
        self.record()

    def on_enter_Work(self):
        self.record()

    def on_enter_PreBreak(self):
        self.record()

    def on_enter_Break(self):
        self.record()
