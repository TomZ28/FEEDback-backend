from users.models import FEEDbackUser
from restaurants.models import Restaurant, RestaurantFollower, RestaurantLike, Comment
from blogs.models import Blog, BlogLike
from images.models import RestaurantImage
from menuitems.models import MenuItem
from django.contrib.auth.hashers import make_password

import random
from django.core.files import File

# Source: https://nameberry.com/popular-names
first_names = ["Olivia", "Liam", "Emma", "Noah", "Amelia", "Oliver", "Ava", "Elijah", "Sophia", "Lucas", "Charlotte", "Levi", "Isabella", "Mason", "Mia", "Asher", "Luna", "James",
"Harper", "Ethan", "Gianna", "Mateo", "Evelyn", "Leo", "Aria", "Jack", "Ella", "Benjamin", "Ellie", "Aiden", "Mila", "Logan", "Layla", "Grayson", "Avery", "Jackson",
"Camila", "Henry", "Lily", "Wyatt", "Scarlett", "Sebastian", "Sofia", "Carter", "Nova", "Daniel", "Aurora", "William", "Chloe", "Alexander", "Riley", "Ezra",
"Nora", "Owen", "Hazel", "Michael", "Abigail", "Muhammad", "Rylee", "Julian", "Penelope", "Hudson", "Zoey", "Samuel", "Isla", "Jacob",
"Eleanor", "Lincoln"]

# Source: https://babynames.com/blogs/names/1000-most-popular-last-names-in-the-u-s/
last_names = [
"SMITH",
"JOHNSON",
"WILLIAMS",
"BROWN",
"JONES",
"GARCIA",
"MILLER",
"DAVIS",
"RODRIGUEZ",
"MARTINEZ",
"HERNANDEZ",
"LOPEZ",
"GONZALEZ",
"WILSON",
"ANDERSON",
"THOMAS",
"TAYLOR",
"MOORE",
"JACKSON",
"MARTIN",
"LEE",
"PEREZ",
"THOMPSON",
"WHITE",
"HARRIS",
"SANCHEZ",
"CLARK",
"RAMIREZ",
"LEWIS",
"ROBINSON",
"WALKER",
"YOUNG",
"ALLEN",
"KING",
"WRIGHT",
"SCOTT",
"TORRES",
"NGUYEN",
"HILL",
"FLORES",
"GREEN",
"ADAMS",
"NELSON",
"BAKER",
"HALL",
"RIVERA",
"CAMPBELL",
"MITCHELL",
"CARTER",
"ROBERTS"
]

# GTA area codes
area_codes = ["416", "647", "437"]

# Emails
emails = ["gmail", "hotmail", "outlook", "yahoo"]

# Restaurants 
restaurant_names = [
    "85C Bakery Cafe",
    "A&W Restaurants",
    "Arby's",
    "Auntie Anne's",
    "Big Boy Restaurants",
    "Blaze Pizza",
    "Boston Market",
    "Buffalo Wild Wings",
    "Burger King",
    "Carl's Jr.",
    "Chipotle Mexican Grill",
    "Church's Chicken",
    "Cicis",
    "Cinnabon",
    "Culver's",
    "Dairy Queen",
    "Domino's Pizza",
    "Dunkin' Donuts",
    "Five Guys",
    "Gatti's Pizza",
    "Godfather's Pizza",
    "Golden Chick",
    "Hardee's",
    "In-N-Out Burger",
    "Jack in the Box",
    "Jersey Mike's Subs",
    "Jet's Pizza",
    "Jollibee",
    "KFC",
    "Little Caesars",
    "Long John Silver's",
    "Louisiana Famous Fried Chicken",
    "Marco's Pizza",
    "McDonald's",
    "Miami Subs Grill",
    "MOD Pizza",
    "Orange Julius",
    "Panda Express",
    "Papa Gino's",
    "Papa John's Pizza",
    "Peter Piper Pizza",
    "The Pizza Company",
    "Pizza Hut",
    "Pizza Inn",
    "Pollo Campero",
    "Pollo Tropical",
    "Popeyes",
    "Quiznos",
    "Sonic Drive-In",
    "Starbucks"
]

restaurant_descriptions = [
    "We sell the best food!",
    "Try our new menu items!",
    "We have the best customer service in town!",
    "Serving our customers since 1984.",
    "The greatest dining experience in town",
    "Our food is the healthiest!",
    "A true culinary experience.",
    "The greasiest food you can find!",
    "Best restaurant ever!",
    "Visit us today!",
    "Fast service",
    "Better than the others",
    "Offering a comfortable atmosphere",
    "Quick service here!!",
    "Our food sells like hotcakes!",
    "An experience like no other",
    "We do delivery!",
    "We're hiring!",
    "Free delivery!",
    "New job openings!",
    "Big big discounts during happy hour!",
    "Our menu is like no other",
    "Try our new $5 meal!",
    "Try the new $4 combo!",
    "Please visit us!",
    "Grand opening!! Come visit us!",
    "Happiness guaranteed!"
]

