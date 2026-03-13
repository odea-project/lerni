::slide kind=overview template=title-overview
# Lerni Browser Intro
::region explanation
The browser renderer can now load deck payloads from a repository deck directory instead of one hard-coded demo file.
::region example
- static site build
- manifest-driven selection

---

::slide kind=quiz template=quiz-feedback
# Browser Flow Check
::region question
What now decides which deck the browser loads?
::region answer_choices
- A hard-coded file name in the UI
- A manifest plus selected deck id
::region feedback
::reveal step=1
The browser now reads a manifest and loads the selected deck payload by id.
::endreveal