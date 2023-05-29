def debug_message(cfg, level=1, message="Debug Message"):
    if int(cfg["Debug"]) >= level:
        print("[%d]%s" % (level, message))