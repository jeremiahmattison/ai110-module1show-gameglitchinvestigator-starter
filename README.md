# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  A Streamlit number-guessing game: pick a difficulty, the app secretly picks a number in that range, and you guess until you run out of attempts, getting a "Too High"/"Too Low" hint after each try.

- [x] **Detail which bugs you found.**
  - The secret number was being re-rolled on every rerun (every click/keystroke), because `random.randint(...)` wasn't guarded by `st.session_state`, so Streamlit's "rerun the whole script" behavior generated a brand-new secret constantly.
  - The hint messages were swapped in `check_guess`: a "Too High" outcome said "Go HIGHER!" and a "Too Low" outcome said "Go LOWER!" — the exact opposite of what the player needed to do.
  - `st.session_state.attempts` initializes to `1` on first load but resets to `0` on "New Game," so the very first game of a session shows one fewer attempt remaining than it should (marked with a `# FIXME` in `app.py`, not yet fixed).

- [x] **Explain what fixes you applied.**
  - Wrapped secret generation in `if "secret" not in st.session_state:` so it's only rolled once per game instead of on every rerun.
  - Swapped the hint strings in `check_guess` so "Too High" returns "Go LOWER!" and "Too Low" returns "Go HIGHER!".
  - Added pytest regression tests (`test_too_high_message_tells_player_to_go_lower`, `test_too_low_message_tells_player_to_go_higher`) in `tests/test_game_logic.py` to lock in the corrected hint pairing.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]
![winning game](screenshot/Screenshot%202026-10-04%20185540.png)

## 🚀 Stretch Features

- [x] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here] 
![Enhanced Game UI](screenshot/Screenshot%202026-10-05%20075335.png)

### UI Enhancements

- **Color-coded hints.** Instead of every hint showing in the same yellow `st.warning`, the submit handler now checks `outcome` and picks a color that matches the message: `st.error` (red) for "Too High," `st.info` (blue) for "Too Low," and `st.success` (green) for "Win."
- **Hot/Cold emoji hints.** A new `get_temperature_hint(guess, secret, low, high)` function in `app.py` measures how close a guess is to the secret as a fraction of the difficulty's range and returns a label from `🔥🔥 Red Hot!` down to `🥶 Freezing`. It's shown right next to the Too High/Too Low hint so players get a sense of distance, not just direction.
- **Game session summary table.** `st.session_state.history` now stores a dict per attempt (`Attempt`, `Guess`, `Outcome`, `Temperature`) instead of a bare value. A new "📊 Game Session Summary" section renders this with `st.table()` so players can see their whole guessing history — including invalid entries, marked `❌ Invalid` — at a glance.

These changes only touch display code in the `submit` block and add the standalone `get_temperature_hint` helper — `check_guess`, `update_score`, and `parse_guess` (the core game logic covered by the pytest suite) are untouched.
