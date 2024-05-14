import requests


def fetch_joke():
    try:
        response = requests.get("https://api.chucknorris.io/jokes/random")
        joke_data = response.json()
        joke = joke_data['value']
    except:
        joke = "Something went wrong. Check Connection"
    return joke
    # self.joke_label.setText(f"Joke of the Day: {joke}")

def fetch_motivation():
    try:
        response = requests.get("https://api.quotable.io/random")
        quote_data = response.json()
        quote = quote_data['content']
        author = quote_data['author']
    except:
        quote = "Something went wrong. Check Connection"
        author = None
    return quote, author