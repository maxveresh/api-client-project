import pytest

# """Маркер параметризации, позволяет добавлять несколько значений для прогона по одной функции"""
#
# @pytest.mark.parametrize("a,b,expected", [
#     (1, 1, 2),
#     (2, 2, 4),
#     (3, 3, 6),
# ])
# def test_sum_parametrized(a, b, expected):
#     assert a + b == expected
#
# @pytest.mark.parametrize("text,expected", [
#     ("qa", True),
#     ("automation", False),
#     ("qa engineer", True),
# ])
# def test_contains_qa(text, expected):
#     result = "qa" in text
#     assert result == expected
#
# @pytest.mark.parametrize("index,expected", [
#     (0,1),
#     (1,2),
#     (2,3),
# ])
# def test_sample_list_of_index(sample_list, index, expected):
#     assert sample_list[index] == expected

# """Маркер пропуска выполнения"""
#
# @pytest.mark.skip(reason='Feature not implemented yet')
# def test_skip_example():
#     assert 1 == 0
#
# """Маркер потенциальной ошибки. Выполнение не останавливается, но потенциальная ошибка
# при срабатывании не считается упавшей, как FAILED"""
#
# @pytest.mark.xfail(reason='Known bug in system')
# def test_expected_fail():
#     assert 2 * 2 == 5
#
# """
# """
# @pytest.mark.api
# def test_api_example():
#     assert 1 == 1
#
# @pytest.mark.ui
# def test_ui_example():
#     assert 2 == 2