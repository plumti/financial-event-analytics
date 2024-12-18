import os
from crewai import Agent
from langchain_groq import ChatGroq


class FinancialAgents():
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="mixtral-8x7b-32768"
        )

    def financial_researcher_agent(self):
        return Agent(
            role="Financial Researcher",
            goal="""
                Gather all of the necessary data for algorithmic trading e.g current financial information. Using search tools, about a company for the Financial Analyst to prepare a detailed analysis.
                """,
            backstory="""
                An expert financial researcher, who spends all day and night thinking about financial performance of different companies.
                """,
            verbose=True,
            llm=self.llm,
            max_iter=2,
        )

    def event_extraction_agent(self):
        return Agent(
            role="Financial event extraction analyst",
            goal="""
                Identify 5 or less major events that have recently happened or will happen, that may cause market disruptions.
                """,
            backstory="""
                An expert financial analyser, who spends all day and night thinking about financial performance and sentiment of different companies.
                """,
            verbose=True,
            llm=self.llm,
            max_iter=2,
        )
        
    def financial_analyst_agent(self):
        return Agent(
            role="Financial Analyst",
            goal="""
                Take provided company financial information and create a thorough numerical financial report about a given company, analyze cumulative major financial events for companies.
                """,
            backstory="""
                An expert financial analyst, who prides themselves on creating clear and easily readable financial reports of different companies.
                """,
            verbose=True,
            llm=self.llm,
            max_iter=2,
        )


    def cumulative_event_agent(self):
            return Agent(
                role="Financial Analysis Agent",
                goal="""
                    To identify and analyze cumulative major financial events for companies, providing a brief description and assessing the potential impact on the market.""",
                backstory="""
                        This agent was developed to assist financial analysts by automating the extraction and analysis of significant financial events from large datasets. The agent leverages advanced text analysis techniques to ensure accurate and insightful analysis.""",
                verbose=True,
                llm=self.llm,
                max_iter=2,
            )


    def trading_decision_agent(self):
            return Agent(
            role="Trading decision maker",
            goal="Make informed trading decisions based on financial data.",
            backstory="An intelligent agent designed to analyze stock market data and make buying or selling decisions.",
            verbose=True,
            llm=self.llm,
            max_iter=2,
        )


    