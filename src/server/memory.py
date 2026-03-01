import os

def mem(size="rss"):
    """Generalization; memory sizes: rss, rsz, vsz."""
#    time.sleep(0.5)
    return int(os.popen('ps -p %d -o %s | tail -1' %
                        (os.getpid(), size)).read())

def rss():
    """Return ps -o rss (resident) memory in kB."""
    return mem("rss")

def rsz():
    """Return ps -o rsz (resident + text) memory in kB."""
    return mem("rsz")

def vsz():
    """Return ps -o vsz (virtual) memory in kB."""
    return mem("vsz")