good_comments = [
    "Great food for great prices!",
    "Fantastic restaurant, I love it here!",
    "Very good"
]

okay_comments = [
    "It's okay, could be better",
    "You get what you pay for, it's fine",
    "It's edible, at least"
]

bad_comments = [
    "Trash. Absolutely disgusting.",
    "DON'T EAT HERE",
    "Never going to come here again!"
]

# Addresses
address_first = ["Sky", "Wall", "Main", "Ocean", "Water", "Bay", "Middle", "Shell", "Rock", "Ice"]
address_type = ["Road", "Street", "Avenue", "Drive"]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

fnamelen = len(first_names)
lnamelen = len(last_names)
desclen = len(restaurant_descriptions)

users = []
restaurants = []
name_choices = []
rest_addrs = []
for i in range(50):
    fnamenum = random.randint(0, fnamelen-1)
    lnamenum = random.randint(0, lnamelen-1)
    while (fnamenum, lnamenum) in name_choices:
        fnamenum = random.randint(0, fnamelen-1)
        lnamenum = random.randint(0, lnamelen-1)
    first = first_names[fnamenum]
    last = last_names[lnamenum]
    phone = "{}{}".format(area_codes[random.randint(0, 2)], random.randint(100000, 999999))
    user = "{}{}{}".format(first, last, phone[0:2])
    email = "{}.{}{}@{}.com".format(first, last, phone[0:4], emails[random.randint(0, 3)])

    new_user = FEEDbackUser(username=user, first_name=first, last_name=last, phone_number=phone, email=email, password=make_password("password"))
    new_user.save()
    users.append(new_user)
    name_choices.append((fnamenum, lnamenum))

    restaddrnum = random.randint(1, 999)
    while restaddrnum in rest_addrs:
        restaddrnum = random.randint(1, 999)
    addr = "{} {} {}".format(restaddrnum, address_first[random.randint(0, 9)], address_type[random.randint(0, 3)])
    postal = "L{}{} {}{}{}".format(random.randint(1, 9), alphabet[random.randint(0, 25)], random.randint(1, 9), alphabet[random.randint(0, 25)], random.randint(1, 9))
    rest_phone = "{}{}".format(area_codes[random.randint(0, 2)], random.randint(100000, 999999))
    desc = restaurant_descriptions[random.randint(0, desclen-1)]

    new_rest = Restaurant(name=restaurant_names[i], address=addr, postal_code=postal, phone_number=rest_phone, description=desc, owner=new_user)
    new_rest.save()
    restaurants.append(new_rest)

lorem_ipsum = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam et nisi mauris. Curabitur eu ante sit amet nisi scelerisque accumsan. Duis at venenatis nisi, sed cursus dui. Mauris pharetra malesuada bibendum. In feugiat eu mauris sit amet venenatis. Curabitur lobortis tristique augue at feugiat. Morbi feugiat, sapien eu fringilla varius, lorem lacus semper eros, id bibendum felis magna in est. Suspendisse libero massa, sollicitudin ac sem sed, mollis mattis tellus. Vivamus accumsan convallis odio quis laoreet. Fusce urna risus, maximus id consequat consectetur, pretium tristique enim. Curabitur volutpat elit erat, at pretium arcu laoreet et. Vivamus in ligula risus. Aliquam malesuada tortor a condimentum gravida. Suspendisse potenti. Fusce viverra lorem euismod, iaculis purus eget, sollicitudin urna.",
    "Nullam id convallis augue, eget gravida urna. Nullam consequat vulputate ante accumsan lacinia. Etiam facilisis sem ac urna viverra laoreet. Ut auctor nunc ac nisi fermentum, ac porttitor dolor blandit. Mauris convallis nisl lorem, nec dictum nibh rutrum vitae. Nam sagittis sapien lorem, et efficitur nunc pharetra nec. Nullam enim dolor, luctus sed neque id, semper pharetra velit. Quisque at imperdiet ex. Quisque interdum ornare convallis. Etiam sed tempor dolor, vel blandit enim. Sed ac hendrerit mauris, vel lacinia ante. Cras id mi diam. Nam viverra libero at neque malesuada, eget vestibulum lectus facilisis. Duis sed euismod neque.",
    "Phasellus pellentesque nunc ut urna rhoncus molestie. Etiam a quam dui. Nulla facilisi. Proin scelerisque libero odio, vulputate vestibulum sapien laoreet non. Nullam quis hendrerit ante. Morbi suscipit auctor dolor non feugiat. Phasellus ut malesuada tortor. Mauris at turpis nisl. Vestibulum vitae velit feugiat erat blandit volutpat quis ut risus. Pellentesque dictum eros eget turpis lobortis, eu tincidunt mi tincidunt. Pellentesque hendrerit venenatis metus, in porta dui venenatis at. Curabitur in nunc eros. Mauris hendrerit ipsum non auctor aliquet. Nulla turpis mi, pellentesque vel purus in, vulputate ornare nunc.",
    "Mauris condimentum lacus nec ex facilisis venenatis non quis lacus. Duis fermentum feugiat ante. Aliquam erat volutpat. Aenean scelerisque lorem luctus sem ultrices, quis vehicula metus fringilla. Nulla convallis quis nunc eu viverra. Donec vitae commodo tellus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Praesent semper felis at nulla fringilla, at mollis dui dapibus. Etiam dapibus orci id quam suscipit, vitae malesuada arcu tincidunt. Sed accumsan lectus sapien, lacinia maximus tellus facilisis ut.",
    "Curabitur erat quam, vulputate a aliquam at, rutrum eu ex. Aliquam convallis ac ante a consequat. Donec iaculis tempus aliquet. Donec sollicitudin sit amet sapien nec viverra. Cras orci massa, blandit vitae porttitor quis, interdum eget neque. Cras feugiat metus elementum nisi suscipit, nec feugiat enim pellentesque. Integer interdum nisi diam, sed dignissim purus feugiat eu. Donec tellus lectus, vulputate et urna ac, blandit dictum sem. In malesuada sit amet nibh quis bibendum. Morbi eget egestas nisl, ac lobortis erat. Nulla malesuada porttitor vehicula. Sed rutrum facilisis eros, at ultricies metus suscipit quis. Nullam viverra sollicitudin urna, at viverra nulla. Mauris sit amet posuere nisl. Nulla eleifend mauris in ipsum semper, vel fringilla leo scelerisque."
]

