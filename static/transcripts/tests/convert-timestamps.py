#!/usr/bin/env python3
import json
import argparse
import sys

def convert_timestamp_to_seconds(timestamp):
    """Convert timestamp format 'HH:MM:SS,mmm' to seconds with three decimal precision."""
    hours, minutes, seconds = timestamp.split(':')
    seconds, milliseconds = seconds.split(',')
    total_seconds = (int(hours) * 3600 + 
                    int(minutes) * 60 + 
                    int(seconds) + 
                    int(milliseconds) / 1000)
    return round(total_seconds, 3)

def process_json(data):
    """Process all timestamps in the JSON data."""
    for turn in data:
        for utterance in turn.get('utterances', []):
            if 'timestamps' in utterance:
                from_time = utterance['timestamps']['from']
                to_time = utterance['timestamps']['to']
                
                # Convert timestamps to seconds
                utterance['timestamps']['from'] = convert_timestamp_to_seconds(from_time)
                utterance['timestamps']['to'] = convert_timestamp_to_seconds(to_time)
    
    return data

def main():
    parser = argparse.ArgumentParser(description='Convert timestamps in JSON from HH:MM:SS,mmm format to seconds')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output JSON file path')
    
    args = parser.parse_args()
    
    try:
        # Load JSON data from input file
        with open(args.input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Process the data
        processed_data = process_json(data)
        
        # Write the processed data to the output file
        with open(args.output_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, indent=2, ensure_ascii=False)
        
        print(f"Conversion completed. Output saved to '{args.output_file}'")
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
