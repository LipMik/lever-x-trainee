import json
from argparse import ArgumentParser


class Room:

    isinstances = {}

    def __init__(self, room_number):
        self.room_number = room_number
        self.students = {self.room_number: []}
        self.isinstances[room_number] = self

    def appending_st_to_room(self, name):
        self.students[self.room_number].append(name)

        return self.students


def reading_room_file(r_file):
    """
    This function creates list of room numbers from rooms.json
    :param r_file: path to room-file

    :return: room_list: list of room numbers
    """
    room_list = []

    with open(r_file, 'r') as file:
        rooms = json.load(file)

        for line in rooms:
            room_list.append(line['id'])

    return room_list


def creating_result(room_list, stud_file_path):
    """
    This function reads student file line by line and creates instances of Room class

    :param room_list: list of room number from room.json
    :param stud_file_path: path to student.json
    :return: result_dict : { room_number : [name1, ... name_N ]}
    """

    result_dict = {}

    with open(stud_file_path, 'r') as st_file:
        students = json.load(st_file)
        created_instances = []

        for line in students:

            if (line['room'] in created_instances) and (line['room'] in room_list):
                room = Room.isinstances[line['room']]
                student = room.appending_st_to_room(line['name'])
                result_dict[room.room_number] = student[room.room_number]

            elif line['room'] in room_list:
                room = Room(line['room'])
                created_instances.append(line['room'])
                student = room.appending_st_to_room(line['name'])
                result_dict[room.room_number] = student[room.room_number]

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
        file.close()


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
    parser = ArgumentParser(description='Reading students.json and room.json')
    parser.add_argument('-s', '--students', type=str, default='data/students.json', help='Path to students-file')
    parser.add_argument('-r', '--rooms', type=str, default='data/rooms.json', help='Path to rooms-file')
    parser.add_argument('-f', '--format', type=str, default='json', help='Format output file')
    parser.add_argument('-res', '--result', type=str, default='result', help='Name output file. Enter the name of the resulting file without the extension')

    args = parser.parse_args()

    try:
        if args.format.lower() == 'json' or args.format.lower() == 'xml':
            pass

        else:
            raise ValueError
    except ValueError:
        print('Invalid output file extension. Try again!')

    try:
        room_list = reading_room_file(args.rooms)
        result = creating_result(room_list, args.students)
    except Exception as exc:
        print('Incorrect path', exc)

    try:
        if args.format.lower() == 'json':
            writing_json_file(result, args.result)
        elif args.format.lower() == 'xml':
            writing_xml_file(result, args.result)

    except Exception as exc:
        print('Try again!', exc)


if __name__ == '__main__':
    main()
