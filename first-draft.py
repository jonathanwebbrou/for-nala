import cv2
import pandas as pd
import requests
import time
import os
from datetime import datetime

# Load the existing CSV file
def load_csv(csv_path):
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        # Create a new DataFrame with the correct columns if file doesn't exist
        return pd.DataFrame(columns=['Card Name', 'Quantity', 'Set Code', 'Rarity', 
                                    'Type', 'Value (USD)', 'Deck / Archetype', 
                                    'Box / Label', 'Row in Box'])

# Function to interact with Ollama API
def identify_card(image_path):
    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"
    
    # Read image as base64
    with open(image_path, "rb") as image_file:
        import base64
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Create the prompt for the model
    prompt = """
    This is an image of a Yugioh card. Please extract the following information:
    - Card Name
    - Set Code (alphanumeric code usually at the bottom of the card)
    - Rarity (Common, Rare, Super Rare, Ultra Rare, etc.)
    - Card Type (Monster, Spell, Trap, etc.)
    
    Format the response as JSON with these fields only. If you can't identify any field, use null.
    """
    
    # Make the API request
    payload = {
        "model": "llava:latest", # or another multimodal model available in Ollama
        "prompt": prompt,
        "images": [image_data],
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    try:
        # Parse the model's response to extract structured data
        # This would need refinement based on actual model output
        import json
        from io import StringIO
        import re
        
        output = result.get('response', '')
        
        # Extract JSON from the response if it's wrapped in markdown or other text
        json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON-like structure without markdown
            json_match = re.search(r'({[\s\S]*})', output)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = output
                
        # Clean and parse the JSON
        json_str = json_str.replace("'", '"')
        card_data = json.loads(json_str)
        
        return card_data
    except Exception as e:
        print(f"Error parsing model output: {e}")
        print(f"Raw output: {output}")
        return None

# Function to update the CSV with new card data
def update_csv(csv_df, card_data, csv_path):
    # Check if card already exists in the DataFrame
    card_name = card_data.get('Card Name')
    if card_name is None:
        print("Could not identify card name")
        return csv_df
    
    # Look for the card in the CSV
    existing_card = csv_df[csv_df['Card Name'] == card_name]
    
    if len(existing_card) > 0:
        # Card exists, update quantity
        idx = existing_card.index[0]
        csv_df.at[idx, 'Quantity'] = csv_df.at[idx, 'Quantity'] + 1
        print(f"Updated quantity for {card_name}")
    else:
        # New card, add it to the DataFrame
        new_row = {
            'Card Name': card_name,
            'Quantity': 1,
            'Set Code': card_data.get('Set Code'),
            'Rarity': card_data.get('Rarity'),
            'Type': card_data.get('Type'),
            'Value (USD)': None,  # This could be fetched from a pricing API
            'Deck / Archetype': None,
            'Box / Label': None,
            'Row in Box': None
        }
        csv_df = pd.concat([csv_df, pd.DataFrame([new_row])], ignore_index=True)
        print(f"Added new card: {card_name}")
    
    # Save the updated DataFrame
    csv_df.to_csv(csv_path, index=False)
    return csv_df

# Main function to capture image from webcam and process it
def main():
    csv_path = "yugioh_collection.csv"
    csv_df = load_csv(csv_path)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)  # 0 is usually the default webcam
    
    # Create a folder for storing captured images
    os.makedirs('captured_cards', exist_ok=True)
    
    print("Press 's' to scan a card, 'q' to quit")
    
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        
        # Display the frame
        cv2.imshow('Yugioh Card Scanner', frame)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        
        # 's' key to scan card
        if key == ord('s'):
            # Save the current frame as an image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"captured_cards/card_{timestamp}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Image saved to {image_path}")
            
            # Process the image to identify the card
            print("Identifying card...")
            card_data = identify_card(image_path)
            
            if card_data:
                print(f"Card identified: {card_data.get('Card Name', 'Unknown')}")
                # Update the CSV with the new card data
                csv_df = update_csv(csv_df, card_data, csv_path)
            else:
                print("Failed to identify card")
        
        # 'q' key to quit
        elif key == ord('q'):
            break
    
    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
