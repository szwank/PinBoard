FROM python:3.11-slim as base

# switch to "builder" image. Image python:3.11 contains additional packages thus building is faster,
# but in the end we will use python:3.11-slim - end image will be smaller
FROM python:3.11 as builder

ARG REQUIREMENTS_FILE

# create directory to store built files, this data will be discarded after builds ends
RUN mkdir /install
WORKDIR /install

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# switch back to "master" image
FROM base

ARG APP_DIR=/opt/PinBoard

# set environment variables
ENV USING_DOCKER 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# where the code lives
WORKDIR $APP_DIR

# coppy installed dependencies from "build image"
COPY --from=builder /install /usr/local

# create directory for static files
RUN mkdir $APP_DIR/staticfiles

# copy project
COPY . .

# create the app user and make him the owner of workdir
RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --shell /bin/bash app \
    && chown -R app:app $APP_DIR \
    && chmod u+rx -R $APP_DIR

# change to the app user
USER app

# convert end of line in entrypoint.sh to linux. This is very important as the file
# with wrong end lines coding would not be visible. Additionally some of the editors
# change end of line coding automatically
RUN sed -i 's/\r$//' entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
