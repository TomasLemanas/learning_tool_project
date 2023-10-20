# Remove all csv and txt files before starting 

import pytest
from learning_tool import LearningTool, PracticeMode, TestMode, StatisticsViewer

# Create an instance of LearningTool to use for testing
learning_tool = LearningTool()

# Test the load_last_question_id method
def test_load_last_question_id():
    assert learning_tool.load_last_question_id() == 1  # Check if it returns 1 for the default value


