policies = ({}
    #{% for src in tags %}
    #{% for item in dst %}
    #{"src": "{{ src }}", "dst": "{{ item }}"},
   # {% endfor %}
    #{% endfor %}
)


def check_operation(id, details) -> bool:
    """ Проверка возможности совершения обращения. """
    src: str = details.get("source")
    dst: str = details.get("deliver_to")

    if not all((src, dst)):
        return False

    print(f"[info] checking policies for event {id}, {src}->{dst}")

    return {"src": src, "dst": dst} in policies