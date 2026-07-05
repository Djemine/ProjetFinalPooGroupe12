import customtkinter as ctk

from desktop_client.assets.api_client import ApiClient
from desktop_client.views.login_view import LoginFrame
from desktop_client.views.menu_principal_view import MenuPrincipalView


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rakieta Transport")
        self.geometry("1200x750")

        self.api_client = ApiClient()

        self.frame_actuelle = None
        self.afficher_login()

    def afficher_login(self):
        if self.frame_actuelle:
            self.frame_actuelle.destroy()

        self.frame_actuelle = LoginFrame(
            self,
            self.api_client,
            self.connexion_reussie
        )
        self.frame_actuelle.pack(fill="both", expand=True)

    def connexion_reussie(self, admin):
        if self.frame_actuelle:
            self.frame_actuelle.destroy()

        self.frame_actuelle = MenuPrincipalView(
            self,
            self.api_client,
            admin,
            self.afficher_login
        )

        self.frame_actuelle.pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = Application()
    app.mainloop()