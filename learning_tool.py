import csv
import random
import datetime

    # creating a LeariningTool Class
class LearningTool:
    def __init__(self):
        # Initialize your data structures and load existing data from a single CSV file
        self.questions = []  # Stores questions in a list
        self.next_question_id = self.load_last_question_id()  # Get the last used question ID
        self.load_questions()  # Load existing questions and their statuses from a CSV file
        self.practice_mode = PracticeMode(self.questions, self.save_questions)  # Create PracticeMode instance
        self.test_mode = TestMode(self.questions)  # Create TestMode instance

    #method for loading last question ID from a .txt file
    def load_last_question_id(self):
        try:
            # Try to load the last used question ID from a text file
            with open("last_question_id.txt", "r") as file:
                return int(file.read())  # Return the stored ID as an integer
        except (FileNotFoundError, ValueError):
            # If the file doesn't exist or is invalid, start with ID 1
            return 1  # Default to the initial question ID

    # method for creating a main menu
    def main_menu(self):
        while True:
            print("Learning Tool Menu:")
            print("1. Adding Questions")
            print("2. Statistics Viewing")
            print("3. Disable/Enable Question")
            print("4. Practice Mode")
            print("5. Test Mode")
            print("6. Exit")
            choice = input("Enter your choice: ")  # Prompt user for a menu option
            if choice == "1":
                self.add_questions_menu()
            elif choice == "2":
                statistics_viewer = StatisticsViewer(self.questions)
                statistics_viewer.view_statistics()
            elif choice == "3":
                self.disable_enable_question()
            elif choice == "4":
                self.practice_mode.start()
            elif choice == "5":
                self.test_mode.start_test()
            elif choice == "6":
                print("Exiting Learning Tool.")  # Exit the program
                break
            else:
                print("Such option doesn't exist")  # Display error for invalid input

    # method for creating a menu for adding questions
    def add_questions_menu(self):
        while True:
            print("Adding Questions Menu:")
            print("1. Add Quiz Question")
            print("2. Add Free-Form Question")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")  # User input for choosing options
            if choice == "1":
                self.add_quiz_question()  # Call method to add a quiz question
            elif choice == "2":
                self.add_free_form_question()  # Call method to add a free-form question
            elif choice == "3":
                print("Returning to the Main Menu.")  # Return to the main menu
                break
            else:
                print("Such option doesn't exist")  # Display error for invalid input

    # method for additng a quiz queestion
    def add_quiz_question(self):
        # Implement adding a quiz question here
        question_text = input("Enter the question text: ")  # Prompt for the question text
        options = []  # Initialize an empty list to store answer options
        for i in range(3):  # Loop to get 3 answer options
            option = input(f"Enter option {i + 1}: ")  # Prompt for an option
            options.append(option)  # Add the option to the list
        while True:
            correct_option = input("Enter correct option 1, 2, or 3: ")  # Prompt for the correct option
            if correct_option in ["1", "2", "3"]:  # Check if the input is one of the valid options
                break
            else:
                print("Invalid input. Please enter '1', '2', or '3'.")  # Display an error for invalid input

        question_id = self.next_question_id  # Get the next question ID
        self.next_question_id += 1  # +1 for question ID for the next question

        # Create a dictionary to represent the quiz question
        question = {
            "id": question_id,  # Assign question ID
            "text": question_text,  # Assign question text
            "type": "quiz",  # Set the question type to 'quiz'
            "options": options,  # Assign the answer options
            "correct_option": int(correct_option),  # Assign the correct option as an integer
            "disabled": False,  # Default value for "disabled"
            "times_shown": 0,  # Initialize times_shown to 0
            "times_answered_correctly": 0,  # Initialize times_answered_correctly to 0
            "times_answered_incorrectly": 0,  # Initialize times_answered_incorrectly to 0
        }

        # Add the question to the list of questions
        self.questions.append(question)  # Append the question dictionary to the list
        print("Quiz question added successfully!")  # Display a success message


        # Save the questions to the merged CSV file
        self.save_questions()  # Call the method to save questions to a CSV file

    #method to add a free-form question
    def add_free_form_question(self):
        # Implement adding a free-form text question here
        question_text = input("Enter question text: ")  # Prompt for the question text
        correct_option = input("Enter the expected answer: ").strip().lower()  # Prompt for the correct answer
        question_id = self.next_question_id  # Get the next question ID
        self.next_question_id += 1  # Increment the question ID for the next question

        # Create a dictionary to represent the free-form question
        question = {
            "id": question_id,  # Assign the question ID
            "text": question_text,  # Assign the question text
            "type": "free-form",  # Set the question type to 'free-form'
            "correct_option": correct_option,  # Assign the correct answer
            "disabled": False,  # Default value for "disabled"
            "times_shown": 0,  # Initialize times_shown to 0
            "times_answered_correctly": 0,  # Initialize times_answered_correctly to 0
            "times_answered_incorrectly": 0,  # Initialize times_answered_incorrectly to 0
        }

        # Add the question to the list of questions
        self.questions.append(question)  # Append the question dictionary to the list
        print("Free-form question added successfully")  # Display a success message

        # Save the questions to the merged CSV file
        self.save_questions()  # Call the method to save questions to a CSV file

    # method to load question from CSV file
    def load_questions(self):
        try:
            with open("questions.csv", newline="", mode="r") as file:
                reader = csv.DictReader(file)  # Create a CSV reader
                for row in reader:
                    question_id = int(row["id"])  # Extract question ID
                    disabled = bool(row["disabled"]) if "disabled" in reader.fieldnames and row["disabled"].lower() == "true" else False  # Check if the question is disabled
                    times_shown = int(row["times_shown"]) if "times_shown" in reader.fieldnames else 0  # Extract times shown

                    question = {
                        "id": question_id,  # Assign the question ID
                        "text": row["text"],  # Assign the question text
                        "type": row["type"],  # Assign the question type
                        "options": row["options"].split(",") if "options" in reader.fieldnames else [],  # Extract answer options
                        "correct_option": row["correct_option"] if "correct_option" in reader.fieldnames else None,  # Extract the correct option
                        "disabled": disabled,  # Assign the disabled status
                        "times_shown": times_shown,  # Assign the times shown
                        "times_answered_correctly": int(row.get("times_answered_correctly", 0)),  # Extract times answered correctly
                        "times_answered_incorrectly": int(row.get("times_answered_incorrectly", 0))  # Extract times answered incorrectly
                    }

                    self.questions.append(question)  # Append the question dictionary to the list
        except FileNotFoundError:
            pass

    # method to disable or enable a question
    def disable_enable_question(self):
        question_id = input("Enter the ID of the question you want to disable/enable: ")  # Prompt for the question ID
        question = self.find_question_by_id(question_id)  # Find the question by its ID

        if question:
            self.show_question_details(question)  # Display the question details
            while True:
                disable = input("Do you want to change disable/enable status for this question? (yes/no): ")  # Prompt for disabling/enabling
                if disable.lower() == "yes":
                    question["disabled"] = True  # Disable the question
                    print("Question status updated successfully")  # Display a success message
                    self.save_questions()  # Update the CSV file
                    break
                if disable.lower() == "no":
                    question["disabled"] = False  # Enable the question
                    print("Question status updated successfully")  # Display a success message
                    self.save_questions()  # Update the CSV file
                    break
                elif disable.lower() not in ["yes", "no"]:
                    print("Please enter 'yes' or 'no'")  # Display an error for invalid input
                    continue
        else:
            print(f"Question with ID {question_id} not found.")  # Display an error if the question is not found


    # Method to save a question
    def save_questions(self):
        # Save questions to the merged CSV file
        with open("questions.csv", newline="", mode="w") as file:
            fieldnames = ["id", "text", "type", "options", "correct_option", "disabled",
                          "times_shown", "times_answered_correctly", "times_answered_incorrectly"]  # Define CSV field names
            writer = csv.DictWriter(file, fieldnames=fieldnames)  # Create a CSV writer
            writer.writeheader()  # Write the header row

            for question in self.questions:
                writer.writerow({
                    "id": question["id"],  # Write the question ID
                    "text": question["text"],  # Write the question text
                    "type": question["type"],  # Write the question type
                    "correct_option": question.get("correct_option", ""),  # Write the correct option (empty string if not available)
                    "options": ",".join(question.get("options", [])),  # Write the answer options as a comma-separated string
                    "times_shown": question.get("times_shown", 0),  # Write the times shown (default to 0 if not available)
                    "times_answered_correctly": question.get("times_answered_correctly", 0),  # Write times answered correctly (default to 0 if not available)
                    "times_answered_incorrectly": question.get("times_answered_incorrectly", 0),  # Write times answered incorrectly (default to 0 if not available)
                    "disabled": question["disabled"]  # Write the disabled status
                })

        # Update the last used question ID in the file
        with open("last_question_id.txt", "w") as id_file:
            id_file.write(str(self.next_question_id))  # Write the next question ID to the file


    def show_question_details(self, question):
        print(f"Question ID: {question['id']}")  # Display the question ID
        print(f"Question Text: {question['text']}")  # Display the question text
        if question['type'] == 'quiz':
            print(f"Options: {', '.join(question['options'])}")  # Display answer options for quiz questions
            print(f"Correct Option: {question['correct_option']}")  # Display the correct option for quiz questions
        else:
            print(f"Expected Answer: {question['correct_option']}")  # Display the expected answer for free-form questions
        print(f"Disabled: {question['disabled']}")  # Display the disabled status

    def find_question_by_id(self, question_id):
        question_id = int(question_id)  # Convert the input to an integer
        for question in self.questions:
            if question["id"] == question_id:  # Check if the question ID matches
                return question  # Return the question if found
        return None  # Return None if the question is not found

