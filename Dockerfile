FROM snakepacker/python:all as builder

RUN python3.8 -m venv /usr/share/python3/ybs_task
RUN /usr/share/python3/ybs_task/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/ybs_task/bin/pip install -Ur /mnt/requirements.txt

COPY dist/ /mnt/dist/
RUN /usr/share/python3/ybs_task/bin/pip install /mnt/dist/* --target /usr/share/python3/ybs_task/ybs_task \
    && /usr/share/python3/ybs_task/bin/pip check

FROM snakepacker/python:3.8 as api

COPY --from=builder /usr/share/python3/ybs_task /usr/share/python3/ybs_task

#RUN ln -snf /usr/share/python3/ybs_task/bin/analyzer-* /usr/local/bin/

ENV PYTHONPATH "${PYTHONPATH}:/usr/share/python3/ybs_task/ybs_task"

CMD ["/usr/share/python3/ybs_task/bin/python3.8", "/usr/share/python3/ybs_task/ybs_task/bin/manage.py", "runserver", "0.0.0.0:8000"]
