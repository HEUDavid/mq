import pika
"""
这种模式下，传递到 exchange 的消息将会转发到所有与其绑定的 queue 上。

不需要指定 routing_key ，即使指定了也是无效。
需要提前将 exchange 和 queue 绑定，一个 exchange 可以绑定多个 queue，一个queue可以绑定多个exchange。
需要先启动 订阅者，此模式下的队列是 consumer 随机生成的，发布者 仅仅发布消息到 exchange ，由 exchange 转发消息至 queue。


"""

mport json


if __name__ == '__main__':

    credentials = pika.PlainCredentials('test', '123456')  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='api.mdavid.cn', port=5672, virtual_host='xiang_test', credentials=credentials))
    channel = connection.channel()
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。
    # durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')
    for i in range(10):
        message = json.dumps({'OrderId': "1000%s" % i})
        # 向队列插入数值 routing_key是队列名。
        # delivery_mode = 2 声明消息在队列中持久化，
        # delivery_mode = 1 消息非持久化。routing_key 不需要配置
        channel.basic_publish(exchange='python-test', routing_key='queue_1', body=message,
                              properties=pika.BasicProperties(delivery_mode=2))
        print(message)
    connection.close()
