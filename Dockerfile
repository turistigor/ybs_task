FROM snakepacker/python:all as builder

RUN python3.8 -m venv /usr/share/python3/ybs_task
RUN /usr/share/python3/ybs_task/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/ybs_task/bin/pip install -Ur /mnt/requirements.txt

COPY dist/ /mnt/dist/

# install my app at the known place
RUN /usr/share/python3/ybs_task/bin/pip install /mnt/dist/* \ 
    --target /usr/share/python3/ybs_task/ybs_task \
    && /usr/share/python3/ybs_task/bin/pip check


FROM snakepacker/python:3.8 as api

COPY --from=builder /usr/share/python3/ybs_task /usr/share/python3/ybs_task

COPY wait-for-it.sh /usr/share/python3/ybs_task
USER root
RUN chmod ugo=rwx /usr/share/python3/ybs_task/wait-for-it.sh

# make my app visible for django
ENV PYTHONPATH "${PYTHONPATH}:/usr/share/python3/ybs_task/ybs_task"

# run django server on '0.0.0.0:80'
CMD ["/usr/share/python3/ybs_task/bin/python3.8", \
     "/usr/share/python3/ybs_task/ybs_task/bin/manage.py",  \
     "runserver", "0.0.0.0:80"]
