
from auto_buy_script.script_conf import ScriptConf
import random

class GetInterval:
    # 等待用户登陆的时间间隔
    @classmethod
    def get_wait_login_interval(cls):
        return ScriptConf.get_time_interval("wait_login")

    # 等待刷新的时间间隔，防止长时间不操作，退出登陆
    @classmethod
    def get_wait_refresh_interval(cls):
        return cls.__get_interval("wait_refresh")

    @classmethod
    def get_wait_next_action_interval(cls):
        return cls.__get_interval("wait_next_action")

    @classmethod
    def get_wait_retry_click_settlement_interval(cls):
        return cls.__get_interval("wait_retry_click_settlement") / 1000

    @classmethod
    def get_wait_retry_submit_order_interval(cls):
        return cls.__get_interval("wait_retry_submit_order") / 1000

    @classmethod
    def get_wait_entry_ready_rush_to_buy(cls):
        return ScriptConf.get_time_interval("wait_entry_ready_rush_to_buy")

    @classmethod
    def get_wait_check_status_is_ok(cls):
        return ScriptConf.get_time_interval("wait_check_status_is_ok")/1000

    @classmethod
    def get_advance_in_rush_to_buy(cls):
        return ScriptConf.get_time_interval("advance_in_rush_to_buy")

    # 仅作为该模块内部使用的函数
    @classmethod
    def __get_interval(cls,key):
        low = ScriptConf.get_time_interval(key + "_low")
        high = ScriptConf.get_time_interval(key + "_high")
        return random.randint(low, high)

class GetTimes:
    @classmethod
    def get_login_retry_times(cls):
        return ScriptConf.get_retry_times("login_retry_times")

    @classmethod
    def get_submit_order_retry_times(cls):
        return ScriptConf.get_retry_times("submit_order_retry_times")

    @classmethod
    def get_click_settlement_order_retry_times(cls):
        return ScriptConf.get_retry_times("click_settlement_order_retry_times")
