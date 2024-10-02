#!/bin/bash

# Define the port to listen on
PORT=6969
LOG_FILE="log.txt"

# Create or clear the log file
> $LOG_FILE

# Function to listen for incoming connections and update the log file
function listen_for_updates {
    local last_entry=""
    
    while true; do
        # Use netcat (nc) to listen for a connection and write incoming data to a temporary file
        nc -l -p $PORT > temp_log.txt
        
        # If temp_log.txt has content
        if [[ -s temp_log.txt ]]; then
            # Read the new data
            new_entry=$(cat temp_log.txt)
            
            # Check if the new data is different from the last logged entry
            if [[ "$new_entry" != "$last_entry" ]]; then
                # Append the new entry to the main log file
                echo "$new_entry" >> $LOG_FILE
                # Update last_entry to the new entry
                last_entry="$new_entry"
            fi
        fi

        # Clean up the temporary log file
        rm temp_log.txt

        # Wait for 10 seconds before listening again
        sleep 10
    done
}

# Start listening for incoming connections and updating the log file
listen_for_updates