# Blogs
blogs = []
for i in range(25):
    for i in range(12):
        new_blog = Blog(title=restaurant_descriptions[random.randint(0, desclen-1)], details=lorem_ipsum[random.randint(0, 4)], restaurant=restaurants[i])
        val = random.randint(0, 10)
        if val < 2:
            new_blog.image.save('sample.png', File(open('example/sample.png', 'rb')))
        new_blog.save()
        blogs.append(new_blog)

for i in range(25, 50):
    for i in range(2):
        new_blog = Blog(title=restaurant_descriptions[random.randint(0, desclen-1)], details=lorem_ipsum[random.randint(0, 4)], restaurant=restaurants[i])
        val = random.randint(0, 4)
        if val == 2:
            new_blog.image.save('sample.png', File(open('example/sample.png', 'rb')))
        new_blog.save()
        blogs.append(new_blog)

blogslen = len(blogs)

for user in users:
    blog_liked = []
    for i in range(random.randint(4, 7)):
        choicenum = random.randint(0, blogslen-1)
        while choicenum in blog_liked:
            choicenum = random.randint(0, blogslen-1)
        blog = blogs[choicenum]
        blog_like = BlogLike(liker=user, blog=blog)
        blog_like.save()
        blog.likes += 1
        blog.save()
        blog_liked.append(choicenum)

    rest_liked = []
    for i in range(random.randint(4, 7)):
        choicenum = random.randint(0, 49)
        while choicenum in rest_liked:
            choicenum = random.randint(0, 49)
        rest = restaurants[choicenum]
        rest_like = RestaurantLike(liker=user, restaurant=rest)
        rest_like.save()
        rest.likes += 1
        rest.save()
        rest_liked.append(choicenum)

    rest_followed = []
    for i in range(random.randint(4, 7)):
        choicenum = random.randint(0, 49)
        while choicenum in rest_liked:
            choicenum = random.randint(0, 49)
        rest = restaurants[choicenum]
        rest_follow = RestaurantFollower(follower=user, restaurant=rest)
        rest_follow.save()
        rest.follower_count += 1
        rest.save()
        rest_followed.append(choicenum)

    for i in range(random.randint(4, 7)):
        choicenum = random.randint(0, 49)
        rest = restaurants[choicenum]
        rating = rating=random.randint(1, 5)
        comment_choice = random.randint(0, 2)
        if rating >= 4:
            details = good_comments[comment_choice]
        elif rating == 1:
            details = bad_comments[comment_choice]
        else:
            details = okay_comments[comment_choice]
        comment = Comment(author=user, details=details, rating=rating, restaurant=rest)
        comment.save()
        rest.rating_count += 1
        rest.save()

