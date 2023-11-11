from app import pubsub


class PubSubManager:
    @staticmethod
    def new_queue(channel):
        pubsub.subscribe(channel)

    def test_subscribe(self):
        pubsub.publish("test", "hello world")

    def test_unsubscribe(self):
        sub = pubsub.subscribe("test")
        pubsub.publish("test", "hello world 1")
        sub.unsubscribe()
        pubsub.publish("test", "hello world 2")
        # msgs = list(sub.listen(block=False))
