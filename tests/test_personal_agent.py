import pytest
import personal_agent as agent

def test_calculate_basic_math():
    assert agent.calculate("(12 + 8) * 3") == "60"

def test_calculate_rejects_python_expressions():
    with pytest.raises(ValueError):
        agent.calculate("__import__('os').system('echo unsafe')")

def test_save_and_list_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(agent, "DB", tmp_path / "notes.sqlite3")
    saved = agent.save_note("Trip plan", "Compare trains to Jaipur")
    assert "Saved local note" in saved
    notes = agent.list_notes()
    assert "Trip plan" in notes
    assert "Compare trains to Jaipur" in notes
