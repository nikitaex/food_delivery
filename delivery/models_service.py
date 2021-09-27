def calculate_discount(discount, quantity, price,):
    if discount < 1:
        final_price = quantity * price
        return final_price
    final_price = (quantity * price * (100 - discount)) / 100
    return final_price