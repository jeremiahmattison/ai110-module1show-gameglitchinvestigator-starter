# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

--- The game would give the opposite hint of what it was supposed to give in the beginning. For example if the was 80 and I guessed 79, it would tell me "go lower" instead of "go higher". This was the main bug that I fixed. 

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

--- I used Claude code and the suggestion of the hints being swapped was correct and I verified the result with a pytest case. An AI suggestion that was misleading was the fixing of the attempts. It changed the bug so the very first game of a session shows one fewer attempt remaining than it should before any guess is made.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

--- I decided the bug was fixed by manually trying the too low/too high hints on 3 different games. I ran both manual and pytests to ensure that the hint was no the opposite of what it should be. The AI helped mostly to design the pytests, I was able to understand them on my own after reading the code. 

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

--- The secret number kept changing because Streamlit restarts the script from top to bottom everytime we interact. A streamlit reruns is essentially a restart of the entire program everytime a button is clicked, but it gives a storage box that keeps track of the values so they aren't really completely wiped out. The fix was to only generate the secret the first time by checking if secret was not in the st.session_state (storage box). 

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

--- I'd want to reuse the habit of having claude explain a section of code to me that I don't understand, so I'm not blindly prompting to fix bugs. Next time, I'd probably deeply review the pytests that claude created, regardless of whether I manually tested it or not. This project taught me that AI generated code saves lots of logical time especially when it comes to creating test cases. 