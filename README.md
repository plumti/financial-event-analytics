# financial-event-analytics
Quick example of how financial events can be extracted using the Reddit API and Crew AI agents, and then used for stock analytics.
## Project Overview

In this project, I aimed to analyse multiple events within articles to see if they overlap and make informed trading decisions based on the extracted financial events. 

### Key Components

**Crew AI Agent and Task**: analyse financial data and suggest the best trading actions based on the current subreddit / topic.
Have a look at 
![Basic Task](/task.png)

![Basic Agent](/agent.png)
**Reddit API**: To fetch articles related to financial events.
   See the
   [Basic example](/Apple_articles_20240705_33.csv)
   ![Basic example](/article_content.png)
   ![Basic event extract](/event_ext.png)
[Basic event extraction](/events_Apple_2024-07-18.csv)


**Results of AI agents**:
[Basic results](/results_Apple_2024-07-18.csv)

### Challenges 
Data filtering was tricky,
Writing concise prompts for the AI agents and tasks as LLMs outputs can be irregular in terms of formatting

Sources:
https://www.crewai.com/


**Disclaimer: This example is for educational purposes only and should not be interpreted as trading advice. The provided code, timestamps, and datasets are used for visualisation and experimentation purposes and may not represent a realistic trading model.**
