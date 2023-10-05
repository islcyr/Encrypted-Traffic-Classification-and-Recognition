import keras
from keras.layers import Conv1D, Dense, Reshape, MaxPooling1D, Dropout, Flatten
from keras.optimizers import adam_v2

conv = Conv1D(32, 25, padding='same', activation='relu', input_shape=(784,1))
maxpool = MaxPooling1D(3, strides=3, padding='same')
conv2 = Conv1D(64, 25, padding='same', activation='relu')
maxpool2 = MaxPooling1D(3, strides=3, padding='same')

def createModel(do_compile=False, class_num=12):
    model = keras.models.Sequential([
        conv,
        maxpool,
        conv2,
        maxpool2,
        Flatten(),
        Dense(1024, activation='relu'),
        Dropout(0.5),
        Dense(class_num, activation='softmax')
        ]
    )

    if do_compile:
        model.compile(optimizer = adam_v2.Adam(learning_rate=0.001),
                      loss = 'categorical_crossentropy',
                      metrics = ['acc'])
    return model