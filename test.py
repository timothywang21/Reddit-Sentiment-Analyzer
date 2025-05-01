from reddit2text import Reddit2Text

print("******Reddit text saver program [Powered by Reddit2Text Library]*******")
r2t = Reddit2Text(
    # replace with your actual creds
    client_id='AAgLx2p8_YvX_eF9a5X7IQ',
    client_secret='TZUlcxTySuYGglE7LOfQlFRKKPDccQ',
    user_agent='script:my_app:v1.0 (by u/Salty_Reputation6394)'
)

URL = 'https://www.reddit.com/r/OnlineMCIT/comments/1cj28ui/does_anyone_else_think_the_ai_degree_is_useless/'

#Save the text read from Reddit API to output str variable
output = r2t.textualize_post(URL)

# Specify the path and filename where you want to save the output
file_path = "C:/Users/Tim/Desktop/output.txt"

# Open the file in write mode
with open(file_path, "w", encoding="utf-8") as file:
    # Write the output to the file
    file.write(output)

print("Output saved to:", file_path)