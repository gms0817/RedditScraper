# Imports
import tkinter as tk

import pmaw.Metadata
import praw
import pandas as pd
import os
import time
import sv_ttk
from pmaw import PushshiftAPI
import datetime as dt
from tkinter import ttk

# Test
# Test

def main():
    # Scrape Reddit Based on User Input
    def scrape_reddit(subreddit_input, num_of_posts):
        # Initialize PushshiftAPI
        api = PushshiftAPI()

        # Update Status Label
        status_label.config(text="Scraping...")

        # Remove r/ if user puts it in
        if "/r" in subreddit_input:
            subreddit_input = subreddit_input[2:]
        print("Subreddit: " + subreddit_input)  # For debugging

        # Collect integer from num_of_posts input
        if "all" in num_of_posts:
            num_of_posts = None
        else:
            num_of_posts = int(num_of_posts)
        print("Number of Posts: " + str(num_of_posts))  # For debugging

        # Read-only instance of scraper
        reddit = praw.Reddit(client_id="RVwOTqiFJbXKWzeHRztGHQ",
                             client_secret="cg70MVjFpakehf6k-zwCXXim0KymfA",
                             user_agent="GmS_11702")

        subreddit = subreddit_input

        # Directory to store data
        directory = 'datasets/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        submissions_dict = {
            "title": [],
            "selftext": []
        }

        # Use PSAW to get ID of submissions based on time interval
        print('Getting IDs...')
        gen = api.search_submissions(
            filter=['id'],
            subreddit=subreddit,
            limit=num_of_posts
        )
        print('IDs Obtained.')
        print('Getting Posts...')
        # Use PRAW to get submission information
        submission_count = 0
        start_time = time.time()
        for submission_pmaw in gen:
            time_elapsed = time.time() - start_time
            submission_count = submission_count + 1

            # Use pmaw
            submission_id = submission_pmaw['id']

            # Use praw
            submission_praw = reddit.submission(id=submission_id)

            # Add submission data to submissions dictionary
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["selftext"].append(submission_praw.selftext)

            # Provide scraping progress to console
            print(f'Elapsed Time: {time_elapsed / 60: .2f}m | '
                  f'Submissions Scraped: {submission_count}/{num_of_posts} | '
                  f'Target Subreddit: {subreddit_input}')

            # Save scraped data to csv
            pd.DataFrame(submissions_dict).to_csv(directory + subreddit + '-' + str(num_of_posts) + '.csv', index=False)
        print(f'Obtained {num_of_posts} from {subreddit_input}.')

    # -----------------------------------------------------------------------
    # Create window
    reddit_scraper = tk.Tk()
    reddit_scraper.title("Reddit Scraper")

    # Setup window dimensions
    window_width = 720
    window_height = 480

    # Get screen dimensions
    screen_width = reddit_scraper.winfo_screenwidth()
    screen_height = reddit_scraper.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Configure Window
    reddit_scraper.geometry(f'{400}x{400}+{center_x + 160}+{center_y}')
    reddit_scraper.focus()

    # Tool Title
    title_label = ttk.Label(reddit_scraper, text="Reddit Scraper")
    title_label.pack(padx=10, pady=15)

    # Subreddit to Scrape
    subreddit_label = ttk.Label(reddit_scraper, text="What subreddit do you want to scrape?")
    subreddit_label.pack(padx=10, pady=10)

    subreddit_field = ttk.Entry(reddit_scraper, width=25)
    subreddit_field.pack(padx=10, pady=10)

    # Number of Posts to Scrape
    num_of_posts_label = ttk.Label(reddit_scraper, text="How many posts would you like to scrape?")
    num_of_posts_label.pack(padx=10, pady=10)

    num_of_posts_field = ttk.Entry(reddit_scraper, width=25)
    num_of_posts_field.pack(padx=10, pady=10)

    # Status Label
    status_label = ttk.Label(reddit_scraper, text="Waiting...")
    status_label.pack(padx=10, pady=10)

    # Submit Button
    reddit_submit_button = ttk.Button(reddit_scraper,
                                      text="Scrape",
                                      command=lambda: [status_label.config(text="Scraping..."),
                                                       scrape_reddit(subreddit_field.get(),
                                                                     num_of_posts_field.get())])
    reddit_submit_button.pack(padx=10, pady=10)

    # Set theme
    sv_ttk.set_theme("dark")
    # Show window
    reddit_scraper.mainloop()


if __name__ == '__main__':
    main()
