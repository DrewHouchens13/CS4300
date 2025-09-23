''' 
task6.py 
Reads a text file and counts the number of words in it. 
'''


"""
count_words_in_file(filename)
Reads a file and returns the number of words it contains.
"""
def count_words_in_file(filename):

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    return len(words)
