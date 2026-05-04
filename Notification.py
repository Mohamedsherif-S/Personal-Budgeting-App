class Notification:
    def create_notification(self, user_id, n_type, ref_id, data=None):
        print(f"  [Notification] {n_type}")

    def send_alert(self, user_id, message, priority="normal"):
        print(f"  [Alert] {message}")

    def send_celebration_alert(self, user_id, message):
        print(f"  🎉 {message}")
