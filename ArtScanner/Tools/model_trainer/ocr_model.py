import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from mobilenetv3 import MobileNetV3_Small
import numpy as np

@tf.autograph.experimental.do_not_convert
def ctc_loss(y_true, y_pred):
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.math.count_nonzero(y_true, axis=-1, keepdims=True)

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    return keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)


# A utility function to decode the output of the network
def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
              :, :max_length
              ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = num_to_char(res)
        res = tf.strings.reduce_join(res)
        res = res.numpy().decode("utf-8")
        output_text.append(res)
    return output_text


class CTCAccuracy(tf.keras.metrics.Metric):
    def __init__(self, name='ctc_accuracy', **kwargs):
        super(CTCAccuracy, self).__init__(name=name, **kwargs)
        self.correct_count = 0
        self.all_count = 0

    def update_state(self, y_true, y_pred, sample_weight=None):
        pred_text = decode_batch_predictions(y_pred)
        self.all_count += len(pred_text)
        true_text = []
        for res in y_true:
            res = num_to_char(res)
            res = tf.strings.reduce_join(res)
            res = res.numpy().decode("utf-8")
            true_text.append(res)
        self.correct_count += sum([i == j for i, j in zip(pred_text, true_text)])

    def result(self):
        return self.correct_count / self.all_count

    def reset_states(self):
        self.correct_count = 0
        self.all_count = 0


def build_model():
    # Inputs to the model
    input_img = layers.Input(
        shape=(img_width, img_height, 1), name="image", dtype="float32"
    )

    mobilenet = MobileNetV3_Small(
        (img_width, img_height, 1), 0, alpha=1.0, include_top=False
    ).build()
    x = mobilenet(input_img)

    new_shape = ((img_width // 8), (img_height // 8) * 576)
    x = layers.Reshape(target_shape=new_shape, name="reshape")(x)
    x = layers.Dense(64, activation="relu", name="dense1")(x)
    x = layers.Dropout(0.2)(x)

    # RNNs
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.25))(x)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.25))(x)

    # Output layer
    output = layers.Dense(len(characters) + 2, activation="softmax", name="dense2")(x)

    # Define the model
    model = keras.models.Model(inputs=[input_img], outputs=output, name="ocr_model_v1")
    # Optimizer
    return model


# Get the model
model = build_model()
opt = keras.optimizers.Adam()
# Compile the model and return
model.compile(loss=ctc_loss, optimizer=opt, metrics=[CTCAccuracy('ctc_accu')])
model.run_eagerly = True
model.summary()
