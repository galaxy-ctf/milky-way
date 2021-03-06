FROM quay.io/erasche/docker-django:3.5

# Add our project to the /app/ folder
ADD . /app/
# Install dependencies
RUN pip install -r /app/requirements.txt
# Set current working directory to /app
WORKDIR /app/

# Fix permissions on folder while still root, and collect static files for use
# if need be.
RUN chown -R django /app && \
	python manage.py collectstatic --noinput

# Drop permissions
RUN printf '#!/bin/bash\ncrond -l 4 -L /var/log/cron.log\n' > /docker/docker-entrypoint.d/cron.sh
ADD crontab /var/spool/cron/crontabs/django
