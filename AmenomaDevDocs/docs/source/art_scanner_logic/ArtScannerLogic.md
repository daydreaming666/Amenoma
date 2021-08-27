# ArtScannerLogic类

该类包含扫描原神背包界面的执行逻辑，包括逐行扫描圣遗物、模拟滚动鼠标、对齐首行等。

## 方法

### \__init__

构造函数。

```python
def __init__(self, game_info: GameInfo)
```

#### 参数

``game_info``

一个``GameInfo``类型（参考[GameInfo](/source/art_scanner_logic/GameInfo)）的实例，表示原神窗口数据。

---

### interrupt

终止逐行扫描圣遗物。

```python
def interrupt(self)
```

#### 参数

无

#### 返回值

无

---

### waitSwitched

鼠标点击下一个圣遗物后，等待切换动画完成。

```python
def waitSwitched(
    self,
    art_center_x: float,
    art_center_y: float,
    min_wait: float = 0.1,
    max_wait: float = 3,
    condition = lambda pix: xum(pix) / 3 > 200
)
```

#### 参数

``art_center_x``

点击的圣遗物图标水平坐标的中心位置，用于计算圣遗物切换动画是否完成。

``art_center_y``

点击的圣遗物图标垂直坐标的中心位置，用于计算圣遗物切换动画是否完成。

``min_wait``

最小等待时间。该函数采用不断循环监测的方法判断切换动画是否完成，该值表示两次循环检测的最小间隔，单位为秒。

``max_wait``

最大等待时间。若循环等待时间超过``max_wait``，则返回``False``，表示未检测到切换。

``condition``

等待切换的条件。若指定像素满足``condition``，即``condition(pix)``返回``True``，则认为切换完成。

#### 返回值

如果超时前检测到切换完成，则返回``True``，否则返回``False``。注意，如果下一个位置没有圣遗物，也会返回``False``。

---

### getArtCenter

获取圣遗物的中心坐标.

```python
def getArtCenter(self, row: int, col: int)
```

#### 参数

``row``

表示圣遗物在背包第``row``行。注意``row``从0开始计数。

``col``

表示圣遗物在背包第``col``列。注意``col``从0开始计数。

#### 返回值

返回两个``float``，第一个为圣遗物中心的横坐标，第二个为圣遗物中心的纵坐标。

---

### scanRows

扫描原神窗口，捕获窗口图片并调用回调函数。

```python
def scanRows(self, rows: int, callback: lambda)
```

#### 参数

``rows``

要扫描的行数。该函数从背包的第0行开始扫描。

``callback``

回调函数，接受一个``PIL.Image``参数。每扫描完一个圣遗物的信息，就将圣遗物详情界面图片传入``callback``。

#### 返回值

若整个页面的所有圣遗物均扫描完成，返回``True``，否则返回``False``。

注意，若最后一行的圣遗物不满或者被其他线程调用了``interrupt``，该函数也会返回``False``。

---

### alignFirstRow

对齐背包界面的第一行。

```python
def alignFirstRow(self)
```

#### 参数

无

#### 返回值

无

---

### scrollToRow

滚动至背包界面的第``target_row``行。

```python
def scrollToRow(
    self,
    target_row: int,
    max_scrolls: int = 20,
    extra_scroll: int = 0,
    interval: float = 0.05
)
```

#### 参数

``target_row``

要滚动到的目标行。

``max_scrolls``

最多滚动的行数。

``extra_scroll``

每次滚动后要额外滚动的行数。

``interval``

两次滚动之间的间隔。
