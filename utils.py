import re


# Generate filename using pattern: "Show Name - S01E01(-E02) - Episode Name"
def generate_filename(show_name, season, episode, second_episode, episode_name):
    filename = f"{show_name} - S{int(season):02d}E{int(episode):02d}"
    if second_episode:
        filename += f"-E{int(second_episode):02d}"
    filename += f" - {episode_name}"
    return slugify(filename)


# Return alphanumeric characters and spaces from start of the filname to sXXeXX
def guess_the_show(filename):
    filename = filename.replace("_", " ").replace(".", " ")
    pattern = "^(.*?)(?=\s+s\d{1,2}[-._ ]?e\d{1,2})"
    match = re.search(pattern, filename, re.IGNORECASE)
    try:
        return match.group()
    except:
        return None


# Return true if filename contains exactly two episodes
# Will return false positive if an episode is called something like "Pawn E2-E4", etc
def is_dual_episode(filename):
    return len(re.findall("e\d{1,2}", filename, re.IGNORECASE)) == 2


# Return true if filename contains season & episode numbers in sXXeXX pattern
def is_valid_file(filename):
    return re.search("s\d{1,2}[-._ ]?e\d{1,2}", filename, re.IGNORECASE) is not None


# Extract season & episode numbers
def parse_filename(filename):
    if is_valid_file(filename):
        season = int(re.findall("s\d{1,2}", filename, re.IGNORECASE)[0][1:])
        episodes = re.findall("e\d{1,2}", filename, re.IGNORECASE)
        episode = int(episodes[0][1:])
        second_episode = int(episodes[1][1:]) if len(episodes) == 2 else None
        return season, episode, second_episode
    else:
        return None, None, None


# Remove Windows reserved chars from filename
def slugify(filename):
    reserved_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
    for char in reserved_chars:
        filename = filename.replace(char, "")
    return filename
