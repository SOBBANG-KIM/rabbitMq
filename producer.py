import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Exchange 선언 (topic 타입)
exchange_name = 'topic_logs' 
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

# 패턴 2로만 메시지 전송
routing_key = 'mp_mate-1001-1009782.instore-to'  # 패턴 1
#routing_key = 'mp_mate-1001-1009782.instore.to.ssid002'  # 패턴 2
# routing_key = 'mp_mate-1001-1009782.instore-to.A01'  # 패턴 3
messages = [
    {
        'routing_key': routing_key,  # consumer.py를 위한 메시지
        'message': 'Message for consumer.py'
    }
]

# 각 consumer를 위한 메시지 발행
for msg in messages:
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=msg['routing_key'],
        body=msg['message']
    )
    print(f"Sent message: {msg['message']} with routing key: {msg['routing_key']}")

# 연결 종료
connection.close()
print("Connection closed") 