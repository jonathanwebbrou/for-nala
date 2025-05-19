# Yugioh Card Scanner

A Python application that uses computer vision and AI to scan Yugioh cards via webcam and automatically update a collection CSV file.

## Description

This tool helps Yugioh collectors maintain an accurate inventory of their cards by:
- Capturing card images through a webcam
- Using AI (via Ollama) to identify card details (name, set code, rarity, type)
- Automatically updating a CSV inventory with the scanned cards
- Tracking quantities of duplicate cards

## Setup and Requirements

### Prerequisites

- Python 3.7+
- Webcam
- Ollama installed on your system

### Required Python Packages

```
pip install opencv-python pandas requests
```

### Ollama Setup

1. Download and install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull a multimodal model that can process images:
   ```
   ollama pull llava
   ```
   (Alternative models: llava:13b, bakllava, or other multimodal models)
3. Ensure Ollama is running before starting the application

## Usage

1. Place your existing CSV file (if any) in the same directory as the script
2. Run the script:
   ```
   python yugioh_scanner.py
   ```
3. Point your webcam at a Yugioh card
4. Press 's' to scan and identify the card
5. Press 'q' to quit the application

The script will:
- Save captured images to a 'captured_cards' folder
- Update the 'yugioh_collection.csv' file with new card data
- Increment the quantity for cards already in the collection

## Potential Improvements

### Card Value Integration
- Connect to a Yugioh pricing API (like TCGPlayer or YugiohPrices)
- Automatically fetch and update current market values for cards

### Image Enhancement
- Implement card edge detection for better framing
- Add perspective correction for cards captured at angles
- Include image preprocessing for better recognition in poor lighting

### User Interface
- Develop a graphical user interface (GUI) for easier operation
- Add card preview and confirmation before adding to database
- Include collection statistics dashboard

### Batch Processing
- Enable scanning multiple cards in sequence
- Add bulk import/export functionality
- Implement collection backup features

### Advanced Features
- Card authentication (detecting fake cards)
- Deck building recommendations based on collection
- Archetype tracking and completion percentage

## Troubleshooting

- **Card Not Recognized**: Ensure good lighting and that the card is clearly visible
- **Ollama Connection Failed**: Verify Ollama is running with `ollama list`
- **Webcam Not Working**: Check your camera permissions and connections

## License

[MIT License](LICENSE)

## Contributing

Contributions, issues, and feature requests are welcome!
