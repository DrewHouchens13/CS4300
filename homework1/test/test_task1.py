from src import task1

def test_hello_output(capsys):
    task1.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"
