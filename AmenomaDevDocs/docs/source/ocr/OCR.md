# OCR类

该类包含文字识别、图像处理和调用``Tensorflow``相关的方法。

## 方法

### \__init__

构造函数。

```python
def __init__(
    self,
    model_weight: str = 'mn_model_weight.h5',
    scale_ratio: float = 1.0
)
```

#### 参数

``model_weight``

可能是机器学习相关参数，超出文档作者知识范畴。

``scale_ratio``

图片缩放比例。

---

### setScaleRatio

设置缩放比例。

```python
def setScaleRatio(self, scaleRatio: float)
```

#### 参数

``scaleRatio``

新的缩放比例。~~所以到底是用小驼峰命名法还是下划线连接啊喂！~~

#### 返回值

无

