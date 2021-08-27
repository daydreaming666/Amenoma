# GameInfo类<!-- {docsify-ignore-all} -->

``GameInfo``类存储原神游戏窗口相关数据，包括位置坐标、长度、宽度等。

## 成员变量

|   属性  | 类型 | 说明 |
|--------|-----|-----|
|``hwnd``| ``win32api.HWND`` | 原神游戏窗口的Handle |
|``w``|``int``|原神游戏窗口像素宽度|
|``h``|``int``|原神游戏窗口像素高度|
|``left``|``int``|原神游戏窗口最左端坐标|
|``top``|``int``|原神游戏窗口最顶端坐标|
|``art_width``|``float``| 背包单个圣遗物图标像素宽度 |
|``art_height``|``float``| 背包单个圣遗物图标像素高度 |
|``art_expand``|``float``| 没整明白 |
|``art_gap_x``|``float``|背包圣遗物水平间隙像素宽度|
|``art_gap_y``|``float``|背包圣遗物垂直间隙像素宽度|
|``art_info_width``|``float``|背包圣遗物详情界面像素宽度|
|``art_info_height``|``float``|背包圣遗物详情界面像素高度|
|``left_margin``|``float``|背包圣遗物界面左侧空白像素宽度|
|``right_margin``|``float``|背包圣遗物图标界面至最右侧像素宽度|
|``info_margin``|``float``|没整明白|
|``art_rows``|``int``|背包圣遗物图标的行数|
|``art_cols``|``int``|背包圣遗物图标的列数|
|``art_shift``|``float``|背包圣遗物图标单列宽度 + 列间距，表示每次鼠标的水平偏移量|
|``first_art_x``|``float``|背包第一个圣遗物的横坐标|
|``first_art_y``|``float``|背包第一个圣遗物的垂直坐标|
|``art_info_top``|``float``|背包圣遗物详情界面顶端坐标|
|``art_info_left``|``float``|背包圣遗物详情界面左端坐标|
|``scroll_fin_keypt_x``|``float``|没整明白|
|``scroll_fin_keypt_y``|``float``|没整明白|
|``incomplete_lastrow``|``float``|没整明白|
