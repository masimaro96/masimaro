import time, sys, unittest, random, json
from datetime import datetime
from appium import webdriver
from random import randint
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

# Connect to Appium with the below desire capabilities
# http://appium.io/docs/en/writing-running-appium/caps/
dc = {
    "deviceName": "4458f4df58c6a32c",
    "platformName": "Android",
    "app": "E:\\Quynh\\Selenium\\Appium-Python\\HR-app\\app-hanbiro-release.apk",
    "automationName": "UiAutomator2",
    "autoGrantPermissions": "true",
    "appWaitPackage": "com.hanbiro.hanbirohrm",
    "appWaitActivity": "com.hanbiro.globalhr.MainActivity",
    "locale": "US",
    "language": "en"
}

with open("config-10.json") as json_data_file:
    data = json.load(json_data_file)

n = random.randint(1,3000)

# If desire capabilities are valid, the app will be open at Log in screen
driver = webdriver.Remote('http://localhost:4723/wd/hub', dc)

def execution():
    try:
        checkcrashapp = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Domain']")))
        if checkcrashapp.is_displayed():
            print("------- Login to app -------")
            # Input information for log-in
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Domain']")))
            driver.find_element_by_xpath(data["domain"]).send_keys(data["domain_name"])
            print("- Input Domain")
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='ID']")))
            driver.find_element_by_xpath(data["id_app"]).send_keys(data["id_name"])
            print("- Input ID")
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Password']")))
            driver.find_element_by_xpath(data["password"]).send_keys(data["pass_input"])
            print("- Input Password")
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Login')]")))
            driver.find_element_by_xpath(data["button_login"]).click()
            print("=> Click Log In button")
            driver.implicitly_wait(50)

            ''' * Check crash app done
            => Execute function '''
            # clock_in_GPS()
            # break_time()
            # clock_out_GPS()
            # viewNoti()
            # add_event()
            # timecard()
            # admin()
            # settings()
            access_vacation()
            # vacation()
            # approve_request()
        else:
            print("=> Crash app")
            exit(0)
    except WebDriverException:
            print("=> Crash app")
            exit(0)

def clock_in_GPS():
    print(" ")
    print("------- Clock In -------")
    try:
        title_app = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["title"])))
        if title_app.text == 'GPS':
            print("Clock in - GPS")
            try:
                OT = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["clock_in"]["nightshift"])))
                if OT.text == 'Night Shift':
                    print("=> Work night shift")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["OT"]["confirm_OT"]))).click()
                    print("- Confirm OT / Work night shift")
                    time.sleep(5)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["OT"]["OT_apply"]))).click()
                    print("- Apply OT")
                    time.sleep(5)
                    
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["OT"]["select_time"]))).click()
                    print("- Select time")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["OT"]["time"]))).click()
                    time.sleep(5)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please input a reason to apply OT')]"))).send_keys(data["OT"]["text"])
                    print("-> Input reason")

                    driver.swipe(start_x=675, start_y=2458, end_x=675, end_y=2000, duration=800)
                    time.sleep(5)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["OT"]["apply_OT"]))).click()
                    time.sleep(5)

                    try:
                        check_OT = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["OT"]["apply_text"])))
                        if check_OT.text == 'Apply OT':
                            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Close')]"))).click()
                            print("=> Apply OT success")
                        else:
                            print("=> Crash app")
                    except WebDriverException:
                        print("=> Crash app")        
                        exit(0)
                else:
                    print("=> Apply OT not display")
            except WebDriverException:
                print("=> Apply OT not display")  
        
            try:
                icon_clock_in = driver.find_element_by_xpath(data["clock_in"]["icon_clock_in_button"])
                if icon_clock_in.is_displayed():
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,data["clock_in"]["icon_clockin"]))).click()
                    print("=> Clock In with GPS")
                    try:
                        status_late = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["clock_in_late"])))
                        if status_late.text == 'Tardiness':
                            print("=> Clock in late")
                            driver.find_element_by_xpath(data["clock_in"]["text_input"]).send_keys(data["clock_in"]["text"])
                            print("- Input reason")
                            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]")))
                            driver.find_element_by_xpath(data["clock_in"]["save_button"]).click()
                            print("=> Save")
                        else:
                            print("=> Clock in on time") 
                            time.sleep(5)
                    except WebDriverException:
                        print("=> Crash app")
                        exit(0)
                else:
                    print(" Clock in button not display")
                    time.sleep(5)
            except WebDriverException:
                print("=> Clock in button not display")
            time.sleep(5)

            try:
                icon_clock_out = driver.find_element_by_xpath(data["clock_in"]["icon_breaktime"])
                if icon_clock_out.is_displayed():
                    print("=> Already clock in")
                else:
                    print("=> Break time button not display")
            except WebDriverException:
                print("=> Fail") 
        else:
            print("=> .Crash app") 
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["IN"]))).click()
            print("- Select IN on map")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["select_branch"]))).click()
            print("- Select branch")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["close_popup"]))).click()
            print("- Close popup")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["IN"]))).click()
            print("- Select OUT on map")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["select_branch"]))).click()
            print("- Select branch")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["close_popup"]))).click()
            print("- Close popup")
            time.sleep(5)
        except WebDriverException:
            print("=> IN - OUT not display")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Wifi')]"))).click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'GPS')]"))).click() 
            print("- Change to wifi -> GPS") 
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["IN"]))).click()
            print("- Select IN on map")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["select_branch"]))).click()
            print("- Select branch")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["close_popup"]))).click()
            print("- Close popup")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["IN"]))).click()
            print("- Select OUT on map")
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["select_branch"]))).click()
            print("- Select branch")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["close_popup"]))).click()
            print("- Close popup")
        time.sleep(5)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["preview"]))).click()
        print("- View preview date")
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["next"]))).click()
        print("- View next date")
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["calendar"]))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='0']//android.view.ViewGroup[@index='3']//android.widget.ScrollView[@index='0']//android.view.ViewGroup[@index='1']//android.widget.Button[@index=3]"))).click()
        print("- Select date")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["clock_in"]["select"]))).click()
    except WebDriverException:
        print("=> Crash app")
        exit(0)

