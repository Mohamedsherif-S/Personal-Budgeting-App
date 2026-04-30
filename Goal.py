"""
Goal.py — Contains Goal class and GoalManager for User Story 7: Set and Track Financial Goals.

Sequence diagram trace:
  User creates goal:
    → Goal.createGoal() → Goal.validateGoalData() → Goal.saveGoal()
    → Goal.calculateProgress()
    → Goal.calculateMonthlySavingsNeeded()

  User contributes to goal:
    → Goal.contributeToGoal() → Goal.updateGoalProgress()
    → Goal.calculateProgress()
    → Goal.markGoalAsCompleted()   ← only when target reached
    → Notification.createNotification()
"""

import datetime
import Storage


class Goal:
    """
    Represents financial goals.
    """

    def create_goal(self, user_id, name, target, deadline, initial):
        return True

    def validate_goal_data(self, name, target, deadline):
        return True

    def save_goal(self, user_id, name, target, deadline, initial):
        pass

    def calculate_progress(self, current, target):
        return current / target

    def calculate_monthly_savings_needed(self, target, current, deadline):
        return (target - current) / 12

    def contribute_to_goal(self, user_id, goal_id, amount):
        pass

    def update_goal_progress(self, goal_id, amount):
        pass

    def mark_goal_as_completed(self, goal_id):
        print("Goal completed")

    def get_all_goals(self, user_id):
        return []

    def fetch_goals(self, user_id):
        return []


class GoalManager:
    """
    Orchestrates goal creation and contribution flows.
    Delegates to the existing Goal and Notification class instances.
    """

    def __init__(self, goal, notification):
        self.goal = goal
        self.notification = notification

    # ─────────────────────────────────────────────────────────────────────────
    #  Create a new goal
    # ─────────────────────────────────────────────────────────────────────────

    def create_goal(self, user_id, name, target, deadline, initial=0.0):
        """
        Full goal-creation flow (sequence diagram US-7).
        Returns the new goal's id, or None on failure.
        """
        print("\n── Create Goal ────────────────────────────────────")

        # Step 1 — Validate goal data (sequence diagram)
        valid = self.goal.validate_goal_data(name, target, deadline)
        if not valid:
            print("  [GoalManager] Invalid goal data — aborting.")
            return None

        # Step 2 — Persist & register (sequence diagram: saveGoal)
        goal_id = self._next_goal_id(user_id)
        self.goal.save_goal(user_id, name, target, deadline, initial)

        goal_record = {
            "goal_id":  goal_id,
            "user_id":  user_id,
            "name":     name,
            "target":   target,
            "deadline": deadline,
            "current":  initial,
            "completed": False
        }
        self._persist_goal(goal_record)

        # Step 3 — Show progress snapshot (sequence diagram)
        progress = self.goal.calculate_progress(initial, target)
        monthly  = self.goal.calculate_monthly_savings_needed(target, initial, deadline)
        print(f"  [GoalManager] Goal '{name}' created!")
        print(f"  [GoalManager] Progress: {progress*100:.1f}%  |  Monthly savings needed: ${monthly:.2f}")

        # Step 4 — Notify user
        self.notification.create_notification(
            user_id,
            n_type="goal_created",
            ref_id=goal_id,
            data={"name": name, "target": target}
        )

        return goal_id

    # ─────────────────────────────────────────────────────────────────────────
    #  Contribute to an existing goal
    # ─────────────────────────────────────────────────────────────────────────

    def contribute(self, user_id, goal_id, amount):
        """
        Add funds to a goal (sequence diagram US-7 contribution flow).
        """
        print("\n── Contribute to Goal ─────────────────────────────")

        goals = Storage.load_goals()
        goal_record = self._find_goal(goals, goal_id, user_id)

        if goal_record is None:
            print("  [GoalManager] Goal not found.")
            return

        if goal_record["completed"]:
            print("  [GoalManager] This goal is already completed! 🎉")
            return

        # Step 1 — Contribute (sequence diagram: contributeToGoal)
        self.goal.contribute_to_goal(user_id, goal_id, amount)

        # Step 2 — Update stored progress (sequence diagram: updateGoalProgress)
        goal_record["current"] += amount
        self.goal.update_goal_progress(goal_id, amount)

        current = goal_record["current"]
        target  = goal_record["target"]

        # Step 3 — Recalculate progress (sequence diagram: calculateProgress)
        progress = self.goal.calculate_progress(current, target)
        print(f"  [GoalManager] Contributed ${amount:.2f}. Progress: {progress*100:.1f}%")

        # Step 4 — Check for completion (sequence diagram: markGoalAsCompleted)
        if current >= target:
            goal_record["completed"] = True
            self.goal.mark_goal_as_completed(goal_id)

            # Step 5 — Celebrate notification (sequence diagram)
            self.notification.send_celebration_alert(
                user_id,
                f"You've reached your goal: '{goal_record['name']}'!"
            )
            self.notification.create_notification(
                user_id,
                n_type="goal_completed",
                ref_id=goal_id,
                data={"name": goal_record["name"]}
            )
        else:
            # Regular progress notification
            self.notification.create_notification(
                user_id,
                n_type="goal_contribution",
                ref_id=goal_id,
                data={"amount": amount, "progress": progress}
            )

        # Persist updated goal list
        Storage.save_goals(goals)

    # ─────────────────────────────────────────────────────────────────────────
    #  View all goals for a user
    # ─────────────────────────────────────────────────────────────────────────

    def list_goals(self, user_id):
        """Return and display all goals belonging to this user."""
        goals = Storage.load_goals()
        user_goals = [g for g in goals if g["user_id"] == user_id]

        if not user_goals:
            print("  [GoalManager] No goals found.")
            return []

        print(f"\n  {'ID':<6} {'Name':<20} {'Progress':>10} {'Target':>10} {'Done':>6}")
        print("  " + "─" * 56)
        for g in user_goals:
            pct  = (g["current"] / g["target"] * 100) if g["target"] else 0
            done = "✓" if g["completed"] else ""
            print(f"  {g['goal_id']:<6} {g['name']:<20} {pct:>9.1f}% ${g['target']:>9.2f} {done:>6}")

        return user_goals

    # ─────────────────────────────────────────────────────────────────────────
    #  Private helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _persist_goal(self, goal_record):
        goals = Storage.load_goals()
        if isinstance(goals, dict):
            goals = list(goals.values()) if goals else []
        if not isinstance(goals, list):
            goals = []
        goals.append(goal_record)
        Storage.save_goals(goals)

    def _find_goal(self, goals, goal_id, user_id):
        for g in goals:
            if g["goal_id"] == goal_id and g["user_id"] == user_id:
                return g
        return None

    def _next_goal_id(self, user_id):
        """Generate a simple sequential goal ID."""
        goals = Storage.load_goals()
        user_goals = [g for g in goals if g["user_id"] == user_id]
        return f"G{user_id[:3].upper()}{len(user_goals)+1:03d}"