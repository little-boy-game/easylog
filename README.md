# log 库 使用说明（精简与改进版）

这是一个轻量级的文件日志库说明，包含功能概览、用法示例以及注意事项。

## 概览
Logger 提供三种记录模式：
- imm — 立即写入：每次写入时以追加方式打开文件（线程安全）。
- alw — 持久打开：构造时以追加模式打开文件，需手动调用 close() 关闭（线程安全）。
- beh — 缓存记录：在内存中缓存日志，调用 save() 将所有记录写入文件（适合批量输出）。

每条日志的默认格式：
[(level) HH:MM:SS] message

支持的语言用于构造时的初始化提示：zh, en, es, fr, de, jp, ru, it, pt, kr。

## 各模式的优点与缺点

- imm（立即写入）
  - 优点：
    - 写入即时落盘，程序异常或崩溃时日志不易丢失。
    - 不需要管理文件句柄，使用简单。
    - 适合低频或对可靠性要求高的记录场景。
  - 缺点：
    - 每次写入都打开/关闭文件，性能开销较大（I/O 多）。
    - 在高并发或高频写入场景可能成为瓶颈。

- alw（持久打开）
  - 优点：
    - 打开一次复用文件句柄，写入性能优于 imm。
    - 适合长时间运行并频繁写日志的进程。
  - 缺点：
    - 需要手动 close()，否则可能导致文件句柄泄漏或数据未 flush。
    - 若程序异常退出且未 flush，部分日志可能丢失（取决于缓冲策略）。

- beh（缓存记录）
  - 优点：
    - 所有写操作只在内存完成，速度最快，适合批量写入或性能敏感场景。
    - 可以在 save() 时一次性写入，便于做合并、格式化或条件过滤。
  - 缺点：
    - 日志长期保存在内存，进程崩溃或未调用 save() 时会丢失数据。
    - 内存占用随日志量增长，需要注意内存管理。

## 构造与主要方法
构造函数：
```python
from log import Logger
lg = Logger(method="imm", logname="app.log", lang="zh")
```

主要方法：
- info(msg: str)
- warning(msg: str)
- error(msg: str)
- debug(msg: str)
- log(level: str, msg: str) — 自定义级别
- close() — 仅在 method=="alw" 时有效
- save() — 仅在 method=="beh" 时有效

所有写入操作由实例级 threading.Lock() 保护，支持多线程安全写入。

## 使用示例
立即写入模式：
```python
lg = Logger(method="imm", logname="app.log", lang="zh")
lg.info("程序启动")
lg.error("发生错误")
```

持久打开模式（记得 close）：
```python
lg = Logger(method="alw", logname="app_alw.log", lang="en")
lg.debug("调试信息")
lg.close()
```

缓存模式（批量写入）：
```python
lg = Logger(method="beh", logname="batch.log", lang="en")
lg.info("第一条")
lg.error("第二条")
lg.save()
```

## 依赖与注意事项
- 依赖：arrow（用于格式化时间）、threading（用于锁）。
- 在 alw 模式下确保在程序退出前调用 close()，避免文件句柄泄漏。
- 在 beh 模式下若不调用 save()，日志只保存在内存中不会写入磁盘。
- logname 支持相对路径与绝对路径；如果需要覆盖已有日志文件，选择合适的模式（imm 会追加，构造时若使用 "w" 打开则会覆盖，本库默认追加或按行为决定）。

## 常见错误
- 构造时 method 非法会抛出 ValueError（当前实现接受 imm / alw / beh）。
- 在非 alw 模式调用 close() 或在非 beh 模式调用 save() 将不会写入文件，请检查使用模式。

欢迎根据项目需要扩展级别格式、时间格式或增加轮转（rotation）功能。