# >>>>>>>>>>>PRACTICE MODE<<<<<<<<<<<<<<

    #Creating a PracticeMode Class
class PracticeMode:
    def __init__(self, questions, save_questions_method):
        self.questions = questions
        self.save_questions = save_questions_method

    # method for starting the practice mode
    def start(self):
        enabled_questions = [q for q in self.questions if not q["disabled"]]  # Create a list of enabled questions

        if not enabled_questions:
            print("No enabled questions available for practice.")  # Display a message if no enabled questions

        while True:
            if not enabled_questions:
                print("No enabled questions available for practice.")  # Display a message if no enabled questions
                return

            selected_question = random.choice(enabled_questions)  # Select a random question from the enabled questions
            question_id = int(selected_question["id"])
            selected_question["times_shown"] += 1  # Increment the times shown

            print(f"Practice Question ID: {question_id}")  # Display the question ID
            print(f"Question Text: {selected_question['text']}")  # Display the question text

            if selected_question["type"] == "free-form":
                user_answer = input("Your answer (or 'exit' to quit practice mode): ").strip().lower()  # Prompt for a user's answer or exit
            elif selected_question["type"] == "quiz":
                options = selected_question['options']
                print("Options:")
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")
                user_answer = input("Enter the number of the correct option (or 'exit' to quit practice mode): ")  # Prompt for the number of the correct option

            if user_answer == 'exit':
                break  # Exit practice mode
            elif user_answer == str(selected_question["correct_option"]):
                print("Correct!")  # Display a message for a correct answer
                selected_question["times_answered_correctly"] += 1  # Increment times answered correctly
            else:
                print("Incorrect!")  # Display a message for an incorrect answer
                selected_question["times_answered_incorrectly"] += 1  # Increment times answered incorrectly

            self.save_questions()  # Save questions after each interaction

            enabled_questions = [q for q in self.questions if not q["disabled"]]  # Update the list of enabled questions

