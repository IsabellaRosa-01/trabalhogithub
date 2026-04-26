FROM python:3
<<<<<<< Updated upstream

WORKDIR /usr/src/app

COPY . .

=======
WORKDIR /usr/src/app
COPY . .
>>>>>>> Stashed changes
CMD ["python", "main.py"]
