import csv
import tempfile
import pytest
from learning_tool import LearningTool

# Helper function to generate a CSV file with sample questions
def generate_sample_csv():
    sample_data = [
        {"id": 1, "text": "Sample Quiz Question", "type": "quiz", "options": "Option 1,Option 2,Option 3", "correct_option": "1", "disabled": "False", "times_shown": 0}
    ]
    fieldnames = sample_data[0].keys()

    # Create a temporary CSV file with sample data
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)

    return csv_file.name

@pytest.mark.parametrize("input_values", [("Sample Quiz Question", "Option 1", "Option 2", "Option 3", "1")])
def test_add_quiz_question(input_values, monkeypatch):
    # Convert input_values to a list
    input_values = list(input_values)

    # Arrange
    sample_csv_file = generate_sample_csv()
    learning_tool = LearningTool()
    learning_tool.load_questions()

    # Simulate user input using monkeypatch
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))

    # Act
    learning_tool.add_quiz_question()

    # Assert
    question = learning_tool.questions[0]
    assert question["text"] == "Sample Quiz Question"
    assert question["type"] == "quiz"
    assert question["options"] == ["Option 1", "Option 2", "Option 3"]
    assert int(question["correct_option"]) == 1  # Convert to int before assertion
    assert question["disabled"] is False

# To run this test, make sure the learning_tool.py and test_learning_tool.py files are in the same directory and run pytest on test_learning_tool.py.




