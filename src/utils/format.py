def format_message(message, format={}):
    ret = message
    
    for rep, val in format.items():
        ret = ret.replace(rep, val)

    return ret

def retrieve_formats(cfg, avg_rate, low_or_high="Low"):
    return {
        "{avg}": avg_rate,
        "{low_or_high}": low_or_high,
        "{cfg_high_threshold}": cfg["HighThreshold"],
        "{cfg_low_threshold}": cfg["LowThreshold"],
        "{cfg_count}": cfg["AvgCount"]
    }