import os
from google.cloud import pubsub_v1

from .utils import encrypt_message

def publish_message(message: bytes, project_id: str, topic_id: str, **kwargs) -> str:  # type: ignore[no-untyped-def]
    if kwargs.get("ordering_key", ""):
        publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
        # Sending messages to the same region ensures they are received in order
        # even when multiple publishers are used.
        client_options = {"api_endpoint": "us-central1-pubsub.googleapis.com:443"}
        publisher = pubsub_v1.PublisherClient(
            publisher_options=publisher_options, client_options=client_options
        )
    else:
        publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Message encryption
    encrypted_message = encrypt_message(message)

    future = publisher.publish(topic=topic_path, data=encrypted_message, **kwargs)
    message_id = future.result()
    
    return message_id


if __name__ == "__main__":
    import random

    for i in range(10):
        ri = random.randint(1, 100)
        data = f"Random number {ri}"
        print(data)

        publish_message(
            data.encode("utf-8"),
            "input_speech",
            name="kyumin",
            organization="coddlers",
            ordering_key="key1",
        )
