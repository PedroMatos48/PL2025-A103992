import time
import psutil
from PascalYacc import parser
from test import ex8, ex9, ex10, ex1, ex2, ex3
from ASTInterpreter import ASTInterpreter

def measure_interp(ex, runs=3):
    times = []
    mems = []
    for i in range(runs):
        process = psutil.Process()
        mem_before = process.memory_info().rss
        start = time.perf_counter()

        ast = parser.parse(ex)
        interp = ASTInterpreter()
        interp.interpret(ast)

        #interp.run()

        end = time.perf_counter()
        mem_after = process.memory_info().rss

        times.append(end - start)
        mems.append(mem_after - mem_before)

    avg_time = sum(times) / runs
    avg_mem = sum(mems) / runs / (1024*1024)

    filename = f"ex{i}.vm"

    with open(filename, "w") as f:
        for line in interp.result:
            f.write(line + "\n")

    return avg_time, avg_mem

def measure_external_compiler(command, runs=3):
    import subprocess

    times = []
    mems = []

    for _ in range(runs):
        start = time.perf_counter()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = psutil.Process(proc.pid)
        max_mem = 0

        while proc.poll() is None:
            try:
                mem = p.memory_info().rss
                if mem > max_mem:
                    max_mem = mem
            except psutil.NoSuchProcess:
                break
            time.sleep(0.01)

        proc.communicate()
        end = time.perf_counter()
        times.append(end - start)
        mems.append(max_mem / (1024*1024)) 

    avg_time = sum(times) / runs
    avg_mem = sum(mems) / runs
    return avg_time, avg_mem

if __name__ == "__main__":
    examples = [("ex1", ex1), ("ex2", ex2), ("ex3", ex3), ("ex8", ex8), ("ex9", ex9), ("ex10", ex10)]

    print("Benchmark do seu interpretador:")
    for name, code in examples:
        t, m = measure_interp(code)
        print(f"{name}: Tempo médio = {t:.4f} s, Memória média = {m:.11f} MB")

    print("\nBenchmark compilador externo (exemplo com fpc):")
    for name, code in examples:
        filename = f"{name}.pas"
        with open(filename, "w") as f:
            f.write(code)

        command = ["C:\\FPC\\3.2.2\\bin\\i386-win32\\fpc.exe", "-q", filename]

        t, m = measure_external_compiler(command)
        print(f"{name}: Tempo médio = {t:.4f} s, Memória média = {m:.3f} MB")