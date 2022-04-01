import psutil, os, time


def uptime():
    p = psutil.Process(os.getpid())

    p.create_time()

    uptime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time()))

    return uptime