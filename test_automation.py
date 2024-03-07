from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from roles import data_roles
import openpyxl
import time
import re
import random
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter

"""
Macros to ENABLE the required features
"""
ENABLE_DEBUG_LOG = 0
SELECT_PRIMARY_SKILLS = 0
ANY_EXPERIENCE = 0
ANY_PAY = 0
DEFAULT_POS = 0
DEFAULT_NOTICE_PERIOD = 0
FLEXIBLE_LOCATION = 0
DEFAULT_WORK_LOCATION = 1

DELETE_TABLE = 0
OLD = 0

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
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

"""
# select add job for recruitment to create a Table
"""
def add_job_recruitment():
    try:
        # wait for the "Add" button to be clickable
        add_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-tabs-nav-add")))
        add_button.click()
    except TimeoutException:
        # if the "Add" button is not found within 10 seconds, wait for the "Add Job" button to be clickable
        try:
            add_job_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-tabs-nav-operations .ant-tabs-nav-add")))
            add_job_button.click()
        except TimeoutException:
            print("An unexpected error occurred while clicking the 'Add Job' button.")
    finally:
        # wait for the page to load
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-tabs-tab")))
        time.sleep(2)


"""
select add job role by entering the role
"""
def sel_job_role(role):
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
def set_primary_skills(skills,index):
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    requirement_body = requirement_ele.find_element_by_class_name("ant-card-body")

    if SELECT_PRIMARY_SKILLS:
        suggest_ele = requirement_body.find_element_by_id(f"rc-tabs-{index}-panel-1")
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

    # send the input to be searched (DATA is entered using JSON)
    if ENABLE_DEBUG_LOG:
        print(f"The json file has the following skills \n{skills}")
    for skill in skills[:6]:
        search_box.send_keys(skill)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        requirement_body.click()
        if ENABLE_DEBUG_LOG:
            print(skill)

"""
Function to add experience
"""
def add_exprience(index,i):
    if ANY_EXPERIENCE:
        # do nothing return
        # if ENABLE_DEBUG_LOG:
        print("Any experiance Switch is enabled")
        return
    else:
        time.sleep(3)
        requirement_ele = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-card.ant-card-bordered")))
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id(f"rc-tabs-{index}-tab-2")
        exp_tab.click()
        toggle_sw = driver.find_element_by_id(f"rc-tabs-{index}-panel-2")
        toggle= toggle_sw.find_element_by_class_name("ant-switch.ant-switch-small.css-1yjlpyq")#ant-switch ant-switch-small css-1yjlpyq ant-switch-checked
        toggle.click()


        min_exps = driver.find_elements_by_id(f"rc-tabs-{index}-panel-2")

        for min_exp in min_exps:
            comp_1 = min_exp.find_elements_by_class_name("ant-input-number.css-1yjlpyq.ant-input-number-borderless.requirement-exp-inputNum")
            set_min_exp = comp_1[0].find_element_by_xpath(".//input")
            set_min_exp.clear()

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)


            min = i+2
            set_min_exp.send_keys(str(min))

            set_min_exp.send_keys(Keys.ENTER)
            set_min_exp = comp_1[1].find_element_by_xpath(".//input")

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)


            max = i+4
            set_min_exp.send_keys(str(max))


            relevent_exps = driver.find_elements_by_id(f"rc-tabs-{index}-panel-2")

            for relevent_exp in relevent_exps:
                comp_1 = relevent_exp.find_elements_by_class_name("ant-segmented.exp-segment.css-1dny6fm")# ant-segmented exp-segment css-1yjlpyq 1dny6fm

                for comp in comp_1:
                    set_num_pos = comp.find_elements_by_css_selector(".ant-segmented-item")
                    set_num_pos[2].click()
        time.sleep(2)


def add_kasu(index,i):
    if ANY_PAY:
        # do Nothing and return
        print("Any pay switch is Enabled")
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id(f"rc-tabs-{index}-tab-4")
        exp_tab.click()

        toggle_sw = driver.find_element_by_id(f"rc-tabs-{index}-panel-4")
        toggle = toggle_sw.find_element_by_class_name("ant-switch.ant-switch-small.css-1yjlpyq.ant-switch-checked")
        toggle.click()
        time.sleep(2)

        min_exps = driver.find_elements_by_id(f"rc-tabs-{index}-panel-4")

        for min_exp in min_exps:

            comp_1 = min_exp.find_elements_by_class_name("ant-input-number-input-wrap")#TODO Input has to be automated
            set_min_exp = comp_1[0].find_element_by_xpath(".//input")
            set_min_exp.clear()

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)

            min_kasu = i+2
            set_min_exp.send_keys(str(min_kasu))

            set_min_exp.send_keys(Keys.ENTER)
            set_min_exp = comp_1[1].find_element_by_xpath(".//input")

            set_min_exp.send_keys(Keys.CONTROL, 'a')
            set_min_exp.send_keys(Keys.BACK_SPACE)

            max_kasu = i+4
            set_min_exp.send_keys(str(max_kasu))

