from testers.lintingTest import lintingTest
from testers.tagHandler import tagHandler

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    text = read_file("prompt//flaskr/flaskr_code.txt")
    tH = tagHandler(text)
    lT = lintingTest(tH.remove_python_tags())
    res = lT.run_lint()
    print(res)
main()