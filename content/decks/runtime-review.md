::slide kind=overview template=title-overview
# Runtime Review
::region explanation
Core runtime state still lives in the exported contract, while the browser layer only consumes those bounded semantics.
::region example
- reveal progression
- feedback visibility

---

::slide kind=quiz template=quiz-feedback
# Runtime Boundary
::region question
Which layer owns Markdown parsing?
::region answer_choices
- The browser renderer
- The Python pipeline
::region feedback
::reveal step=1
Markdown parsing remains on the Python side; the browser only reads exported payloads.
::endreveal