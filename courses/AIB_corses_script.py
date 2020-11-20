"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 20-11-20
    * description:This script extracts the corresponding undergraduate courses details and tabulate it.
"""

import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from CustomMethods import DurationConverter as dura

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/AIB_courses_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/AIB_courses.csv'

course_data = {'Level_Code': '', 'University': 'Australian Institute of Business', 'City': '',
               'Country': 'Australia', 'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD',
               'Currency_Time': 'year', 'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
               'Prerequisite_1': '', 'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '',
               'Prerequisite_2_grade': '6.5', 'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '',
               'Availability': 'A', 'Description': '','Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': '',
               'Face_to_Face': '', 'Blended': '', 'Remarks': ''}

possible_cities = {
                   'online': 'Online', 'mixed': 'Online', 'brisbane': 'Brisbane', 'sydney': 'Sydney',
                   'melbourne': 'Melbourne', 'perth': 'Perth'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []
    remarks_list = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE
    title = soup.find('h1')
    if title:
        course_data['Course'] = title.get_text()
        print('COURSE TITLE: ', title.get_text())

        # DECIDE THE LEVEL CODE
        for i in level_key:
            for j in level_key[i]:
                if j in course_data['Course']:
                    course_data['Level_Code'] = i
        print('COURSE LEVEL CODE: ', course_data['Level_Code'])

        # DECIDE THE FACULTY
        for i in faculty_key:
            for j in faculty_key[i]:
                if j.lower() in course_data['Course'].lower():
                    course_data['Faculty'] = i
        print('COURSE FACULTY: ', course_data['Faculty'])

        # COURSE LANGUAGE
        for language in possible_languages:
            if language in course_data['Course']:
                course_data['Course_Lang'] = language
            else:
                course_data['Course_Lang'] = 'English'
        print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # DESCRIPTION
    desc_block = soup.find('div', attrs={"id": "block1"})
    desc_block_1 = soup.find('div', attrs={"id": "tag-overview"})
    desc_ = soup.find('p', class_='intro')
    if desc_block:
        desc_container = desc_block.find('div', class_='container')
        if desc_container:
            desc_p = desc_container.find('p')
            if desc_p:
                desc = desc_p.get_text().strip()
                course_data['Description'] = desc
                print('COURSE DESCRIPTION: ', desc)
    elif desc_:
        desc = desc_.get_text().strip()
        course_data['Description'] = desc
        print('COURSE DESCRIPTION: ', desc)
    elif desc_block_1:
        desc_container = desc_block_1.find('div', class_='container')
        if desc_container:
            desc_p = desc_container.find('p')
            if desc_p:
                desc = desc_p.get_text().strip()
                course_data['Description'] = desc
                print('COURSE DESCRIPTION: ', desc)

    # FEES
    fee_a_tag = soup.find('a', text=re.compile('CALCULATE THE IMPACT OF FEE-HELP ON YOUR INCOME', re.IGNORECASE))
    fee_p_tag = soup.find('p', text=re.compile(r'Total Upfront Cost \(2020\)',re.IGNORECASE ))
    if fee_a_tag:
        fee_p = fee_a_tag.find_previous_sibling('p')
        if fee_p:
            fee = re.search(r'\d+,\d+', fee_p.get_text())
            if fee is not None:
                course_data['Local_Fees'] = fee.group()
                print('LOCAL FEES: ', fee.group())
    elif fee_p_tag:
        fee_h = fee_p_tag.find_previous_sibling('h3')
        if fee_h:
            fee = re.search(r'\d+,\d+', fee_h.get_text())
            if fee is not None:
                course_data['Local_Fees'] = fee.group()
                print('LOCAL FEES: ', fee.group())