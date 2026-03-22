This is the Ai_agent I made I had to edit it to run on my computer I have it so that it can take inputs (pdf,text,etc) and gives a response it is very rough but it works

examples
1.
What can I help you research: Can you summarize the pdf

[Model decision]: You should read the PDF first. Once you have done so, I can help you summarize it.

[Tool detected]: pdf
[Auto-detected PDF]: pdfs\Persona_and_Scenario.pdf

Structured Output:
 topic='User Experience (UX) and Interaction Design for Academic Collaboration' summary="The summary discusses the persona of Dani Rogers, an Environmental Science student who uses 'CollabNotes,' a mobile app designed for academic collaboration. The app helps in real-time note-taking, sharing research findings, and brainstorming with group members scattered across different locations. It features synchronization, highlighting, integrated chat, voting, and real-time updates, enhancing productivity and effective remote collaboration." source=['CS280: Introduction to User Experience (UX), User Interface (UI) and Interaction Design Semester II, 2026'] tools_used=['CollabNotes']

2.
What can I help you research: What is the capital of France

[Model decision]: No tools are needed. The capital of France is Paris.

[No tool detected]

Structured Output:
 topic='Capital of France' summary='The capital of France is Paris.' source=['General knowledge'] tools_used=['GeneralKnowledge']

3.
What can I help you research: what does x equal in this equation 2x+4=1

[Model decision]: No tools are needed to solve this problem. Let's solve it:

Given: \(2x + 4 = 1\)

Subtract 4 from both sides:
\[2x = 1 - 4\]
\[2x = -3\]

Divide by 2:
\[x = \frac{-3}{2}\]
\[x = -1.5\]

So, \(x\) equals \(-1.5\).

[No tool detected]

Structured Output:
 topic='Algebraic Equation' summary='Solving for variable x in the equation 2x + 4 = 1.' source=['Math problem'] tools_used=['Basic algebra']