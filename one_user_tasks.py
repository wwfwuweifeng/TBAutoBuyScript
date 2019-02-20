import configparser
import datetime


class OneUserTasks:
    SUCCESS="success"
    FAIL="fail"
    RUN="running"
    WAIT="waitting"
    # tasks_url = {
    #     "TASK-2": "https://detail.tmall.com/item.htm?spm=a1z0d.6639537.1997196601.4.209e7484NMeXUt&id=526177665200",
    #     "TASK-1":"https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w5003-15656860923.3.3a834822qUj2Zb&id=581082533591&scene=taobao_shop"
    # }
    def __init__(self,user_name,user_conf_file_name):
        self.__user_name=user_name
        self.__task_cf = configparser.ConfigParser()
        self.__task_cf.read("buy_tasks/" + user_conf_file_name, encoding="utf-8")
        self.__tasks_list = []
        self.__user_conf_file_name = user_conf_file_name
        self.__init_tasks_list()

    def __init_tasks_list(self):
        for oneNode in self.__task_cf.sections():
            if oneNode.startswith("TASK") and oneNode.endswith("num"):
                pass
            else:
                one_task=dict(self.__task_cf[oneNode])
                one_task["task_id"] = oneNode
                one_task["start_time"]=datetime.datetime.strptime(one_task["start_time"], '%Y-%m-%d %H:%M:%S')
                # one_task["business_url"]=self.tasks_url[oneNode]
                self.__tasks_list.append(one_task)


    def change_task_state(self, task_id, value):
        self.__task_cf.set(task_id, "state", value)
        self.__task_cf.write(open("buy_tasks/" + self.__user_conf_file_name, "w", encoding="utf-8"))


    def get_user_tasks(self):
        return self.__tasks_list

    def get_user_name(self):
        return self.__user_name