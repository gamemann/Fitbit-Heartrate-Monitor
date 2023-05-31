import sys
import time

import config
import fitbit
import actions
import utils

def main():
    cfg_file: str = "/etc/fhm/cfg.json"
    list: bool = False

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

        if rates is None:
            print("Error retrieving heart rates... Sleeping for 5 seconds.")

            time.sleep(5)

        # Get the average between our heart rates.
        avg_rate: int = int(sum(rates) / len(rates))

        utils.debug_message(cfg, 3, "Heart rates retrieved :: Avg => " + str(avg_rate))

        # Check if we're below or above threshold.
        if avg_rate > int(cfg["HighThreshold"]) or avg_rate < int(cfg["LowThreshold"]):
            utils.debug_message(cfg, 1, "Heart rates are below or above thresholds!")

            # Determine if we have a low or high threshold.
            low_or_high: str = "High"

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
                if action["Type"].lower() == "http":
                    utils.debug_message(cfg, 2, "Found action with type HTTP!")

                    # Make sure we have a URL set.
                    if "Url" not in action:
                        print("Action of HTTP request does NOT contain a URL!")

                        continue

                    url: str = str(action["Url"])

                    # Format URL in the case of GET request.
                    url = utils.format_message(url, formats)

                    method: str = "POST"

                    if "Method" in action:
                        method = str(action["Method"])

                    timeout: float = 5.0

                    if "Timeout" in action:
                        timeout = float(action["Timeout"])
                    
                    headers: dict[str, str] = {}

                    if "Headers" in action:
                        headers = action["Headers"]

                    body: dict[str, str] = {}

                    if "Body" in action:
                        body = action["Body"]

                    # Format values for body.
                    for key, val in body.items():
                        newVal = utils.format_message(val, formats)

                        body[key] = newVal

                    # Make request and retrieve response.
                    resp = actions.send_http_request(action["Url"], method, headers, body, timeout)

                    utils.debug_message(cfg, 1, "Sending HTTP request :: %s (method => %s)!" % (action["Url"], method))

                    utils.debug_message(cfg, 3, "HTTP request status code => %d. JSON Response => %s." % (resp.status_code, resp.json()))
                # Otherwise, we want to send an email.
                else:
                    utils.debug_message(cfg, 2, "Found action with type email!")
                    # Retrieve SMTP/email configuration.
                    host: str = "localhost"

                    if "Host" in action:
                        host = str(action["Host"])

                    port: int = 25

                    if "Port" in action:
                        port = int(action["Port"])

                    from_email: str = "test@localhost"

                    if "FromEmail" in action:
                        from_email = str(action["FromEmail"])

                    to_email = "test@localhost"

                    if "ToEmail" in action:
                        to_email = str(action["ToEmail"])

                    subject: str = "Heartrate threshold!"

                    if "Subject" in action:
                        subject = str(action["Subject"])

                    # Format subject.
                    subject = utils.format_message(subject, formats)

                    message: str = "Test contents!"

                    if "Message" in action:
                        message = str(action["Message"])

                    # Format message.
                    message = utils.format_message(message, formats)

                    # Send email.
                    actions.send_email(host, port, from_email, to_email, subject, message)

                    # Debug
                    utils.debug_message(cfg, 1, "Sending email :: %s => %s!" % (from_email, to_email))
        time.sleep(1)

if __name__ == "__main__":
    main()