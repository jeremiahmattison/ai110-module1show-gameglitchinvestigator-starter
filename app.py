import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIXME: Logic breaks here - "Too High"/"Too Low" outcomes paired with
    # swapped hint messages. (Already fixed below: see FIX comment.)
    #
    # FIX: 
    # "Too High" was paired with "Go HIGHER!" and "Too Low" with "Go LOWER!",
    # telling the player the opposite of what to do. I described the
    # symptom (100 said go higher, 0 said go lower) and the AI traced it
    # to these swapped strings and fixed both branches below.
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def get_temperature_hint(guess: int, secret: int, low: int, high: int) -> str:
    """Return a Hot/Cold style emoji hint based on how close guess is to secret."""
    span = max(high - low, 1)
    distance = abs(guess - secret)
    closeness = distance / span

    if closeness <= 0.03:
        return "🔥🔥 Red Hot!"
    if closeness <= 0.10:
        return "🔥 Hot"
    if closeness <= 0.25:
        return "🌡️ Warm"
    if closeness <= 0.50:
        return "❄️ Cold"
    return "🥶 Freezing"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIXME: Logic breaks here - attempts starts at 1 on first load but is
# reset to 0 by "New Game" below, so the very first game of a session
# shows one fewer attempt remaining than it should before any guess is made.
if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({
            "Attempt": st.session_state.attempts,
            "Guess": raw_guess,
            "Outcome": "❌ Invalid",
            "Temperature": "-",
        })
        st.error(err)
    else:
        outcome, message = check_guess(guess_int, st.session_state.secret)
        temperature = get_temperature_hint(guess_int, st.session_state.secret, low, high)

        st.session_state.history.append({
            "Attempt": st.session_state.attempts,
            "Guess": guess_int,
            "Outcome": outcome,
            "Temperature": temperature,
        })

        if show_hint:
            # Color-coded hint: red for "too high", blue for "too low",
            # each paired with a Hot/Cold style emoji showing how close you are.
            if outcome == "Too High":
                st.error(f"{message}  |  {temperature}")
            elif outcome == "Too Low":
                st.info(f"{message}  |  {temperature}")
            else:
                st.success(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.history:
    st.subheader("📊 Game Session Summary")
    st.table(st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
