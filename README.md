# financial-event-analytics
This repository contains a quick example of how using the reddit api and crew ai agents financial events can extracted and used for stock analytics.

**Disclaimer: This example is for educational purposes only and should not be interpreted as trading advice. The provided code, timestamps, and datasets are used for visualisation and experimentation purposes and may not represent a realistic trading model.**

## Project Overview

In this project, I aimed to analyse multiple events within articles to see if they overlap and make informed trading decisions based on the extracted financial events. 

### Key Components

1. **Crew AI Agent and Task**: analyse financial data and suggest the best trading actions based on the current subreddit / topic.
Have a look at 
![Basic Task](/task.png)
![Basic Agent](/agent.png)

2. **Reddit API**: To fetch articles related to financial events.
   See the
   [Basic example](/Apple_articles_20240705_33.csv)
   ![Basic example](/article_content.png)

### Challenges 
Data filtering was tricky,
Writing concise prompts for the AI agents and tasks as LLMs outputs can be irregular in terms of formatting

Sources:
https://www.crewai.com/
