# prompt v2
### changed
- "exactly 5 letters" instead of "can only guess 5 letter words"
- Length restated in the output instruction
- Visual separators between sections
### results
- dominant failure is now the model emitting emoji feedback strings instead of words: 🟨🟨🟩🟨⬛

# prompt v3
### changed
- state format changed to -> C: in word, R: not in word, A: correct position, N: in word, E: not in word
### results
- invalid guess lengths increased
- removed emoji guesses completely
- model emits the same handful of words regardless of state

# prompt v4
### changed
- instead of giving each guess as state, give C_R__, ruled out: D, A, B, S, must include: I (not position 3)
- similar to how the actual wordle game handles things
- STATE -> Known: ____E. Ruled out: R, C, H, O, L, T. Must include A (not in position 3), N (not in position 4), S (not in position 1)
