import re


class Version:
    def __init__(self, version):
        """
        The versions are reduced to a format of five numeric values separated by a dot.
        1.2.0.0.0
        The class returns a tuple.

        :param version: str
        :return tuple: ('*','*','*','*','*')
        """
        lst = version.split('.')
        version_lst = []

        for ind in lst:

            verbal_version = re.findall('[a-z]{1,5}', ind)

            if verbal_version != []:
                try:
                    temp_val = verbal_version[0]
                    if temp_val == 'a' or temp_val == 'alpha':
                        r = 0
                    elif temp_val == 'b' or temp_val == 'beta':
                        r = 1
                    elif temp_val == 'rc':
                        r = 2
                    elif temp_val == 'r':
                        r = 3
                    else:
                        raise ValueError
                except ValueError:
                    print('Undefined version')
                    break

                digital_version = re.findall('\d{1,5}', ind)
                if digital_version != []:
                    version_lst.append(digital_version[0])

                version_lst.append(r)

            else:
                version_lst.append(ind)

        while len(version_lst) < 5:
            version_lst.append('0')

        self.version = tuple(version_lst)

    def __le__(self, other):
        return self.version <= other.version

    def __ge__(self, other):
        return self.version >= other.version

    def __lt__(self, other):
        return self.version < other.version

    def __gt__(self, other):
        return self.version > other.version

    def __eq__(self, other):
        return self.version == other.version

    def __str__(self):
        return '.'.join(self.version)


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]


if __name__ == "__main__":
    main()
