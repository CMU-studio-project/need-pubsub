# NEED Project
Google Pub/Sub wrapper for NEED project


## Installation
```shell
git clone https://github.com/CMU-studio-project/need-pubsub.git
pip install need-pubsub
```

## Usage
### Publishing message
```python
from needpubsub.publish import publish_message

publish_message(
    message,
    project_id=project_id,
    topic_id=topic_id,
    ordering_key=ordering_key,
    **kwargs,
)
```

### Subscribing from Google Pub/sub
#### Async subscription
```python
from needpubsub.subscribe import subscribe_message_async

subscribe_message_async(project_id, subscription_id, sub_callback_fn)
```

#### Sync subscription
```python
from needpubsub.subscribe import subscribe_message_sync

subscribe_message_sync(project_id, subscription_id, sub_callback_fn)
```
