users = [{"name": "Kamil", "country": "Poland"}, {"name": "John", "country": "USA"}, {"name": "Yeti"}]

list1 = [user for user in users if user.get("country") == "Poland"]

print(list1)