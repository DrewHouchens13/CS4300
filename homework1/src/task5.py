'''
Create a new file named task5.py and inside create a list of your favorite books, including book
titles and authors. Use list slicing to print the first three books in the list. Create a dictionary that
represents a basic student database, including student names and their corresponding student IDs.
'''


# A list of favorite books (title, author)
favorite_books = [
    ("The Gunslinger", "Stephen King"),
    ("Farewell to Arms", "Ernest Hemingway"),
    ("Dinosaurs Before Dark", "Mary Pope Osborne")
]

# Use slicing to get the first three books
first_three_books = favorite_books[:3]

# A dictionary representing a basic student database
# student name -> student ID
student_db = {
    "Ricky": "S001",
    "Bobby": "S002",
    "Slick": "S003"
}
