import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Exchange 선언 (topic 타입)
exchange_name = 'topic_logs'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

# Queue 생성
queue_name = 'id_specific_queue1'
channel.queue_declare(queue=queue_name)

# 여러 바인딩 패턴 사용
binding_patterns = [
    'mp_mate-1001-1009782.instore.to',  # 패턴 1
    'mp_mate-1001-1009782.instore.to.ssid000',  # 패턴 3
]

for pattern in binding_patterns:
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=pattern
    )

# 콜백 함수 정의
def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()} with routing key: {method.routing_key}")

# 메시지 수신 설정
channel.basic_consume(
    queue=queue_name,
    auto_ack=True,
    on_message_callback=callback
)

print("Waiting for messages. To exit press CTRL+C")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close() 