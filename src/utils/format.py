def format_message(message: str, format: dict = {}):
    ret = message
    
    for rep, val in format.items():
        ret = ret.replace(rep, val)

    return ret

def retrieve_formats(cfg: dict, avg_rate: int, low_or_high: str = "Low") -> dict:
    return {
        "{avg}": avg_rate,
        "{low_or_high}": low_or_high,
        "{cfg_high_threshold}": cfg["HighThreshold"],
        "{cfg_low_threshold}": cfg["LowThreshold"],
        "{cfg_count}": cfg["AvgCount"]
    }