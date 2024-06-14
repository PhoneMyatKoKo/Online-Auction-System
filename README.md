Online Auction Website
Welcome to the Online Auction Website, an auction platform built using Django where users can view, search, and bid on listings. Users can also create their own listings and manage a personalized watchlist.

Table of Contents
Features
Installation
Usage

Features
For All Users:
View Listings: Browse all available listings with details such as item description, starting bid, and current highest bid.
Search Listings: Use the search functionality to find specific listings by keywords.
For Registered Users:
Add to Watchlist: Save interesting listings to a personal watchlist for easy access later.
Bid on Listings: Place bids on listings and compete with other users.
Post Listings: Create new listings with a title, description, image, and starting bid.
Manage Watchlist: View and remove items from the watchlist.
Installation
To get this project up and running locally, follow these steps:

Prerequisites
Python 3.x
Django 3.x
SQLite (default for Django)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/online-auction.git
cd online-auction
Create a virtual environment and activate it:

bash
Copy code
python -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate`
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Apply migrations:

bash
Copy code
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Open your browser and go to:

Usage
Browsing Listings
Go to the homepage to see all active listings.
Click on a listing to view its details, including the current highest bid and a description.
Searching Listings
Use the search bar to find listings by entering keywords related to the items you are looking for.
Managing Watchlist
To add a listing to your watchlist, click the "Add to Watchlist" button on the listing's detail page.
View your watchlist by navigating to the watchlist section from the navigation bar.
Remove items from your watchlist by clicking the "Remove from Watchlist" button.
Bidding on Listings
Enter your bid amount on the listing detail page and click "Place Bid."
Ensure your bid is higher than the current highest bid.
Creating Listings
Go to the "Create Listing" page from the navigation bar.
Fill in the details of your item and submit to post the listing.
