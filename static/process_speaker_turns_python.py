def process_transcript(transcript_data):
    """
    Groups consecutive arrays with the same speaker into structured objects.
    
    Args:
        transcript_data (list): List of transcript segments in JSON format
        
    Returns:
        list: List of grouped speaker turns with consolidated information
    """
    if not transcript_data:
        return []
    
    processed_turns = []
    current_turn = {
        "speaker": transcript_data[0]["speaker"],
        "speaker-turn": transcript_data[0]["text"],
        "speaker-turn-start": transcript_data[0]["start"],
        "speaker-turn-end": transcript_data[0]["end"],
        "utterances": [transcript_data[0]]
    }
    
    for segment in transcript_data[1:]:
        if segment["speaker"] == current_turn["speaker"]:
            # Same speaker, append to current turn
            current_turn["speaker-turn"] += " " + segment["text"]
            current_turn["speaker-turn-end"] = segment["end"]
            current_turn["utterances"].append(segment)
        else:
            # New speaker, save current turn and start a new one
            processed_turns.append(current_turn)
            current_turn = {
                "speaker": segment["speaker"],
                "speaker-turn": segment["text"],
                "speaker-turn-start": segment["start"],
                "speaker-turn-end": segment["end"],
                "utterances": [segment]
            }
    
    # Don't forget to add the last turn
    processed_turns.append(current_turn)
    
    # Wrap in the final structure
    return {"turns": processed_turns}

# Example usage:
# result = process_transcript(transcript_data)
