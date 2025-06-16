#!/usr/bin/env python
"""
测试 ProgramVersion 在不同Python版本中的兼容性
支持pytest运行，提供全面的测试覆盖

Windows PowerShell运行示例:
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py -v
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py -k "test_basic"
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py::TestVersionComparison -v
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py -m "not slow"

Linux/macOS Bash运行示例:
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py -v
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py -k "test_basic"
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py::TestVersionComparison -v
    python -m pytest src/shmtu_auth/src/utils/test_version_compatibility.py -m "not slow"
"""

import sys

import pytest
from shmtu_auth.src.utils.program_version import ProgramVersion

# pytest运行配置
pytest_plugins = []

# 自定义标记
# 使用方法: pytest -m "not slow" 跳过慢速测试
# 使用方法: pytest -m "slow" 只运行慢速测试


class TestVersionCompatibility:
    """版本兼容性测试类"""

    def setup_method(self):
        """每个测试方法执行前的设置"""
        print(f"Python 版本: {sys.version}")
        print(f"Python 版本信息: {sys.version_info}")

    def test_import_program_version(self):
        """测试ProgramVersion导入"""
        # 如果导入失败，pytest会自动捕获ImportError
        assert ProgramVersion is not None
        print("✅ 成功导入 ProgramVersion")

    def test_create_basic_version(self):
        """测试创建基本版本对象"""
        v1 = ProgramVersion(1, 2, 3)
        assert v1.major == 1
        assert v1.minor == 2
        assert v1.patch == 3
        assert v1.prerelease is None
        print(f"✅ 成功创建版本对象: {v1}")

    def test_create_prerelease_version(self):
        """测试创建预发布版本"""
        v2 = ProgramVersion(1, 2, 4, "alpha.1")
        assert v2.major == 1
        assert v2.minor == 2
        assert v2.patch == 4
        assert v2.prerelease == "alpha.1"
        print(f"✅ 成功创建预发布版本: {v2}")

    def test_version_comparison(self):
        """测试版本比较"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 4, "alpha.1")

        assert v1 < v2
        print(f"✅ 版本比较: {v1} < {v2} = {v1 < v2}")

    def test_string_parsing(self):
        """测试字符串解析"""
        v3 = ProgramVersion.from_str("2.0.0-beta.1")
        assert v3.major == 2
        assert v3.minor == 0
        assert v3.patch == 0
        assert v3.prerelease == "beta.1"
        print(f"✅ 字符串解析: {v3}")

    def test_set_support(self):
        """测试集合支持（去重功能）"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 4, "alpha.1")

        version_set = {v1, v2, v1}  # v1重复，应该被去重
        assert len(version_set) == 2
        print(f"✅ 集合支持: 长度为 {len(version_set)}")

    def test_all_compatibility(self):
        """综合兼容性测试"""
        # 创建多个版本进行全面测试
        versions = [
            ProgramVersion(1, 0, 0),
            ProgramVersion(1, 0, 1),
            ProgramVersion(1, 1, 0, "alpha.1"),
            ProgramVersion(2, 0, 0, "beta.2"),
        ]

        # 测试排序
        sorted_versions = sorted(versions)
        assert len(sorted_versions) == 4

        # 测试字符串表示
        for v in versions:
            str_repr = str(v)
            assert isinstance(str_repr, str)
            assert len(str_repr) > 0

        print("🎉 所有兼容性测试通过！")