# Sources:
# image1: By Mcg2132 - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=79877802
# image2: By Nick Webb - Flickr: Petrus Kitchen, CC BY 2.0, https://commons.wikimedia.org/w/index.php?curid=20011392
# image3: By MattiPaavola - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=4932572
# image4: By Mwr14 - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=36567276
# image5: By loustejskal.com - https://www.flickr.com/photos/63311602@N08/36832718622/, CC BY 2.0, https://commons.wikimedia.org/w/index.php?curid=86395242
# image6: By Michael Rys - https://www.flickr.com/photos/mrys/176993289/, CC BY-SA 2.0, https://commons.wikimedia.org/w/index.php?curid=6958533
# image7: By Fabio Alessandro Locati - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=8252117
# image8: By Unknown author - This image was released by the National Cancer Institute, an agency part of the National Institutes of Health, with the ID 2397 (image) (next)., Public Domain, https://commons.wikimedia.org/w/index.php?curid=10531946
images = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg']
for restaurant in restaurants:
    image_choices = []
    for i in range(random.randint(1, 5)):
        choicenum = random.randint(0, 7)
        while choicenum in image_choices:
            choicenum = random.randint(0, 7)
        new_image = RestaurantImage(restaurant=restaurant)
        new_image.image.save(images[choicenum], File(open('example/' + images[choicenum], 'rb')))
        image_choices.append(choicenum)

# Sources:
# Pizza: By Valerio Capello at English Wikipedia - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=372337
# Water: By W.J.Pilsak, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=194110
# Burger: By Len Rizzi (photographer, original image), reprocessed by Off-shell - File:NCI Visuals Food Hamburger.jpg, Public Domain, https://commons.wikimedia.org/w/index.php?curid=56736132
# Sushi: By FranHogan - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=92638006
# Orange Juice: By USDA photo by Scott Bauer. Image Number K7237-8. - http://www.ars.usda.gov/is/graphics/photos/k7237-8.htm, Public Domain, https://commons.wikimedia.org/w/index.php?curid=41503
# Rice: By Estwordenn - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=40887642
# Cheese: By Jon Sullivan - http://pdphoto.org/PictureDetail.php?mat=pdef&amp;pg=8553, Public Domain, https://commons.wikimedia.org/w/index.php?curid=834876
# Salmon: By Robpedia at English Wikipedia - Transferred from en.wikipedia to Commons by Kelly using CommonsHelper., Public Domain, https://commons.wikimedia.org/w/index.php?curid=34817315
# Ice Cream: By Nicolas Ettlin - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=90940831
# Hot Dog: By Czar, original photographed by Renee Comet - This image was released by the National Cancer Institute, an agency part of the National Institutes of Health, with the ID 2669 (image) (next)., Public Domain, https://commons.wikimedia.org/w/index.php?curid=26844059
# Tea: By Sgtblackpepper - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=85840732
# Chips: By Evan-Amos - Own work, Public Domain, https://commons.wikimedia.org/w/index.php?curid=11926930
# Fries: By StockSnap - pixabay.com/photos/french-fries-salt-food-brown-food-923687/, CC0, https://commons.wikimedia.org/w/index.php?curid=113264465
# Cake: By Scheinwerfermann - Own work, Public Domain, https://commons.wikimedia.org/w/index.php?curid=4179330
# Noodles: By The original uploader was Hykw-a4 at Japanese Wikipedia. - File:Nabeyakuramen.jpg, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=72564006
foods = [
    ("Pizza", "pizza.jpg", "A hot slice of pizza"),
    ("Water", "water.jpg", "A nice bottle of water"),
    ("Burger", "burger.jpg", "A delicious burger"),
    ("Sushi", "sushi.jpg", "Fresh sushi"),
    ("Orange Juice", "oj.jpg", "Freshly squeezed orange juice"),
    ("Rice", "rice.jpg", "Freshly cooked rice"),
    ("Cheese", "cheese.jpg", "Cheese."),
    ("Salmon", "salmon.jpg", "Fresh salmon"),
    ("Ice Cream", "icecream.jpg", "Sweet sweet ice cream"),
    ("Hot Dog", "hotdog.jpg", "Tasty hot dog"),
    ("Tea", "tea.jpg", "Hot tea"),
    ("Chips", "chips.jpg", "Crispy chips"),
    ("Fries", "fries.jpg", "Fried to perfection"),
    ("Cake", "cake.jpg", "It's cake!"),
    ("Noodles", "noodles.jpg", "Delicious noodles")
]

for restaurant in restaurants:
    menu_choices = []
    for i in range(random.randint(5, 8)):
        choicenum = random.randint(0, 14)
        while choicenum in image_choices:
            choicenum = random.randint(0, 14)
        food = foods[choicenum]
        price = round(random.uniform(0.49, 20), 2)
        new_item = MenuItem(name=food[0], price=price, description=food[2], restaurant=restaurant)
        new_item.image.save(food[1], File(open('example/' + food[1], 'rb')))
        menu_choices.append(choicenum)
