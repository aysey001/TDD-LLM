from  tagHandler import tagHandler
def main():
    text = """[PYTHON]
import pylint.lint
[/PYTHON]"""
    tHp = tagHandler(text)
    text2 = """[LIST]
1. test
2. hallo
3. world
[/LIST]"""
    tHl = tagHandler(text2)

    text3 = """[TESTS]
def test1():
    pass
[/TESTS]"""
    tht = tagHandler(text3)

            
    print(text)
    print(tHp.has_python_tags())
    print(tHp.remove_python_tags())

    print(text2)
    print(tHl.has_list_tags())
    print(tHl.remove_list_tags())

    print(text3)
    print(tht.has_tests_tags())
    print(tht.remove_tests_tags())

main()