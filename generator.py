import os, shutil
def gen_make(name):
    makefile = f"""SHELL := bash\n\nMODULES := monitor \ \n"""

    for i in range (1, len(name)):
        if i == len(name)-1:
            makefile = makefile + f"\t\t{name[i]}\n"
        else:
            makefile = makefile + f"\t\t{name[i]} \\\n"

    makefile = makefile + """\nSLEEP_TIME := 5

    all:
        docker-compose up --build -d
        sleep ${SLEEP_TIME}

        for MODULE in ${MODULES}; do \\
            echo Creating $${MODULE} topic; \\
            docker exec broker \\
                kafka-topics --create --if-not-exists \\
                --topic $${MODULE} \\
                --bootstrap-server localhost:9092 \\
                --replication-factor 1 \\
                --partitions 1; \\
        done
        
    clean:
	    docker-compose down"""

    temp = open(f"{name[0]}/Makefile", "w")
    temp.write(makefile)
    temp.close()

def gen_conf(name):
    conf = f"""[default]\nbootstrap.servers=broker:9092\nauto.offset.reset=earliest\n\n[monitor]\ngroup.id=monitor\n"""

    for i in range(1, len(name)):
        conf = conf + f"\n[{name[i]}]\ngroup.id={name[i]}\n"
    temp = open(f"{name[0]}/shared/config.ini", "w")
    temp.write(conf)
    temp.close()



with open('data.txt', 'r') as file:
    name = [line.replace('\n', '') for line in file]

try: 
    shutil.copytree('source', name[0])
    gen_make(name)
    gen_conf(name)
except OSError:
    print('restart')
    shutil.rmtree(name[0])

