import tensorflow as tf
coeff = [0.00024685431464582943, 0.006937918978475038,
         148.66285448846736, 58600.0, 123.0]
coeff = [7.2386710133583996e-06, -0.13467534047367463, 0.0, 0.0, 715.0]
x = tf.Variable(0, dtype=tf.float32)  # 定义一个可以优化的x值
y = tf.Variable(0, dtype=tf.float32)  # 定义一个可以优化的x值
cost = tf.add_n([tf.multiply(coeff[0], x**2), tf.multiply(coeff[1], x*y), tf.multiply(coeff[2], x),
                 tf.multiply(coeff[3], y), tf.multiply(coeff[4], y**2)])  # x**2 -10x + 26 即 (x-5)**2 + 1 最小值应该是1
train = tf.train.GradientDescentOptimizer(0.01).minimize(cost)  # 用梯度下降法优化
init = tf.global_variables_initializer()  # 初始化所有的变量节点
with tf.Session() as sess:
    sess.run(init)  # 初始化所有变量节点
    for i in range(1000):
        sess.run(train)  # 进行优化
        print('当前最小值是：', sess.run(cost), '\t对应的x值是：', sess.run(x), sess.run(y))
