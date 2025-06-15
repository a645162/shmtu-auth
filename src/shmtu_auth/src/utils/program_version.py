# -*- coding: utf-8 -*-


class ProgramVersion:
    """
    程序版本
    """

    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        if isinstance(other, ProgramVersion):
            return (
                self.major == other.major
                and self.minor == other.minor
                and self.patch == other.patch
            )
        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, ProgramVersion):
            if self.major < other.major:
                return True
            elif self.major == other.major:
                if self.minor < other.minor:
                    return True
                elif self.minor == other.minor:
                    if self.patch < other.patch:
                        return True
        return False

    def __gt__(self, other):
        if isinstance(other, ProgramVersion):
            if self.major > other.major:
                return True
            elif self.major == other.major:
                if self.minor > other.minor:
                    return True
                elif self.minor == other.minor:
                    if self.patch > other.patch:
                        return True
        return False

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    @staticmethod
    def from_str(version_str: str):
        """
        从字符串解析版本
        :param version_str: 版本字符串
        :return: 版本对象
        """
        version_str = version_str.replace("v", "").strip()

        if version_str == "":
            return None

        if version_str.count(".") != 2:
            return None

        spilt_list = version_str.split(".")
        if len(spilt_list) != 3:
            return None
        for i in spilt_list:
            if len(i) == 0 or not i.isdigit():
                return None

        major, minor, patch = map(int, version_str.split("."))
        return ProgramVersion(major, minor, patch)
