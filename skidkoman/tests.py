from datetime import datetime, timedelta

value = datetime.now() + timedelta(weeks=2)
print(value)
r = (value - datetime.now()).days + 1
print(r)

