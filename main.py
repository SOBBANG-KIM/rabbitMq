# 1. rabbitmq 를 connect 하고 연결 확인
# 2. 연결 확인 후 채널 생성
# 3. 채널 생성 후 큐 생성
# 4. 큐 생성 후 메시지 전송
# 5. 메시지 전송 후 큐에서 메시지 수신
# 6. 메시지 수신 후 메시지 출력
# 7. 메시지 출력 후 연결 종료
import pika

# 1. Connect to RabbitMQ and verify connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
print("Connected to RabbitMQ")

# 2. Create channel after connection verified
channel = connection.channel()
print("Channel created")

# Exchange 선언 (topic 타입)
exchange_name = 'topic_logs'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

# Queue 생성 및 바인딩
queue_name = 'test_queue'
channel.queue_declare(queue=queue_name)

# 세 가지 바인딩 패턴 적용
binding_patterns = [
    'mp_mate-1001-1009782.to.#',          # 패턴 1: 모든 하위 레벨 매치
    'mp_mate-1001-1009782.to.e75dee4d1a6878ea.*',  # 패턴 2: 특정 ID와 한 레벨 매치
    'mp_mate-1001-1009782.to.*.001'       # 패턴 3: 중간 레벨 와일드카드
]

for pattern in binding_patterns:
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=pattern
    )

# 메시지 발행
routing_key = 'mp_mate-1001-1009782.to.e75dee4d1a6878ea.001'
message = "Hello Topic Exchange!"
channel.basic_publish(
    exchange=exchange_name,
    routing_key=routing_key,
    body=message
)
print(f"Sent message: {message} with routing key: {routing_key}")

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
channel.start_consuming()

# 7. Close connection
connection.close()
print("Connection closed")


