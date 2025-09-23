'''
Implement pytest test cases to verify the correctness of your code for each data structure.
'''

from src import task5 

'''
test_favorite_books_list()
Purpose: checks the number of books in list and validates first entry
'''
def test_favorite_books_list():   
    assert len(task5.favorite_books) >= 3
    assert task5.favorite_books[0] == ("The Gunslinger", "Stephen King")


'''
test_first_three_books_slice()
Purpose: Checks that slicing returns first 3 books
'''
def test_first_three_books_slice():
    assert task5.first_three_books == task5.favorite_books[:3]

'''
test_student_db_dictionary
Purpose: Check keys exist and values match expected IDs
'''
def test_student_db_dictionary():
    assert "Ricky" in task5.student_db
    assert "Bobby" in task5.student_db
    assert task5.student_db["Ricky"] == "S001"
    assert task5.student_db["Slick"] == "S003"