def add_positions(index,i):
    if DEFAULT_POS:
        # Do nothing and return [Default position is 1]
        if ENABLE_DEBUG_LOG:
            print("Default position is set" )
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id(f"rc-tabs-{index}-tab-5")
        exp_tab.click()
        time.sleep(2)

        min_exps = driver.find_elements_by_id(f"rc-tabs-{index}-panel-5")

        for min_exp in min_exps:
            comp_1 = min_exp.find_elements_by_class_name("ant-segmented.exp-segment.css-1dny6fm")#ant-segmented exp-segment css-1dny6fm 13a5vx0


            for comp in comp_1:
                set_num_pos = comp.find_elements_by_css_selector(".ant-segmented-item")
                set_num_pos[i].click()
                time.sleep(3)


def add_notice_period(index,i):
    # Click on the side tab to enter notice period
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
    exp_tab = sel_exp.find_element_by_id(f"rc-tabs-{index}-tab-6")
    exp_tab.click()
    time.sleep(2)

    if DEFAULT_NOTICE_PERIOD:
        #do nothing and return
        if ENABLE_DEBUG_LOG:
            print("The Default notice period is set for 90 days")
    else:
        notice_period_eles = driver.find_elements_by_id(f"rc-tabs-{index}-panel-6")

        for notice_period_ele in notice_period_eles:
            notice_periods = notice_period_ele.find_elements_by_class_name("ant-segmented.exp-segment.css-1dny6fm")# ant-segmented exp-segment css-1dny6fm

            for notice_period in notice_periods:
                set_num_pos = notice_period.find_elements_by_css_selector(".ant-segmented-item")
                set_num_pos[i].click()

def add_location(index):
    if FLEXIBLE_LOCATION:
        #do nothing and return
        print("The Default notice period is set for 90 days")
        return
    else:
        requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
        sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
        exp_tab = sel_exp.find_element_by_id(f"rc-tabs-{index}-tab-7")
        exp_tab.click()
        time.sleep(2)
        #
        loc_tick_box = driver.find_elements_by_id(f"rc-tabs-{index}-panel-7")
        un_tick = loc_tick_box[0].find_element_by_class_name("ant-checkbox.ant-wave-target.css-1yjlpyq.ant-checkbox-checked")#ant-checkbox ant-wave-target css [16s6j8 1yjlpyq]
        un_tick.click()
        time.sleep(2)

        requirement_body = driver.find_element_by_class_name("ant-card-body")
        search_boxes = requirement_body.find_elements_by_css_selector(".ant-select-selection-search-input")
        search_box = search_boxes[2]
        # search_box.click()
        search_box.send_keys("Hyderabad")
        search_box.send_keys(Keys.ENTER)#ant-selebiggworksct-selection-search-mirror
        time.sleep(3)
        search_box.send_keys("Chennai")
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)#ant-selebiggworksct-selection-search-mirror
        exp_tab.click()
        time.sleep(3)

        # The work location to be selected
        if DEFAULT_WORK_LOCATION:
            if ENABLE_DEBUG_LOG:
                # Do nothing and return
                print("Default work location is selected\n")
            return
        else:
            work_loc = driver.find_elements_by_id(f"rc-tabs-{index}-panel-7")
            # Iterate over the elements in the toggle list and perform the desired action on each element
            for element in work_loc: #toggle:
                sel_all = element.find_elements_by_class_name("ant-checkbox.ant-wave-target.css-16s6j8")
                sel_all[1].click()#untick default
                sel_all[2].click()

def job_discription(index):
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    sel_exp = requirement_ele.find_element_by_class_name("ant-tabs-nav-list")
    exp_tab = sel_exp.find_element_by_id(f"rc-tabs-{index}-tab-8")
    exp_tab.click()
    time.sleep(2)

    data_box = driver.find_element_by_id(f"rc-tabs-{index}-panel-8")
    data_box_ele = data_box.find_elements_by_class_name("ql-editor.ql-blank")
    text_box_1 = data_box_ele[0]
    text_box_2 = data_box_ele[1]
    text_box_3 = data_box_ele[2]
    #enter the job Description
    text_box_1.send_keys("note1")
    text_box_2.send_keys("note2")
    text_box_3.send_keys("note3")

