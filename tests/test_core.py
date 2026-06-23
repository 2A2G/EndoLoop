import pytest
from unittest.mock import MagicMock
from endloop.core import EndLoopSystem

def test_endloop_approved_first_try(mocker):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    
    # Simulate auditor returning the cleaned payload
    mock_response.choices[0].message.content = "[STATE: APPROVED]\nClean data here."
    mock_client.chat.completions.create.return_value = mock_response
    
    system = EndLoopSystem(client=mock_client)
    result = system.run("Test task")
    
    # We should get the extracted payload, not the raw output
    assert result == "Clean data here."
    assert mock_client.chat.completions.create.call_count == 2

def test_endloop_refine_then_approve(mocker):
    mock_client = MagicMock()
    
    responses = [
        "Bad output",
        "[STATE: REFINE] Syntax error",
        "Good output",
        "[STATE: APPROVED] Looks great"
    ]
    
    def side_effect(*args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = responses.pop(0)
        return mock_resp
        
    mock_client.chat.completions.create.side_effect = side_effect
    
    system = EndLoopSystem(client=mock_client)
    result = system.run("Test task")
    
    # Result should be what the auditor approved
    assert result == "Looks great"
    assert mock_client.chat.completions.create.call_count == 4

def test_endloop_timeout(mocker):
    mock_client = MagicMock()
    
    def side_effect(*args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        # Check temperature to simulate audit vs generation
        if kwargs.get("temperature") == 0.0:
            mock_resp.choices[0].message.content = "[STATE: REFINE] still bad"
        else:
            mock_resp.choices[0].message.content = "some output"
        return mock_resp
        
    mock_client.chat.completions.create.side_effect = side_effect
    
    system = EndLoopSystem(max_loops=2, client=mock_client)
    
    with pytest.raises(TimeoutError):
        system.run("Impossible task")

def test_endloop_custom_checkpoints(mocker):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "[STATE: APPROVED]\nClean"
    mock_client.chat.completions.create.return_value = mock_response
    
    checkpoints = ["No Python 2 syntax"]
    system = EndLoopSystem(client=mock_client, custom_checkpoints=checkpoints)
    system.run("Task")
    
    # Check that the second call (the audit call) contains our custom rule
    audit_call_kwargs = mock_client.chat.completions.create.call_args_list[1].kwargs
    audit_message = audit_call_kwargs['messages'][-1]['content']
    
    assert "No Python 2 syntax" in audit_message
