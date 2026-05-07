class Notification:
    """Handles system notifications and user alerts."""

    def create_notification(self, user_id, n_type, ref_id, data=None):
        """
        Logs a notification event in the console.
        Takes user info and notification type (e.g., goal_created).
        """
        print(f"  [Notification] {n_type}")

    def send_alert(self, user_id, message, priority="normal"):
        """
        Sends a standard text alert to the user.
        Priority can be set to 'high' or 'normal'.
        """
        print(f"  [Alert] {message}")

    def send_celebration_alert(self, user_id, message):
        """
        Displays a special formatted alert for positive milestones like reaching a goal.
        """
        print(f"  🎉 {message}")
