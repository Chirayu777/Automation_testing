from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl
import time
import re
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter

"""
Macros to ENABLE the required features
"""
ENABLE_DEBUG_LOG = 0
SELECT_PRIMARY_SKILLS = 1
ANY_EXPERIENCE = 0
ANY_PAY = 0
DEFAULT_POS = 1
DEFAULT_NOTICE_PERIOD = 1
FLEXIBLE_LOCATION = 0
DEFAULT_WORK_LOCATION = 1


"""
Private macros
"""
PRIMARY_SKILLS = 2





# select and install webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(r"--user-data-dir=/home/vithamas/.config/google-chrome/Default/Profile 1")
chrome_options.add_argument(r"--profile-directory=Profile 1")  # Replace 'Profile 1' with your actual profile directory name if needed

# Instantiate Chrome WebDriver with Chrome options
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver.get('https://app.kalibre.ai/candidates')
# wait for driver to complete loading
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

"""
# select add job for recruitment to create a Table
"""
def add_job_recruitment():
    add_job = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-tabs-nav-add")))
    add_job.click()
    time.sleep(1)

"""
select add job role by entering the role
"""
def sel_job_role():
    role  = "React"
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    requirement_body = requirement_ele.find_element_by_class_name("ant-card-body")
    search_box = requirement_body.find_element_by_class_name("ant-select-selection-search-input ")
    search_box.send_keys(role)
    search_box.send_keys(Keys.ENTER)
    get_search_box = requirement_body.find_element_by_class_name("ant-select-selection-item")
    time.sleep(1)
    if ENABLE_DEBUG_LOG:
        # verify the role is entered matches the entered role
        #
        role_data = get_search_box.get_attribute("title")
        print(role_data)
        try:
            if role_data == "React Developer":
                print("roles successfully updated")
                return role_data
        except:
            print("role not succesfully entered")


'''
select set the primary skill
'''
def set_primary_skills():
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    requirement_body = requirement_ele.find_element_by_class_name("ant-card-body")

    if SELECT_PRIMARY_SKILLS:
        suggest_ele = requirement_body.find_element_by_id("rc-tabs-1-panel-1")
        ant_space_class = suggest_ele.find_elements_by_class_name("ant-space.css-16s6j8.ant-space-horizontal.ant-space-align-center.ant-space-gap-row-small.ant-space-gap-col-small")
        items = ant_space_class[PRIMARY_SKILLS].find_elements_by_class_name("ant-space-item")
        pattern = re.compile(r'\b(?:Clear|Cancel|Save)\b')

        # Iterate over each item
        for item in items:
            # Check if the text matches the pattern
            if not pattern.search(item.text):
                # If no match is found, print the text
                if ENABLE_DEBUG_LOG:
                    print(item.text)
                item.click()

    # find search box to select primary skill
    search_boxes = requirement_body.find_elements_by_css_selector(".ant-select-selection-search-input")
    search_box = search_boxes[1]

    # send the input to be searched (manually entered for now) #
    search_box.send_keys("ang")
    search_box.send_keys(Keys.ENTER)
    requirement_body.click()
    time.sleep(1)

    if ENABLE_DEBUG_LOG:
        #verify the skill matches with the entered skill
        verify_skill_ele = driver.find_element_by_class_name("ant-select.ant-select-lg.ant-select-outlined.css-k8v0t7.ant-select-multiple.ant-select-allow-clear.ant-select-show-arrow.ant-select-show-search")
        verify_skill = verify_skill_ele.find_element_by_class_name("ant-select-selection-item")
        primary_skill_data = verify_skill.get_attribute("title")

        #verify the primary skill data is entered correctly

        print(primary_skill_data)
        try:
            if primary_skill_data == "AngularJS":
                print("primary skill updated successfully")
                return primary_skill_data
        except:
            print("primary skill not succesfully entered")

"""
Function to add experience
"""
def add_exprience():
    if ANY_EXPERIENCE:
        # do nothing return
        # if ENABLE_DEBUG_LOG:
        print("Any experiance Switch is enabled")
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id("rc-tabs-1-tab-2")
        exp_tab.click()
        toggle_sw = driver.find_element_by_id("rc-tabs-1-panel-2")
        toggle= toggle_sw.find_element_by_class_name("ant-switch.ant-switch-small.css-16s6j8")
        toggle.click()


        min_exps = driver.find_elements_by_id("rc-tabs-1-panel-2")

        for min_exp in min_exps:
            comp_1 = min_exp.find_elements_by_class_name("ant-input-number.css-16s6j8.ant-input-number-borderless.requirement-exp-inputNum")
            set_min_exp = comp_1[0].find_element_by_xpath(".//input")
            set_min_exp.clear()

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)
            set_min_exp.send_keys("6")

            set_min_exp.send_keys(Keys.ENTER)
            set_min_exp = comp_1[1].find_element_by_xpath(".//input")

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)
            set_min_exp.send_keys("9")
            relevent_exps = driver.find_elements_by_id("rc-tabs-1-panel-2")

            for relevent_exp in relevent_exps:
                comp_1 = relevent_exp.find_elements_by_class_name("ant-segmented.exp-segment.css-13a5vx0")

                for comp in comp_1:
                    set_num_pos = comp.find_elements_by_css_selector(".ant-segmented-item")
                    set_num_pos[4].click()
        time.sleep(2)


