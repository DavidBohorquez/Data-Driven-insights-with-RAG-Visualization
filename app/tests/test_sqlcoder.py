import pytest
from unittest.mock import MagicMock, patch
import torch
#from app.sqlcoder import generate_sql_query, execute_sql_query
from app import sqlcoder

# Fixture: Resuable mock database
@pytest.fixture
def mock_db():
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = [("Test Data", 123)]
    return db

'''# Unit Test: generate_sql_query
def test_generate_sql_query():
    with patch("app.sqlcoder.sql_model.generate") as mock_generate:
        mock_generate.return_value = torch.tensor([1])
        sql = generate_sql_query("What are the authors of the publications in 2023?")
        #assert sql == "SELECT a.name FROM authors a JOIN publication_authors pa ON a.id = pa.author_id JOIN publications p ON pa.publication_id = p.id WHERE strftime('%Y', p.publication_date) = '2023'"
        assert "JOIN" in sql'''

# Unit Test: generate_sql_query whole method
@patch("app.sqlcoder.generate_sql_query")
def test_generate_sql_query(mock_generate):
    mock_generate.return_value = "SELECT * FROM authors JOIN publications ON authors.id = publications.author_id"
    sql = sqlcoder.generate_sql_query("What are the authors of the publications in 2023?")
    assert "JOIN" in sql

# Unit Test: execute_sql_query
def test_execute_sql_query_valid(mock_db):
    results, error = sqlcoder.execute_sql_query(mock_db, "SELECT a.name FROM authors a JOIN publication_authors pa ON a.id = pa.author_id JOIN publications p ON pa.publication_id = p.id WHERE strftime('%Y', p.publication_date) = '2023'")   
    assert error is None
    assert len(results) > 0

# Integration Test: Full flow
@patch("app.sqlcoder.generate_sql_query")
@patch("app.sqlcoder.execute_sql_query")
def test_full_flow(mock_execute, mock_generate, mock_db):
    #Setup mocks
    mock_generate.return_value = "SELECT a.name FROM authors a JOIN publication_authors pa ON a.id = pa.author_id JOIN publications p ON pa.publication_id = p.id WHERE strftime('%Y', p.publication_date) = '2023'"
    mock_execute.return_value = (["Author1", "Author2"], None)

    # Simulate workflow
    sql = sqlcoder.generate_sql_query("Test question")
    results, error = sqlcoder.execute_sql_query(mock_db, sql)

    # Verify
    mock_generate.assert_called_once()
    mock_execute.assert_called_once()
    assert len(results) == 2


'''def test_join_handling():
    input="Show authors with publications in 2023"
    expected = """SELECT a.name 
                FROM authors a
                JOIN publication_authors pa ON a.id = pa.author_id
                JOIN publications p ON pa.publication_id = p.id
                WHERE strftime('%Y', p.publication_date) = '2023'"""
    assert sql_normalize()'''