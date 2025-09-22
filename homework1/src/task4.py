'''
Create a new file named task4.py that calculates the final price of a product after 
applying a given discount percentage inside of a function named calculate_discount. 
The function should accept any numeric type for price and discount
'''

'''
calculate_discount(price, discount)
price = price of good
discount = percentage off good (0-100)
Returns: adjusted price
'''
def calculate_discount(price, discount):

    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")
        
    final_price = price - (price * discount / 100)
    return final_price
