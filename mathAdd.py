import tensorflow as tf

@tf.function
def add(v1, v2):
    return tf.math.add(v1, v2)

tf.print(add(3, 5)) # => 8
tf.print(add([1, 2], [3, 4])) # => [4 6]
