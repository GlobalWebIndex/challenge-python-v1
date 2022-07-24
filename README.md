# GlobalWebIndex Python Challenge - v1 | Exercise: DinosaursAficionado

Create a Python application for Dinosaurs Aficionados which is going to be used to maintain and provide various information about all kinds of Dinosaurs.

## First Part

As an application administrator you’d like to have the ability to :
* Add a kind of dinosaur 
  * Name
  * Eating classification e.g [herbivores, omnivores, and carnivores]
  * Typical Colour
  * Period they lived e.g [triassic , jurassic, cretaceous, paleogene, neogene]
  * Average Size e.g [tiny, very small, small, medium, large, very large etc]).
* Remove a kind(s) of dinosaur(s)
* Associate up to 2 images with each dinosaur
* Remove image(s) 

### Technical Approach

Python 3.8 is used (not 3.10) and Poetry as package manager.

Django is used to create the model.

The model persists in Postgres database.

Docker with docker compose is used to containerize the app; some care is needed for 
- the creation of the volumes
- the creation of the superuser, and
- the migrations
- TODO: add a volume for the database

Run with 
```
docker-compose up --build -d
```

For the images we install the package Pillow.

Black is used for formatting.

In this section we do not use the Pytest suite yet.

PgAdmin is used to check that everything in the database are as planned (both for the local development and for the docker)

### Admin tasks

The model is implemented in the admin site. From there the admin can apply the necessary actions.

More specifically, the admin can create:
- the Periods, with start and end years BC, and a description 
- the dinosaur Sizes, with min and max heights, lenghts, widths and weights
  - with the limitation of the following types: tiny, very small, small, medium, large, very large, gigantic
- the Eating classification with a description
  - with the limitation: herbivores, omnivores, and carnivores
- the dinosaur with the above, plus a list of typical colours up to four, a description
  - he/she can also associate two images whose path are saved in the database, but the images are saved in the system
    - the images are saved in the path dinopedia/images in a separate folder for each dinosaur.

The admin can edit or remove any of the above in the admin site.

#### TODO

There is one exception : remove the image from the admin site.

### Roadmap

Delete the images folder associated with a dinosaur upon the deletion of the specific dinosaur

If we want to be a bit more playful, we can create Dinosaur Owners and implement a spefic dinosaur for each owner.

## Second Part

As a developer you’d like to Integrate with the application and have the ability to : 
* Find all the available kinds of dinosaurs
* Search for a particular kind and get their images
* Like your favourite (Optional)
* See your favourites (Optional)

### Technical approach

We use django rest framework (DRF) in conjuction django-filters to filter and order the Dinosaurs.

Additionally, the drf-yasg package is included to create API documentation (Swagget and Redoc) dynamically

### Developers Task

The developer can find all dinosaur by using the API endpoint
api/dinosaurs

The response proviades all the available data for the dinosaur, as well as for details for the period, size and eating type. Below find and example of a response with one dinosaur

<details><summary>api/dinosaurs response</summary>
<p>

```json

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "image1": "http://127.0.0.1:8001/images/images/Dino%20API/fausto-garcia-menendez-hYKG311mff8-unsplash.jpg",
            "image2": "http://127.0.0.1:8001/images/images/Dino%20API/jon-butterworth-_BJVJ4WcV1M-unsplash.jpg",
            "name": "Dino API",
            "description": "A dinosaur to the the API",
            "typical_colours": [
                "yellow",
                "orange"
            ],
            "period": {
                "id": 3,
                "name": "api period",
                "start_year": 1000,
                "end_year": 900,
                "description": "to test with API"
            },
            "size": {
                "id": 4,
                "size": "VL",
                "height_min": 40.0,
                "height_max": 50.0,
                "length_min": 7.0,
                "length_max": 10.0,
                "width_min": 3.0,
                "width_max": 4.0,
                "weight_min": 120.0,
                "weight_max": 320.0
            },
            "eating_type": {
                "id": 3,
                "eating_type": "C",
                "description": "MEAAAAAT"
            }
        }
    ]
}
```

</p>
</details>

Finally, the developer can click on the url for the image to see it. 

(_Detail_ / _TODO_: a better practice would be to hold the folder images a folder media which would allow to keep our other types of files more tidy.)

#### Filtering
More specifically he can filter them according to the following criteria:
- name
- period; name of the period, start year, and end_year
- size; type, height (min and max), weight(min and max)
- eating_type; C for Carnivore, H for Herbivore, O for omnivore
- description

To filter add at the end of the endpoint
 ?<field>=<value>

TODO: give examples


#### Ordering

The developer can also order the dinosaurs by:
- name
- size
- size__height_min
- size__height_max
- size__weight_min
- size__weight_max
- period__start_year
- period__end_year

To order add at the end of the endpoint ?ordering=<field>
By default the ordering is ascending; with ?ordering=<-field> the order is descending.

### YASG - Yet Another Swagger Generator

The libary yasg facilitates the creation of the API Documenation dynamically
The user can browse to the endpoints:
- swagger
- redoc

and get a good idea on how to use the API.

## Technical requirements for the exercise

We would like you to try and present a well written solution that will cover the above criteria. Utilising the following points
* Python 3.*
* Django (_Current repo uses a django template. Feel free to restructure if your solution is based on anything else like flask/fast api etc_)
* Database integration (Postgres or any equivalent)
* Docker
* Testing suite
* README

## More points for 

Get creative as much as you want, we WILL appreciate it. You will not be evaluated based on how well you follow these instructions, but based on how sensible your solution will be. In case you are not able to implement something you would normally implement for time reasons, make it clear with a comment.

# Submission

Just fork and share with us your work <cbekos@gwi.com> / <tvesela@gwi.com> / <zmaxa@gwi.com> / <tcechal@gwi.com>
