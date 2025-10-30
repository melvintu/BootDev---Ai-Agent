from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print("")

    tests = run_python_file("calculator", "tests.py")
    print(tests)
    print("")

    result = run_python_file("calculator", "../main.py")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print("")

    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print("")

if __name__ == "__main__":
    test()