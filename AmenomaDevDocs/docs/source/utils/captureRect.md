# captureRect<!-- {docsify-ignore-all} -->

截图，范围为给定的矩形。该矩形以整个屏幕作为基准，而非针对某特定窗口，因此窗口被覆盖部分不会被截取到。

```python
def captureRect(rect: List[int])
```

## 参数

``name``

类型：**List[int]**

一个数组，共4个元素，由0到3分别表示top、left、width、height。

## 返回值

类型：**PIL.Image**

返回截取的图片。

## 依赖

* ``mss``
* ``PIL``