# >>>>>>>>>>>TEST MODE<<<<<<<<<<<<<<<<
class TestMode:
    def __init__(self, questions):
        self.questions = questions

    #Method for starting Test mode
    def start_test(self):
        print("Test Mode")
        num_questions = self.get_number_of_questions()  # Get the number of questions for the test
        if num_questions is None:
            print("Exiting Test Mode.")  # Exit test mode
            return

        test_questions = self.select_random_questions(num_questions)  # Select a random set of test questions
        correct_answers = self.administer_test(test_questions)  # Administer the test and get the number of correct answers
        score = self.calculate_score(correct_answers, num_questions)  # Calculate the test score

        print(f"Test completed. Your score: {score}/{num_questions}")  # Display the test score
        self.save_score(score, num_questions)  # Save the test score

    # Method for getting a number of questions
    def get_number_of_questions(self):
        while True:
            try:
                num_questions = input("Enter the number of questions for the test, or 'exit' to return: ")  # Prompt for the number of test questions
                if num_questions == "exit":
                    break
                elif 0 < int(num_questions) <= len(self.get_enabled_questions(self.questions)):
                    return int(num_questions)
                elif int(num_questions) > len(self.get_enabled_questions(self.questions)):
                    print(f"max number of questions is {len(self.get_enabled_questions(self.questions))} ")  # Display a message for too many questions
                elif num_questions == "exit":
                    print("back to main menu")  # Display a message for returning to the main menu
                else:
                    print("Invalid input")  # Display an error for invalid input
            except ValueError:
                print("Invalid input. Please enter a valid number.")  # Display an error for invalid input

    # Methof for getting enabled questions
    def get_enabled_questions(self, test_questions):
        return [question for question in test_questions if not question["disabled"]]

    # selecting random questions
    def select_random_questions(self, num_questions):
        enabled_questions = self.get_enabled_questions(self.questions)

        if not enabled_questions:
            print("No enabled questions available for the test.")
            return []

        random.shuffle(enabled_questions)
        return enabled_questions[:num_questions]


    # Method for administering the test
    def administer_test(self, test_questions):
        correct_answers = 0
        enabled_questions = self.get_enabled_questions(test_questions)  # Filter out disabled questions
        for question in enabled_questions:
            print(f"Question: {question['text']}")  # Display the test question
            if question['type'] == 'quiz':
                for i, option in enumerate(question['options'], 1):
                    print(f"{i}. {option}")
                user_answer = input("Enter the number of the correct option: ")  # Prompt for the number of the correct option
                if user_answer == str(question['correct_option']):
                    correct_answers += 1  # Increment correct answers for quiz questions
            else:
                user_answer = input("Your answer: ").strip().lower()
                if user_answer == question['correct_option'].strip().lower():
                    correct_answers += 1  # Increment correct answers for free-form questions
        return correct_answers  # Return the total number of correct answers

    # Method for calculating score
    def calculate_score(self, correct_answers, num_questions):
        return correct_answers  # Calculate the score based on the number of correct answers

    # Method for saving score in a . txt file
    def save_score(self, score, num_questions):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:S")  # Get the current date and time
        with open("results.txt", "a") as file:
            file.write(f"Score: {score}/{num_questions}, Date: {timestamp}\n")  # Write the test score and timestamp to a results file

