import streamlit as st
import boto3
import pandas as pd
import os

# --- AWS & App Configuration ---
# Boto3 will automatically find the credentials
# you set in your terminal (Access Key, Secret Key, Token)
DYNAMO_TABLE_NAME = "NewsAnalysisTable"

@st.cache_data(ttl=60) # Caches the data for 60 seconds
def get_data_from_dynamodb():
    """
    Connects to DynamoDB and scans the entire table.
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(DYNAMO_TABLE_NAME)
        
        # Scan the table. For a hackathon, a scan is fine.
        # In production, you'd use a query.
        response = table.scan()
        
        items = response.get('Items', [])
        
        # Keep scanning if the table is large (paginated)
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
            
        return items
        
    except Exception as e:
        # Display a prominent error in the app if it fails
        st.error(f"Error connecting to DynamoDB: {e}")
        st.error("Have you run the 'export AWS_...' commands in your terminal?")
        return None

# --- Build the Web App ---
st.set_page_config(page_title="News Intelligence Agent", layout="wide")
st.title("📰 News & Trend Intelligence Agent")
st.write("This dashboard pulls live data from the DynamoDB table populated by our agent.")

# --- Fetch and Display Data ---
data = get_data_from_dynamodb()

if data:
    # Convert the list of dictionaries (from DynamoDB) into a Pandas DataFrame
    df = pd.DataFrame(data)
    
    # --- Data Cleanup & Display ---
    # Convert numeric strings to actual numbers for better sorting
    if 'sentimentPositive' in df.columns:
        df['sentimentPositive'] = pd.to_numeric(df['sentimentPositive'])
    if 'sentimentNegative' in df.columns:
        df['sentimentNegative'] = pd.to_numeric(df['sentimentNegative'])
    
    # Re-order columns to be more logical
    # Use only columns that we know exist from our pivoted script
    columns_to_show = ['title', 'source', 'topic', 'fetchedAt']
    
    # But if the 'sentiment' column exists (from your 'Option 3' idea), show it!
    if 'sentiment' in df.columns:
        columns_to_show.insert(1, 'sentiment')

    # Filter the DataFrame to only show the columns we want
    display_df = df[columns_to_show]

    st.dataframe(display_df, use_container_width=True)
    
    st.success(f"Successfully fetched {len(df)} articles from DynamoDB.")
    
    # Show the raw data in an expandable section
    with st.expander("Show Raw Data"):
        st.json(data)
else:
    st.warning("No data found in DynamoDB table.")