class TestVersionCreation:
    """版本创建相关测试"""

    def test_basic_version_creation(self):
        """测试基本版本创建"""
        v = ProgramVersion(1, 0, 0)
        assert v.major == 1
        assert v.minor == 0
        assert v.patch == 0
        assert v.prerelease is None

    def test_prerelease_version_creation(self):
        """测试预发布版本创建"""
        v = ProgramVersion(1, 0, 0, "alpha")
        assert v.prerelease == "alpha"
        assert v.is_prerelease

    def test_invalid_version_creation(self):
        """测试无效版本创建"""
        with pytest.raises(ValueError):
            ProgramVersion(-1, 0, 0)

        with pytest.raises(ValueError):
            ProgramVersion(1, -1, 0)

        with pytest.raises(ValueError):
            ProgramVersion(1, 0, -1)

        with pytest.raises(TypeError):
            ProgramVersion("1", 0, 0)

        with pytest.raises(ValueError):
            ProgramVersion(1, 0, 0, "")

        with pytest.raises(ValueError):
            ProgramVersion(1, 0, 0, "invalid-pre-release-")

    @pytest.mark.parametrize(
        "major,minor,patch",
        [
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (999, 999, 999),
        ],
    )
    def test_valid_version_numbers(self, major, minor, patch):
        """测试有效的版本号组合"""
        v = ProgramVersion(major, minor, patch)
        assert v.major == major
        assert v.minor == minor
        assert v.patch == patch

    @pytest.mark.parametrize(
        "prerelease",
        [
            "alpha",
            "beta",
            "rc",
            "alpha.1",
            "beta.2",
            "rc.1",
            "dev",
            "snapshot",
            "1",
            "a",
        ],
    )
    def test_valid_prerelease_formats(self, prerelease):
        """测试有效的预发布版本格式"""
        v = ProgramVersion(1, 0, 0, prerelease)
        assert v.prerelease == prerelease


class TestVersionParsing:
    """版本解析相关测试"""

    @pytest.mark.parametrize(
        "version_str,expected",
        [
            ("1.0.0", (1, 0, 0, None)),
            ("1.2.3", (1, 2, 3, None)),
            ("0.0.1", (0, 0, 1, None)),
            ("10.20.30", (10, 20, 30, None)),
            ("1.0.0-alpha", (1, 0, 0, "alpha")),
            ("1.0.0-beta.1", (1, 0, 0, "beta.1")),
            ("2.1.3-rc.2", (2, 1, 3, "rc.2")),
            ("v1.0.0", (1, 0, 0, None)),
            ("V2.1.3", (2, 1, 3, None)),
            ("v1.0.0-alpha", (1, 0, 0, "alpha")),
        ],
    )
    def test_valid_version_parsing(self, version_str, expected):
        """测试有效版本字符串解析"""
        v = ProgramVersion.from_str(version_str)
        assert v is not None
        assert v.major == expected[0]
        assert v.minor == expected[1]
        assert v.patch == expected[2]
        assert v.prerelease == expected[3]

    @pytest.mark.parametrize(
        "invalid_str",
        [
            "",
            "   ",
            "v",
            "V",
            "1.0",
            "1.0.0.0",
            "1.0.0-",
            "1.0.0-.",
            "1.0.0-.alpha",
            "1.0.0-alpha.",
            "invalid",
            "1.a.0",
            "a.1.0",
            "1.0.a",
            "-1.0.0",
            "1.-1.0",
            "1.0.-1",
            None,
            123,
            [],
        ],
    )
    def test_invalid_version_parsing(self, invalid_str):
        """测试无效版本字符串解析"""
        result = ProgramVersion.from_str(invalid_str)
        assert result is None

    def test_parse_method_with_valid_string(self):
        """测试parse方法处理有效字符串"""
        v = ProgramVersion.parse("1.2.3-alpha")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.prerelease == "alpha"

    def test_parse_method_with_invalid_string(self):
        """测试parse方法处理无效字符串"""
        with pytest.raises(ValueError):
            ProgramVersion.parse("invalid")


