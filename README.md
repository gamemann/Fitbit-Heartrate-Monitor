# Fitbit Heartrate Monitor (Work In Progress)
An application that interacts with [Fitbit's](https://fitbit.com/) [Web API](https://dev.fitbit.com/build/reference/web-api) to retrieve information on a person's heart rate. If the heart rate goes below or above a certain threshold, certain actions may be performed such as sending an email or HTTP request.

## Command Line
The following command-line options are available.

```
cfg=<file> => Custom config path.
-l or --list => List all contents from config file.
```

### Examples
```bash
# List contents of config.
python3 src/main.py -l

# Use custom.json as config file in working directory.
python3 src/main.py cfg=./custom.json
```

## Configuration
All configuration is handled in a file with the JSON format. The default config is `/etc/fhm/cfg.json`. You may find documented configuration below.

```
{
    // Debug level from 0 - 3 (0 = no debug).
    "Debug": 0,

    // Authorization Bearer key (do not include "Bearer").
    "Authorization": "",

    // Fitbit user's ID. '-' indicates currently signed in user.
    "UserID": "-",

    // Low threshold for triggering heart rate action.
    "LowThreshold": 50,

    // High threshold for trigger heart rate action.
    "HighThreshold": 120,

    // The amount of previous heart rates to include in average.
    "AvgCount": 10,

    // Actions array.
    "Actions": 
    [
        // Action: Send HTTP request.
        {
            // Type of action (HTTP in this case).
            "Type": "http",

            // URL to send HTTP request to.
            "Url": "testdomain.com?get1=val1&get2=val2",

            // The HTTP request's method (e.g. GET or POST).
            "Method": "GET",

            // HTTP requests timeout (default 5.0).
            "Timeout": 5.0,

            // Headers (if any).
            "Headers": {
                "Authorization": "Bearer <some key>"
            }

            // Request's body (most useful for POST request; For GET, this is params).
            "Body": {}
        },
        // Action: Send Email
        {
            // Type of action (Email in this case).
            "Type": "email",

            // SMTP host.
            "Host": "localhost",

            // SMTP port.
            "Port": 25,

            // From email.
            "FromEmail": "ian.demi@testdomain.com",

            // Emails to send to in an array.
            "ToEmail": ["christian.deacon@anothertestdomain.com"],

            // Subject of email.
            "Subject": "Heart rate warning!",

            // Message/body of email.
            "Message": "Your heart rate is currently too high or too low!"
        }
    ]
}
```

**Warning** - The above JSON is **not** valid due to comments. Please use the `cfg.json.example` if you want to start from somewhere (preferably with `sudo make install`)

### Action Format Options
Format options for an action's HTTP URL/body or email subject/body message include the following.

```
{avg_rate} => The average heart rate detected.
{low_or_high} => Prints "Low" if the average heart rate was below threshold or "High" if the average heart rate was above threshold.
{cfg_high_threshold} => The config's high theshold value.
{cfg_low_threshold} => The config's low threshold value.
{cfg_count} => The config's average count value.
```

## Motives
I currently live with a family member who has health issues with their heart and high blood pressure. I wanted to make something to alert my other family members and I if this person's heart rate is abnormally low or high.

## Credits
* [Christian Deacon](https://github.com/gamemann)
