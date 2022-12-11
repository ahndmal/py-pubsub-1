import os
from typing import Optional
from google.cloud import pubsub_v1


def pub(proj_id: str, topic_id: str):
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(proj_id, topic_id)
    data = b"Hello from Python Pub1"

    # When you publish a message, the client returns a future.
    api_future = client.publish(topic_path, data)
    message_id = api_future.result()
    print(f"Published {data.decode()} to {topic_path}: {message_id}")


def sub1(proj_id: str, sub_id: str, timeout: Optional[float] = None):
    sub_client = pubsub_v1.SubscriberClient()
    subscription_path = sub_client.subscription_path(proj_id, sub_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        # Acknowledge the message. Unack'ed messages will be redelivered.
        message.ack()
        print(f"Acknowledged {message.message_id}.")

    streaming_pull_future = sub_client.subscribe(
        subscription_path, callback=callback
    )
    print(f"Listening for messages on {subscription_path}..\n")

    try:
        # Calling result() on StreamingPullFuture keeps the main thread from
        # exiting while messages get processed in the callbacks.
        streaming_pull_future.result(timeout=timeout)
    except:  # noqa
        streaming_pull_future.cancel()
        streaming_pull_future.result()  # Block until the shutdown is complete.

    sub_client.close()


if __name__ == '__main__':
    print("... starting")
    proj_id = os.getenv("GCP_PROJ_ID")
    topic = "wiki-pages-main"
    pub(proj_id, topic)
    sub1(proj_id, "sub1", 2.0)