# >>>>>>>>>>STATISTICS VIEWER<<<<<<<<<<<<

#Creating a StatisticsViewer Class
class StatisticsViewer:
    def __init__(self, questions):
        self.questions = questions

    # Method for viewing statistics
    def view_statistics(self):
        print("STATISTICS VIEWING MODE:")
        for question in self.questions:
            question_id = question["id"]  # Get the question ID
            question_text = question["text"]  # Get the question text
            is_active = "Active" if not question["disabled"] else "Inactive"  # Determine if the question is active or inactive
            times_shown = question.get("times_shown", 0)  # Get the number of times the question has been shown
            times_answered_correctly = question.get("times_answered_correctly", 0)  # Get the number of times answered correctly
            percentage = 0  # Initialize the percentage to 0
            if times_shown > 0:
                percentage = (times_answered_correctly / times_shown) * 100  # Calculate the percentage correct

            print(f"Question ID: {question_id}")  # Display the question ID
            print(f"Question Status: {is_active}")  # Display the question status
            print(f"Question Text: {question_text}")  # Display the question text
            print(f"Times Shown: {times_shown}")  # Display the number of times shown
            print(f"Percentage Correct: {percentage:.2f}%")  # Display the percentage correct
            print("-" * 30)  # Display a separator line



if __name__ == "__main__":
    learning_tool = LearningTool()  # Create an instance of the LearningTool class
    choice = learning_tool.main_menu()  # Start the main menu loop
