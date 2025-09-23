'''
Implement pytest test cases to verify the correctness of your code for each data structure.
'''

from src import task5 

'''
Check that the list has at least 3 entries
Check first entry (tuple with title and author)
'''
def test_favorite_books_list():   
    assert len(task5.favorite_books) >= 3
    assert task5.favorite_books[0] == ("The Gunslinger", "Stephen King")


'''
Slicing should return first 3 books
'''
def test_first_three_books_slice():
    assert task5.first_three_books == task5.favorite_books[:3]

'''
Check keys exist
Check values match expected IDs
'''
def test_student_db_dictionary():
    assert "Ricky" in task5.student_db
    assert "Bobby" in task5.student_db
    assert task5.student_db["Ricky"] == "S001"
    assert task5.student_db["Slick"] == "S003"