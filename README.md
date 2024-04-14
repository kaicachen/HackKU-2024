# HackKU-2024

## Inspiration
We believe that Mental Health is equally important as Physical Health, so we wanted to create something that would aide in the journey to bettering ourselves emotionally.

## What it does
Once logging in you can record your current mood, view your mood from previous days, and see a generated chart of your mood over the past month. If you haven't logged in before, you can create an account for free. We also provide a list of resources that we encourage you to go check out!

## How we built it
We used HTML/JavaScript/CSS for the Front-End, and Flask for the back-end. To store user data, we used MySQL

## Challenges we ran into
One of the main challenges we encountered was visualizing the data held in MySQL into charts for the user to see.

## Accomplishments that we're proud of
We're very proud of how we handled user interactions with out website. We had never used a framework before, so it was fun to implement it for the first time.

## What we learned
Our primary focus was learning Flask. We learned how to load pages, store session data, log in and log out, redirect to different pages, and much much more.

## What's next for Mind Mapper
We would love to add online capabilities, so people from all over the world could catalogue their journey.

## Features:
- Mood check in with optional notes
- Data visualization using Numpy
- Mental health resources: links to mental health websites
- Long form notes to record thoughts

## Database Tables:
- Users(username, password, firstname, lastname, location)
- Logs(username, date, score, note)