def clock_in_Wifi():
    print(" ")
    print("------- Clock In -------")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Wifi')]"))).click()
    print("=> Change to wifi")
    try:
        wifitext = driver.find_element_by_xpath(data["WIFI_settings"]["wifi_text"])
        if wifitext.is_displayed():
            print("Clock in - wifi")
            try:
                OT = driver.find_element_by_xpath(data["clock_in"]["nightshift"])
                if OT.is_displayed():
                    print("=> Work night shift")
                    driver.find_element_by_xpath(data["OT"]["confirm_OT"]).click()
                    print("- Confirm OT / Work night shift")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Apply OT')]")))
                    driver.find_element_by_xpath(data["OT"]["OT_apply"]).click()
                    print("- Apply OT")
                    driver.find_element_by_xpath(data["OT"]["select_time"]).click()
                    print("- Select time")

                    driver.find_element_by_xpath(data["OT"]["time"]).click()

                    driver.find_element_by_xpath(data["OT"]["text_input"]).send_keys(data["OT"]["text"])
                    print("-> Input reason")

                    driver.swipe(start_x=675, start_y=2458, end_x=675, end_y=2000, duration=800)

                    driver.find_element_by_xpath(data["OT"]["apply_OT"]).click()

                    try:
                        check_OT = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["OT"]["apply_text"])))
                        if check_OT.text == 'Apply OT':
                            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Close')]"))).click()
                            print("=> Apply OT success")
                        else:
                            print("=> Crash app")
                    except WebDriverException:
                        print("=> Crash app")        
                        exit(0)
                else:
                    print("=> Apply OT not display")
                    time.sleep(5)
            except WebDriverException:
                print("=> Apply OT not display")  
        
            try:
                icon_clock_in = driver.find_element_by_xpath(data["clock_in"]["icon_clock_in_button"])
                if icon_clock_in.is_displayed():
                    driver.find_element_by_xpath(data["clock_in"]["icon_clockin"]).click()
                    print("=> Clock In with Wifi")
                    time.sleep(5)
                    try:
                        late = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please enter your reason')]")))
                        if late.is_displayed():
                            print("=> Clock in late")
                            driver.find_element_by_xpath(data["clock_in"]["text_input"]).send_keys(data["clock_in"]["text"])
                            print("- Input reason")
                            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]")))
                            driver.find_element_by_xpath(data["clock_in"]["save_button"]).click()
                            print("=> Save")
                        else:
                            print("=> Clock in on time") 
                            time.sleep(5)
                    except WebDriverException:
                        print("=> Crash app")
                        exit(0)
                else:
                    print(" Clock in button not display")
                    time.sleep(5)
            except WebDriverException:
                print("=> Clock in button not display")

            try:
                icon_clock_out = driver.find_element_by_xpath(data["clock_in"]["icon_breaktime"])
                if icon_clock_out.is_displayed():
                    print("=> Already clock in")
                else:
                    print("=> Break time button not display")
            except WebDriverException:
                print("=> Break time button not display") 
        else:
            print("=> Crash app") 
    except WebDriverException:
        print("=> Crash app")
        exit(0)

def clock_in_Beacon():
    print(" ")
    print("------- Clock In -------")  
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Beacon')]"))).click()
    print("=> Change to Beacon")
    try:
        try:
            OT = driver.find_element_by_xpath(data["clock_in"]["nightshift"])
            if OT.is_displayed():
                print("=> Work night shift")
                driver.find_element_by_xpath(data["OT"]["confirm_OT"]).click()
                print("- Confirm OT / Work night shift")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Apply OT')]")))
                driver.find_element_by_xpath(data["OT"]["OT_apply"]).click()
                print("- Apply OT")
                driver.find_element_by_xpath(data["OT"]["select_time"]).click()
                print("- Select time")

                driver.find_element_by_xpath(data["OT"]["time"]).click()

                driver.find_element_by_xpath(data["OT"]["text_input"]).send_keys(data["OT"]["text"])
                print("-> Input reason")

                driver.swipe(start_x=675, start_y=2458, end_x=675, end_y=2000, duration=800)

                driver.find_element_by_xpath(data["OT"]["apply_OT"]).click()

                try:
                    check_OT = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["OT"]["apply_text"])))
                    if check_OT.text == 'Apply OT':
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Close')]"))).click()
                        print("=> Apply OT success")
                    else:
                        print("=> Crash app")
                except WebDriverException:
                    print("=> Crash app")        
                    exit(0)
            else:
                print("=> Apply OT not display")
                time.sleep(5)
        except WebDriverException:
            print("=> Apply OT not display")  
        
        try:
            icon_clock_in = driver.find_element_by_xpath(data["clock_in"]["icon_clock_in_button"])
            if icon_clock_in.is_displayed():
                driver.find_element_by_xpath(data["clock_in"]["icon_clockin"]).click()
                print("=> Clock In with Beacon")
                time.sleep(5)
                try:
                    late = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please enter your reason')]")))
                    if late.is_displayed():
                        print("=> Clock in late")
                        driver.find_element_by_xpath(data["clock_in"]["text_input"]).send_keys(data["clock_in"]["text"])
                        print("- Input reason")
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]")))
                        driver.find_element_by_xpath(data["clock_in"]["save_button"]).click()
                        print("=> Save")
                    else:
                        print("=> Clock in on time") 
                        time.sleep(5)
                except WebDriverException:
                    print("=> Crash app")
                    exit(0)
            else:
                print(" Clock in button not display")
                time.sleep(5)
        except WebDriverException:
            print("=> Clock in button not display")

        try:
            icon_clock_out = driver.find_element_by_xpath(data["clock_in"]["icon_breaktime"])
            if icon_clock_out.is_displayed():
                print("=> Already clock in")
            else:
                print("=> Break time button not display")
        except WebDriverException:
            print("=> Break time button not display")

    except WebDriverException:
        print("=> Crash app")
        exit(0)

def viewNoti():
    print(" ")
    print("------- View notification -------")
    time.sleep(10)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["view_noti"]["noti"]))).click()
    print("=> Click view notification")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["view_noti"]["back_homepage"]))).click()
    print("=> Back to homepage")       
    time.sleep(5)
    
def add_event():
    print(" ")
    print("------- Add event -------")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["timecard"]))).click()
    print("- Select time card")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["timesheet"]))).click()
    title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["title_timesheet"])))
    if title.text == 'Timesheet':
        print("- Select time sheet")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["add"]))).click()
        print("- Select add")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please input data.')]"))).send_keys(data["event"]["title_text"])
        print("- Input title")
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["choose_event"]))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["type_event"]))).click()
        print("- Choose event")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["select_color"]))).click()
        print("- Select color")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please input data.')]"))).send_keys(data["event"]["location_text"])
        print("- Input location")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please add a memo.')]"))).send_keys(data["event"]["memo_text"])
        print("- Input memo")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["button_save"]))).click()

    print("** Check event use approval type")
    try:
        approval_type = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["popup"])))
        if approval_type.text == '[Approved] Your request approval request has been approved automatically':
            print("=> Use approval type: Automatic approval")

        elif approval_type.text == 'The approval request has been submitted. Please wait until the approval is completed.':
            print("=> Use approval type: Approval Line")

        elif approval_type.text == 'The approval request has been delivered to Head of Department. Please wait until the approval is completed.':
            print("=> Use approval type: Head Dept.")

        elif approval_type.text == 'The approval request has been delivered to Timecard Managers. Please wait until the approval is completed.':
            print("=> Use approval type: Timecard Manager")
        else:
            print("=> Use approval type: Dept. Manager")
    except WebDriverException:
        print("=> Use approval type: Dept. Manager") 

    driver.find_element_by_xpath(data["event"]["close_popup"]).click()
    print("=> Save event")
    time.sleep(5)


