import sys
import time

import config
import fitbit
import actions
import utils

def main():
    cfg_file = "/etc/fhm/cfg.json"
    list = False

    # Parse arguments.
    for arg in sys.argv:
        # Check for custom config path.
        if arg.startswith("cfg="):
            cfg_file = arg.split("=")[1]

        # Check for list.
        if arg == "-l" or arg == "--list":
            list = True
    
    # Load config.
    cfg = config.loadCFG(cfg_file)

    # Check if we need to print config.
    if list:
        print(cfg)

        return

    # Create an infinite loop that executes each second.
    while True:
        utils.debug_message(cfg, 3, "Retrieving heart rates...")

        # Retrieve our heart rates as a list.
        rates = fitbit.retrieve_heartrates(cfg)

        # Get the average between our heart rates.
        avg_rate = sum(rates) / len(rates)

        utils.debug_message(cfg, 3, "Heart rates retrieved :: Avg => " + str(avg_rate))

        # Check if we're below or above threshold.
        if avg_rate > int(cfg["HighThreshold"]) or avg_rate < int(cfg["LowThreshold"]):
            utils.debug_message(cfg, 1, "Heart rates are below or above thresholds!")

            # Determine if we have a low or high threshold.
            low_or_high = "High"

            if avg_rate < int(cfg["LowThreshold"]):
                low_or_high = "Low"

            # Retrieve default formats for our action messages.
            formats = utils.retrieve_formats(cfg, avg_rate, low_or_high)

            # Loop through actions.
            for action in cfg["Actions"]:
                utils.debug_message(cfg, 3, "Parsing action...")

                # Ensure we have a type.
                if "Type" not in "action":
                    print("Action doesn't contain a type!")

                    continue

                # Check for HTTP request.
                if action.lower() == "http":
                    utils.debug_message(cfg, 2, "Found action with type HTTP!")

                    # Make sure we have a URL set.
                    if "Url" not in action:
                        print("Action of HTTP request does NOT contain a URL!")

                        continue

                    method = "POST"

                    if "Method" in action:
                        method = action["Method"]

                    timeout = 5.0

                    if "Timeout" in action:
                        timeout = float(action["Timeout"])
                    
                    headers = {}

                    if "Headers" in action:
                        headers = action["Headers"]

                    body = {}

                    if "Body" in action:
                        body = action["Body"]

                    # Make request and retrieve response.
                    resp = actions.send_http_request(action["Url"], method, headers, body, timeout)

                    utils.debug_message(cfg, 1, "Sending HTTP request :: %s (method => %s)!" % (action["Url"], method))

                    utils.debug_message(cfg, 3, "HTTP request status code => %d. JSON Response => %s." % (resp.status_code, resp.json()))
                # Otherwise, we want to send an email.
                else:
                    utils.debug_message(cfg, 2, "Found action with type email!")
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
                    message = utils.format_message(message, formats)

                    # Send email.
                    actions.send_email(host, port, from_email, from_name, to_name, to_email, subject, message)

                    # Debug
                    utils.debug_message(cfg, 1, "Sending email :: %s => %s!" % (from_email, to_email))
        time.sleep(1)

if __name__ == "__main__":
    main()