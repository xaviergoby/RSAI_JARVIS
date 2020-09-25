import time
import datetime
import numpy as np

def delay_timer(delay, display_info=True):
    """
    :param delay: int or float of seconds to delay for.
    Guaranteed to work for delay of:
    0.1 <= delay < 1.0
    or
    1 <= delay
    :param display_info: Whether to print information regarding the status of the
    delay timer. Is True by def. If False then nothing is printed!
    :return: NoneType after delay # of seconds. Simply returns control after delay amount of seconds!
    """
    if display_info is True:
        print(f"Time of start: {time.time()%60} seconds")
        print("Delay of ...")
    if 0.1 <= delay < 1.0:
        count_down_timer_array = np.round(np.arange(delay, 0, -0.1), 2)
        for delay_sec in list(count_down_timer_array):
            if display_info is True:
                print("{0} seconds left...".format(delay_sec))
            sleep_duration = np.round(np.absolute(np.diff(count_down_timer_array)), 1)[0]
            time.sleep(sleep_duration)
    elif 1.0 <= delay:
        for delay_sec in range(delay, 0, -1):
            if display_info is True:
                print("{0} seconds left...".format(delay_sec))
            time.sleep(1)
    if display_info is True:
        print(f"Delay time of {delay} seconds complete!\n")
        print(f"Time of completion: {time.time()%60} seconds")


class StopWatchTimer:
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.stopped = False
        self.timer_start = None
    
    def reset(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = datetime.datetime.now()
        self.stopped = False
    
    def end(self):
        self.end_time = datetime.datetime.now()
    
    def get_elapsed_time(self):
        current_time = datetime.datetime.now()
        current_dt = current_time - self.start_time
        current_tot_dts = current_dt.total_seconds()
        return current_tot_dts
    
    def get_current_time_seconds_diff(self):
        current_time = datetime.datetime.now()
        current_dt = current_time - self.start_time
        current_tot_dts = current_dt.total_seconds()
        return current_tot_dts
    
    def set_timer(self, time_duration_seconds):
        self.timer_start = datetime.datetime.now()
    
    def timed_duration(self, reset_stop_watch=True):
        if self.end_time is None:
            self.end()
        else:
            pass
        dt = self.end_time - self.start_time
        tot_dts = dt.total_seconds()
        if reset_stop_watch is True:
            self.reset()
        else:
            pass
        return tot_dts



# def time_seconds_diff()

if __name__ == "__main__":
    # delay = 5
    # delay_timer(delay)
    delay = 5
    delay_timer(delay, display_info=False)
    # import time
    # stop_watch = StopWatchTimer()
    # stop_watch.start()
    # time.sleep(2.3)
    # stop_watch.end()
    # print(stop_watch.timed_duration())