'''
1. Add/Edit/Delete GPS
2. Add/Edit/Delete Wifi
* Delete function can't use when run appium

3. Add/Edit/Delete Beacon
* Time to find beacon take to long, can't find beacon
'''
def admin():
    try:
        print(" ")
        print("------- Add GPS -------")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["admin"]["Admin"]))).click()
        print("- Select admin")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'GPS Setting')]"))).click()
        print("- Click GPS Setting")
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["admin"]["GPS_settings"]["add_gps"]))).click()
        print("- Add GPS")

        try:
            check_gps = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["admin"]["GPS_settings"]["popup"])))
            if check_gps.is_displayed():
                check_gps.click()
            else:
                print("=> Crash app")
        except WebDriverException:
            print("=> Crash app")        
            exit(0)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please input a address')]")))
        address = driver.find_element_by_xpath(data["admin"]["GPS_settings"]["search"])
        address.click()
        address.send_keys(data["admin"]["GPS_settings"]["search_text"])
        print("- Search address")

        driver.hide_keyboard()
        time.sleep(5)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["admin"]["GPS_settings"]["list"]))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'400 Nguyễn Thị Thập, Tân Quy, District 7, Ho Chi Minh City, Vietnam')]"))).click()
        print("- Select address")

        location = driver.find_element_by_xpath(data["admin"]["GPS_settings"]["location"])
        location.clear()
        location.send_keys(data["admin"]["GPS_settings"]["location_text"] + str(n))
        print("- Input location")
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["workPlace"]).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Vietnam Office')]")))
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["workPlace_input"]).click()
        print("- Select work Place")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]"))).click()
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["close_save"]).click()
        print("- Save")
        time.sleep(5)
        
        print("- Search GPS")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please enter your keyword.')]"))).click()
        
        ''' Send key "hr-GPS" from keyboard mobile '''
        driver.is_keyboard_shown()
        driver.press_keycode(36)
        driver.press_keycode(46)
        driver.press_keycode(69)
        driver.press_keycode(35)
        driver.press_keycode(44)
        driver.press_keycode(47)
        driver.press_keycode(66)

        print("** Edit GPS")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'hr-GPS')]"))).click()
        location = driver.find_element_by_xpath(data["admin"]["GPS_settings"]["location"])
        location.clear()
        location.send_keys(data["admin"]["GPS_settings"]["location_text_edit"] + str(n))
        print("- Input edit location")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]")))
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["button_save"]).click()
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["close_save"]).click()
        print("- Save")
        time.sleep(10)
        
        print("** Delete GPS")
        driver.swipe(start_x=1000, start_y=550, end_x=500, end_y=550, duration=800)

        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Delete')]"))).click()
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["delete"]).click()
        print("- Select GPS delete")
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["accept_delete"]).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Close')]"))).click()
        print("- Accept delete")
        time.sleep(10)
        
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["back"]).click()
        print(" ")

        '''print("------- Add Wifi -------")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'WiFi Setting')]"))).click()
        print("- Select Wifi setting")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["add_wifi"]).click()
        print("- Add new wifi")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["wifi_name"]).click()
        print("- Select name wifi")

        try:
            warning = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'WIFI Settings')]")))
            if warning.is_displayed():
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["admin"]["WIFI_settings"]["add_wifi"])))
            else:
                print("=> Fail")
        except WebDriverException:
            print("=> Fail")

        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["button_next"][0]).click()
        print("- Select next step")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["workPlace"]).click()
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["workPlace_input"]).click()
        print("- Select work Place")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["button_next"][1]).click()
        print("- Select next step")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["close_popup"]).click()
        print("- Close pop up")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["complete"]).click()
        print("- Add wifi success")
        time.sleep(5)'''

        '''
        * Can't use function delete when run auto appium
        -> When swpie element, delete button can't click on. 
        -> When finish auto, open app and delete element => can't click on button, must kill app and open again it's can be use again
        * Can delete when use manaul 
        '''
        '''print("** Delete wifi")
        driver.swipe(start_x=1000, start_y=550, end_x=500, end_y=550, duration=800)
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Delete')]"))).click()
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["delete"]).click()
        print("- Select wifi")
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["accept_delete"]).click()
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["popup"]).click()
        print("- Accept delete")'''

        print("- Search wifi")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'WiFi Setting')]"))).click()
        print("- Select Wifi setting")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please enter your keyword.')]"))).click()
        
        ''' Send key from keyboard mobile '''
        driver.is_keyboard_shown()
        driver.press_keycode(38)
        driver.press_keycode(47)
        driver.press_keycode(62)
        driver.press_keycode(50)
        driver.press_keycode(37)
        driver.press_keycode(42)
        driver.press_keycode(29)
        driver.press_keycode(66)

        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["back"]).click()

        '''
        * Recomment not run this function
        Take to much time to find beacon and maybe beacon can't be found 
        '''

        print(" ")
        print("------- Add Beacon -------")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Beacon Setting')]"))).click()
        print("- Select Beacon")
        '''driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["add_wifi"]).click()
        print("- Add new Beacon")
        time.sleep(20)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'MiniBeacon_00997')]"))).click()
        print("- Select Beacon")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Next')]"))).click()
        print("- Select next step")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["workPlace"]).click()
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["workPlace_input"]).click()
        print("- Select work Place")
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["button_next"][1]).click()
        print("- Select next step")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Close')]"))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Complete')]"))).click()
        print("- Add Beacon success")
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["back"]).click()'''

        driver.find_element_by_xpath(data["admin"]["BEACON_settings"]["edit"]).click()
        beacon = driver.find_element_by_xpath(data["admin"]["BEACON_settings"]["edit_name"])
        beacon.clear()
        beacon.send_keys(data["admin"]["BEACON_settings"]["name"] + str(n))
        driver.find_element_by_xpath(data["admin"]["WIFI_settings"]["button_next"][1]).click()
        print("- Select next step")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Close')]"))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Complete')]"))).click()
        print("- Edit Beacon success")
        driver.find_element_by_xpath(data["admin"]["GPS_settings"]["back"]).click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["admin"]["homepage"]))).click()
    except WebDriverException:
        print("=> Crash app")
        exit(0)

