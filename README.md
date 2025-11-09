Here is a great description you can use for your README.md file on GitHub. This is the first thing the judges will read.

Hackathon Track 1: News & Trend Intelligence Agent
This is our submission for the News & Trend Intelligence Agent track. Our project fetches live news articles, performs real-time sentiment analysis, and displays the results on an interactive web dashboard.

Workflow
Our project works in two parts:

The Agent (run_agent.py): A Python script that:

Fetches live news headlines from the NewsAPI.

Performs keyword-based sentiment analysis (POSITIVE, NEGATIVE, NEUTRAL) on each title.

Writes the article data and its sentiment to a cloud database (Amazon DynamoDB).

The Dashboard (dashboard.py): A Streamlit web app that:

Connects live to the Amazon DynamoDB table.

Displays all the fetched articles and their sentiment in a clean, filterable table.

Acts as the final "intelligence brief" for the user.





Our Hackathon Story: Pivots & Problem-Solving
We hit several real-world roadblocks and successfully pivoted to deliver a working project:

Problem 1: Our AWS hackathon role was locked down and blocked AWS Lambda and EventBridge.

Our Pivot: We re-engineered the agent to run as a local script that still connected to cloud services (DynamoDB), proving the pipeline works.

Problem 2: The AWS role also blocked the Amazon Comprehend AI service for sentiment analysis.

Our Pivot: We wrote our own sentiment analyzer from scratch, using keyword matching to fulfill the project's "intelligence" requirement.

Problem 3: We encountered deep C++ build errors (pyarrow) due to using the brand-new Python 3.14.

Our Pivot: We debugged the environment issue, built a stable Python 3.12 virtual environment (venv), and successfully ran the project.





How to Run This Project
Clone this repository: git clone ...

Install a stable Python version (e.g., python3.12).

Create a virtual environment: python3.12 -m venv venv

Activate it: source venv/bin/activate

Install all dependencies

Copy the example environment file: cp .env.example .env

Edit .env and add your personal NewsAPI key.

Set your AWS credentials (Access Key, Secret Key, Session Token) in your terminal.

Run the Agent (to get data): venv/bin/python run_agent.py

Run the Dashboard: venv/bin/python -m streamlit run dashboard.py