class TestVersionComparison:
    """版本比较相关测试"""

    def test_major_version_comparison(self):
        """测试主版本号比较"""
        v1 = ProgramVersion(1, 0, 0)
        v2 = ProgramVersion(2, 0, 0)
        assert v1 < v2
        assert v2 > v1
        assert not v1 == v2

    def test_minor_version_comparison(self):
        """测试次版本号比较"""
        v1 = ProgramVersion(1, 0, 0)
        v2 = ProgramVersion(1, 1, 0)
        assert v1 < v2
        assert v2 > v1

    def test_patch_version_comparison(self):
        """测试补丁版本号比较"""
        v1 = ProgramVersion(1, 0, 0)
        v2 = ProgramVersion(1, 0, 1)
        assert v1 < v2
        assert v2 > v1

    def test_prerelease_vs_release_comparison(self):
        """测试预发布版本与正式版本比较"""
        v_release = ProgramVersion(1, 0, 0)
        v_prerelease = ProgramVersion(1, 0, 0, "alpha")
        assert v_prerelease < v_release
        assert v_release > v_prerelease

    def test_prerelease_comparison(self):
        """测试预发布版本之间的比较"""
        v_alpha = ProgramVersion(1, 0, 0, "alpha")
        v_beta = ProgramVersion(1, 0, 0, "beta")
        v_rc = ProgramVersion(1, 0, 0, "rc")

        assert v_alpha < v_beta
        assert v_beta < v_rc

    def test_version_equality(self):
        """测试版本相等性"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3)
        v3 = ProgramVersion(1, 2, 3, "alpha")

        assert v1 == v2
        assert v1 != v3
        assert v2 != v3

    def test_version_sorting(self):
        """测试版本排序"""
        versions = [
            ProgramVersion(2, 0, 0),
            ProgramVersion(1, 0, 0, "alpha"),
            ProgramVersion(1, 0, 0),
            ProgramVersion(1, 1, 0),
            ProgramVersion(1, 0, 1),
        ]

        sorted_versions = sorted(versions)
        expected_order = [
            ProgramVersion(1, 0, 0, "alpha"),
            ProgramVersion(1, 0, 0),
            ProgramVersion(1, 0, 1),
            ProgramVersion(1, 1, 0),
            ProgramVersion(2, 0, 0),
        ]

        assert sorted_versions == expected_order

    def test_compare_to_method(self):
        """测试compare_to方法"""
        v1 = ProgramVersion(1, 0, 0)
        v2 = ProgramVersion(1, 1, 0)
        v3 = ProgramVersion(1, 0, 0)

        assert v1.compare_to(v2) == -1
        assert v2.compare_to(v1) == 1
        assert v1.compare_to(v3) == 0


class TestVersionProperties:
    """版本属性相关测试"""

    def test_is_prerelease_property(self):
        """测试is_prerelease属性"""
        v_release = ProgramVersion(1, 0, 0)
        v_prerelease = ProgramVersion(1, 0, 0, "alpha")

        assert not v_release.is_prerelease
        assert v_prerelease.is_prerelease

    def test_base_version_property(self):
        """测试base_version属性"""
        v_prerelease = ProgramVersion(1, 2, 3, "alpha")
        base = v_prerelease.base_version

        assert base.major == 1
        assert base.minor == 2
        assert base.patch == 3
        assert base.prerelease is None

    def test_version_tuple_property(self):
        """测试version_tuple属性"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3, "alpha")

        assert v1.version_tuple == (1, 2, 3, "")
        assert v2.version_tuple == (1, 2, 3, "alpha")


class TestVersionOperations:
    """版本操作相关测试"""

    def test_bump_major(self):
        """测试主版本号递增"""
        v = ProgramVersion(1, 2, 3, "alpha")
        bumped = v.bump_major()

        assert bumped.major == 2
        assert bumped.minor == 0
        assert bumped.patch == 0
        assert bumped.prerelease is None

    def test_bump_minor(self):
        """测试次版本号递增"""
        v = ProgramVersion(1, 2, 3, "alpha")
        bumped = v.bump_minor()

        assert bumped.major == 1
        assert bumped.minor == 3
        assert bumped.patch == 0
        assert bumped.prerelease is None

    def test_bump_patch(self):
        """测试补丁版本号递增"""
        v = ProgramVersion(1, 2, 3, "alpha")
        bumped = v.bump_patch()

        assert bumped.major == 1
        assert bumped.minor == 2
        assert bumped.patch == 4
        assert bumped.prerelease is None

    def test_with_prerelease(self):
        """测试添加预发布标识符"""
        v = ProgramVersion(1, 2, 3)
        v_pre = v.with_prerelease("alpha")

        assert v_pre.major == 1
        assert v_pre.minor == 2
        assert v_pre.patch == 3
        assert v_pre.prerelease == "alpha"

    def test_without_prerelease(self):
        """测试移除预发布标识符"""
        v = ProgramVersion(1, 2, 3, "alpha")
        v_release = v.without_prerelease()

        assert v_release.major == 1
        assert v_release.minor == 2
        assert v_release.patch == 3
        assert v_release.prerelease is None


