from line_notify import LineNotify


def sendMessage(message):
    token = '7w9sX5x78568L8lCGQ27hfvEyXPfzxZF2orUcCavcJ2'

    notify  = LineNotify(token)
    notify.send(message,sticker_id = 283 , package_id =4)
