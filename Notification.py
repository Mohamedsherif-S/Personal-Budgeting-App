class Notification:
    """
    Handles notifications.
    """

    def create_notification(self, user_id, n_type, ref_id, data=None):
        print("Notification created")

    def send_alert(self, user_id, message, priority):
        print("Alert:", message)

    def setup_budget_alert(self, user_id, budget_id, threshold):
        pass

    def configure_alert_rules(self, budget_id, threshold, frequency):
        pass

    def send_celebration_alert(self, user_id, message):
        print("🎉", message)