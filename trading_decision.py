import os
import time
import csv
import logging
import re
from crewai import Crew
from crewai import Task
from dotenv import load_dotenv
from agents import FinancialAgents
from tasks import FinancialAnalysisTasks
import subprocess
import schedule
from reddit_scraper import scrape_subreddit, TextProcessor
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
from article_preprocessor import read_company_for_event_extraction, load_processed_urls
from event_extraction import financial_event_extraction
class financial_trading_decision():

    # Setup environment
    load_dotenv()

    # Setup logging
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)

    agents = FinancialAgents()
    trading_decision_agent = agents.trading_decision_agent()

    tasks = FinancialAnalysisTasks()
    logger.info("Current working directory: %s", os.getcwd())
    cumulated_csv_file_path = "/teamspace/studios/this_studio/crewai-groq-reddit/data/cumulated_results.csv"

    trading_decision_task = tasks.trading_decision_task(
        agent=trading_decision_agent,
        company_name=financial_event_extraction.company_name,
        financial_data=financial_event_extraction.event_extraction_task
        # context = event_extraction_task
    )

    crew = Crew(
        agents=[
            trading_decision_agent
        ],
        tasks=[
            trading_decision_task
        ],
        max_rpm=25
    )

    start_time = time.time()
    results = crew.kickoff()
    end_time = time.time()
    elapsed_time = end_time - start_time

    logger.info(f"Crew kickoff for {financial_event_extraction.company_name} took {elapsed_time} seconds.")
    logger.info("Crew usage: %s", crew.usage_metrics)

    # Print results for debugging
    print("Results:")
    print(results)

    # Parse results for action and rationale
    # Look for common trading action phrases
    action_keywords = ['buy', 'sell', 'short', 'hold']
    action = 'Unknown Action'

    # Finding action
    for keyword in action_keywords:
        if keyword in results.lower():
            action = keyword.capitalize()
            break

    # Extracting rationale after the action keyword
    action_index = results.lower().find(action.lower())
    if action_index != -1:
        rationale = results[action_index + len(action):].strip()
    else:
        rationale = results.strip()

    # Clean up the rationale text to make it more readable
    rationale = rationale.replace('\n', ' ').strip()

    # Define the CSV file name with the company name and current date
    date_str = datetime.now().strftime('%Y-%m-%d')
    company_name_safe = re.sub(r'\W+', '_', financial_event_extraction.company_name)
    csv_file = f'/teamspace/studios/this_studio/crewai-groq-reddit/data/results_{company_name_safe}_{date_str}.csv'

    # Write the trading decision to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Action', 'Rationale'])
        writer.writerow([action, rationale])

    print(f'Trading decisions have been saved to {csv_file}')
