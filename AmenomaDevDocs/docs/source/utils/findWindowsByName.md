# findWindowsByName<!-- {docsify-ignore-all} -->

该函数根据窗口的名称获取窗口的Handle。

```python
def findWindowsByName(name: str)
```

## 参数

``name``

类型：**str**

待获取窗口的名称。

## 返回值

类型：**win32api.HWND**

若成功则返回对应窗口的Handle，若失败则为``None``。

## 依赖

* ``win32api``
