#!/bin/bash
source /opt/venv/bin/activate

cd /code
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app
# source /opt/venv/bin/activate

# cd /code
# # Run_Port:- 8080 is the default value set for the port. 
# RUN_PORT=${PORT:-8000}
# # Run_Host:- The Symbol :- Stands for the default variable value if nothing is found
# RUN_HOST=${HOST:-0.0.0.0}

# gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app
#!/bin/bash

# gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app
# gunicorn — a production-grade server (more robust than plain uvicorn)
# -k uvicorn.workers.UvicornWorker — tells gunicorn to use uvicorn under the hood (so you get the best of both)
# -b $RUN_HOST:$RUN_PORT — binds to the host and port defined above
# main:app — same as before, your main.py file and app instance