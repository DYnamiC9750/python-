from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

fault = 0


def load(username, passpord, driver):
    url = 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com'
    driver.get(url)

    inputAction = webdriver.ActionChains(driver=driver)  # 初始化动作链
    # 用户密码提交按钮
    userName_tag = driver.find_element(By.XPATH, value='//*[@id="phone"]')
    passpord_tag = driver.find_element(By.XPATH, value='//*[@id="pwd"]')
    load_but = driver.find_element(By.XPATH, value='//*[@id="loginBtn"]')
    inputAction.click(userName_tag)
    inputAction.send_keys_to_element(userName_tag, username)
    inputAction.click(passpord_tag)
    inputAction.send_keys_to_element(passpord_tag, passpord)
    inputAction.click(load_but)
    inputAction.perform()
    sleep(3)
    driver.refresh()
# input('输入任意键关闭')
    sleep(3)


def findClass(driver, cllassName):
    global fault
    overTime(driver)
    action = webdriver.ActionChains(driver=driver)
    frame = driver.find_element(
        By.XPATH, value='//iframe[@id="frame_content"]')
    driver.switch_to.frame(frame)
    # action.move_by_offset(200,0)
    # action.perform()
    # 以社会心理学课程测试
    class_list = driver.find_elements(
        By.XPATH, value='//span[@class="course-name overHidden2"]')
    flag = 0
    for class_ in class_list:
        if class_.text == cllassName:
            flag = 1
            action.click(class_)
            action.perform()
            break
    if flag == 0:
        print("没有找到该课,请确定输入名称是否正确！")
        fault = 1
        return

    sleep(3)
    driver.switch_to.window(driver.window_handles[1])  # 跳转新页面获得新的driver


def findVideo(driver):
    global fault
    if fault == 1:
        return
    overTime(driver)
    chapter_but = driver.find_element(
        By.XPATH, value='/html/body/div[1]/div[3]/div[1]/div/ul[1]/li[2]')
    chapter_but.click()  # 点击章节
    frame = driver.find_element(
        By.XPATH, value='//*[@id="frame_content-zj"]')
    driver.switch_to.frame(frame)  # 跳入frame框架
    video_link = driver.find_element(
        By.XPATH, value='/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]/div/div/div[2]')
    sleep(4)
    video_link.click()

    sleep(2)


def inner_playvideo(driver, frames, frame_out):
    i = 0
    for frame_ in frames:
        try:
            driver.switch_to.frame(frame_out)
            driver.switch_to.frame(frame_)
        except:
            driver.switch_to.frame(frame_)
        video = driver.find_element(
            By.XPATH, value='//*[@id="video"]')
        video.click()
        i += 1
        print("第{}个视频播放".format(i))

        while not isVideoOver(driver):
            if isStop(driver) == 1:
                video.click()
            # try:
            #     ProbleminVideo(driver)
            # except:
            #     continue
            sleep(10)
        sleep(5)
        driver.switch_to.default_content()


def playVideo(driver):  # 播放视频
    global fault
    flag = 0  # 判断是否找到视频
    if fault == 1:
        return
    driver.switch_to.default_content()
    overTime(driver)
    frame_out = driver.find_element(
        By.XPATH, value='//*[@id="iframe"]')  # 外部大的frame框架
    driver.switch_to.frame(frame_out)
    frames = driver.find_elements(  # 视频所在的frame
        By.XPATH, value='//iframe[@class="ans-attach-online ans-insertvideo-online"]')
    if len(frames) != 0:
        inner_playvideo(driver, frames, frame_out)
        print("播放视频")
    else:
        print("无视频")
    Next_but(driver)
    playVideo(driver)


# def BeTree(html_str):
#     tree=etree.HTML(html_str)
#     div_list=tree.xpath()

def isVideoOver(driver):
    # 现在进度条时间：
    now_time = driver.find_element(
        By.XPATH, value='//span[@class="vjs-current-time-display"]').text
    sleep(1)
    all_time = driver.find_element(
        By.XPATH, value='//span[@class="vjs-duration-display"]').text
    i = 1
    # p = 1  # 判断是否暂停
    if((len(now_time) == 0) | (len(all_time) == 0)):
        i -= 1  # 异常，都为空
    if i == 1:
        print('已播放{}/{}'.format(now_time, all_time))
        # time_list.append(now_time)
        # if(time_list[t] == time_list[t-1]):
        #     p = 0
        return now_time == all_time
    else:
        isVideoOver(driver)


def Next_but(driver):  # 按下一章按钮
    driver.switch_to.default_content()  # 跳转到主界面
    Next_but = driver.find_element(
        By.XPATH, value='//div[@class="jb_btn jb_btn_92 fs14 prev_next next"]')
    Next_but.click()
    sleep(2)


def findWork(driver):
    driver.switch_to.default_content()
    # frame = driver.find_element(By.XPATH, value='//*[@id="iframe"]')
    # driver.switch_to.frame(frame)
    span_list = driver.find_elements(
        By.XPATH, value='//span[@class="orangeNew"]')

    return span_list


def overTime(driver):
    try:
        WebDriverWait(driver, 30)
    except Exception as e:
        print(e)
        print("网页加载太慢了!")


def isStop(driver):  # 判断视频是否暂停/结束
    try:
        try:
            stop_but = driver.find_element(
                By.XPATH, value='//button[@class="vjs-play-control vjs-control vjs-button vjs-playing"]').get_attribute('title')
        except:
            stop_but = driver.find_element(
                By.XPATH, value='//button[@class="vjs-play-control vjs-control vjs-button vjs-paused"]').get_attribute('title')
    except:
        stop_but = driver.find_element(
            By.XPATH, value='//button[@class="vjs-play-control vjs-control vjs-button vjs-paused vjs-ended"]').get_attribute('title')
# <button class="vjs-play-control vjs-control vjs-button vjs-paused vjs-ended" type="button" title="重播" aria-disabled="false"><span aria-hidden="true" class="vjs-icon-placeholder"></span><span class="vjs-control-text" aria-live="polite">重播</span></button>
    if stop_but == "播放":
        return 1
    else:
        return 0
    # <span class="vjs-control-text" aria-live="polite">播放</span>


def ProbleminVideo(WebDriver):
    '''
    处理视频中的题
    '''
    ProblemChoices = WebDriver.find_elements_by_name('ans-videoquiz-opt')
    SubmitAnswer = WebDriver.find_element_by_class_name('ans-videoquiz-submit')
    print('发现视频中题')
    for i in range(len(ProblemChoices)):
        print('正在尝试第{}个选项'.format(i+1))
        ProblemChoices = WebDriver.find_elements_by_name('ans-videoquiz-opt')
        ProblemChoices[i].click()
        sleep(2)
        SubmitAnswer.click()
        sleep(2)
        alert = WebDriver.switch_to.alert
        alert.accept()
