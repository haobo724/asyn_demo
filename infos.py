import tkinter as tk
import time
import asyncio
import threading
import queue
import numpy as np
from contextlib import suppress

q = queue.Queue()
stop_event = threading.Event()


class Form:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title('asyn——test')

        self.button = tk.Button(self.root, text="Testbutton1", command=self.change_form_state)
        self.button2 = tk.Button(self.root, text="Testbutton2", command=self.dummy_func2)
        # self.button3 = tk.Button(self.root, text="Close", command=self.root.quit)
        self.button3 = tk.Button(self.root, text="Close", command=self.shut_down)
        self.label = tk.Label(master=self.root, text="label1")
        self.label2 = tk.Label(master=self.root, text="label2")

        self.button.pack()
        self.label.pack()
        self.button2.pack()
        self.button3.pack()
        self.label2.pack()
        self.new_loop = asyncio.new_event_loop()
        self.new_loop2 = asyncio.new_event_loop()
        self.t = threading.Thread(target=self.get_loop, args=(self.new_loop,), name='thread1')  # 通过当前线程开启新的线程去启动事件循环
        self.t2 = threading.Thread(target=self.get_loop, args=(self.new_loop2,), name='thread2')  # 通过当前线程开启新的线程去启动事件循环
        self.t.daemon = 1
        self.t2.daemon = 1
        self.t.start()
        self.t2.start()
        self.root.mainloop()

    async def dummy_func1(self, text):

        await asyncio.sleep(1)
        self.label["text"] = text
        q.put(lambda: self.show())

        print(time.time())


    def dummy_func2(self):
        coroutine = self.dummy_func3('信号')
        stop_event.clear()
        asyncio.run_coroutine_threadsafe(coroutine,self.new_loop2)  # 这几个是关键，代表在新线程中事件循环不断“游走”执行

    async def dummy_func3(self, text):
        self.label2["text"] = text
        while not stop_event.is_set():
            print('what1!')

    def show(self):
        self.label2["text"] = 'show'

    def get_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def change_form_state(self):
        coroutine1 = self.dummy_func1(200)
        # asyncio.run_coroutine_threadsafe(coroutine1, self.new_loop)  # 这几个是关键，代表在新线程中事件循环不断“游走”执行
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coroutine1)

    def shut_down(self):
        # self.t.join()
        # loop = asyncio.get_event_loop()
        #
        stop_event.set()
        # pending = asyncio.all_tasks()
        # for task in pending:
        #     task.cancel()
        #     # Now we should await task to execute it's cancellation.
        #     # Cancelled task raises asyncio.CancelledError that we can suppress:
        #     with suppress(asyncio.CancelledError):
        #         self.new_loop.run_until_complete(task)
        self.root.quit()
if __name__ == '__main__':
    form = Form()
