import Storage


class Admin:
    # This class handles admin-related actions such as notifications

    def notify_new_user(self, user_id, date):
        # Print a message to indicate a new user has been registered
        print(f"  [Admin] New user '{user_id}' registered on {date}.")

        # Load existing notifications from storage
        notifs = Storage.load_notifications()

        # Ensure that notifications are stored as a list
        if not isinstance(notifs, list):
            notifs = []

        # Add a new notification with user ID and registration date
        notifs.append({
            "type": "new_user",
            "user_id": user_id,
            "date": date
        })

        # Save the updated notifications list back to storage
        Storage.save_notifications(notifs)
