# Project: Sartel.io

## Introduction

We're looking to create a web application game, which allows two players to join a lobby and play a game we called Sartel.io

Sartel.io is a game that goes as follows:
1. Players are given a table list of categories (i.e., Surnames, Companies, Countries, Cities, Animals, Plants, Items, etc..)
1. A random letter is choosen
2. Two players will begin at the same time, where they will have to list out a word that starts with the randomly generated numbr which
corresponds for each category.
3. For example: If "A" is selected then the user would do Surname: Andrew, Companies: Apple, Countries: Austrailia
4. Both players have a shared minute timer
5. Players cannot see what their opponent wrote until the timer runs out
6. Players must self judge their individual work and keep a tally of how many valid words they came up with

## Expected features and fuctionality
Now that we know the rules I will break down the features we're looking to implement
1. Lobby creation: Users should be able to create a lobby where another player can join (using a random 5 character password generated
at point lobby is created)
2. Real-time updates: Both players will share same counttime timer and be able to see answers in between rounds
3. Temporary server usage: Lobby are ephermal but we do want to keep analytics on how many lobbies are created/how many players play/how many words created

The look should be a table spanning across, as users write words in each cell when they hit enter they enter the nect column cell.

## Tech Stack & Procedures
Tech Stack:
- Python with FastAPI (a must)
- Storage (we could use Redis or a memory DB since we are persisting anything long term)
- Railway for hosting (a must)
- React with Vite and Shadcn (modern UI)

Claude Note: Please feel free to opine on tech Stack

#### Procdures
- We're looking for a lean application, do not install packages unless fully needed.
- As well keep unit tests intentional and not verbose
- We're looking for deployments each time we push to master (railway)
