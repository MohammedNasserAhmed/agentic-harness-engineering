*install codex cli*
npm install -g @openai/codex@latest

*install codex app*
https://openai.com/codex/?utm_source=chatgpt.com

*Using Codex in VS*
*Midad*
1
Build a sleek, minimalist, and modern landing page for an Arabic study notes platform called **Midad (مِداد)**.
**Target directory:**\
`AIE2631/module-02-agentic-coding/`Midad

2
Add a minimalist Arabic RTL book offer section to the Midad landing page showing only the book title and price, matching the existing design; modify only index.html

*PROMPTING*

Add a second button labeled "Remove Book".
It should render for example: "Book #4 removed from the library."

--------------
TASK
Add a second button labeled "Remove Book".
It should render for example: "Book #4 dropped."

CONTEXT
Inspect the existing code and shared logic where possible. Avoid duplicating event handlers.

OUTPUT
Keep the cod DRY as possible and easy to extend if we add extra buttons later.

----------------------------------------
*CPrompting*

[Refactor this function to follow the same style as the model function.] [Complete the todo in api.js]

-----------------------------------------
*Agents.md*
_ using PROMPTING DEMO _

-----------------------------------------
*Plan Mode / Edge CASES*
_ using PROMPTING DEMO _

-----------------------------------------
*Skill*

TASK & PURPOSE

Create a repo-specific dev skill for this project.
Its purpose is to help the agent work safely in this codebase when fixing bugs, reviewing changes, or doing maintenance.


INSPECT/CAPTURE

As you create it, inspect the repo for project-specific guardrails, known platform constraints, pinned dependencies, and anything the agent should avoid changing.


CONSTRAINTS

This should not be a generic debugging checklist. It should capture the specific rules and quirks of this repo so a dev can invoke it later when something breaks.


HOW TO INVOKE

The skill should be invoked with /style-dev and an explanation of a bug or problem.

-----------------
-----------------
*USING CODEX APP SECTION*

*codex agent loop*
Give me a comprehensive, well-structured rundown of everything we worked on in this project over the past seven days

*codex plugin*
Search the web for today's top five AI news stories from reliable sources, summarize each story in 2–3 sentences, and create a new Notion page titled "AI News Daily Brief — November 22, 2026" containing the headlines, summaries, source links, and publication dates. If the Notion plugin is unavailable or not connected, explain how to enable it before proceeding.


*codex skill*

List subtitles :
- What are skills
- Install existing skills
-  Is there any reday-made skills with others
-  create your custom skills
  

Create a SKILL:
- I would like to create a skill that takes a description of a YouTube video and returns an SEO-friendly title and description for my video. Create a list of about five engaging titles so I can choose from them, and recommend the best one. The skill should work for different video topics and support both English and Arabic.

Use the SKILL

- "I created a video about how to use skills within the Codex app. In this video, we cover what skills are, how to find and install skills, how to use existing skills, and how to create custom skills. Generate five SEO-friendly titles and an optimized YouTube description for this video."
- 
*codex subagent*
Hey, I need you to search through X (Twitter), Linkedin, Reddit, and relevant AI communities to find out what people are talking about in the AI space right now. Identify major AI news, trending discussions, emerging technologies, controversies, and industry drama. I want you to delegate the research to multiple specialized sub-agents working in parallel, each focusing on a different platform or topic. Have all sub-agents use GPT-5.6 Terra as their model, if available, and report their findings with source links, key insights, and a concise summary of the most significant trends.