# PawPal+ Project Reflection Post-Capstone Update

## AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Throughout the project I constantly ran through a lot of brainstorming and implementation rounds. 
For example, I would often start with plan mode with Claude Code, explain the feature I am trying to build and continuously iterate through the prompt
until I think they have the full scope of my vision.  

So, I found that prompts that always stated the context of my plan, caveats it should follow, 
and a balance of specificity and conciseness gave me the most valuable outputs. I believe having the 
AI always asking you clarifying questions and giving its assumptions allows you to bring the most 
potential out of the LLM because it requires you to be very minute and mindful with your prompts. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I was focusing on asking the AI to iterate on a mermaid.js diagram, I prompted the AI to 
develop the diagram so that it matches the implementation of PawPal, the overall data flow, and the major components. 
However, on the first draft, it correctly ouputted to the key components, but it was unreadable such that it had tangling and lengthy arrows pointing
to one another. 

The evaluation came through to how I perceived the diagram and found that the top-down and verbose approach the AI employed was unfavorable for other people
looking to understand the system architecture. 

---

## Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

For the test suite, I added tests that primarily tests the 3 main cases:
Preston returns a response to a valid query;  a question about general dogs and cats
Preston does not respond to an empty query
Preston does not try to give a confident answer on an animal they cannot answer about;
a type of species of dog or cat, or other animals
---


## Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I was satisfied with being able to seamlessly integrate an LLM like Gemini onto my project by applying the concepts I've been taught in class; e.g Guardrails, Fine-Tuning, etc. 
Throughout this project, I've realized just how much better I've gotten with working with AI and by being responsible, specific, and organized, I can use AI to accelerate my 
workflow.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would continue to iterate on the scope of animals that PawPal Preston could give advice on. For this iteration, I've decided to just focus on general dogs and cats without going into any of the species or other animals to narrow the scope and meet the sprint. Additionally, I would also try to redesign PawPal with a different stack (e.g React, Go, PostgreSQL) so I can have more control and turn it into a more fully-fledged
full-stack project. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Throughout the time that I have been working on this feature, I believe the most important thing I've learned about
designing a system is that you won't get everything in one shot. Regardless of how confident I felt that I've handled all the edge cases,
there will be a thumb that sticks out when I am prototyping a feature. i.e there will be times where you think you've made a completely robust 
architecture in one go, but it's very likely there was more cases to think about. 