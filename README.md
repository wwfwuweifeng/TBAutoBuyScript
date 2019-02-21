# TBAutoBuyScript
>一个简易的淘宝自动抢购脚本。  

PS：别指望它能抢得过黄牛，亲测，次次惨败；若淘宝前端代码进行了修改，也可能导致脚本失效。

# How to use
### 1. 环境配置
- Python和第三方模板的版本配置
   ```python
    Python版本：3.6
    selenium模块版本：3.141.0
   ```
- 其他配置

  运行前，请先确保你的电脑上安装有Chrome浏览器，然后下载浏览器对应版本的chromedriver程序（具体对应规则自行查找），并配置环境变量。[chromedriver下载地址](http://chromedriver.storage.googleapis.com/index.html)

### 2. 添加任务
- 在buy_tasks目录下，新建你的任务文件，命名规则：*.conf，任务文件中的格式，可以参考 buy_tasks/myself.conf；
- 编写完自己的任务文件之后，在main.py中，创建一个属于该任务文件的OneUserTasks对象和PurchaseProcess对象，然后调用PurchaseProcess对象的start方法，即可添加完成。

PS：支持使用多进程，同时运行多个抢购任务

### 3. 启动任务
运行main.py即可

# About setting.conf file
里面涉及一些重试次数，等待时间等参数的设置。如有需要，可自行修改

