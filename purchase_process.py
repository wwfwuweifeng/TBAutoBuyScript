import time
from selenium import webdriver
from common_func import GetInterval,GetTimes
from one_user_tasks import OneUserTasks
import time
import datetime

class PurchaseProcess:
    # 让浏览器不要显示当前受自动化测试工具控制的提醒
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')

    def __init__(self,one_user_tasks):
        self.buy_tasks=one_user_tasks.get_user_tasks()
        self.user_name=one_user_tasks.get_user_name()
        self.one_users_tasks=one_user_tasks
        self.driver=None
        self.is_login=False
        self.now_task=None

    def open_chrome(self):
        print("chrome is openning ,please wait a moment")
        self.driver = webdriver.Chrome(chrome_options=self.option)
        self.driver.maximize_window()
        print("chrome is open")

    def login(self):
        for _ in range(GetTimes.get_login_retry_times()):
            self.driver.get("https://www.taobao.com")
            time.sleep(GetInterval.get_wait_next_action_interval())
            try:
                if self.driver.find_element_by_link_text("亲，请登录"):
                    self.driver.find_element_by_link_text("亲，请登录").click()
                    print("请扫描二维码进行登陆,当前需登陆的用户为："+self.user_name)
                    time.sleep(GetInterval.get_wait_login_interval())
            except Exception as e:
                self.is_login = True
                print("已登录，即将进行页面跳转")
                break

        if not self.is_login:
            print("登陆失败，程序停止执行")
            exit(-1)
        else:
            time.sleep(GetInterval.get_wait_next_action_interval())
            print("打开购物车")
            self.driver.get("https://cart.taobao.com/cart.htm")
            time.sleep(GetInterval.get_wait_next_action_interval())

    def wait_rush_to_buy(self):     #等待进入抢购
        for one_task in self.buy_tasks:
            self.now_task = one_task
            time.sleep(GetInterval.get_wait_next_action_interval())
            # self.driver.get(self.now_task["business_url"])
            while True:
                current_time = datetime.datetime.now()
                if one_task["start_time"] < current_time:
                    print("该任务已过抢购时间，跳过此任务")
                    self.one_users_tasks.change_task_state(self.now_task["task_id"], OneUserTasks.FAIL)
                    break

                if (one_task["start_time"] - current_time).seconds > GetInterval.get_wait_entry_ready_rush_to_buy():
                    # self.driver.get(self.now_task["business_url"])
                    self.driver.get("https://cart.taobao.com/cart.htm")
                    print("刷新商品页面")
                    time.sleep(GetInterval.get_wait_refresh_interval())
                else:
                    print("进入准备抢购阶段...")
                    self.ready_rush_to_buy(one_task)
                    break

            print("\n---------------------------开始一个新的任务--------------------------------------\n")
        else:
            print("用户："+self.user_name+" 已经没有抢购任务了，程序退出")


    def select_cart(self,one_task):
        if one_task["business_name"]=="all":
            if self.driver.find_element_by_id("J_SelectAll1"):
                self.driver.find_element_by_id("J_SelectAll1").click()
                print("已全选购物车中的物品")
                time.sleep(GetInterval.get_wait_next_action_interval())
                return True
        else:
            items = self.driver.find_elements_by_class_name("item-content")
            for one_goods in one_task["business_name"].split(","):
                for one_item in items:
                    try:
                        if one_item.find_element_by_link_text(one_goods):
                            one_item.find_element_by_class_name("cart-checkbox").click()
                            print("已选中商品："+one_goods)
                            break
                    except:
                        pass
                else:
                    print("没有找到与商品："+one_goods+" 相匹配的商品")
                    self.one_users_tasks.change_task_state(self.now_task["task_id"], OneUserTasks.FAIL)
                    return False
                time.sleep(GetInterval.get_wait_next_action_interval())
                return True


    def ready_rush_to_buy(self,one_task):
        if not self.select_cart(one_task):
            return
        interval=(one_task["start_time"]-datetime.datetime.now()).seconds
        time.sleep(interval-4)  #休息至抢购开始前的4秒

        while (one_task["start_time"]-datetime.datetime.now()).seconds > GetInterval.get_advance_in_rush_to_buy(): #提前一秒进入抢购状态
            time.sleep(GetInterval.get_wait_check_status_is_ok())

        while one_task["start_time"] > datetime.datetime.now():
            time.sleep(GetInterval.get_wait_check_status_is_ok())

        print("开始进行抢购")
        # self.rush_to_buy()

    def rush_to_buy(self):
        click_settlement_num=0
        step_one_start_time=datetime.datetime.now()
        print("当前时间为：",step_one_start_time)
        # self.driver.get(self.now_task["business_url"])
        self.one_users_tasks.change_task_state(self.now_task["task_id"],OneUserTasks.RUN)

        #点击购买按钮
        while True:
            try:
                click_settlement_num += 1
                # self.driver.find_element_by_link_text("结算").click()

                self.driver.find_element_by_id("J_Go").click()
                print("已经点击结算，进入提交订单页面")
                step_tow_start_time=datetime.datetime.now()
                print("已经点击结算按钮，当前时间为：",step_tow_start_time)
                break
            except:
                if click_settlement_num % 10 == 0:
                    print("已尝试点击结算按钮第", click_settlement_num, "次")
                if (datetime.datetime.now() - step_one_start_time).seconds >= 10:  #默认10秒还未进入结算页面，则默认抢购失败
                    print("该抢购任务抢购失败，失败阶段为结算阶段,当前时间点为：",datetime.datetime.now())
                    self.one_users_tasks.change_task_state(self.now_task["task_id"],OneUserTasks.FAIL)
                    return

        submit_order_num=0
        #点击提交订单
        while True:
            try:
                submit_order_num+=1
                self.driver.find_element_by_link_text('提交订单').click()
                print("已经点击提交订单按钮，总共耗时：",datetime.datetime.now()-step_tow_start_time)
                print("等待90秒，让页面跳转至付款页面")
                time.sleep(90)
                self.one_users_tasks.change_task_state(self.now_task["task_id"], OneUserTasks.SUCCESS)
                break
            except:
                if submit_order_num % 10 == 0:
                    print("已尝试点击提交按钮第", click_settlement_num, "次")
                if (datetime.datetime.now() - step_tow_start_time).seconds >= 10:   #默认10秒还未提交成功订单，则默认抢购失败
                    print("该抢购任务抢购失败，失败阶段为提交订单阶段，当前时间点为：",datetime.datetime.now())
                    self.one_users_tasks.change_task_state(self.now_task["task_id"],OneUserTasks.FAIL)
                    return

        print("抢购成功，总耗时：",datetime.datetime.now()-step_one_start_time)


    def start(self):
        self.open_chrome()
        self.login()
        self.wait_rush_to_buy()


    def __del__(self):
        self.driver.close()