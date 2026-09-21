# lists_and_dicts_cart.py

# List of products (dictionary inside list)
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 2000},
    {"id": 4, "name": "Mouse", "price": 800}
]

# Shopping cart (empty list)
cart = []

# 1. Add items to cart
cart.append(products[0])  # Laptop
cart.append(products[2])  # Headphones
cart.append(products[3])  # Mouse

print("Items in Cart:")
for item in cart:
    print(f"{item['name']} - ₹{item['price']}")

print("\n")

# 2. Calculate total bill
total = sum(item["price"] for item in cart)
print(f"Total Bill: ₹{total}")

print("\n")

# 3. Apply discount if total > 30000
if total > 30000:
    discount = total * 0.1  # 10% discount
    total -= discount
    print(f"Discount Applied: ₹{discount}")
    print(f"Final Bill: ₹{total}")
else:
    print("No discount applied.")

print("\n")

# 4. Search product by name
search_name = "Phone"
found = next((p for p in products if p["name"] == search_name), None)
if found:
    print(f"Product Found: {found['name']} - ₹{found['price']}")
else:
    print("Product not found.")