class TestVersionCompatibilityChecks:
    """版本兼容性相关测试"""

    def test_is_compatible_with_same_major(self):
        """测试相同主版本号的兼容性"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 3, 0)

        assert v1.is_compatible_with(v2)
        assert v2.is_compatible_with(v1)

    def test_is_compatible_with_different_major(self):
        """测试不同主版本号的兼容性"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(2, 0, 0)

        assert not v1.is_compatible_with(v2)
        assert not v2.is_compatible_with(v1)

    def test_is_compatible_with_invalid_type(self):
        """测试与非版本对象的兼容性检查"""
        v = ProgramVersion(1, 0, 0)

        with pytest.raises(TypeError):
            v.is_compatible_with("1.0.0")

        with pytest.raises(TypeError):
            v.is_compatible_with(123)


class TestVersionHashing:
    """版本哈希相关测试"""

    def test_hash_consistency(self):
        """测试哈希一致性"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3)

        assert hash(v1) == hash(v2)

    def test_hash_in_set(self):
        """测试在集合中的哈希行为"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3)
        v3 = ProgramVersion(1, 2, 4)

        version_set = {v1, v2, v3}
        assert len(version_set) == 2  # v1和v2应该被视为相同

    def test_hash_in_dict(self):
        """测试在字典中的哈希行为"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3)

        version_dict = {v1: "first"}
        version_dict[v2] = "second"

        assert len(version_dict) == 1
        assert version_dict[v1] == "second"


class TestVersionStringRepresentation:
    """版本字符串表示相关测试"""

    def test_str_representation(self):
        """测试字符串表示"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3, "alpha")

        assert str(v1) == "1.2.3"
        assert str(v2) == "1.2.3-alpha"

    def test_repr_representation(self):
        """测试repr表示"""
        v1 = ProgramVersion(1, 2, 3)
        v2 = ProgramVersion(1, 2, 3, "alpha")

        assert repr(v1) == "ProgramVersion(1, 2, 3)"
        assert repr(v2) == "ProgramVersion(1, 2, 3, prerelease='alpha')"


class TestEdgeCases:
    """边界情况测试"""

    def test_zero_versions(self):
        """测试零版本号"""
        v = ProgramVersion(0, 0, 0)
        assert str(v) == "0.0.0"

    def test_large_version_numbers(self):
        """测试大版本号"""
        v = ProgramVersion(999999, 999999, 999999)
        assert v.major == 999999
        assert v.minor == 999999
        assert v.patch == 999999

    def test_complex_prerelease(self):
        """测试复杂的预发布版本"""
        v = ProgramVersion(1, 0, 0, "alpha.1.2.3")
        assert v.prerelease == "alpha.1.2.3"

    def test_single_character_prerelease(self):
        """测试单字符预发布版本"""
        v = ProgramVersion(1, 0, 0, "a")
        assert v.prerelease == "a"

    def test_numeric_prerelease(self):
        """测试数字预发布版本"""
        v = ProgramVersion(1, 0, 0, "1")
        assert v.prerelease == "1"


class TestPytestFeatures:
    """pytest特定功能测试"""

    @pytest.fixture
    def sample_versions(self):
        """提供示例版本对象的fixture"""
        return [
            ProgramVersion(1, 0, 0),
            ProgramVersion(1, 0, 1),
            ProgramVersion(1, 1, 0),
            ProgramVersion(1, 0, 0, "alpha"),
            ProgramVersion(2, 0, 0),
        ]

    def test_with_fixture(self, sample_versions):
        """使用fixture的测试"""
        assert len(sample_versions) == 5
        assert all(isinstance(v, ProgramVersion) for v in sample_versions)

    @pytest.mark.parametrize(
        "version_str",
        [
            "1.0.0",
            "2.1.3-alpha",
            "0.0.1-beta.1",
            "10.20.30-rc.1",
        ],
    )
    def test_parametrized_parsing(self, version_str):
        """参数化解析测试"""
        v = ProgramVersion.from_str(version_str)
        assert v is not None
        assert str(v) == version_str

    @pytest.mark.slow
    def test_performance_with_many_versions(self):
        """性能测试（标记为慢速测试）"""
        versions = []
        for i in range(1000):
            versions.append(ProgramVersion(i % 10, i % 5, i % 3))

        # 测试排序性能
        sorted_versions = sorted(versions)
        assert len(sorted_versions) == 1000

    def test_version_in_collection_operations(self):
        """测试版本对象在集合操作中的表现"""
        versions = [
            ProgramVersion(1, 0, 0),
            ProgramVersion(1, 0, 1),
            ProgramVersion(1, 1, 0),
            ProgramVersion(1, 0, 0),  # 重复
        ]

        # 测试去重
        unique_versions = list(set(versions))
        assert len(unique_versions) == 3

        # 测试成员检查
        v = ProgramVersion(1, 0, 0)
        assert v in versions

        # 测试计数
        assert versions.count(v) == 2


