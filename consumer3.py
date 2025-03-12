import pika

# Connect to RabbitMQ
credentials = pika.PlainCredentials('rabbitmq_conn', 'Food12#$')
connection_params = pika.ConnectionParameters(
    host='mate-mq.qaftk.kr',
    port=5672,
    credentials=credentials
    # connection_timeout=5000
)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Exchange 이름 설정 (기존 exchange 사용)
exchange_name = 'amq.topic'

# Queue 생성 (고유한 큐 이름 사용)
queue_name = 'mp_extpos_test-1001-1012886.instore-to.01-006'
channel.queue_declare(queue=queue_name, durable=True)

# 여러 바인딩 패턴 사용
binding_patterns = [
    'mp_extpos_test-1001-1012886.instore-to.01-006'
]

for pattern in binding_patterns:
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=pattern
    )

# 콜백 함수 정의
def callback(ch, method, properties, body):
    print(f"ID Specific Consumer - Received message: {body.decode()} with routing key: {method.routing_key}")

# 메시지 수신 설정
channel.basic_consume(
    queue=queue_name,
    auto_ack=True,
    on_message_callback=callback
)

print(f"Waiting for messages for ID ssid002. To exit press CTRL+C")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close() 