def add_kasu():
    if ANY_PAY:
        # do Nothing and return
        print("Any pay switch is Enabled")
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id("rc-tabs-1-tab-4")
        exp_tab.click()

        toggle_sw = driver.find_element_by_id("rc-tabs-1-panel-4")
        # toggle= toggle_sw.find_element_by_class_name("ant-switch.ant-switch-small.css-k8v0t7")
        toggle = toggle_sw.find_element_by_class_name("ant-switch.ant-switch-small.css-16s6j8.ant-switch-checked")
        toggle.click()
        time.sleep(2)

        min_exps = driver.find_elements_by_id("rc-tabs-1-panel-4")

        for min_exp in min_exps:

            comp_1 = min_exp.find_elements_by_class_name("ant-input-number-input-wrap")#TODO Input has to be automated
            set_min_exp = comp_1[0].find_element_by_xpath(".//input")
            set_min_exp.clear()

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)
            set_min_exp.send_keys("6")

            set_min_exp.send_keys(Keys.ENTER)
            set_min_exp = comp_1[1].find_element_by_xpath(".//input")

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)
            set_min_exp.send_keys("9")

def add_positions():
    if DEFAULT_POS:
        # Do nothing and return [Default position is 1]
        if ENABLE_DEBUG_LOG:
            print("Default position is set" )
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id("rc-tabs-1-tab-5")
        exp_tab.click()
        time.sleep(2)

        min_exps = driver.find_elements_by_id("rc-tabs-1-panel-5")

        for min_exp in min_exps:
            comp_1 = min_exp.find_elements_by_class_name("ant-segmented.exp-segment.css-13a5vx0")


            for comp in comp_1:
                set_num_pos = comp.find_elements_by_css_selector(".ant-segmented-item")
                set_num_pos[4].click()


def add_notice_period():
    # Click on the side tab to enter notice period
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
    exp_tab = sel_exp.find_element_by_id("rc-tabs-1-tab-6")
    exp_tab.click()
    time.sleep(2)

    if DEFAULT_NOTICE_PERIOD:
        #do nothing and return
        print("The Default notice period is set for 90 days")
    else:
        notice_period_eles = driver.find_elements_by_id("rc-tabs-1-panel-6")

        for notice_period_ele in notice_period_eles:
            notice_periods = notice_period_ele.find_elements_by_class_name("ant-segmented.exp-segment.css-13a5vx0")

            for notice_period in notice_periods:
                set_num_pos = notice_period.find_elements_by_css_selector(".ant-segmented-item")
                set_num_pos[4].click()

def add_location():
    if FLEXIBLE_LOCATION:
        #do nothing and return
        print("The Default notice period is set for 90 days")
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id("rc-tabs-1-tab-7")
        exp_tab.click()
        time.sleep(2)
        #
        loc_tick_box = driver.find_elements_by_id("rc-tabs-1-panel-7")
        un_tick = loc_tick_box[0].find_element_by_class_name("ant-checkbox.ant-wave-target.css-16s6j8.ant-checkbox-checked")
        un_tick.click()
        time.sleep(2)

        requirement_body = driver.find_element_by_class_name("ant-card-body")
        search_boxes = requirement_body.find_elements_by_css_selector(".ant-select-selection-search-input")
        search_box = search_boxes[2]
        # search_box.click()
        search_box.send_keys("mysuru")# TODO automate the inputs

        search_box.send_keys(Keys.ENTER)#ant-select-selection-search-mirror
        exp_tab.click()
        time.sleep(3)

        # The work location to be selected
        if DEFAULT_WORK_LOCATION:
            # Do nothing and return
            print("Default work location is selected")
            return
        else:
            work_loc = driver.find_elements_by_id("rc-tabs-1-panel-7")
            # Iterate over the elements in the toggle list and perform the desired action on each element
            for element in work_loc: #toggle:
                sel_all = element.find_elements_by_class_name("ant-checkbox.ant-wave-target.css-16s6j8")
                sel_all[1].click()#untick default
                sel_all[2].click()

def job_discription():
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
    exp_tab = sel_exp.find_element_by_id("rc-tabs-1-tab-8")
    exp_tab.click()
    time.sleep(2)

    data_box = driver.find_element_by_id("rc-tabs-1-panel-8")
    data_box_ele = data_box.find_elements_by_class_name("ql-editor.ql-blank")
    text_box_1 = data_box_ele[0]
    text_box_2 = data_box_ele[1]
    text_box_3 = data_box_ele[2]
    #enter the job Description
    text_box_1.send_keys("note1")
    text_box_2.send_keys("note2")
    text_box_3.send_keys("note3")

def save():
    save = driver.find_element_by_class_name("ant-card.ant-card-bordered.requirement-modal.css-ozaxbp")
    save_btn = save.find_element_by_class_name("ant-btn.css-ozaxbp.ant-btn-primary.ant-btn-sm")
    save_btn.click()

add_job_recruitment()
# time.sleep(2)
sel_job_role()
# time.sleep(2)
set_primary_skills()
# driver.quit()
# time.sleep(2)
add_exprience()
# time.sleep(2)
add_kasu()
# time.sleep(2)
add_positions()
# time.sleep(2)
add_notice_period()
# time.sleep(2)
add_location()
# time.sleep(2)
job_discription()
# time.sleep(2)
save()
