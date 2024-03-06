from testers.lintingTest import lintingTest
from testers.tagHandler import tagHandler

def main():
    text = """[PYTHON]
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))  # Output: 120
[/PYTHON]
"""

    tH = tagHandler(text)
    lT = lintingTest(tH.remove_python_tags())
    res = lT.run_lint()
    print(res)
main()