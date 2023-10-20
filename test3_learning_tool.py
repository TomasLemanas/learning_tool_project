# Remove all csv and txt files before starting

from unittest.mock import patch
import pytest
from learning_tool import LearningTool

def test_add_quiz_question_with_mock_inputs():
    learning_tool = LearningTool()

    # Prepare mock inputs
    mock_inputs = [
        "Sample Quiz Question Text",
        "Option 1",
        "Option 2",
        "Option 3",
        "2",  # Correct option
    ]

    with patch('builtins.input', side_effect=mock_inputs):
        learning_tool.add_quiz_question()

    # Verify the result
    assert len(learning_tool.questions) == 1
    question = learning_tool.questions[0]
    assert question['text'] == "Sample Quiz Question Text"
    assert question['type'] == "quiz"
    assert question['options'] == ["Option 1", "Option 2", "Option 3"]
    assert question['correct_option'] == 2
    assert not question['disabled']

# Run the test
if __name__ == '__main__':
    pytest.main()