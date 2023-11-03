import os
import shlex, subprocess
from typing import Callable, Collection, Iterable, Literal, Any
from logging import getLogger

logger = getLogger(__name__)

class ParentConsole:
    def __init__(self, default_flags: int | None = None):
        self.children: list[subprocess.Popen] = []
        self.num_children = 0
        if default_flags is not None:
            self.default_flags = default_flags
        else:
            self.default_flags = subprocess.CREATE_NEW_CONSOLE

    def makeChild(
            self, 
            cmdline: str, 
            returncode: int = 0,
            stdin: subprocess._FILE = subprocess.PIPE,
            stdout: subprocess._FILE = subprocess.PIPE,
            stderr: subprocess._FILE = subprocess.PIPE,
            shell: bool = False,
            universal_newlines: bool | None = None,
            text: bool = True,
            encoding: None = None,
            errors: None = None,
    ) -> None:
        """
        Creates child process from `cmdline` and appends to children list.
        """
        args = shlex.split(cmdline)
        process = subprocess.Popen(
            args, 
            shell=shell, 
            stdin=stdin, 
            stdout=stdout, 
            stderr=stderr,
            universal_newlines=universal_newlines,
            text=text,
            encoding=encoding,
            errors=errors,
            startupinfo=self.default_flags
        )
        process.returncode = returncode
        if process.poll() is None:
            logger.info("ParentConsole: started process %s" % cmdline)
            self.children.append(process)
            self.num_children += 1
            logger.info("ParentConsole: number of processes %d" % self.num_children)

    def clearDone(self) -> None:
        """
        Removes finished Popen objects from children list.
        """
        done = []
        for i in range(self.num_children):
            if self.isDone(i):
                logger.info("Tagged process %d for removal" % i)
                done.append(i)
        for i in done[::-1]:
            del self.children.pop(i)

    def isDone(self, index: int) -> bool:
        """
        Returns whether the `index`-th process has finished.
        """
        return self.children[index].poll() is not None
    
    def poll(self, index: int) -> int | None:
        """
        Returns `index`-th process' status. If not terminated, returns None.
        """
        return self.children[index].poll()

    def wait(
            self, 
            index: int, 
            timeout: float | None = None, 
            kill_on_timeout: bool = False
    ) -> int:
        """
        Waits for `index`-th process to finish.
        If process hasn't terminated after `timeout` seconds and `kill_on_timeout` is True, process is killed.
        Returns process' `returncode` attribute.
        """
        try:
            self.children[index].wait(timeout)
        except subprocess.TimeoutExpired:
            if kill_on_timeout:
                self.children[index].kill()
                return self.children[index].wait()
            return None
    
    def communicate(
            self, 
            index: int, 
            input: str | None = None, 
            timeout: float | None = None,
            timeout_callback: Callable | None = None,
            timeout_callback_args: Iterable[Any] | None = None,
            timeout_callback_kwargs: dict[Any] | None = None
    ) -> tuple[str, str]:
        """
        Sends `input` to the `index`-th process stdin channel and waits for process to terminate.
        If streams were opened in text mode, `input` should be a string. Otherwise, it must be bytes.
        If process doesn't terminate after `timeout` seconds, kills process and executes callback.
        Returns tuple with `(stdout_data, stderr_data)` in the form of strings.
        """
        try:
            (stdout_data, stderr_data) = self.children[index].communicate(input, timeout)
            return (stdout_data, stderr_data)
        except subprocess.TimeoutExpired:
            self.children[index].kill()
            (stdout_data, stderr_data) = self.children[index].communicate(input, timeout)
            if timeout_callback is not None:
                timeout_callback(*timeout_callback_args, **timeout_callback_kwargs)
            return (stdout_data, stderr_data)
    
    def sendSignal(self, index: int, signal) -> None:
        """
        Sends signal `signal` to `index`-th process.
        """
        self.children[index].send_signal(signal)

    def terminate(self, index: int) -> None:
        """
        Terminates `index`-th process.
        """
        self.children[index].terminate()

    def kill(self, index: int) -> None:
        """
        Kills `index`-th process.
        """
        self.children[index].kill()
        
class Redirect:
    """
    Mapper class to redirect `stderr`.
    """

    def __init__(self, func: Callable) -> 'Redirect':
        self.func = func
    
    def write(self, line: str) -> None:
        self.func(line)

class MP(ParentConsole):
    def __init__(self):
        super().__init__()
        self.command: str = ''

    def mpConnect(self, auto: bool = True, port: str | None = None, id: str | None = None):
        """
        ...
        """
        pass

    def mpListDevices(self):
        """
        ...
        """
        pass

    def mpReset(self, soft: bool = True):
        """
        ...
        """
        pass

def main():
    remote = MP()


if __name__=="__main__":
    main()