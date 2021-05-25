import json
import re
from datetime import date
from argparse import ArgumentParser
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def writing_json_file(result_dict, output_file_name):
    """
    This function writes the dictionary to a json file

    :param result_dict:
    :param output_file_name:
    :return: None
    """
    json_data = json.dumps(result_dict)
    with open('{}.json'.format(output_file_name), "w", encoding="utf-8") as file:
        file.write(json_data)


def writing_xml_file(result_dict, output_file_name):
    """
    This function writes the dictionary to a xml file

    :param result_dict:
    :param output_file_name:
    :return: None
    """
    with open('{}.xml'.format(output_file_name), "w", encoding="utf-8") as xml_file:
        xml_file.write(str(result_dict))
    xml_file.close()


def query(request):
    try:
        result_dict = {}
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        cursor.execute(request)
        rows = cursor.fetchall()

        for row in rows:
            result_dict[row[0]] = row[1]
        return result_dict

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def insert_student_data(id_, name_, room_, sex_, birthday_):
    query = "INSERT INTO students(id, name, room, sex, birthday) " "VALUES(%s,%s,%s,%s,%s)"

    args = (id_, name_, room_, sex_, birthday_)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        cursor.execute(query, args)
        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def read_student_file(st_path):

    with open(st_path, 'r') as file:
        students = json.load(file)

        for student in students:

            temp = re.findall(r'\d{4}-\d{2}-\d{2}', student['birthday'])
            temp_lst = temp[0].split('-')
            list_of_ints = [int(n) for n in temp_lst]

            birthday = date(year=list_of_ints[0], month=list_of_ints[1], day=list_of_ints[2])
            id_ = student['id']
            name = student['name']
            room = student['room']
            sex = student['sex']

            insert_student_data(id_, name, room, sex, birthday)


def insert_room_data(id_, name_):
    query = "INSERT INTO rooms(id,name_room) " "VALUES(%s,%s)"

    args = (id_, name_)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()

    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def read_room_file(r_path):

    with open(r_path, 'r') as file:
        rooms = json.load(file)

        for room in rooms:
            insert_room_data(room['id'], room['name'])


def main():
    parser = ArgumentParser(description='MySQl task')
    parser.add_argument('-s', '--students', type=str, default='data/students.json', help='Path to students-file')
    parser.add_argument('-r', '--rooms', type=str, default='data/rooms.json', help='Path to rooms-file')
    parser.add_argument('-f', '--format', type=str, default='json', help='Format output file')

    args = parser.parse_args()

    try:
        if args.format.lower() == 'json' or args.format.lower() == 'xml':
            pass

        else:
            raise ValueError
    except ValueError:
        print('Invalid output file extension. Try again!')

    try:
        requests = [
            # 0 список комнат и количество студентов в каждой из них
            ("select room, count(id) as count from students group by room;"),

            # 1 top 5 комнат, где самые маленький средний возраст студентов
            (
                "select room as r, CEILING(avg(year(current_date)-year(birthday))) as age from students group by room order by age limit 5;"),

            # 2 top 5 комнат с самой большой разницей в возрасте студентов
            ("select rooms.name_room, max(year(current_date)-year(students.birthday)) - "
             "min(year(current_date)-year(students.birthday)) as result  "
             "from rooms inner join students "
             "on rooms.id =  students.room "
             "group by rooms.name_room order by result DESC limit 5;"),

            # 3 список комнат где живут разнополые студенты
            ("select * from rooms "
             "where rooms.id in (select room from students where sex = 'M'group by room) "
             "      and rooms.id in (select room from students where sex = 'F' group by room ) "
             "order by id; "),

        ]
        names_output_files = ['amount_st_in_room', 'avg_age', 'age_dif', 'sex_dif']

        read_room_file(args.rooms)
        read_student_file(args.students)

        for j, ind in enumerate(requests):
            result = query(ind)
            if args.format.lower() == 'json':
                writing_json_file(result, names_output_files[j])
            else:
                writing_xml_file(result,names_output_files[j])

    except Exception as exc:
        print('Try again!', exc)


if __name__ == '__main__':
    main()
