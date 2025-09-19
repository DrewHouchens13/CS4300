from src.task1 import main

def test_hello_output(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"
