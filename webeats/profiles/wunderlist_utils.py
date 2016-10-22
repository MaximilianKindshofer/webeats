
def get_authorization_url(client_id, redirect_url, state):
    return authorize_url = "https://www.wunderlist.com/oauth/authorize?client_id={}&redirect_uri={}&state={}".format(client_id, redirect_url, state)


