import re
import os
import csv


with open(os.path.join(os.getcwd(), 'phonebook_raw.csv'), 'r', encoding="utf-8") as f:
    rows = csv.reader(f, delimiter =',')
    contact_lists = list(rows)

phonebook = []
phonebook_lst = []


def delete_commas():
    for i in contact_lists:
        list_i = list(filter(lambda x: x != '', i))
        phonebook_lst.append(list_i)


def separation_last_first_surname(phonebook_lst):
    lst1, lst2 = [], []
    for i in phonebook_lst:
        for j in range(2):
            lst1 = lst1 + (i[j].split(' '))
        lst1 = lst1 + (i[2:])
        lst2.append(lst1)
        lst1 =[]
    return lst2


def addition_without_repetitions(lst1, lst2):
    for i in lst2:
        if i not in lst1:
            lst1.append(i)
    return lst1


def joining_repeats(separation_last_first_surname):
    lst, k = [], 1
    for i in range(len(separation_last_first_surname)):
        for j in range(k, len(separation_last_first_surname)):
            if separation_last_first_surname[i][0:2] == \
                    separation_last_first_surname[j][0:2]:
                lst.append(addition_without_repetitions(separation_last_first_surname[i],
                                                    separation_last_first_surname[j]))
        k += 1
    return lst


def assembly_phonebook():
    global phonebook_lst
    lst1 = separation_last_first_surname(phonebook_lst)
    lst2 = joining_repeats(separation_last_first_surname(phonebook_lst))
    for i in joining_repeats(separation_last_first_surname(phonebook_lst)):
        for j in separation_last_first_surname(phonebook_lst):
            if i[0:2] == j[0:2]:
                lst1.remove(j)
    phonebook_lst = lst1+lst2
    return phonebook_lst


def regex_phone(number):
    pattern1 = r'\доб.'
    ext_number = re.findall(pattern1, number)
    if len(ext_number) != 0:
        pattern2 = r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2}).*?(\доб.(?= )).*?(\d+)'
        phone = re.match(pattern2, number)
        return '8' + '(' + phone.group(2) + ')'+phone.group(3)+'-'+phone.group(4)+'-'+phone.group(5)+\
           ' '+phone.group(6)+phone.group(7)
    else:
        pattern2 = r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})'
        phone = re.match(pattern2, number)
        return '8' + '(' + phone.group(2) + ')'+phone.group(3)+'-'+phone.group(4)+'-'+phone.group(5)


def phone_number_or_not(str):
    try:
        return regex_phone(str)
    except Exception:
        return str


def phone_or_email(str):
    phone = r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})'
    email = r'\@\w*\.'
    result_phone = re.findall(phone, str)
    result_email = re.findall(email, str)
    if len(result_phone) > 0:
        return 'its phone'
    elif len(result_email) > 0:
        return 'its email'


def correcting_phone_number():
    for i in range(len(phonebook_lst)):
        for j in range(len(phonebook_lst[i])):
            phonebook_lst[i][j] = phone_number_or_not(phonebook_lst[i][j])


def fix_incorrect_locations():
    for i in range(len(assembly_phonebook())):
        A = assembly_phonebook()[i][-2]
        B = assembly_phonebook()[i][-1]
        if phone_or_email(A) == 'its phone' and phone_or_email(B) != 'its email':
            assembly_phonebook()[i][-2] = B
            assembly_phonebook()[i][-1] = A
        elif phone_or_email(A) == 'its email' and phone_or_email(B) == 'its phone':
            assembly_phonebook()[i][-2] = B
            assembly_phonebook()[i][-1] = A


if __name__ == '__main__':
    delete_commas()
    correcting_phone_number()
    fix_incorrect_locations()

with open(os.path.join(os.getcwd(),  'phonebook_new.csv'),mode='w', newline='', encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(phonebook_lst)