#function for debug
def check_candidate_on_list():
    wait = WebDriverWait(driver, 20)
    candidate = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-menu.ant-menu-root.ant-menu-inline.ant-menu-light.css-1bkj34a")))
    click_unlocks = candidate.find_elements_by_class_name("ant-typography.table-main-text.css-1bkj34a")

    for click_unlock in click_unlocks:
        wait.until(EC.element_to_be_clickable((By.XPATH, f"(.//*[contains(@class, 'ant-typography') and contains(@class, 'table-main-text') and contains(@class, 'css-1bkj34a')])[{click_unlocks.index(click_unlock) + 1}]")))
        click_unlock.click()
        time.sleep(3)



ind = 1
def save():
        save = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-card.ant-card-bordered.requirement-modal.css-bcvueg")))
        save_btn = save.find_element_by_class_name("ant-btn.css-bcvueg.ant-btn-primary.ant-btn-sm")
        save_btn.click()
        time.sleep(3)
        try:
            notification = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-notification-notice-message")))
        except:
            print("The saved notification pop-up ")
index = 1

# To delete the created table
def delete_table():
        index = 2
        for i in range(20):

            time.sleep(5)
            delete_job_block = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-tabs.ant-tabs-top.ant-tabs-editable.ant-tabs-card.ant-tabs-editable-card.tabs-in-tables.css-bcvueg")))
            delete_job_eles = delete_job_block.find_elements_by_class_name("ant-tabs-tab")
            delete_job_eles[index].click()
            time.sleep(2)

            # #click delete on dropdown window
            parent_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ant-tabs-tab.ant-tabs-tab-active")))
            svg_element = parent_element.find_element_by_css_selector("svg.ant-dropdown-trigger.iconify.iconify--fluent")
            svg_element.click()
            time.sleep(2)
            delete_butt = driver.find_element_by_xpath("//span[contains(@class, 'ant-typography') and contains(., 'Delete')]")
            delete_butt.click()
            time.sleep(5)
            # #delete confirmation
            confirm_del_window_ele = driver.find_element_by_class_name("ant-modal.css-bcvueg")
            del_comfirm = confirm_del_window_ele.find_element(By.CLASS_NAME, "ant-btn.css-bcvueg.ant-btn-primary.ant-btn-sm.ant-btn-dangerous")
            del_comfirm.click()
            time.sleep(2)
            driver.refresh()
            time.sleep(5)


#primary skills role p1
def generate_random_skill(skills,index,i):
    requirement_ele = driver.find_element_by_class_name("ant-card.ant-card-bordered")
    requirement_body = requirement_ele.find_element_by_class_name("ant-card-body")

    if SELECT_PRIMARY_SKILLS:
        suggest_ele = requirement_body.find_element_by_id(f"rc-tabs-{index}-panel-1")
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

    # send the input to be searched (DATA is entered using JSON)
    if ENABLE_DEBUG_LOG:
        print(f"The json file has the following skills \n{skills}")
    # Select a random skill from the list of skills
    for skill in list(skills)[i:(i+6)]:
        # random_skill = random.choice(skills)
        # If the random skill is selected, print a message

        if ENABLE_DEBUG_LOG:
                print(f"Selected random skill: {skill}")
        try:
            search_box.send_keys(skill)
            time.sleep(3)
            search_box.send_keys(Keys.ENTER)
            requirement_body.click()
        except:
            print(f"didnt find the skill ={skill}")
        time.sleep(2)
        if ENABLE_DEBUG_LOG:
            print(skill)




time.sleep(9)

if DELETE_TABLE:
        delete_table()

else :
    #Implemented at the begining dont know to keep it or delete
    if OLD:
        for data in data_roles:

            roles = data.get('Roles ')
            skills = data.get('Primary skills ').split(',')
            add_job_recruitment()
            sel_job_role(roles)
            set_primary_skills(skills,index)
            add_exprience(index)
            add_kasu(index)
            add_positions(index)
            add_notice_period(index)
            add_location(index)
            job_discription(index)
            save()
            time.sleep(7)
            print(f"table {index} CREATED")
            index += 1
            # check_candidate_on_list()

        # except:
        #     driver.quit()

    for data in data_roles:
            for iteration in range(5):
                i= iteration
                roles = data.get('Roles ')
                skills = data.get('Primary skills ').split(',')
                add_job_recruitment()
                sel_job_role(roles)
                generate_random_skill(skills,index,i)
                add_exprience(index,i)
                add_kasu(index,i)
                add_positions(index,i)
                add_notice_period(index,i)
                add_location(index)
                # job_discription(index)
                save()
                time.sleep(2)
                index+=1
                print(f"{roles} = {iteration}")



