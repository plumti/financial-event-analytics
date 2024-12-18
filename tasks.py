import os
import csv
from crewai import Task
class FinancialAnalysisTasks():
    def event_extraction_task(self, agent, company_name, financial_data):
        output_description = "List of major events with their descriptions and potential impact"

        return Task(
            description=f"""
                Analyze {company_name}'s financial information and identify major events that may cause market changes.
            """,
            agent=agent,
            context=[financial_data],
            expected_output=output_description,
        )

    def cumulative_events_task(self, agent, company_name, financial_data):
            output_description = "List of cumulative major events with their descriptions and potential impact"

            return Task(
                description=f"""
                    Analyze {company_name}'s list of financial events to identify cumulative major events that have appeared in multiple instances. List each cumulative event no explanation needed.
                """,
                agent=agent,
                context=[financial_data],
                expected_output=output_description,
            )

    def trading_decision_task(self, agent, company_name, financial_data):
        shares_held = False
        context = None
        quantity = 0
        
        try:
            with open("/teamspace/studios/this_studio/crewai-groq-reddit/data/stock_holdings_status.csv", 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    timestamp, symbol, status, qty = row
                    if symbol == company_name:
                        shares_held = True
                        context = status
                        quantity = int(qty)
                        break
                        
        except Exception as e:
            print(f"Error occurred while reading CSV: {e}")

        # Set a different precondition based on the context
        if shares_held and context == "held":
            precondition = f"""as we have
            a Position held for {company_name}:
            choose one only:
            - Hold the position
            - Buy more
            - Get out of position
            """
        elif shares_held and context == "shorting":
            precondition = f"""as we have
            a short position for {company_name}:
            choose one only:
            - Hold the short position
            - Short more
            - Get out of short position
            """  
        else:
            precondition = f"""as we don't
            hold a Position for {company_name}:
            choose one only:
            - Buy
            - Short """

        output_description = f"""
        Decision options for {company_name}:
        choose one only:
        - Buy
        - Hold
        - Get out of position
        - Short 
        """

      

        return Task(
            description=f"""
            Evaluate {company_name} and suggest Precondition: {precondition}
            """,
            agent=agent,
            context=[financial_data, {
                "shares_held": shares_held,
                "context": context,
                "quantity": quantity,
                "description": f"Trading decision for {company_name}",
                "expected_output": output_description
            }],
            expected_output=output_description,
        )