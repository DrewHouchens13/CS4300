'''
Set up a pytest test case that verifies the output of your 
task 1 hello world script
''' 

from src import task1

'''
test_hello_output(capsys)
Purpose: Uses capsys to test for "Hello World" on terminal
'''
def test_hello_output(capsys):
    task1.task1()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"
