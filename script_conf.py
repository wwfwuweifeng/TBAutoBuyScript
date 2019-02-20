import configparser
import datetime
class ScriptConf:
    __cf = configparser.ConfigParser()
    __cf.read("setting.conf",encoding="utf-8")
    __conf_dict={}

    @classmethod
    def get_time_interval(cls,key):
        if cls.__conf_dict.get(key) is None:
            value=cls.__cf.get("TIME_INTERVAL",key)
            value=value.strip().replace(" ","")
            value=value[:value.find("#")]
            cls.__conf_dict[key]=int(value)
        return cls.__conf_dict[key]

    @classmethod
    def get_retry_times(cls,key):
        if cls.__conf_dict.get(key) is None:
            value=cls.__cf.get("RETRY_TIMES",key)
            value=value.strip().replace(" ","")
            value=value[:value.find("#")]
            cls.__conf_dict[key]=int(value)
        return cls.__conf_dict[key]


