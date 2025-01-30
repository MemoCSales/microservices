# RabbitMQ Queue Name Validator

A utility class that validates RabbitMQ queue names according to standard naming conventions and RabbitMQ requirements.

## Description
Validates if a given queue name adheres to RabbitMQ naming conventions. RabbitMQ queue names must:
- Be between 1 and 255 characters long
- Contain only valid ASCII characters (letters, numbers, hyphens, and underscores)
- Follow the format: [environment]-[application]-[purpose]

## RabbitMQ Queue Name Rules
- Queue names have a maximum length of 255 bytes
- Can contain letters, digits, hyphens, underscores, periods, and colons
- Must start with a letter
- Case-sensitive
- Cannot be empty

## Usage
Use this validator to ensure queue names comply with RabbitMQ standards before creating or working with queues. This helps prevent errors and maintains consistency in queue naming across the system.

## Returns
- `true` if the queue name is valid according to RabbitMQ standards
- `false` if the queue name violates any naming conventions or requirements

## Best Practices
- Use descriptive names that indicate the queue's purpose
- Follow a consistent naming pattern across your application
- Consider including environment identifiers for different deployment stages
- Avoid special characters that might cause issues in different environments

## Error Handling
```bash
(venv) guillermosales@MBP-de-Jimena MessageQueues % python consumer.py 
Traceback (most recent call last):
  File "/Users/guillermosales/Documents/MEMO/42/Core/transcendence/microservices/MessageQueues/consumer.py", line 4, in <module>
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  File "/Users/guillermosales/Documents/MEMO/42/Core/transcendence/microservices/MessageQueues/venv/lib/python3.10/site-packages/pika/adapters/blocking_connection.py", line 360, in __init__
    self._impl = self._create_connection(parameters, _impl_class)
  File "/Users/guillermosales/Documents/MEMO/42/Core/transcendence/microservices/MessageQueues/venv/lib/python3.10/site-packages/pika/adapters/blocking_connection.py", line 451, in _create_connection
    raise self._reap_last_connection_workflow_error(error)
pika.exceptions.AMQPConnectionError
```

This error `pika.exceptions.AMQPConnectionError` means that Python code couldn't connect to RabbitMQ at localhost:5672 (default port). Once RabbitMQ is running, the connection in the code should work:

```python
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
```

To debug connection:
1. First, install RabbitMQ server on macOS using Homebrew:
```bash
# Install RabbitMQ
brew install rabbitmq

# Start RabbitMQ service
brew services start rabbitmq
```

2. Verify RabbitMQ is running:
```bash
brew services list | grep rabbitmq
```

3. Then you can run your `consumer.py` again:
```bash
cd MessageQueues
source venv/bin/activate
python consumer.py
```

* Verify everythin is working by using:
```bash
# Check RabbitMQ status
brew services info rabbitmq

# Check logs
tail -f /usr/local/var/log/rabbitmq/rabbit@localhost.log
```

4. After using. Stop RabitMQ on macOS:
```bash
brew services stop rabbitmq
```

5. Verify it's stopped with:
```bash
brew services list | grep rabbitmq
```

* Check RabbitMQ status: `brew services info rabbitmq`
* Check logs: `tail -f /usr/local/var/log/rabbitmq/rabbit@localhost.log`
* Ensure port 5672 is available: `lsof -i :5672`
