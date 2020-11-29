# Keep Track of Delicious Donuts
#### A donut tracking app using Flask and POSTGRESql.

This app has helped me practice my `jQuery`, `SQLalchemy` queries, and `CSS`.
I'm particularly happy with my search route that handles both integer and string searches.

I've also been having fun using jQuery and Javascript to practice the concept of having a frame of HTML preloaded that eventually gets replaced with information.

## To Run App
Db Setup for a psql database:
- Install psql
Enter
`createdb donuts`

In the app's main directory enter:
`python3 seed.py`

In the app's main directory enter:
`flask run`

In you browser go to:
`localhost:5000`

## To Run Tests
In the app's main directory enter:
`python -m unittest tests -v`

#### Future Functionality I Would Like to Add
- [ ] Restore donuts on all search
- [X] Fix error on no search term
- [ ] User login and auth for security and individual donut lists
- [X] Search for donuts using one term
- [ ] Sort donuts
- [ ] Add html skeleton frame lines/animations
- [ ] More skeleton/pre load to be replaced html
- [ ] Smooth out html jumps when donut list expands
- [ ] Complete all further studies
- [ ] Refactor to OO
- [X] Set timeouts for message reset
- [X] Visuals for messages
- [ ] More tests: for web page, for search route...