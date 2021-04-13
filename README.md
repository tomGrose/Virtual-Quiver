# Virtual Quiver
https://virtual-quiver.herokuapp.com/

### Overview
Virtual Quiver was designed with the purpose of helping users (more specifically, disc golfers) find new disc golf discs. 
It achieves this goal in multiple ways.
One of the unique things about this application is that it let's user's save discs to their "quiver" that they already own. They are then able to see recommendations for new discs based off of the discs in their quiver.
Users are also able to discover discs by utilizing the search feature with filters based on the different attributes disc golf discs have.

Personalized reccomendations and a robust search feature are just the start however. 

User's are also able to leave two different type's of reviews for discs so other user's know what to expect if they eventually want to pick one up.
The first type of review is open for anyone who has an account to leave. It's just a simple review for the user to leave their thoughts on the disc. 
The second type of review will only become available to a user who has had the disc in their quiver for longer than 4 months. As disc golf discs break in their flight characteristics tend to change.
By allowing users to leave these types of reviews other users can get a better understanding of how the disc might throw after they have bought it and used it for a couple of months.

### User Flow
When a user first signs up they will be greeted with a page that informs them they need to search for the discs they already own to add to their quiver.
They can accomplish this by searching for the discs in the search bar, or by finding them within the discover discs page.
Once a user has added discs to their quiver they will be able to see recommendations based on a certain disc, or see a random assortment of recommendations based on all the discs in their quiver.
If a user see's a disc they like they will then be able to add it to their wishlist to remember it for a time when they embark on the exciting adventure of buying new discs.

### API
One of the setbacks of this project was finding a large dataset of discs. Unfortunately there is no publicly available API for disc golf discs.
This required me to write my own API using Flask and Python. This API was then used to seed the disc table in the database.

### Technology Stack
- Flask/Python
- PostgreSQL
- SQLAlchemy
- Axios
- JavaScript
- BootStrap
