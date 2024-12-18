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

class financial_event_extraction():
    # Setup environment
    load_dotenv()

    # Setup logging
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)

    agents = FinancialAgents()
    event_extraction_agent = agents.event_extraction_agent()
    #cumulative_event_agent = agents.cumulative_event_agent()
    trading_decision_agent = agents.trading_decision_agent()

    tasks = FinancialAnalysisTasks()
    logger.info("Current working directory: %s", os.getcwd())
    csv_file_path = "/teamspace/studios/this_studio/crewai-groq-reddit/data/sentiment_results.csv"
    output_csv_file_path = "/teamspace/studios/this_studio/crewai-groq-reddit/data/event_analysis_results.csv"
    cumulated_csv_file_path = "/teamspace/studios/this_studio/crewai-groq-reddit/data/cumulated_results.csv"
    decision_csv_file_path = "/teamspace/studios/this_studio/crewai-groq-reddit/data/decision_results.csv"

    processed_urls = load_processed_urls(output_csv_file_path)


    # Read input CSV file
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        # Print headers to check for mismatches



            # Process each row
        for row in csv_reader:

                article_url = row['Article URL']

                if article_url in processed_urls:
                    print(f"Skipping already processed article: {article_url}")
                    continue


                company_name = row['Company']
                print(company_name)
                article_content = row['Article Content']

                submission_date = row['Submission Date']


                event_extraction_task = tasks.event_extraction_task(
                    agent=event_extraction_agent,
                    company_name=company_name,
                    financial_data={
                        'company_name': company_name,
                        'content': article_content,
                        'submission_date': submission_date,
                        'description': 'event identification of article content',
                        'expected_output': 'Major events detected?'
                    }
                )

            
                trading_decision_task = tasks.trading_decision_task(
                    agent=trading_decision_agent,
                    company_name=company_name,
                    financial_data=event_extraction_task
                    #context = event_extraction_task
                )

                crew = Crew(
                    agents=[
                    event_extraction_agent
                                
                    ],
                    tasks=[
                        event_extraction_task
                        
                        ],
                        max_rpm=25)
                


                start_time = time.time()
                #
                #crew.train(n_iterations=1)

                results = crew.kickoff()
                end_time = time.time()
                elapsed_time = end_time - start_time

                logger.info(f"Crew kickoff for {company_name} took {elapsed_time} seconds.")
                logger.info("Crew usage: %s", crew.usage_metrics)
               

            

            

    logger.info("Event analysis results have been saved to %s", output_csv_file_path)


    lines = results.split('\n')

    # Initialize an empty list to store the events
    events = []

    # Use a regular expression to match lines starting with a number followed by a period
    pattern = re.compile(r'^\d+\.\s+Event:')

    # Temporary variables to hold the current event and details
    current_event = None
    current_detail = []

    for line in lines:
        if pattern.match(line.strip()):
            # If we find a new event, save the previous event if it exists
            if current_event:
                events.append((current_event, ' '.join(current_detail).strip()))
            current_event = line.strip()
            current_detail = []
        elif current_event:
            current_detail.append(line.strip())

    # Add the last event if it exists
    if current_event:
        events.append((current_event, ' '.join(current_detail).strip()))

    # Print events for debugging
    print("Parsed Events:")
    for event, detail in events:
        print(f"{event}: {detail}")

    # Define the CSV file name
    date_str = datetime.now().strftime('%Y-%m-%d')
    csv_file = f'/teamspace/studios/this_studio/crewai-groq-reddit/data/events_{company_name}_{date_str}.csv'
  # Define the CSV file name with the company name
    # Write the events to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Event', 'Details'])
        writer.writerows(events)

    print(f'Events have been saved to {csv_file}')
