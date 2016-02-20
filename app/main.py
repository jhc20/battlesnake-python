import bottle
import os

''' Example Recieved Snake Object

{
    "id": "1234-567890-123456-7890",
    "name": "Well Documented Snake",
    "status": "alive",
    "message": "Moved north",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 83,
    "coords": [ [1, 1], [1, 2], [2, 2] ],
    "kills": 4,
    "food": 12,
    "gold": 2
}

'''


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#4099ff',
        'head': "http://imgur.com/uajfGft"
    }


''' Object recieved for /start
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 0,
    "height": 20,
    "width": 30,
    "snakes": [
        <Snake Object>, <Snake Object>, ...
    ],
    "food": [],
    "walls": [],  // Advanced Only
    "gold": []    // Advanced Only
}
'''

@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'Lorem Ipsum'
    }

'''  Recieved Move object for /move
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "height": 20,
    "width": 30,
    "snakes": [
        <Snake Object>, <Snake Object>, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ],
    "walls": [    // Advanced Only
        [2, 2]
    ],
    "gold": [     // Advanced Only
        [5, 5]
    ]
}

'''



@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    

    return {
        'move': 'north',
        'taunt': 'Lorem Ipsum'
    }

'''  Object revcieved for /end
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "height": 20,
    "width": 30,
    "snakes": [
        <Snake Object>, <Snake Object>, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ],
    "walls": [    // Advanced Only
        [2, 2]
    ],
    "gold": [     // Advanced Only
        [5, 5]
    ]
}

'''


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'YEEZY YEEZY YEEZY JUST JUMPED OVER JUMPMAN'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
