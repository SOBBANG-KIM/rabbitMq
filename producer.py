import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Headers Exchange 선언
exchange_name = 'mp_mate-1001-1009782.instore'
channel.exchange_declare(exchange=exchange_name, exchange_type='headers')

# 메시지 속성 정의 - ssid001만을 위한 헤더
headers = {
    'service': 'tablet',
    # 'tableId': '003',
    # 'ssid': 'ssid001',
}

message = "Test message for ssid001"
channel.basic_publish(
    exchange=exchange_name,
    routing_key='',  # headers exchange는 routing key 불필요
    body=message,
    properties=pika.BasicProperties(
        headers=headers
    )
)

print(f"Sent message with headers: {headers}")

# 연결 종료
connection.close()
print("Connection closed") 