import Storage


class Admin:
    def notify_new_user(self, user_id, date):
        print(f"  [Admin] New user '{user_id}' registered on {date}.")
        notifs = Storage.load_notifications()
        if not isinstance(notifs, list):
            notifs = []
        notifs.append({"type": "new_user", "user_id": user_id, "date": date})
        Storage.save_notifications(notifs)