def break_time():
    ''' Break time button '''
    try:
        print("** Check break time - clock out")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["admin"]["homepage"]))).click()
        text_breaktime = driver.find_element_by_xpath(data["clock_in"]["breaktime_text"])
        if text_breaktime.text == 'Break Time':
            print("=> Break time")
            driver.find_element_by_xpath(data["clock_in"]["icon_breaktime"]).click()
            time.sleep(30)
            ''' End break time '''
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'END BREAK TIME')]")))
            driver.find_element_by_xpath(data["clock_in"]["end_break_time"]).click()
            time.sleep(10)
        else: 
            print("=> Already clock out")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["admin"]["homepage"]))).click()
        time.sleep(5)
    except WebDriverException:
        print("=> Already clock out") 
        time.sleep(5)

def clock_out_GPS():
    try:
        print("** Check clock out")
        text_breaktime = driver.find_element_by_xpath(data["clock_in"]["breaktime_text"])
        if text_breaktime.text == 'Break Time':
            print(" ")
            clockout = driver.find_element_by_xpath(data["clock_out"]["icon_clock_out_button"])
            if clockout.is_displayed():
                clockout.click()
                print("=> Click clock out")
                time.sleep(2)
                ''' Check clock out time '''
                popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_out"]["status"])))
                if popup.text == 'Leave Early':
                    print("- Clock out early")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Please input a reason to apply OT')]"))).send_keys(data["clock_in"]["text"])
                    print("- Input reason")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_out"]["save"]))).click()
                    print("=> Save")
                else:
                    print("=> Clock out on time")
                    driver.find_element_by_xpath(data["clock_out"]["close_popup"]).click()
        else:
            print("=> Already clock out")
    except WebDriverException:
        print("=> Already clock out") 
    time.sleep(5)

def clock_out_Wifi():
    try:
        print("** Check clock out")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Wifi')]"))).click()
        print("=> Change to wifi")
        time.sleep(10)
        text_breaktime = driver.find_element_by_xpath(data["clock_in"]["breaktime_text"])
        if text_breaktime.text == 'Break Time':
            print(" ")
            clockout = driver.find_element_by_xpath(data["clock_out"]["icon_clock_out_button"])
            if clockout.is_displayed():
                clockout.click()
                print("=> Click clock out")
                time.sleep(2)
                ''' Check clock out time '''
                popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_out"]["status"])))
                if popup.text == 'Leave Early':
                    print("- Clock out early")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_out"]["input_text"]))).send_keys(data["clock_in"]["text"])
                    print("- Input reason")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]")))
                    driver.find_element_by_xpath(data["clock_in"]["save_button"]).click()
                    print("=> Save")
                else:
                    print("=> Clock out on time")
                    driver.find_element_by_xpath(data["clock_out"]["close_popup"]).click()
        else:
            print("=> Already clock out")
    except WebDriverException:
        print("=> Already clock out") 
    time.sleep(5)

def clock_out_Beacon():
    try:
        print("** Check clock out")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Beacon')]"))).click()
        print("=> Change to Beacon")
        text_breaktime = driver.find_element_by_xpath(data["clock_in"]["breaktime_text"])
        if text_breaktime.text == 'Break Time':
            print(" ")
            clockout = driver.find_element_by_xpath(data["clock_out"]["icon_clock_out_button"])
            if clockout.is_displayed():
                clockout.click()
                print("=> Click clock out")
                time.sleep(2)
                ''' Check clock out time '''
                popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_out"]["status"])))
                if popup.text == 'Leave Early':
                    print("- Clock out early")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["clock_out"]["input_text"]))).send_keys(data["clock_in"]["text"])
                    print("- Input reason")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Save')]")))
                    driver.find_element_by_xpath(data["clock_in"]["save_button"]).click()
                    print("=> Save")
                else:
                    print("=> Clock out on time")
                    driver.find_element_by_xpath(data["clock_out"]["close_popup"]).click()
        else:
            print("=> Already clock out")
    except WebDriverException:
        print("=> Already clock out") 
    time.sleep(5)

def settings():
    print(" ")
    print("** Settings app **")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language"]))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='한국어']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='닫기']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()
    
    korean_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language_text"])))
    if korean_text.text == '한국어':
        print("=> Change to language '한국어' success")
    else:
        print("=> Fail")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='언어 설정']"))).click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Tiếng Việt']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Đóng']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()

    VN_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language_text"])))
    if VN_text.text == 'Tiếng Việt':
        print("=> Change to language 'Tiếng Việt' success")
    else:
        print("=> Fail")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Thay đổi ngôn ngữ']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='日本語']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='閉じる']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()

    JP = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language_text"])))
    if JP.text == '日本語':
        print("=> Change to language '日本語' success")
    else:
        print("=> Fail")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='言語']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='简体中文']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='關閉']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()

    TQ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language_text"])))
    if TQ.text == '简体中文':
        print("=> Change to language '简体中文' success")
    else:
        print("=> Fail")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='語言']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Indonesian']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Tutup']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()

    indo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language_text"])))
    if indo.text == 'Indonesian':
        print("=> Change to language 'Indonesian' success")
    else:
        print("=> Fail")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Ganti BAHASA']"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='English']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Close']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["settings_button"]))).click()
    EN = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["settings"]["language_text"])))
    if EN.text == 'English':
        print("=> Change to language 'English' success")
    else:
        print("=> Fail")
 
