from locust import HttpUser, task, between

class CiberPymeUser(HttpUser):
    # Tiempo de espera aleatorio entre tareas (en segundos)
    wait_time = between(1, 5)

    @task
    def ver_inicio(self):
        self.client.get("/")

    @task
    def ver_login(self):
        self.client.get("/login/")
