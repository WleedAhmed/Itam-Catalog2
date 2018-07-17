from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Movie, User

engine = create_engine('sqlite:///movies.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
User1 = User(name="Waleed Mabrouk", email="Waleed@filmography.com",
             picture='https://fgmxi4ac'
                     'xur9qbg31y9s3a15-wpengine.netdna-ssl.'
                     'com/wp-content/uploads/sites/2/201'
                     '8/06/Ari-Aster-400x400.jpg')
session.add(User1)
session.commit()

# Action category
cat1 = Category(user_id=1, name="Action")

session.add(cat1)
session.commit()

movie1 = Movie(user_id=1, name="The Equalizer",
               description="A man believes he has put his "
               "mysterious past behind him and has dedicated himself"
               " to beginning a new, quiet life. But when he meets a"
               " young girl under the control of ultra-violent Russian"
               " gangsters, he can't stand idly by - he has to help her.",
               category=cat1)

session.add(movie1)
session.commit()


movie2 = Movie(user_id=1, name="Mad Max: Fury Road",
               description="In a post-apocalyptic wasteland, a woman "
               "rebels against a tyrannical ruler in search for her"
               " homeland with the aid of a group of female prisoners"
               ", a psychotic worshiper, and a drifter named Max.",
               category=cat1)

session.add(movie2)
session.commit()

movie3 = Movie(user_id=1, name="Logan", description="In the near futur"
               "e, a weary Logan cares for an ailing Professor X, s"
               "omewhere on the Mexican border. However, Logan's a"
               "ttempts to hide from the world, and his legacy, are"
               " upended when a young mutant arrives, pursued by"
               " dark forces.",
               category=cat1)

session.add(movie3)
session.commit()

movie4 = Movie(user_id=1, name="The Avengers", description="Earth's mi"
               "ghtiest heroes must come together and learn to figh"
               "t as a team if they are going to stop the mischievous"
               " Loki and his alien army from enslaving humanity.",
               category=cat1)

session.add(movie4)
session.commit()


# Adventure category
cat2 = Category(user_id=1, name="Adventure")

session.add(cat2)
session.commit()


movie1 = Movie(user_id=1, name="Avatar", description="A paraplegi"
               "c marine dispatched to the moon Pandora on a unique "
               "mission becomes torn between following his orders a"
               "nd protecting the world he feels is his home.",
               category=cat2)

session.add(movie1)
session.commit()

movie2 = Movie(user_id=1, name="The Lord of the Rings: The Return "
               "of the King", description="Gandalf"
               " and Aragorn lead the World of Men against "
               "Sauron's army to draw his gaze from Frodo and"
               " Sam as they approach Mount Doom with the One Ring.",
               category=cat2)

session.add(movie2)
session.commit()

movie3 = Movie(user_id=1, name="Interstellar", description="A tea"
               "m of explorers travel through a wormhole in sp"
               "ace in an attempt to ensure humanity's survival.",
               category=cat2)

session.add(movie3)
session.commit()

movie4 = Movie(user_id=1, name="Casino Royale", description="Arme"
               "d with a license to kill, Secret Agent James Bond"
               " sets out on his first mission as 007, and must de"
               "feat a private banker to terrorists in a high sta"
               "kes game of poker at Casino Royale, Montenegro"
               ", but things are not what they seem.",
               category=cat2)

session.add(movie4)
session.commit()


# Animation category
cat3 = Category(user_id=1, name="Animation")

session.add(cat3)
session.commit()


movie1 = Movie(user_id=1, name="Zootopia", description="In "
               "a city of anthropomorphic animals, a rookie bunny cop "
               "and a cynical con artist fox must work together to un"
               "cover a conspiracy.",
               category=cat3)

session.add(movie1)
session.commit()

movie2 = Movie(user_id=1, name="Inside Out", description="After young "
               "Riley is uprooted from her Midwest life and moved to S"
               "an Francisco, her emotions - Joy, Fear, Anger, Disgust "
               "and Sadness - conflict on how best to navigate"
               " a new city, house, and school.",
               category=cat3)

session.add(movie2)
session.commit()

movie3 = Movie(user_id=1, name="Toy Story 3", description="The toys are "
               "mistakenly delivered to a day-care center instead of th"
               "e attic right before Andy leaves for college, and it's u"
               "p to Woody to convince the other toys that they "
               "weren't abandoned and to return home.",
               category=cat3)

session.add(movie3)
session.commit()

movie4 = Movie(user_id=1, name="Up", description="Seventy-eight year o"
               "ld Carl Fredricksen travels to Paradise Falls"
               " in his home equipped with balloons, inadvertently"
               " taking a young stowaway.",
               category=cat3)

session.add(movie4)
session.commit()


# Comedy category
cat4 = Category(user_id=1, name="Comedy")

session.add(cat4)
session.commit()


movie1 = Movie(user_id=1, name="The Other Guys", description="Two mismat"
               "ched New York City detectives seize an opportunity to st"
               "ep up like the city's top cops, whom they idolize, o"
               "nly things don't quite go as planned.",
               category=cat4)

session.add(movie1)
session.commit()

movie2 = Movie(user_id=1, name="Due Date", description="High-strun"
               "g father-to-be Peter Highman is forced to hitch a ride"
               " with aspiring actor Ethan Tremblay on a ro"
               "ad trip in order to make it to his child's birth on time.",
               category=cat4)

session.add(movie2)
session.commit()

movie3 = Movie(user_id=1, name="Mr. Bean's Holiday", description="Mr. B"
               "ean wins a trip to Cannes where he unwittingly separat"
               "es a young boy from his father and must help t"
               "he two come back together. On the way he discovers Fran"
               "ce, bicycling, and true love, among other things.",
               category=cat4)

session.add(movie3)
session.commit()

movie4 = Movie(user_id=1, name="Just Go with It", description="On a we"
               "ekend trip to Hawaii, a plastic surgeon convinces his"
               " loyal assistant to pose as his soon-to-be-divorced "
               "wife in order to cover up a careless lie he told"
               " to his much-younger girlfriend.",
               category=cat4)

session.add(movie4)
session.commit()