'''
- Check crash app of timecard
=> when click to menu but don't display data, it'll show result crash app
'''
def timecard():
    ''' Timesheet '''
    print(" ")
    print("** Check crash app **")
    print("- Timesheet - Daily -")
    driver.find_element_by_xpath(data["event"]["timecard"]).click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["timesheet"]))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["next"]))).click()
    print("- View next date")   
    time.sleep(5)
    next_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["policy"])))
    if next_text.text == 'Work Policy':
        print("=> View next date success")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)    

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["prev"]))).click()
    print("- View preview date")
    time.sleep(5)
    prev_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["policy"])))
    if next_text.text == 'Work Policy':
        print("=> View prev date success")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)   

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["calendar"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=13]"))).click()
    print("- Select date from calendar")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["select_date"]))).click()
    time.sleep(5)
    date_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_daily"]["date"])))
    if date_select.is_displayed():
        print("=> Select date success")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)   
    
    print(" ")
    print("- Timesheet - List -")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["list"]))).click()
    print("- Go to List") 
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["next"]))).click()
    print("- View next month")   
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["prev"]))).click()
    print("- View preview month")
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["calendar"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    print("- Select date from calendar")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["select_date"]))).click()
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["sort"]))).click()
    print("- Sort by")
    time.sleep(2)
    list_week = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["list_sort"])))
    if list_week.is_displayed():
        print("- Show list week")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_2"]))).click()
    print("- 2nd Week")
    time.sleep(5)
    
    total_week_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_2_text"])))
    if total_week_1.text == 'TOTAL OF 2ND WEEK':
        print("=> TOTAL OF 2ND WEEK")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["sort"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_3"]))).click()
    print("- 3rd Week")
    time.sleep(5)

    total_week_2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_3_text"])))
    if total_week_2.text == 'TOTAL OF 3RD WEEK':
        print("=> TOTAL OF 3RD WEEK")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["sort"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_4"]))).click()
    print("- 4th Week")
    time.sleep(5)
    total_week_3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_4_text"])))
    if total_week_3.text == 'TOTAL OF 4TH WEEK':
        print("=> TOTAL OF 4TH WEEK")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["sort"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_5"]))).click()
    print("- 5th Week")
    time.sleep(5)
    total_week_4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_list"]["week_5_text"])))
    if total_week_4.text == 'TOTAL OF 5TH WEEK':
        print("=> TOTAL OF 5TH WEEK")
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)
    
    print(" ")
    print("- Timesheet - Calendar -")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_calendar"]["calendar"]))).click()
    print("- Go to List") 
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_calendar"]["next"]))).click()
    print("- View next date")   
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_calendar"]["prev"]))).click()
    print("- View preview date")
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_calendar"]["calendar_select"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    print("- Select date from calendar")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timesheet_calendar"]["select_date"]))).click()
    time.sleep(5)

    driver.find_element_by_xpath(data["event"]["timecard"]).click()

    ''' REPORT '''
    print("** Check report - Monthly")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["MT_report"]))).click()
    print("- Schedule Working")
    time.sleep(10)

    schedule = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["schedule_working"])))
    if schedule.text == 'Scheduled working day':
        count_day = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["count_schedule_working"])))
        print("- Scheduled working day:", count_day.text)
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["events"]))).click()
    print("- Events")
    time.sleep(5)
    clock_in = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["clockin"])))
    if clock_in.text == 'Clock-In':
        count_clock_in = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["count_clockin"])))
        print("- Events - Clock in:", count_clock_in.text)
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["working_status"]))).click()
    print("- Working status")
    time.sleep(5)
    working_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["workingtime"])))
    if working_time.text == 'Working time':
        count_working_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_monthly"]["count_workingtime"])))
        print("- Working status - Working time:", count_working_time.text)
    else:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    print("** Check report - Weekly")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_weekly"]["weekly"]))).click()
    print("- View week tab")
    time.sleep(10)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Device']"))).click()
    print("- View tab device")
    time.sleep(5)

    driver.swipe(start_x=1174, start_y=730, end_x=400, end_y=730, duration=800)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Average working hour per week']"))).click()
    print("- View tab Avg_Working")
    time.sleep(5)
    driver.swipe(start_x=1174, start_y=730, end_x=400, end_y=730, duration=800)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Working hours per day of the week']"))).click()
    print("- View tab working hour")
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_weekly"]["next"]))).click()
    print("- View next month")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_weekly"]["prev"]))).click()
    print("- View preview month")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_weekly"]["calendar_select"]))).click()
    print("- Select calendar")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_weekly"]["select_date"]))).click()
    print("- Select date")
    time.sleep(5)

    print("** Check report - List")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_list"]["list"]))).click()
    print("- View list tab")
    time.sleep(10)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_list"]["next"]))).click()
    print("- View next month")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_list"]["prev"]))).click()
    print("- View preview month")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_list"]["calendar_select"]))).click()
    print("- Select calendar")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report_list"]["select_date"]))).click()
    print("- Select date")
    time.sleep(5)


    print(" ")
    print("** Check Company timecard - Weekly Status")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["weekly_status_CT"]))).click()
    time.sleep(5)
    try:
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_title"])))
        if title.text == 'Weekly Status':
            print("- Show content")

    except WebDriverException:
        print("=> Crash app")
        exit(0)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["sort_week"]))).click()
        print("- Select sort week")
        sortweek = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["list"])))
        if sortweek.is_displayed:
            print("- List week display")
        else:
            print("- List not display")
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    print("- Select week")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_2"]))).click()
    print("- 2nd Week")
    time.sleep(5)
    try:
        user_view = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["user"])))
        if user_view.is_displayed():
            print("- Show content")
        else:
            print("- No data")
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["sort_week"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_3"]))).click()
    print("- 3rd Week")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["sort_week"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_4"]))).click()
    print("- 4th Week")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["sort_week"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_5"]))).click()
    print("- 5th Week")
    time.sleep(5)

    '''WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["sort_week"]))).click()
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1126, end_x=291, end_y=900, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_6"]))).click()
    print("- 6th Week")
    time.sleep(5)'''

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["sort_week"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["week_1"]))).click()
    print("- 1st Week")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["search"]))).click()
    print("- Search user")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()
    
    ''' Send key "quynh" from keyboard mobile '''
    driver.is_keyboard_shown()
    driver.press_keycode(45)
    driver.press_keycode(49)
    driver.press_keycode(53)
    driver.press_keycode(42)
    driver.press_keycode(36)
    driver.press_keycode(66)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()
    time.sleep(5)

    ''' Next - Prev - Select date '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["next"]))).click()
    print("- View next month")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["prev"]))).click()
    print("- View preview month")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["calendar_select"]))).click()
    print("- Select calendar")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=19]"))).click()
    time.sleep(5)

    dateselect = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["date_calendar"])))
    dateselect_text = dateselect.text

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["select_date"]))).click()
    print("- Select date")
    time.sleep(10)

    try:
        user_view = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["user"])))
        if user_view.is_displayed():
            print("- Show content")
        else:
            print("- No data")
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["view_detail"]))).click()
    print("- View detail")

    date_of_calendar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["date"])))
    date = date_of_calendar.text
    x = date.split(" ")[2]
    a = x.split(",")[0]

    if a == dateselect_text:
        print("- Show right date")
    else:
        print("- Crash")
        exit(0)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["weekly_status"]["back"]))).click()
    print(" ")
    print("** Check Company timecard - Time Line")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["timeline_CT"]))).click()
    time.sleep(5)
    try:
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["timeline_title"])))
        if title.text == 'Time Line':
            print("- Show content")

    except WebDriverException:
        print("=> Crash app")
        exit(0)

    ''' Search user '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["search"]))).click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()
    
    ''' Send key "quynh" from keyboard mobile '''
    driver.is_keyboard_shown()
    driver.press_keycode(45)
    driver.press_keycode(49)
    driver.press_keycode(53) 
    driver.press_keycode(42)
    driver.press_keycode(36)
    driver.press_keycode(66)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()
    print("- Select user")
    time.sleep(5)

    ''' Next - Prev - Select date '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["next"]))).click()
    print("- View next date")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["prev"]))).click()
    print("- View preview date")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["calendar_select"]))).click()
    print("- Select calendar")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=19]"))).click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["select_date"]))).click()
    print("- Select date")
    time.sleep(10)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    print("- Sort time line")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["clockin"]))).click()
    print("- Clock in")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    print("- Sort time line")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["tardin"]))).click()
    print("- Tardines")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    print("- Sort time line")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["clockout"]))).click()
    print("- Clock out")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    print("- Sort time line")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["auto_clockout"]))).click()
    print("- Automatically Clock-out")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    print("- Sort time line")
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["outside"]))).click()
    print("- Outside")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["meeting"]))).click()
    print("- Meeting")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["edu"]))).click()
    print("- Education")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["business"]))).click()
    print("- Business Trip")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["working_remote"]))).click()
    print("- Working remote")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["sort_timeline"]))).click()
    time.sleep(5)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    driver.swipe(start_x=291, start_y=1315, end_x=291, end_y=691, duration=800)
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["timeline"]["working"]))).click()
    print("- Working")
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,data["event"]["timecard"]))).click()
    
    print(" ")
    print("** Check Company timecard - Report")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["report_CT"]))).click()
    print("- View by work")
    time.sleep(5)
    try:
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["report_title"])))
        if title.text == 'Report':
            print("- Show content")

    except WebDriverException:
        print("=> Crash app")
        exit(0)

    ''' Next - Prev - Select date '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["next"]))).click()
    print("- View next date")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["prev"]))).click()
    print("- View preview date")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["calendar_select"]))).click()
    print("- Select calendar")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=19]"))).click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["select_date"]))).click()
    print("- Select date")
    time.sleep(10)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["search"]))).click()
    print("- Search user")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()

    ''' Send key "quynh" from keyboard mobile '''
    driver.is_keyboard_shown()
    driver.press_keycode(45)
    driver.press_keycode(49)
    driver.press_keycode(53)
    driver.press_keycode(42)
    driver.press_keycode(36)
    driver.press_keycode(66)
    time.sleep(3)
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()
    print("- Select user")
    time.sleep(5)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["detail"]))).click()
    print("- View detail")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["back"]))).click()
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["view_by_event"]))).click()
    print("- View by event")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["detail"]))).click()
    print("- View detail")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["back"]))).click()
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,data["event"]["timecard"]))).click()

    print(" ")
    print("** Check Company timecard - Approval")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approval_CT"]))).click()
    time.sleep(5)
    try:
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approval_title"])))
        if title.text == 'Approval':
            print("- Show content")
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    time.sleep(10)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["filter_type"]))).click()
    print("- Filter type")
    time.sleep(5)
    try:
        filter = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["detail"])))
        if filter.text == 'Detail':
            print("-")
    except WebDriverException:
        print("=> Crash app")
        exit(0)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["type"]))).click()
    print("- Select type")
    time.sleep(5)
    try:
        type_detail = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["event"])))
        if type_detail.is_displayed():
            type_detail.click()
            time.sleep(5)
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["status"]))).click()
    print("- Select status")
    time.sleep(5)
    try:
        status = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["pending"])))
        if status.is_displayed():
            status.click()
            time.sleep(5)
    except WebDriverException:
        print("=> Crash app")
        exit(0)

    '''WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["peroid"]))).click()
    print("- Select peroid")
    time.sleep(5)
    try:
        peroid = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["today"])))
        if peroid.is_displayed():
            peroid.click()
            time.sleep(5)
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    time.sleep(5)'''

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["back"]))).click()
    time.sleep(5)
    try:
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approval_title"])))
        if title.text == 'Approval':
            print("- Show content")
    except WebDriverException:
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["report"]["search"]))).click()
    print("- Search user")
    
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()

    ''' Send key "quynh" from keyboard mobile '''
    driver.is_keyboard_shown()
    driver.press_keycode(45)
    driver.press_keycode(49)
    driver.press_keycode(53)
    driver.press_keycode(42)
    driver.press_keycode(36)
    driver.press_keycode(66)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["user"]))).click()
    #WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//android.widget.TextView[@text='quynh1']"))).click()
    print("- Select user")
    time.sleep(5)

    ''' Approve '''
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["select"]))).click()
    try:
        approve_line = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approval_line"])))
        if approve_line.is_displayed():
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approve"]))).click()
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["close"]))).click()
            print("- Approve request")
            time.sleep(5)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["filter_type"]))).click()
            print("- Filter type")
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["status"]))).click()
            print("- Select status")
            time.sleep(5)
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approved"]))).click()
            time.sleep(5)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["back"]))).click()
            time.sleep(5)

            status_approve = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["status_text"])))
            if status_approve.text == 'Approved':
                print("- Approve success")
            else:
                print("- Fail")
        else:
            print("=> Approve don't have approve permission")
    except WebDriverException:
        print("=> Approve don't have approve permission")

    ''' Reject '''
    add_event()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["event"]["timecard"]))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approval_CT"]))).click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["select"]))).click()
    try:
        approve_line = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["approval_line"])))
        if approve_line.is_displayed():
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["reject_bt"]))).click()
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["close"]))).click()
            time.sleep(5)
            status_reject = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TimeCard"]["approval"]["status_text"])))
            if status_reject.text == 'Rejected':
                print("- Rejected success")
            else:
                print("- Fail")
        else:
            print("=> Approve don't have approve permission")
    except WebDriverException:
        print("=> Approve don't have approve permission")

