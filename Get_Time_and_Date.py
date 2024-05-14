import datetime

def get_current_datetime():
    now = datetime.datetime.now()
    date_str = now.strftime("%B %d, %Y")  # Example: January 01, 2023
    day_str = now.strftime("%A")  # Example: Monday
    time_str = now.strftime("%I:%M %p")  # Example: 12:30:45 PM

    s=time_str.split(":")
    j=s[1].split(" ")

    greetText=""
    hour = now.hour

    if 5 <= hour < 12:
        greetText="Good morning!, How Are You Feeling Today"
    elif 12 <= hour < 15:
        greetText="Good afternoon!"
    elif 15 <= hour < 22:
        greetText="Good Evening!"
    else:
        greetText="its a Night time Sir ,Good night!"

    return date_str, day_str, time_str,greetText