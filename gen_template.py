from jinja2 import Environment, FileSystemLoader
import json, os, shutil

env = Environment(loader=FileSystemLoader('template'))

def gen_make(data):
    template = env.get_template('Makefile')
    name = data["name_solution"]
    module = data["module"]
    tags = module["tag"]
    with open(f"{name}/Makefile", 'w') as f:
        f.write(template.render(tags=tags))

def gen_conf(data):
    template = env.get_template('config.ini')
    name = data["name_solution"]
    module = data["module"]
    tags = module["tag"]
    with open(f"{name}/shared/config.ini", 'w') as f:
        f.write(template.render(tags=tags))

def gen_docker_compose(data):
    template = env.get_template('docker-compose.yml')
    name = data["name_solution"]
    module = data["module"]
    tags = module["tag"]
    with open(f"{name}/docker-compose.yml", 'w') as f:
        f.write(template.render(name=name, tags=tags))

def gen_module(data):
    name = data["name_solution"]
    module = data["module"]
    tags = module["tag"]
    for tag in tags:
        os.mkdir(f"{name}/modules/{tag}")
        os.mkdir(f"{name}/modules/{tag}/config")
        os.mkdir(f"{name}/modules/{tag}/module")

        template = env.get_template('Dockerfile')
        with open(f"{name}/modules/{tag}/Dockerfile", 'w') as f:
            f.write(template.render())

        template = env.get_template('start.py')
        with open(f"{name}/modules/{tag}/start.py", 'w') as f:
            f.write(template.render())
        
        template = env.get_template('req-docker.txt')
        with open(f"{name}/modules/{tag}/config/requirements.txt", 'w') as f:
            f.write(template.render())
        
        template = env.get_template('init.py')
        with open(f"{name}/modules/{tag}/module/__init__.py", 'w') as f:
            f.write(template.render())

        template = env.get_template('consumer.py')
        with open(f"{name}/modules/{tag}/module/consumer.py", 'w') as f:
            f.write(template.render())

        template = env.get_template('producer.py')
        with open(f"{name}/modules/{tag}/module/producer.py", 'w') as f:
            f.write(template.render())

def gen_polices(data):
    template = env.get_template('policies.py')
    name = data["name_solution"]
    module = data["module"]
    #tags = module["tag"]
    #dst = module["dst"]
    with open(f"{name}/modules/monitor/module/policies.py", 'w') as f:
        f.write(template.render())

def gen():
    with open('data.json') as f:
        data = json.load(f)
    try: 
        shutil.copytree('source', data["name_solution"])
        gen_make(data)
        gen_conf(data)
        gen_docker_compose(data)
        gen_module(data)
        gen_polices(data)
        return("Created")
    except OSError:
        shutil.rmtree(data["name_solution"])
        return("Clear solution")