def access_vacation():
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    print("- Vacation")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request"]))).click() 
    print(" ")

    title_request = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_vacation_text"])))
    if title_request.text == 'Request vacation':
        print("- Request vacation")
    else:
        print("=> Crash app")
        exit(0)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["request_vacation"]["vacation_information"]))).click()
    
    title_page_infor = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["request_vacation"]["vacation_information_text"])))
    if title_page_infor.text == 'Vacation information':
        print("- View detail vacation information")
    else:
        print("=> Crash app")
        exit(0)
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["request_vacation"]["back"]))).click()

    # vacation()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["vacation_status"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_status"]))).click()
    print("- Request status: Sort")
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_request"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["request_vacation"]["back"]))).click()
    print("- Request")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_status"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_processing"]))).click()
    print("- Processing")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_status"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_complete"]))).click()
    print("- Completed")
    time.sleep(5)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["vacation_information"]))).click()
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_vacation"]))).click()
    print("- Vacation_information: Sort")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["sort_vacation_other"]))).click()
    print("- Sort: Other")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["access_pages_vacation"]["my_vacation_status"]["filter"]))).click()
    print("- Filter")
    



def vacation():
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    # print("- Vacation")
    ''' Request vaction'''
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request"]))).click() 
    
    # title_request = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_vacation_text"])))
    # if title_request.text == 'Request vacation':
    #     print("=> Request vacation")
    # else:
    #     print("=> Crash app")
    #     exit(0)   
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["AM"]))).click()  
    print("- Select vacation type")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["calendar"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["select_calendar"]))).click()  
    time.sleep(2)

    ''' Crash app when select date '''
    try:
        title_request = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_vacation_text"])))
        if title_request.text == 'Request vacation':
            print("- Select date vacation")
        else:
            print("=> Crash app")
            exit(0)  
    except WebDriverException: 
        print("=> Crash app")
        exit(0)

    ''' Get data of vacation request '''
    vacation_date = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_date_text"])))
    vacation_text = vacation_date.text
    date_text = vacation_text.split(" ")[0]
    type_vacation = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["AM"])))
    type_text = type_vacation.text
    vacation_date_type = date_text + "(" + type_text + ")"

    driver.swipe(start_x=650, start_y=1844, end_x=650, end_y=355, duration=800)

    ''' Select CC '''
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["CC"]))).click()
    # WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()
    
    # ''' Send key "quynh" from keyboard mobile '''
    # driver.is_keyboard_shown()
    # driver.press_keycode(45)
    # driver.press_keycode(49)
    # driver.press_keycode(53)
    # driver.press_keycode(42)
    # driver.press_keycode(36)
    # driver.press_keycode(66)
    # print("- Search user")
    # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["save_cc"]))).click()
    # print("- Select CC")

    driver.swipe(start_x=650, start_y=1662, end_x=650, end_y=355, duration=800)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please enter your reason']"))).send_keys(data["vacation"]["my_vacation"]["input_test"])
    print("- Input reason")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["button_request"]))).click()
    
    '''- Check day request
      + If vacation day is saturday => fail, check again
      + If memo is empty => fail, check again'''
    try:
        fail = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_fail"])))
        if fail.text == 'request vacation failure':
            print("--- Request vacation failure - vacation day is saturday---")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["close_fail"]))).click()
            time.sleep(2)
            driver.swipe(start_x=650, start_y=355, end_x=650, end_y=2275, duration=800)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["calendar"]))).click()
            time.sleep(2)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["startdate_calendar"]))).click()
            print("=> Select start date")
            
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["enddate_calendar"]))).click()
            print("=> Select end date")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["select_calendar"]))).click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["button_request"]))).click() 
            print("=> Send request vacation")
        else:
            print("=> Request success")
    except WebDriverException:
        print("=> Request success") 

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["button_close"]))).click()

    time.sleep(20)

    ''' Name request vacation '''
    name = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["name_request"])))
    name_user = name.text
    name_user_request = "[ " + name_user + " ]"
    print(name_user_request)

    ''' View detail vacation '''
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["viewdetail"]))).click()
    print("=> View detail vacation")

    ''' Check vacation data '''
    print("*** Check vacation data")
    print("- Check vacation date")
    detail_vacationdate = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["detail_vacation_text"])))
    detail_vacationdate_text = detail_vacationdate.text
    if vacation_date_type == detail_vacationdate_text:
        print("=> Vacation date request is correct")
    else:
        print("=> Vacation date request is wrong")

    print("- Check reason have display")
    reason = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["reason_text"])))
    if reason.text == '-':
        print("=> Reason don't show")
    else:
        print("=> Reason have display")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["back"]))).click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["delete_vacation"]))).click()
    print("- Cancel request")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["OK_cancel_request"]))).click()
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["cancel_request_success"]))).click()
    print("=> Request cancel success")
    time.sleep(5)
    ''' Check vacation status '''
    vacation = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_name"])))
    vacation_text = vacation.text
    vacation_name_text_1 = vacation_text.split(" ")[0]
    # vacation_name_text_2 = vacation_text.split(" ")[1]
    # vacation_name_text = vacation_name_text_1 + " " + vacation_name_text_2
   
    vacation_schedule = str(" " + name_user_request + " " + type_text + " " + "(" + vacation_name_text_1 + ")" + " ")
    print(vacation_schedule)
    time.sleep(2)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["vacationschedule"]))).click()
        title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["vacation_schedule_title"])))
        if title.text == 'Vacation Schedule':
            print("** Vacation Schedule")
            schedule = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["schedule_name"])))
            a = schedule.text
            print(a)
            if a == vacation_schedule:
                print("=> Information of vacation have display")
            else:
                print("=> Request fail")
        else:
            print("=> Crash app")
            exit(0)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["request_vacation"]))).click()
        title_request = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["request_vacation_text"])))
        if title_request.text == 'Request vacation':
            print("=> Move to page request vacation not crash")
        else:
            print("=> Crash app")
            exit(0)
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["back_vacation"]))).click()

        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["vacationschedule"]))).click()
        title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_schedule"]["vacation_schedule_title"])))
        if title.text == 'Vacation Schedule':
            print("Turn back to page Vacation Schedule")
        else:
            print("=> Crash app")
            exit(0)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()

        vacation_title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_text"])))
        if vacation_title.text == 'Vacation':
            print("Turn back to page Vacation")
        else:
            print("=> Crash app")
            exit(0)
    except WebDriverException:
        print("=> Crash app")
        exit(0)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["view_cc"]["viewcc"]))).click()
        viewcc_title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["view_cc"]["viewcc_text"])))
        if viewcc_title.text == 'View CC':
            print("** View CC")
        else:
            print("=> Crash app")
            exit(0)

        detail_CC = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["view_cc"]["CC_detail"])))
        detail_CC_text = detail_CC.text
        if vacation_date_type == detail_CC_text:
            print("=> Vacation date request is correct")
        else:
            print("=> Vacation date request is wrong") 

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()  
    except WebDriverException:
        print("=> Crash app")
        exit(0)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_approve"]))).click()
        text_Approve = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_approve_text"])))
        if text_Approve.text == 'Vacation Approve':
            print("** Vacation Approve")
        else:
            print("=> Crash app")
            exit(0)

        try:
            request_vacation = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_request"])))
            if request_vacation.is_displayed():
                print("=> Check Page: Not crash")
            else:
                print("=> Crash app")
                exit(0)
        except WebDriverException:
            print("=> Crash app")
            exit(0)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["cancel_request"]))).click()
        time.sleep(3)
        try:
            request_vacation = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_request_cancel"])))
            if request_vacation.is_displayed():
                print("=> Check Page: Not crash")
            else:
                print("=> Crash app")
                exit(0)
        except WebDriverException:
            print("=> Crash app")
            exit(0)
    except WebDriverException:
        print("=> Crash app")
        exit(0)    

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_peruse"]))).click()
        title_peruser = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_peruse_text"])))
        if title_peruser.text == 'Vacations Per User':
            print("** Vacations Per User")
        else:
            print("=> Crash app")
            exit(0) 
    except WebDriverException:
        print("=> Crash app")
        exit(0)   

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["viewdetail"]))).click()
        title_vacation_information = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["title_vacation"])))
        if title_vacation_information.text == 'Vacation Information':
            print("=> Check Page: Not crash")
        else:
            print("=> Crash app")
            exit(0) 
    except WebDriverException:
        print("=> Crash app")
        exit(0)

