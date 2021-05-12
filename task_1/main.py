import json
from argparse import ArgumentParser


class Room(object):

    def __init__(self, room_number):
        self.room_number = room_number

    def create_students_list(self, student_file):
        """
        :input: path to student file
        :return: { self.room_number: [student_name_1, ... student_name_N ] }
        """

        with open(student_file, "r") as stud_file:
            students = json.load(stud_file)

            student_list = []
            room_students_dict = {}

            for line in students:

                if line['room'] == self.room_number:
                    student_list.append(line['name'])

            room_students_dict[self.room_number] = student_list

        return room_students_dict


def file_room_reading(rooms):
    """
    This function creates list of room numbers from rooms.json
    :param rooms: path to room-file
    :return: room_list: list of room numbers
    """

    room_list = []

    # reading json-file, creating a list of unique room numbers
    with open(rooms, "r") as room_file:
        room = json.load(room_file)

        for line in room:
            if line['id'] is not room_list:
                room_list.append(line['id'])

    return room_list


def creating_result_dict(room_list, student_file):
    """
    This function creates the resulting dictionary in the following format
        { room_number_1 : [name_1, ... name_N], ... room_number_N : [name_1, ... name_N] }

    :param room_list: list of room numbers
    :param student_file: path to students.json
    :return: result_dict:
    """
    # iterating through the list of rooms, creating class objects
    result_dict = {}
    for index in room_list:
        room = Room(index)
        students_list = room.create_students_list(student_file)

        result_dict.update(students_list)

    return result_dict


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


def main():
    parser = ArgumentParser(description='Rating of films')
    parser.add_argument('-s', '--students', type=str, default='students.json', help='Path to students-file')
    parser.add_argument('-r', '--rooms', type=str, default='rooms.json', help='Path to rooms-file')
    parser.add_argument('-f', '--format', type=str, default='json', help='Format output file')
    parser.add_argument('-res', '--result', type=str, default='result', help='Name output file. Enter the name of the resulting file without the extension')

    args = parser.parse_args()

    try:
        room_list = file_room_reading(args.rooms)
        room_student_dict = creating_result_dict(room_list, args.students)
        if args.format == 'json':
            writing_json_file(room_student_dict, args.result)
        elif args.format == 'xml':
            writing_xml_file(room_student_dict, args.result)

    except Exception as exc:
        print('Try again!', exc)


if __name__ == '__main__':
    main()
