"""
direct模式工作模式的原理是 消息发送至 exchange，exchange 根据 路由键（routing_key）转发到相对应的 queue 上。

可以使用默认 exchange ='' ，也可以自定义 exchange
这种模式下不需要将 exchange 和 任何进行绑定，当然绑定也是可以的。可以将 exchange 和 queue ，routing_key 和 queue 进行绑定
传递或接受消息时 需要 指定 routing_key

需要先启动订阅者，此模式下的队列是 consumer 随机生成的，发布者仅仅发布消息到 exchange ，由 exchange 转发消息至 queue。

topic模式和direct模式差不多，exchange 也是通过 路由键 routing_key 来转发消息到指定的 queue 。
不同点是 routing_key 使用正则表达式支持模糊匹配，但匹配规则又与常规的正则表达式不同，比如“#”是匹配全部，“*”是匹配一个词。

举例：routing_key =“#orderid#”，意思是将消息转发至所有 routing_key 包含 “orderid” 字符的队列中。

"""

import json

import pika

if __name__ == '__main__':

    credentials = pika.PlainCredentials('test', '123456')  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='api.mdavid.cn', port=5672, virtual_host='xiang_test', credentials=credentials))
    channel = connection.channel()
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange='python-test3', durable=True, exchange_type='direct')

    for i in range(10):
        message = json.dumps({'OrderId': "1000%s" % i})
        # 指定 routing_key。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化
        channel.basic_publish(exchange='python-test3', routing_key='OrderId', body=message,
                              properties=pika.BasicProperties(delivery_mode=2))
        print(message)
    connection.close()
