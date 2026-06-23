import pytest
from unittest.mock import MagicMock
from endloop.core import EndLoopSystem

def test_endloop_approved_first_try(mocker):
    # Mock OpenAI client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    
    # First response: Generation
    # Second response: Audit says APPROVED
    mock_response.choices[0].message.content = "[STATE: APPROVED]\nClean data here."
    
    mock_client.chat.completions.create.return_value = mock_response
    
    system = EndLoopSystem(client=mock_client)
    result = system.run("Test task")
    
    assert result is not None
    # Called twice: 1 for generation, 1 for audit
    assert mock_client.chat.completions.create.call_count == 2

def test_endloop_refine_then_approve(mocker):
    mock_client = MagicMock()
    
    # We need sequential responses:
    # 1. Gen 1
    # 2. Audit 1 (REFINE)
    # 3. Gen 2
    # 4. Audit 2 (APPROVED)
    
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
    
    assert result == "Good output"
    assert mock_client.chat.completions.create.call_count == 4

def test_endloop_timeout(mocker):
    mock_client = MagicMock()
    
    # Always return REFINE
    def side_effect(*args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        # Alternate between gen and audit
        if kwargs.get("temperature") == 0.0:
            mock_resp.choices[0].message.content = "[STATE: REFINE] still bad"
        else:
            mock_resp.choices[0].message.content = "some output"
        return mock_resp
        
    mock_client.chat.completions.create.side_effect = side_effect
    
    system = EndLoopSystem(max_loops=2, client=mock_client)
    
    with pytest.raises(TimeoutError):
        system.run("Impossible task")
