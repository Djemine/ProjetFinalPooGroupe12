"""
Service Dashboard : agrège des statistiques issues des autres services
pour alimenter le tableau de bord de l'application.
"""


class DashboardService:
    def __init__(self, compagnie_service, trajet_service, reservation_service):
        self.compagnie_service = compagnie_service
        self.trajet_service = trajet_service
        self.reservation_service = reservation_service

    def statistiques(self) -> dict:
        bus_liste = self.compagnie_service.lister_bus()
        trajets = self.trajet_service.lister_trajets()
        reservations = self.reservation_service.lister_reservations()
        reservations_actives = [r for r in reservations if not r.annulee]

        return {
            "nombre_bus": len(bus_liste),
            "nombre_trajets": len(trajets),
            "nombre_passagers": len(self.reservation_service.passagers),
            "nombre_reservations": len(reservations_actives),
            "places_disponibles": sum(bus.places_disponibles() for bus in bus_liste),
            "recettes_estimees": sum(r.trajet.prix for r in reservations_actives),
        }