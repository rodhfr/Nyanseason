import anitopy

# Options
anitopy_options = {'allowed_delimiters': ' '}

furico = anitopy.parse('[SubsPlease] Dandadan - 05 (1080p) [28020A6E].mkv', options=anitopy_options)

print(furico)