# 保持向后兼容：如果直接运行文件，执行原有的测试逻辑
if __name__ == "__main__":
    print("=" * 60)
    print("运行 ProgramVersion 兼容性测试")
    print("=" * 60)
    print(f"Python 版本: {sys.version}")
    print(f"Python 版本信息: {sys.version_info}")
    print()  # 检查是否安装了pytest
    try:
        import importlib.util

        pytest_spec = importlib.util.find_spec("pytest")
        pytest_available = pytest_spec is not None
        if pytest_available:
            print("✅ pytest 可用，建议使用 'pytest' 命令运行完整测试")
        else:
            print("⚠️  pytest 不可用，将运行基本兼容性测试")
    except ImportError:
        pytest_available = False
        print("⚠️  pytest 不可用，将运行基本兼容性测试")

    print()

    try:
        # 运行基本兼容性测试
        print("运行基本兼容性测试...")
        test_instance = TestVersionCompatibility()
        test_instance.setup_method()

        test_instance.test_import_program_version()
        test_instance.test_create_basic_version()
        test_instance.test_create_prerelease_version()
        test_instance.test_version_comparison()
        test_instance.test_string_parsing()
        test_instance.test_set_support()
        test_instance.test_all_compatibility()

        print()
        print("运行额外的功能测试...")

        # 运行一些额外的测试
        creation_test = TestVersionCreation()
        creation_test.test_basic_version_creation()
        creation_test.test_prerelease_version_creation()
        print("✅ 版本创建测试通过")

        parsing_test = TestVersionParsing()
        parsing_test.test_valid_version_parsing("1.2.3", (1, 2, 3, None))
        parsing_test.test_valid_version_parsing("1.0.0-alpha", (1, 0, 0, "alpha"))
        print("✅ 版本解析测试通过")

        comparison_test = TestVersionComparison()
        comparison_test.test_major_version_comparison()
        comparison_test.test_prerelease_vs_release_comparison()
        print("✅ 版本比较测试通过")

        properties_test = TestVersionProperties()
        properties_test.test_is_prerelease_property()
        properties_test.test_base_version_property()
        print("✅ 版本属性测试通过")

        operations_test = TestVersionOperations()
        operations_test.test_bump_major()
        operations_test.test_bump_minor()
        operations_test.test_bump_patch()
        print("✅ 版本操作测试通过")

        hashing_test = TestVersionHashing()
        hashing_test.test_hash_consistency()
        hashing_test.test_hash_in_set()
        print("✅ 版本哈希测试通过")

        string_test = TestVersionStringRepresentation()
        string_test.test_str_representation()
        string_test.test_repr_representation()
        print("✅ 字符串表示测试通过")
        edge_test = TestEdgeCases()
        edge_test.test_zero_versions()
        edge_test.test_complex_prerelease()
        print("✅ 边界情况测试通过")

        print()
        print("🎉 所有测试通过！ProgramVersion 代码兼容当前Python版本")

        if pytest_available:
            print()
            print("💡 提示：要运行完整的测试套件，请使用以下命令：")
            print("   # 运行所有测试（详细输出）")
            print("   pytest test_version_compatibility.py -v")
            print()
            print("   # 运行特定测试类")
            print("   pytest test_version_compatibility.py::TestVersionCreation -v")
            print()
            print("   # 运行包含特定关键字的测试")
            print("   pytest test_version_compatibility.py -k 'test_parsing' -v")
            print()
            print("   # 跳过慢速测试")
            print("   pytest test_version_compatibility.py -m 'not slow' -v")
            print()
            print("   # 仅运行慢速测试")
            print("   pytest test_version_compatibility.py -m 'slow' -v")
            print()
            print("   # 生成覆盖率报告（需要安装 pytest-cov）")
            print("   pytest test_version_compatibility.py --cov=shmtu_auth.src.utils.program_version --cov-report=html")
            print()
            print("   # PowerShell 中运行所有命令（Windows）")
            print("   python -m pytest test_version_compatibility.py -v")

    except Exception as e:
        print(f"❌ 兼容性测试失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
