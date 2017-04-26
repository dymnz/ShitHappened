import time
import sched
from shit_happened import Shit_Happened


# https://stackoverflow.com/questions/2398661/schedule-a-repeating-event-in-python-3
def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)

def procedure():
	sh.check_site()
	sh.notify_recipients()

scheduler = sched.scheduler(time.time, time.sleep)
setting_name = 'setting.json'
sh = Shit_Happened(setting_name)

periodic(scheduler, 10, procedure)
scheduler.run()