def approve_request():
    '''
    --- User 1 ---
    1. Request vacation
    2. Send request to user 2
    Log out account user 1

    --- User 2 ---
    Log in to account user 2
    => Approve request

    --- User 1 ---
    Log in to account user 1
    => Check request vacation
    '''
    ''' Case of user 1 '''
    time.sleep(15)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    print("- Vacation")
    ''' Request vaction'''
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request"]))).click() 
    
    title_request = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_vacation_text"])))
    if title_request.text == 'Request vacation':
        print("=> Request vacation")
    else:
        print("=> Crash app")
        exit(0)   
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["AM"]))).click()  
    print("- Select vacation type")
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["calendar"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@index='1']//android.widget.Button[@index=16]"))).click()
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["select_calendar"]))).click()  
    time.sleep(2)

    ''' Crash app when select date '''
    try:
        title_request = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["request_vacation_text"])))
        if title_request.text == 'Request vacation':
            print("- Select date vacation")
        else:
            print("=> Crash app")
            exit(0)  
    except WebDriverException: 
        print("=> Crash app")
        exit(0)
    time.sleep(5)

    driver.swipe(start_x=650, start_y=1844, end_x=650, end_y=355, duration=800)

    ''' Select CC '''
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["CC"]))).click()
    # WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()
    
    # ''' Send key "quynh" from keyboard mobile '''
    # driver.is_keyboard_shown()
    # driver.press_keycode(45)
    # driver.press_keycode(49)
    # driver.press_keycode(53)
    # driver.press_keycode(42)
    # driver.press_keycode(36)
    # driver.press_keycode(66)
    # print("- Search user")
    # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["save_cc"]))).click()
    # print("- Select CC")

    driver.swipe(start_x=650, start_y=1662, end_x=650, end_y=355, duration=800)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please enter your reason']"))).send_keys(data["vacation"]["my_vacation"]["input_test"])
    print("- Input reason")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["button_request"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["button_close"]))).click()
    print("=> Send request vacation")
    time.sleep(5)

    print(" ")
    ''' Log out '''
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["setting_button"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["logout"]))).click()
    print("=> Change to user 2 to approve request")

    ''' Log in '''
    id_user2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["user_name"])))
    id_user2.clear()
    id_user2.send_keys(data["id_name_2"])
    print("- Input ID")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Password']")))
    driver.find_element_by_xpath(data["password"]).send_keys(data["pass_input"])
    print("- Input Password")
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Login')]")))
    driver.find_element_by_xpath(data["button_login"]).click()
    print("=> Click Log In button")
    driver.implicitly_wait(50)

    ''' Check request vacation of user 1 '''
    time.sleep(5)
    print("- Check request vacation")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_approve"]))).click()
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["search"]))).click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()
    
    ''' Send key "quynh" from keyboard mobile '''
    driver.is_keyboard_shown()
    driver.press_keycode(45)
    driver.press_keycode(49)
    driver.press_keycode(53)
    driver.press_keycode(42)
    driver.press_keycode(36)
    driver.press_keycode(66)
    print("- Search user")

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["select_user"]))).click()
    print("- Select user")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["approve"]))).click()
    print("- Approve request")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["accept_approve"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["close_popup"]))).click()
    print("=> Approve success")

    text_approve = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["approve_text"])))
    if text_approve.text == 'Approved':
        print("=> Request have approve success")
    else:
        print("=> Approve fail")

    ''' User cancel request '''
    print(" ")
    ''' Log out '''
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["setting_button"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["logout"]))).click()
    print("=> Change to user 1 - check request have been approve - cancel request")

    ''' Log in '''
    id_user2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["user_name"])))
    id_user2.clear()
    id_user2.send_keys(data["id_name"])
    print("- Input ID")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Password']")))
    driver.find_element_by_xpath(data["password"]).send_keys(data["pass_input"])
    print("- Input Password")
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Login')]")))
    driver.find_element_by_xpath(data["button_login"]).click()
    print("=> Click Log In button")
    driver.implicitly_wait(50)

    ''' Check request vacation of user 1 '''
    time.sleep(5)
    print("- Check request vacation")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_approve"]))).click()
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["search"]))).click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Please insert keyword to search']"))).click()
    
    ''' Send key "quynh" from keyboard mobile '''
    driver.is_keyboard_shown()
    driver.press_keycode(45)
    driver.press_keycode(49)
    driver.press_keycode(53)
    driver.press_keycode(42)
    driver.press_keycode(36)
    driver.press_keycode(66)
    print("- Search user")

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'quynh1')]"))).click()

    text_approve = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["approve_text"])))
    if text_approve.text == 'Approved':
        print("=> Request have approve success")
    else:
        print("=> Approve fail")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_status"]["vacationstatus"]))).click()
    time.sleep(10)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_status"]["cancel_request"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_status"]["button_ok"]))).click()
    print("- Cancel request")
    time.sleep(10)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["close_popup"]))).click()
    print("=> Approve cancel request success")
    time.sleep(5)

    text_cancel = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["my_vacation"]["vacation_status"]["text_request"])))
    if text_cancel.text == 'User cancel':
        print("=> Send cancel request success")
    else:
        print("=> Approve Arbitrary decision")

    print(" ")
    ''' Change to user 2 - approve cancel request'''
    ''' Log out '''
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["setting_button"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["logout"]))).click()
    print("=> Change to user 2 - approve cancel request")

    ''' Log in '''
    id_user2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["user_name"])))
    id_user2.clear()
    id_user2.send_keys(data["id_name_2"])
    print("- Input ID")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Password']")))
    driver.find_element_by_xpath(data["password"]).send_keys(data["pass_input"])
    print("- Input Password")
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Login')]")))
    driver.find_element_by_xpath(data["button_login"]).click()
    print("=> Click Log In button")
    driver.implicitly_wait(50)

    ''' Check request vacation of user 1 '''
    time.sleep(5)
    print("- Check request vacation")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["button_vacation"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["manage_processing"]["vacation_approve"]))).click()
    time.sleep(3)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["cancel_request"]))).click()
    print("- Click cancel request")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["status"]))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@text='Request']"))).click()
    print("- Select status request")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["request"]))).click()
    print("- Select request")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["approve_cancel"]))).click()
    print("- APPROVE CANCELLATION")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["accept_approve_cancel"]))).click()
    print("=> Cancel request")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["vacation"]["vacation_approve"]["close_popup"]))).click()









execution()

# clock_in_GPS()
# clock_in_Wifi()
# clock_in_Beacon()
# viewNoti()
# add_event()
# admin()
# break_time()
# clock_out()
# timecard()

# m = driver.page_source
# print(m)