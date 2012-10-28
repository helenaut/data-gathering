import bottle
from bottle import route, post, run, request
from instagram import InstagramAPI

CONFIG = {
  'client_id': 'd67c76fb37a541efbb77d0a5a294bcf8',
  'client_secret': 'e6c4c8a1ae344f0aaa261593b116fc8a',
  'redirect_uri': 'http://localhost:8515/oauth_callback',
  'geo_lat': -122.2744,
  'geo_long': 37.87095
}
api = InstagramAPI(client_id = CONFIG['client_id'], client_secret = CONFIG['client_secret'])
callback = "http://localhost:8515/realtime"
berkeley_subscription = api.create_subscription(object='tag', object_id='food', aspect='media', callback_url=callback)


def process_tag_update(update):
    print update

reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

@route('/realtime')
@post('/realtime')
def on_realtime():
    mode = request.GET.get("hub.mode")
    challenge = request.GET.get("hub.challenge")
    verify_token = request.GET.get("hub.verify_token")
    if challenge: 
        return challenge
    else:
        reactor = subscriptions.SubscriptionsReactor()
        reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)
        x_hub_signature = request.header.get('X-Hub-Signature')
        raw_response = request.body.read()
        try:
            reactor.process(CONFIG['client_secret'], raw_response, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            print "Signature mismatch"
    return Response('Parsed instragram')

run(host='localhost', port=8515, reloader=True)
