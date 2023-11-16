import random
from locust import HttpUser, between, task

correo = "correo1@example.com"

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    
    def on_start(self):
        self.client.get("/auth/login")
        self.client.post("/auth/login", {
            "email": "test@gmail.com",
            "password": ""
        })
    
    @task
    def index(self):
        self.client.get("/")

        #Prueba para registro de usuarios
        email_seleccionado = correo.replace("1", str(random.randint(0, 999)))
        print(email_seleccionado)

        self.client.post("/auth/register", {
            "username": "pruebita",
            "email" : email_seleccionado,
            "password": "123457689@A",
            "selected_question": "¿Cuales nombre de tu restaurante favorito?",
            "recovery_answer": "MiRespuestaSecreta"
        })

    @task
    def about(self):
        self.client.get("/posts")
        self.client.get("/new/news")


