# Overview

This project is a simple task management board, where you can add tasks and epics and track the progress of the work.

# Dependencies

To run the project docker + docker-compose is required. Additionally, it's possible to run the project locally using python.
But this is not described in this readme (look into Makefile, and remember to set current values in .env file)

# How to run?

Copy [.env.example](.env.example) to .env file. The values in the [.env.example](.env.example)
are set, so you can run the project without the need of changing it, but you are welcome to do this ;-).

Next, run: `docker-compose up` and wait till docker image is built, it will take a few minutes.
The next run will not require building an image.

Now you can go to the page http://localhost and explore the page. The database is preloaded with data for you.

To log in use username: user and password: user or create your own user.

**Have fun!**
