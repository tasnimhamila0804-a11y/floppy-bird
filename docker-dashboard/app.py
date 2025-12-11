from flask import Flask, render_template
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    containers = []
    for c in client.containers.list():
        stats = c.stats(stream=False)
        containers.append({
            'name': c.name,
            'status': c.status,
            'cpu_percent': calculate_cpu(stats),
            'mem_usage': stats['memory_stats']['usage'],
            'mem_limit': stats['memory_stats']['limit']
        })
    return render_template('index.html', containers=containers)

def calculate_cpu(stats):
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100
    return round(cpu_percent, 2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
