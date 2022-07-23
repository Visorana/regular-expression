from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

new_contacts_list = []
for person in contacts_list:
    person_string = ','.join(person)
    name_pattern = r'^(\w*)(,| )(\w*)(,| )(\w*)(,| )'
    num_pattern = r'(\+7|8)( ||)(\(||)(\d{3})(\)|| )( |-||)(\d{3})(-|| )(\d{2})(-|| )(\d{2})'
    num_2_pattern = r'(\(|)(доб.)( ||)(\d{4})(\)|)'
    name = re.findall(name_pattern, person_string)
    count = name[0].count(' ')
    new_name_pattern = r'^(\w*)(,| )(\w*)(,| )(\w*)(,| )(,{' + str(count) + '})'
    new_num_pattern = r'+7(\4)\7-\9-\11'
    new_num_2_pattern = r'\2\4'
    person_string = re.sub(new_name_pattern, r'\1,\3,\5,', person_string)
    person_string = re.sub(num_pattern, new_num_pattern, person_string)
    person_string = re.sub(num_2_pattern, new_num_2_pattern, person_string)
    person_string = person_string.split(',')
    new_contacts_list.append(person_string)

keys = new_contacts_list[0]
contacts_list_1 = []
for person_1 in new_contacts_list:
    for person_2 in new_contacts_list:
        if person_1 != person_2 and person_1[0] + person_1[1] == person_2[0] + person_2[1]:
            dict_1 = dict(zip(keys, person_1))
            dict_2 = dict(zip(keys, person_2))
            for k, v in dict_1.items():
                if v == '':
                    dict_1[k] = dict_2[k]
            new_contacts_list.remove(person_1)
            new_contacts_list.remove(person_2)
            contacts_list_1.append(list(dict_1.values()))

for i in contacts_list_1:
    new_contacts_list.append(i)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)