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
               'Availability': 'A', 'Description': '', 'Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': 'no',
               'Face_to_Face': '', 'Blended': 'no', 'Remarks': '', 'Subject_Description_1': '', 'Subject_or_Unit_2': '',
               'Subject_Objective_2': '', 'Subject_Description_2': '','Subject_or_Unit_3': '', 'Subject_Objective_3': '',
               'Subject_Description_3': '',
               'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
               'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
               'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
               'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
               'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
               'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
               'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
               'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
               'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
               'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
               'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
               'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
               'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
               'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
               'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
               'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
               'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
               'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
               'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
               'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
               'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
               'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
               'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
               'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
               'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
               'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
               'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
               'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
               'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
               'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
               'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
               'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
               'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
               'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
               'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
               'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}

possible_cities = {'online': 'Online', 'mixed': 'Online', 'brisbane': 'Brisbane', 'sydney': 'Sydney',
                   'melbourne': 'Melbourne', 'perth': 'Perth', 'adelaide': 'Adelaide'}

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

    # CITY
    actual_cities.append('adelaide')

    # DURATION
    duration_div = soup.find('div', text=re.compile('duration', re.IGNORECASE))
    duration_h = soup.find('h3', text=re.compile('How long will it take to complete?', re.IGNORECASE))
    if duration_div:
        duration = duration_div.find_next_sibling('strong')
        if duration:
            duration_text = duration.get_text().lower()
            converted_duration = dura.convert_duration(duration_text)
            if converted_duration is not None:
                duration_l = list(converted_duration)
                if duration_l[0] == 1 and 'Years' in duration_l[1]:
                    duration_l[1] = 'Year'
                if duration_l[0] == 1 and 'Months' in duration_l[1]:
                    duration_l[1] = 'Month'
                course_data['Duration'] = duration_l[0]
                course_data['Duration_Time'] = duration_l[1]
                print('COURSE DURATION: ', str(duration_l[0]) + ' / ' + duration_l[1])
                actual_cities.append('online')
                course_data['Online'] = 'yes'
                course_data['Face_to_Face'] = 'no'
                course_data['Offline'] = 'no'
    elif '30-Day' in course_data['Course']:
        course_data['Duration'] = '1'
        course_data['Duration_Time'] = 'Month'
        print('COURSE DURATION: ', course_data['Duration'] + ' / ' + course_data['Duration_Time'])
        actual_cities.append('online')
        course_data['Online'] = 'yes'
        course_data['Face_to_Face'] = 'no'
        course_data['Offline'] = 'no'
    elif duration_h:
        duration = duration_h.find_next_sibling('p')
        if duration:
            duration_text = duration.get_text().lower()
            converted_duration = dura.convert_duration(duration_text)
            if converted_duration is not None:
                duration_l = list(converted_duration)
                if duration_l[0] == 1 and 'Years' in duration_l[1]:
                    duration_l[1] = 'Year'
                if duration_l[0] == 1 and 'Months' in duration_l[1]:
                    duration_l[1] = 'Month'
                course_data['Duration'] = duration_l[0]
                course_data['Duration_Time'] = duration_l[1]
                print('COURSE DURATION: ', str(duration_l[0]) + ' / ' + duration_l[1])
                course_data['Face_to_Face'] = 'yes'
                course_data['Offline'] = 'yes'
    # UNIT
    subject_list = soup.find_all('div', class_='accordion-sub accordion-level-2')
    i = 1
    if subject_list:
        for a in subject_list:
            name = a.find('a')
            if name:
                course_name = name.get_text()
                course_data['Subject_or_Unit_' + str(i)] = course_name
            i += 1




    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance',
                          'Face_to_Face', 'Blended', 'Remarks','Subject_or_Unit_1', 'Subject_Objective_1',
                          'Subject_Description_1',
                          'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                          'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                          'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                          'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                          'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                          'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                          'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                          'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                          'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                          'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                          'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                          'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                          'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                          'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                          'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                          'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                          'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                          'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                          'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                          'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                          'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                          'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                          'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                          'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                          'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                          'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                          'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                          'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                          'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                          'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                          'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                          'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                          'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                          'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                          'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                          'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                          'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                          'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                          'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('AIB_courses_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)
