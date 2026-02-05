"""
Questionare for WMC26
"""
import json
import os
import datetime
from typing import List, Dict, Any

# --- CONSTANTS & CONFIGURATION ---
DATA_FILE = "survey_results.json"
DIVIDER = "=" * 50
SUB_DIVIDER = "-" * 50
"""
Servey app
"""
class SurveyApp:
    def __init__(self):
        self.results = []
        self.load_data()

    def load_data(self):
        """Load existing survey data from a JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.results = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.results = []

    def save_data(self, entry: Dict[str, Any]):
        """Append new entry and save to disk."""
        self.results.append(entry)
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.results, f, indent=4)
        except IOError as e:
            print(f"\n[ERROR] Could not save data: {e}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_input(self, prompt: str, options: List[str] = None, is_numeric: bool = False):
        """A robust input handler with validation."""
        while True:
            suffix = f" ({'/'.join(options)})" if options else ""
            user_input = input(f"{prompt}{suffix}: ").strip()

            if not user_input:
                print(">> Input cannot be empty.")
                continue

            if is_numeric:
                try:
                    val = int(user_input)
                    if 1 <= val <= 10:
                        return val
                    print(">> Please enter a number between 1 and 10.")
                    continue
                except ValueError:
                    print(">> Invalid number format.")
                    continue

            if options:
                # Check for case-insensitive match
                match = next((opt for opt in options if opt.lower() == user_input.lower()), None)
                if match:
                    return match
                print(f">> Invalid choice. Please select from {options}.")
                continue

            return user_input

    def run_survey(self):
        """The main survey logic flow."""
        self.clear_screen()
        print(DIVIDER)
        print("   CYBERSECURITY TOOLING & QA INSIGHTS SURVEY   ")
        print(DIVIDER)

        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "responses": {}
        }
        resp = entry["responses"]

        # Question 1: Core usage
        q1 = self.get_input("Do you use QA/SAST tools?", ["Yes", "No"])
        resp["uses_sast"] = q1

        if q1 == "Yes":
            resp["use_case"] = self.get_input(
                "In what context do you use them?", 
                ["Work", "Personal", "Both"]
            )

            q3_text = "What is the primary problem they solve for you?"
            q3_opts = ["Vulnerabilities", "Code Quality", "Both", "None"]
            resp["primary_benefit"] = self.get_input(q3_text, q3_opts)

            if resp["primary_benefit"] == "None":
                resp["pain_point"] = self.get_input(
                    "Why do you feel they provide no value?",
                    ["Too Complex", "Not Useful", "High Noise", "Unsure"]
                )
            else:
                resp["frequency"] = self.get_input(
                    "How often are they integrated into your workflow?",
                    ["Always", "Often", "Sometimes", "Rarely"]
                )
        else:
            resp["barrier"] = self.get_input(
                "What is the main reason for not using them?",
                ["Lack of Awareness", "Lack of Trust", "Cost", "False Positives"]
            )
            resp["future_interest"] = self.get_input(
                "Would you consider adopting them in the future?", 
                ["Yes", "No"]
            )

        # Question 10: Global Evaluation
        resp["rating"] = self.get_input("How would you rate current SAST tech (1-10)?", is_numeric=True)

        self.save_data(entry)
        print(f"\n{SUB_DIVIDER}")
        print("Success! Your responses have been recorded.")
        print(f"{SUB_DIVIDER}\n")

    def show_analytics(self):
        """Generate a summary of all collected data."""
        if not self.results:
            print("\n>> No data available to analyze.")
            return

        total = len(self.results)
        ratings = [r["responses"]["rating"] for r in self.results]
        avg_rating = sum(ratings) / total

        yes_count = sum(1 for r in self.results if r["responses"]["uses_sast"] == "Yes")
        no_count = total - yes_count

        self.clear_screen()
        print(DIVIDER)
        print("            GLOBAL SURVEY ANALYTICS             ")
        print(DIVIDER)
        print(f"Total Participants: {total}")
        print(f"Average Industry Rating: {avg_rating:.1f} / 10")
        print(f"Adoption Rate: {(yes_count/total)*100:.1f}%")
        print(SUB_DIVIDER)

        # Simple breakdown of barriers for non-users
        barriers = {}
        for r in self.results:
            b = r["responses"].get("barrier")
            if b:
                barriers[b] = barriers.get(b, 0) + 1

        if barriers:
            print("Top Barriers to Adoption:")
            for b, count in sorted(barriers.items(), key=lambda x: x[1], reverse=True):
                print(f" - {b}: {count} user(s)")

        input("\nPress Enter to return to menu...")

    def main_menu(self):
        """Application entry point menu."""
        while True:
            self.clear_screen()
            print(DIVIDER)
            print("         INTERNAL DATA COLLECTION TOOL          ")
            print(DIVIDER)
            print("1. Start New Survey")
            print("2. View Analytics Dashboard")
            print("3. Export Raw Data (JSON)")
            print("4. Exit")
            print(SUB_DIVIDER)

            choice = input("Select an option: ")

            if choice == "1":
                self.run_survey()
            elif choice == "2":
                self.show_analytics()
            elif choice == "3":
                print(f"\nData is stored in: {os.path.abspath(DATA_FILE)}")
                input("Press Enter to continue...")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                input("Invalid choice. Press Enter to try again.")

if __name__ == "__main__":
    # Standard Python entry point
    app = SurveyApp()
    app.main_menu()
