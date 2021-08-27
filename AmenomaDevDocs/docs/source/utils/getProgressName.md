# getProgressName<!-- {docsify-ignore-all} -->

该函数根据``hwnd``获取进程的名称。

```python
def getProcessName(hwnd: win32api.HWND)
```

## 参数

``hwnd``

类型：**HWND**

待获取名称的进程窗口的Handle，不能为空。

## 返回值

类型：**str**

若成功则进程的名称，若失败则为``None``。

## 依赖

* ``win32api``
