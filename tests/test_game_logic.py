from logic_utils import check_guess
from app import check_guess as check_guess_app

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# FIX: AI (Claude) wrote these two regression tests, in agent mode, right
# after fixing the swapped hint messages in app.py's check_guess. They lock
# in the correct pairing so the bug can't silently come back.
def test_too_high_message_tells_player_to_go_lower():
    # Regression test: app.py used to attach "Go HIGHER!" to the "Too High"
    # outcome (and "Go LOWER!" to "Too Low"), telling the player the exact
    # opposite of what they should do next.
    outcome, message = check_guess_app(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()

def test_too_low_message_tells_player_to_go_higher():
    outcome, message = check_guess_app(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()

def test_check_guess_numeric_not_lexicographic():
    # Regression test for the app.py line-160 bug: the caller used to
    # stringify the secret on even attempts, making check_guess compare
    # an int guess to a str secret and fall back to lexicographic string
    # comparison. "9" > "10" as strings, but 9 < 10 as numbers - these
    # cases catch that mistake if it ever comes back.
    outcome, _ = check_guess_app(9, 10)
    assert outcome == "Too Low"

    outcome, _ = check_guess_app(100, 20)
    assert outcome == "Too High"
