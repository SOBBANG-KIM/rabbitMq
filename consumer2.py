import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Exchange 선언 (topic 타입)
exchange_name = 'mp_mate-1001-1009782.instore'
channel.exchange_declare(exchange=exchange_name, exchange_type='headers')

# Queue 생성 (고유한 큐 이름 사용)
queue_name = 'device_2_queue'
channel.queue_declare(queue=queue_name)

# x-match=any: 하나라도 일치하면 됨
bind_args = {
    'x-match': 'any',
    'service': 'tablet',
    'ssid': 'ssid002',
    'tableId': '002',
}

channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key='',
    arguments=bind_args
)

# 콜백 함수 정의
def callback(ch, method, properties, body):
    print(f"Region/Device consumer received: {body.decode()}")
    print(f"Headers: {properties.headers}")

# 메시지 수신 설정
channel.basic_consume(
    queue=queue_name,
    auto_ack=True,
    on_message_callback=callback
)

print(f"Waiting for messages for region seoul and device type tablet. To exit press CTRL+C")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close() 