from task1 import task1

def test_hello_output(capsys):
    task1()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"
