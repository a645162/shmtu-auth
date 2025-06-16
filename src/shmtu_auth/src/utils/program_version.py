"""
程序版本管理模块

提供语义化版本控制支持，兼容Python 3.6+
支持 dataclass（Python 3.7+）或传统类定义的自动降级
"""

import re
from functools import total_ordering

# 类型注解支持，兼容旧版本
try:
    from typing import Any, Optional, Tuple, Union
except ImportError:
    # 为更老版本提供基本类型支持
    def Optional(x):
        return x

    def Tuple(*args):
        return tuple

    def Union(*args):
        return tuple(args)

    def Any():
        return object


# dataclass支持，兼容旧版本
HAS_DATACLASS = False
try:
    from dataclasses import dataclass, field

    HAS_DATACLASS = True
except ImportError:

    def dataclass(cls):
        return cls

    def field(**kwargs):
        return None


@total_ordering
class ProgramVersion:
    """
    程序版本类，支持语义化版本控制 (Semantic Versioning)

    支持格式：major.minor.patch[-prerelease]
    例如：1.0.0, 2.1.3, 1.0.0-alpha.1, 2.0.0-beta

    属性：
        major (int): 主版本号，不兼容的API修改
        minor (int): 次版本号，向后兼容的新功能
        patch (int): 补丁版本号，向后兼容的bug修复
        prerelease (Optional[str]): 预发布版本标识符

    示例：
        >>> v1 = ProgramVersion(1, 0, 0)
        >>> v2 = ProgramVersion(1, 0, 1)
        >>> v1 < v2
        True
        >>> str(v1)
        '1.0.0'
        >>> ProgramVersion.from_str('1.2.3-alpha')
        ProgramVersion(1, 2, 3, prerelease='alpha')
    """

    def __init__(self, major, minor, patch, prerelease=None):
        # type: (int, int, int, Optional[str]) -> None
        """
        初始化版本对象

        Args:
            major: 主版本号，必须是非负整数
            minor: 次版本号，必须是非负整数
            patch: 补丁版本号，必须是非负整数
            prerelease: 预发布版本标识符，可选

        Raises:
            ValueError: 当版本号格式无效时
            TypeError: 当参数类型不正确时
        """
        self._validate_params(major, minor, patch, prerelease)
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease

    @staticmethod
    def _validate_params(major, minor, patch, prerelease):
        # type: (int, int, int, Optional[str]) -> None
        """验证版本参数"""
        # 增强的参数验证
        if not all(isinstance(v, int) for v in (major, minor, patch)):
            raise TypeError("版本号必须是整数类型")

        if not all(v >= 0 for v in (major, minor, patch)):
            raise ValueError("版本号必须是非负整数")

        if prerelease is not None:
            if not isinstance(prerelease, str):
                raise TypeError("预发布版本标识符必须是字符串类型")
            if not prerelease.strip():
                raise ValueError("预发布版本标识符不能为空")
            # 增强的预发布版本格式验证
            if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]$|^[a-zA-Z0-9]$", prerelease):
                raise ValueError("预发布版本标识符格式无效，必须以字母或数字开头和结尾，中间可包含字母、数字、点号和连字符")

    def __str__(self):
        # type: () -> str
        """返回版本的字符串表示"""
        base = str(self.major) + "." + str(self.minor) + "." + str(self.patch)
        return base + "-" + self.prerelease if self.prerelease else base

    def __repr__(self):
        # type: () -> str
        """返回版本的详细字符串表示"""
        if self.prerelease:
            return (
                "ProgramVersion("
                + str(self.major)
                + ", "
                + str(self.minor)
                + ", "
                + str(self.patch)
                + ", prerelease='"
                + self.prerelease
                + "')"
            )
        return "ProgramVersion(" + str(self.major) + ", " + str(self.minor) + ", " + str(self.patch) + ")"

    def __eq__(self, other):
        # type: (Any) -> bool
        """版本相等性比较"""
        if not isinstance(other, ProgramVersion):
            return NotImplemented
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.prerelease == other.prerelease
        )

    def __ne__(self, other):
        # type: (Any) -> bool
        """版本不等性比较（Python 2 兼容性）"""
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        # type: (Any) -> bool
        """
        版本比较，遵循语义化版本控制规则
        预发布版本优先级低于正式版本

        使用元组比较优化性能
        """
        if not isinstance(other, ProgramVersion):
            return NotImplemented

        # 使用元组比较主版本号、次版本号、补丁版本号，性能更好
        self_tuple = (self.major, self.minor, self.patch)
        other_tuple = (other.major, other.minor, other.patch)

        if self_tuple != other_tuple:
            return self_tuple < other_tuple

        # 版本号相同时，比较预发布版本
        # 预发布版本排序规则：
        # 1. 正式版本 > 预发布版本
        # 2. 预发布版本之间按字典序比较
        if self.prerelease is None and other.prerelease is None:
            return False  # 完全相同
        elif self.prerelease is None:
            return False  # 正式版本 > 预发布版本
        elif other.prerelease is None:
            return True  # 预发布版本 < 正式版本
        else:
            # 预发布版本之间的比较
            return self.prerelease < other.prerelease

    def __hash__(self):
        # type: () -> int
        """支持在集合和字典中使用，与__eq__保持一致"""
        return hash((self.major, self.minor, self.patch, self.prerelease))

    @property
    def is_prerelease(self):
        # type: () -> bool
        """判断是否为预发布版本"""
        return self.prerelease is not None

    @property
    def base_version(self):
        # type: () -> ProgramVersion
        """获取基础版本（不包含预发布标识符）"""
        return ProgramVersion(self.major, self.minor, self.patch)

    @property
    def version_tuple(self):
        # type: () -> Tuple[int, int, int, str]
        """获取用于比较的版本元组"""
        return (self.major, self.minor, self.patch, self.prerelease or "")

    @classmethod
    def from_str(cls, version_str):
        # type: (str) -> Optional[ProgramVersion]
        """
        从字符串解析版本号，增强的错误处理和验证

        Args:
            version_str: 版本字符串，支持格式：
                - "1.2.3"
                - "v1.2.3"
                - "1.2.3-alpha"
                - "1.2.3-beta.1"
                - "1.2.3-rc.1"

        Returns:
            解析成功返回 ProgramVersion 对象，失败返回 None

        Example:
            >>> ProgramVersion.from_str("1.2.3")
            ProgramVersion(1, 2, 3)
            >>> ProgramVersion.from_str("v2.0.0-alpha.1")
            ProgramVersion(2, 0, 0, prerelease='alpha.1')
            >>> ProgramVersion.from_str("invalid")
            None
            >>> ProgramVersion.from_str("")
            None
        """
        # 类型和空值检查
        if not isinstance(version_str, str):
            return None

        # 清理输入字符串
        version_str = version_str.strip()
        if not version_str:
            return None

        # 移除可选的 'v' 或 'V' 前缀
        if version_str.lower().startswith("v"):
            version_str = version_str[1:].strip()
            if not version_str:
                return None

        # 更严格的版本号正则表达式
        # 支持：major.minor.patch[-prerelease]
        pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]|[a-zA-Z0-9]))?$"
        match = re.match(pattern, version_str)

        if not match:
            return None

        major_str, minor_str, patch_str, prerelease = match.groups()

        try:
            # 尝试转换为整数，检查溢出
            major = int(major_str)
            minor = int(minor_str)
            patch = int(patch_str)

            # 检查数值范围（防止过大的数字）
            if any(v < 0 or v > 999999 for v in (major, minor, patch)):
                return None

            # 使用构造函数进行额外验证
            return cls(major, minor, patch, prerelease)
        except (ValueError, TypeError, OverflowError):
            return None

    def bump_major(self):
        # type: () -> ProgramVersion
        """
        增加主版本号，重置次版本号和补丁版本号

        Returns:
            新的版本对象

        Example:
            >>> v = ProgramVersion(1, 2, 3)
            >>> v.bump_major()
            ProgramVersion(2, 0, 0)
        """
        return ProgramVersion(self.major + 1, 0, 0)

    def bump_minor(self):
        # type: () -> ProgramVersion
        """
        增加次版本号，重置补丁版本号

        Returns:
            新的版本对象

        Example:
            >>> v = ProgramVersion(1, 2, 3)
            >>> v.bump_minor()
            ProgramVersion(1, 3, 0)
        """
        return ProgramVersion(self.major, self.minor + 1, 0)

    def bump_patch(self):
        # type: () -> ProgramVersion
        """
        增加补丁版本号

        Returns:
            新的版本对象

        Example:
            >>> v = ProgramVersion(1, 2, 3)
            >>> v.bump_patch()
            ProgramVersion(1, 2, 4)
        """
        return ProgramVersion(self.major, self.minor, self.patch + 1)

    def with_prerelease(self, prerelease):
        # type: (str) -> ProgramVersion
        """
        创建带有预发布标识符的新版本

        Args:
            prerelease: 预发布版本标识符

        Returns:
            新的版本对象

        Raises:
            ValueError: 当预发布标识符格式无效时

        Example:
            >>> v = ProgramVersion(1, 2, 3)
            >>> v.with_prerelease('alpha')
            ProgramVersion(1, 2, 3, prerelease='alpha')
        """
        return ProgramVersion(self.major, self.minor, self.patch, prerelease)

    def without_prerelease(self):
        # type: () -> ProgramVersion
        """
        创建不带预发布标识符的新版本

        Returns:
            新的版本对象

        Example:
            >>> v = ProgramVersion(1, 2, 3, prerelease='alpha')
            >>> v.without_prerelease()
            ProgramVersion(1, 2, 3)
        """
        return ProgramVersion(self.major, self.minor, self.patch)

    def is_compatible_with(self, other):
        # type: (ProgramVersion) -> bool
        """
        检查是否与另一个版本兼容（主版本号相同）

        Args:
            other: 另一个版本对象

        Returns:
            如果主版本号相同则返回 True

        Raises:
            TypeError: 当参数不是 ProgramVersion 对象时

        Example:
            >>> v1 = ProgramVersion(1, 2, 3)
            >>> v2 = ProgramVersion(1, 3, 0)
            >>> v1.is_compatible_with(v2)
            True
            >>> v3 = ProgramVersion(2, 0, 0)
            >>> v1.is_compatible_with(v3)
            False
        """
        if not isinstance(other, ProgramVersion):
            raise TypeError("参数必须是 ProgramVersion 对象")
        return self.major == other.major

    def compare_to(self, other):
        # type: (ProgramVersion) -> int
        """
        与另一个版本进行比较

        Args:
            other: 另一个版本对象

        Returns:
            -1 如果 self < other
             0 如果 self == other
             1 如果 self > other

        Raises:
            TypeError: 当参数不是 ProgramVersion 对象时

        Example:
            >>> v1 = ProgramVersion(1, 0, 0)
            >>> v2 = ProgramVersion(1, 1, 0)
            >>> v1.compare_to(v2)
            -1
        """
        if not isinstance(other, ProgramVersion):
            raise TypeError("参数必须是 ProgramVersion 对象")

        if self < other:
            return -1
        elif self > other:
            return 1
        else:
            return 0

    # 工厂方法和便利函数
    @classmethod
    def parse(cls, version_str):
        # type: (str) -> ProgramVersion
        """
        从字符串解析版本号，解析失败时抛出异常

        Args:
            version_str: 版本字符串

        Returns:
            ProgramVersion 对象

        Raises:
            ValueError: 当版本字符串格式无效时

        Example:
            >>> ProgramVersion.parse("1.2.3")
            ProgramVersion(1, 2, 3)
            >>> ProgramVersion.parse("invalid")
            Traceback (most recent call last):
                ...
            ValueError: 无效的版本字符串格式: 'invalid'
        """
        result = cls.from_str(version_str)
        if result is None:
            raise ValueError("无效的版本字符串格式: '" + str(version_str) + "'")
        return result


