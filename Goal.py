import Storage

class Goal:
    """Class to handle goal logic like validation and progress calculations."""

    def validate_goal_data(self, name, target, deadline):
        """Checks if goal name exists and target is a positive number."""
        if not name:
            print("  Goal name required.")
            return False
        if target <= 0:
            print("  Target must be greater than 0.")
            return False
        return True

    def calculate_progress(self, current, target):
        """Calculates percentage of goal completion."""
        return (current / target) if target else 0

    def calculate_monthly_savings_needed(self, target, current, deadline):
        """Estimate how much to save monthly (simplified to 12 months)."""
        return (target - current) / 12

    def mark_goal_as_completed(self, goal_id):
        """Prints a success message when a goal is reached."""
        print("  Goal completed! 🎉")

    def get_all_goals(self, user_id):
        """Fetches all goals linked to a specific user ID."""
        return [g for g in Storage.load_goals() if g.get("user_id") == user_id]


class GoalManager:
    """Manages goal operations like creation, contributions, and listing."""

    def __init__(self, goal, notification):
        """Initializes with goal logic and notification services."""
        self.goal         = goal
        self.notification = notification

    def create_goal(self, user_id, name, target, deadline, initial=0.0):
        """
        Creates a new goal, calculates initial status, and saves it.
        Returns the new goal_id or None if validation fails.
        """
        print("\n── Create Goal ────────────────────────────────────")
        if not self.goal.validate_goal_data(name, target, deadline):
            return None

        goals   = Storage.load_goals()
        # Generate a simple unique ID based on user name and count
        goal_id = f"G{user_id[:3].upper()}{len([g for g in goals if g['user_id']==user_id])+1:03d}"
        progress = self.goal.calculate_progress(initial, target)
        monthly  = self.goal.calculate_monthly_savings_needed(target, initial, deadline)

        goals.append({
            "goal_id":   goal_id,
            "user_id":   user_id,
            "name":      name,
            "target":    float(target),
            "deadline":  deadline,
            "current":   float(initial),
            "completed": False,
        })
        Storage.save_goals(goals)
        print(f"  Goal '{name}' created! Progress: {progress*100:.1f}% | Monthly needed: ${monthly:.2f}")
        self.notification.create_notification(user_id, "goal_created", goal_id, {"name": name})
        return goal_id

    def contribute(self, user_id, goal_id, amount):
        """
        Adds money to a goal and checks if it's finished.
        Updates storage and sends relevant notifications.
        """
        print("\n── Contribute to Goal ─────────────────────────────")
        goals       = Storage.load_goals()
        goal_record = next(
            (g for g in goals if g["goal_id"] == goal_id and g["user_id"] == user_id), None
        )
        
        if not goal_record:
            print("  Goal not found.")
            return
        if goal_record["completed"]:
            print("  Goal already completed! 🎉")
            return

        # Update balance and check progress
        goal_record["current"] += float(amount)
        progress = self.goal.calculate_progress(goal_record["current"], goal_record["target"])
        print(f"  Contributed ${amount:.2f}. Progress: {progress*100:.1f}%")

        # Check if the goal is officially reached
        if goal_record["current"] >= goal_record["target"]:
            goal_record["completed"] = True
            self.goal.mark_goal_as_completed(goal_id)
            self.notification.send_celebration_alert(user_id, f"Goal '{goal_record['name']}' reached!")
            self.notification.create_notification(user_id, "goal_completed", goal_id, {})
        else:
            self.notification.create_notification(user_id, "goal_contribution", goal_id, {"amount": amount})

        Storage.save_goals(goals)

    def list_goals(self, user_id):
        """Displays all goals for a user in a formatted table."""
        user_goals = [g for g in Storage.load_goals() if g["user_id"] == user_id]
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
