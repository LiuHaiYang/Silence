#### asyncio

- asyncio 是python3.4 版本引入的标准库，直接内置了对异步IO的支持
- asyncio的编程模型就是一个消息循环。
我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。

#### 小结

---
- asyncio提供了完善的异步IO支持；
- 异步操作需要在coroutine中通过yield from完成；
- 多个coroutine可以封装成一组Task然后并发执行。

#### async/await

- 用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。

- 为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

- 请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

    - 把@asyncio.coroutine替换为async；
    - 把yield from替换为await。