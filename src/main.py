import sys
import time

import config
import fitbit
import actions

def main():
    cfg_file = "/etc/fhm/cfg.json"

    # Check if we have a custom CFG path.
    for arg in sys.argv:
        if arg.startswith("cfg="):
            cfg_file = arg.split("=")[1]
    
    # Load config.
    cfg = config.loadCFG(cfg_file)

    # Create an infinite loop that executes each second.
    while True:
        # Retrieve our heart rates as a list.
        rates = fitbit.retrieve_heartrates(cfg)

        # Get the average between our heart rates.
        avg_rate = sum(rates) / len(rates)

        # Check if we're below or above threshold.
        if avg_rate > int(cfg["HighThreshold"]) or avg_rate < int(cfg["LowThreshold"]):
            # Determine if we have a low or high threshold.
            low_or_high = "High"

            if avg_rate < int(cfg["LowThreshold"]):
                low_or_high = "Low"

            # Loop through actions.
            for action in cfg["Actions"]:
                # Ensure we have a type.
                if "Type" not in "action":
                    print("Action doesn't contain a type!")

                    continue

                # Check for HTTP request.
                if action.lower() == "Http":
                    # Make sure we have a URL set.
                    if "Url" not in action:
                        print("Action of HTTP request does NOT contain a URL!")

                        continue

                    method = "POST"

                    if "Method" in action:
                        method = action["Method"]
                    
                    headers = {}

                    if "Headers" in action:
                        headers = action["Headers"]

                    body = {}

                    if "Body" in action:
                        body = action["Body"]

                    # Make request and retrieve response.
                    resp = actions.send_http_request(action["Url"], method, headers, body)

                    # To Do: Check response.

                    config.debug_message(cfg, 1, "Sending HTTP request :: %s (method => %s)!" % (action["Url"], method))
                # Otherwise, we want to send an email.
                else:
                    # Retrieve SMTP/email configuration.
                    host = "localhost"

                    if "Host" in action:
                        host = action["Host"]

                    port = 25

                    if "Port" in action:
                        port = int(action["Port"])

                    from_name = "Test From"

                    if "FromName" in action:
                        from_name = action["FromName"]

                    from_email = "test@localhost"

                    if "FromEmail" in action:
                        from_email = action["FromEmail"]

                    to_name = "Test User"

                    if "ToName" in action:
                        to_name = action["ToName"]

                    to_email = "test@localhost"

                    if "ToEmail" in action:
                        to_email = action["ToEmail"]

                    subject = "Heartrate threshold!"

                    if "Subject" in action:
                        subject = action["Subject"]

                    message = "Test contents!"

                    if "Message" in action:
                        message = action["Message"]

                    # Format message.
                    message = message.replace("{avg}", avg_rate)
                    message = message.replace("{low_or_high}", low_or_high)
                    message = message.replace("{cfg_high_threshold}", cfg["HighThreshold"])
                    message = message.replace("{cfg_low_threshold}", cfg["LowThreshold"])
                    message = message.replace("{cfg_count}", cfg["AvgCount"])

                    # Send email.
                    actions.send_email(host, port, from_email, from_name, to_name, to_email, subject, message)

                    # Debug
                    config.debug_message(cfg, 1, "Sending email :: %s => %s!" % (from_email, to_email))
        time.sleep(1)

if __name__ == "__main__":
    main()