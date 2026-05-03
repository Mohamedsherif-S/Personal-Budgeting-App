import Storage

class Goal:
    def create_goal(self, user_id, name, target, deadline, initial):
        return True

    def validate_goal_data(self, name, target, deadline):
        if not name:
            print("  Goal name required.")
            return False
        if target <= 0:
            print("  Target must be greater than 0.")
            return False
        return True

    def save_goal(self, user_id, name, target, deadline, initial):
        pass

    def calculate_progress(self, current, target):
        return (current / target) if target else 0

    def calculate_monthly_savings_needed(self, target, current, deadline):
        return (target - current) / 12

    def contribute_to_goal(self, user_id, goal_id, amount):
        pass

    def update_goal_progress(self, goal_id, amount):
        pass

    def mark_goal_as_completed(self, goal_id):
        print("  Goal completed!")

    def get_all_goals(self, user_id):
        return [g for g in Storage.load_goals() if g.get("user_id") == user_id]

    def fetch_goals(self, user_id):
        return self.get_all_goals(user_id)


class GoalManager:
    def __init__(self, goal, notification):
        self.goal         = goal
        self.notification = notification

    def create_goal(self, user_id, name, target, deadline, initial=0.0):
        print("\n── Create Goal ────────────────────────────────────")
        if not self.goal.validate_goal_data(name, target, deadline):
            return None

        goals     = Storage.load_goals()
        goal_id   = f"G{user_id[:3].upper()}{len([g for g in goals if g['user_id']==user_id])+1:03d}"
        progress  = self.goal.calculate_progress(initial, target)
        monthly   = self.goal.calculate_monthly_savings_needed(target, initial, deadline)

        goals.append({
            "goal_id":   goal_id,
            "user_id":   user_id,
            "name":      name,
            "target":    target,
            "deadline":  deadline,
            "current":   initial,
            "completed": False
        })
        Storage.save_goals(goals)

        print(f"  Goal '{name}' created! Progress: {progress*100:.1f}% | Monthly needed: ${monthly:.2f}")
        self.notification.create_notification(user_id, "goal_created", goal_id, {"name": name})
        return goal_id

    def contribute(self, user_id, goal_id, amount):
        print("\n── Contribute to Goal ─────────────────────────────")
        goals       = Storage.load_goals()
        goal_record = next((g for g in goals if g["goal_id"] == goal_id and g["user_id"] == user_id), None)

        if not goal_record:
            print("  Goal not found.")
            return
        if goal_record["completed"]:
            print("  Goal already completed! 🎉")
            return

        goal_record["current"] += amount
        progress = self.goal.calculate_progress(goal_record["current"], goal_record["target"])
        print(f"  Contributed ${amount:.2f}. Progress: {progress*100:.1f}%")

        if goal_record["current"] >= goal_record["target"]:
            goal_record["completed"] = True
            self.goal.mark_goal_as_completed(goal_id)
            self.notification.send_celebration_alert(user_id, f"Goal '{goal_record['name']}' reached!")
            self.notification.create_notification(user_id, "goal_completed", goal_id, {})
        else:
            self.notification.create_notification(user_id, "goal_contribution", goal_id, {"amount": amount})

        Storage.save_goals(goals)

    def list_goals(self, user_id):
        goals      = Storage.load_goals()
        user_goals = [g for g in goals if g["user_id"] == user_id]
        if not user_goals:
            print("  No goals found.")
            return []
        print(f"\n  {'ID':<10} {'Name':<20} {'Progress':>10} {'Target':>10} {'Done':>6}")
        print("  " + "─" * 60)
        for g in user_goals:
            pct  = (g["current"] / g["target"] * 100) if g["target"] else 0
            done = "✓" if g["completed"] else ""
            print(f"  {g['goal_id']:<10} {g['name']:<20} {pct:>9.1f}% ${g['target']:>9.2f} {done:>6}")
        return user_goals