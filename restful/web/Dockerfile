# we have a machine running ubuntu with python3
# our working directory is /usr/src/app
# like using virtual box and install ubuntu and python(puthon image has ubuntu) on it.
FROM python:3
WORKDIR /usr/src/app


# Copying a new file from my machine(requirments.txt) to new machine (.)
COPY requirements.txt .
# install the requirments to the new machine
RUN pip install --no-cache-dir -r requirements.txt


# copying all the files (app.py,requirments.txt,.....) 
# to the new machine (this machine)
COPY . .
# first part (first .) means what on our machine right now
# second part (second .) means whats going into the machine
# introduced virtual box to app.py


# run the command to the new machine
# hey python, run this command to the new machine
CMD [ "python", "app.py" ]


# Process of building the new computer/system from scratch.
# here we are building a machine with a web appplication