if __name__ == "__main__":
    # 测试 ProgramVersion 类的功能
    print("=== ProgramVersion 测试 ===")

    # 测试基本版本号创建
    v1 = ProgramVersion(1, 2, 3)
    v2 = ProgramVersion(1, 2, 4)
    v3 = ProgramVersion(1, 3, 0)

    print("基本版本号创建:")
    print("v1 =", v1)
    print("v2 =", v2)
    print("v3 =", v3)
    print()

    # 测试预发布版本
    v4 = ProgramVersion(1, 2, 3, "alpha.1")
    v5 = ProgramVersion(1, 2, 3, "beta.1")
    v6 = ProgramVersion(1, 2, 3, "rc.1")

    print("预发布版本:")
    print("v4 =", v4)
    print("v5 =", v5)
    print("v6 =", v6)
    print()

    # 测试字符串解析
    print("字符串解析测试:")
    test_strings = [
        "1.0.0",
        "2.1.3",
        "1.0.0-alpha.1",
        "2.0.0-beta.2",
        "3.1.4-rc.1",
        "invalid.version",
        "1.2",
        "1.2.3.4",
    ]

    for version_str in test_strings:
        parsed = ProgramVersion.from_str(version_str)
        if parsed:
            print("  '" + version_str + "' -> " + str(parsed))
        else:
            print("  '" + version_str + "' -> 解析失败")
    print()

    # 测试版本比较
    print("版本比较测试:")
    comparison_tests = [
        (v1, v2),
        (v2, v1),
        (v1, v3),
        (v1, v4),  # 正式版本 vs 预发布版本
        (v4, v5),  # 预发布版本间比较
        (v5, v6),
        (v1, v1),  # 相等比较
    ]

    for va, vb in comparison_tests:
        print("  " + str(va) + " < " + str(vb) + ": " + str(va < vb))
        print("  " + str(va) + " > " + str(vb) + ": " + str(va > vb))
        print("  " + str(va) + " == " + str(vb) + ": " + str(va == vb))
        print()

    # 测试属性
    print("属性测试:")
    print("  v4.is_prerelease:", v4.is_prerelease)
    print("  v1.is_prerelease:", v1.is_prerelease)
    print("  v4.base_version:", v4.base_version)
    print("  v1.version_tuple:", v1.version_tuple)
    print("  v4.version_tuple:", v4.version_tuple)
    print()

    # 测试版本号自增
    print("版本号自增测试:")
    base_version = ProgramVersion(1, 2, 3)
    print("  原始版本:", base_version)
    print("  补丁版本自增:", base_version.bump_patch())
    print("  次版本自增:", base_version.bump_minor())
    print("  主版本自增:", base_version.bump_major())
    print()

    # 测试集合和字典功能（哈希支持）
    print("集合和字典测试:")
    version_set = {v1, v2, v1, v4}  # 重复的v1应该被去重
    print("  版本集合:", version_set)

    version_dict = {v1: "stable", v4: "alpha"}
    print("  版本字典:", version_dict)
    print()

    # 测试错误处理
    print("错误处理测试:")
    try:
        ProgramVersion.parse("invalid.version")
    except ValueError as e:
        print("  捕获到预期的错误:", e)

    try:
        invalid_version = ProgramVersion(-1, 0, 0)
        print("  应该失败但没有:", invalid_version)
    except ValueError as e:
        print("  捕获到预期的错误:", e)

    print("\n=== 测试完成 ===")
