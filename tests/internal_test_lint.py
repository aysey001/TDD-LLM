from verify import lintingTest

def main():
    text = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))  # Output: 120

"""
    print(text)
    lt = lintingTest.lintingTest(text)
    print(lt.run_lint())
main()