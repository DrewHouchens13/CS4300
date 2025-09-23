'''
Include pytest test cases that verify the word count for each text file.
'''

import os
import pytest
from src import task6


'''
test_count_words_in_files(filename, expected)
Purpose: Verify that the word count matches expected numbers
for different files, including the provided task6_read_me.txt.
'''
@pytest.mark.parametrize("filename, expected", [
    # Absolute path to task6_read_me.txt
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "task6_read_me.txt")),
        127
    ),
])
def test_count_words_in_files(filename, expected):
    assert task6.count_words_in_file(filename) == expected


'''
test_count_words_in_empty_file(tmp_path)
Purpose: Verify that empty files return a word count of 0.
'''
def test_count_words_in_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    assert task6.count_words_in_file(str(empty_file)) == 0


'''
test_count_words_in_small_files(tmp_path, content, expected)
Purpose: Verify that files with single-line short text return correct word counts.
'''
@pytest.mark.parametrize("content, expected", [
    ("hello world", 2),
    ("one two three four", 4),
])
def test_count_words_in_small_files(tmp_path, content, expected):
    file = tmp_path / "sample.txt"
    file.write_text(content)

    assert task6.count_words_in_file(str(file)) == expected
