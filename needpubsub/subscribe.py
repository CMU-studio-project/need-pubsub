from concurrent.futures import TimeoutError  # pylint: disable=redefined-builtin
from typing import Callable, Optional

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber import message as sub_message

from .utils import decrypt_message


def subscribe_message_sync(project_id: str, subscription_id: str, callback_fn: Callable) -> None:
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # The subscriber pulls a specific number of messages. The actual
    # number of messages pulled may be smaller than max_messages.
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
    )

    if len(response.received_messages) == 0:
        return

    ack_ids = []
    for received_message in response.received_messages:
        ack_ids.append(received_message.ack_id)

    # Acknowledges the received messages so they will not be sent again.
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": ack_ids}
    )
    
    message = response.received_messages[0].message
    message_data = message.data
    decrypted_message = decrypt_message(message_data)

    rec_data = {
        "message": decrypted_message,
        "message_id": message.message_id,
    }

    if message.attributes:
        rec_data.update(**message.attributes)

    callback_fn(**rec_data)


def subscribe_message_async(project_id: str, subscription_id: str, callback_fn: Callable, timeout: Optional[float] = None) -> None:
    def sub_callback(message: sub_message.Message) -> None:
        message_data = message.data
        decrypted_message = decrypt_message(message_data)
        
        rec_data = {
            "message": decrypted_message,
            "message_id": message.message_id,
        }
        
        if message.attributes:
            rec_data.update(**message.attributes)
            
        message.ack()
        callback_fn(**rec_data)
        
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=sub_callback)
    print(f"Listening for messages on {subscription_path}..")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError or KeyboardInterrupt:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


if __name__ == "__main__":
    import argparse

    def run_task(message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        print(message)
    
        for key, val in kwargs.items():
            print(f"{key}: {val}")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--subscription_id", type=str, help="subscription ID", default="speech-gpu-server"
    )
    args = parser.parse_args()

    subscribe_message_async(args.subscription_id, run_task, timeout=None)
