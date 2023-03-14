from datetime import datetime, timedelta

now = datetime.now()
two_month = timedelta(60)
last_month_one = now - timedelta(60)
last_mont_two = now - timedelta(30)
year, mont_one = str(last_month_one)[:7].split('-')