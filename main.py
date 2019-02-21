from auto_buy_script.one_user_tasks import OneUserTasks
from auto_buy_script.purchase_process import PurchaseProcess

if __name__=="__main__":
    one_user_tasks=OneUserTasks("username","myself2.conf")
    one_process=PurchaseProcess(one_user_tasks)
    # one_user_tasks2=OneUserTasks("wzs","myself2.conf")    #可以同时运行多个抢购任务
    # one_process2=PurchaseProcess(one_user_tasks2)
    # p = Pool(2)
    # p.apply_async(one_process.start)
    # p.apply_async(one_process2.start)
    # p.close()
    # p.join()
    one_process.start()

