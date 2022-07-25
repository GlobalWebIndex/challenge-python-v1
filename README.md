# GlobalWebIndex Python Challenge - v1 | Exercise: DinosaursAficionado

Create a Python application for Dinosaurs Aficionados which is going to be used to maintain and provide various information about all kinds of Dinosaurs.

# TL;DR

How to use:

## Local development

Requires to have postgres and poetry installed.
- create a local database: dinopedia
- browse to the project folder and run:
  ```
  poetry shell
  poetry install
  ```
- browse to the folder dinopedia (where the manage.py resides), and migrate the model to the database
  ```
  ./manage.py makemigration && ./manage.py migrate && ./manage.py
  ```
- create superuser
  ```
  ./manage.py createsuperuser
  ```
  add name, mail and password
- run the server in port 8001 (so it does not conflict with the port run in docker) with: 
  ```
  ./manage.py runserver 8001
  ```
- the address 127.0.0.1:8001 should be running indicating the api endpoints
## Docker

- browse to the project path
- run
  ```
  docker-compose up --build -d
  ```
- the address 127.0.0.1:8000 should be running indicating the api endpoints


# Assignement

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

#### Basic Tools

Python 3.8 is used (not 3.10) and Poetry as package manager.

Django is used to create the model.

The model persists in a Postgres database.
- on the images:
  - the images are held in the file system in the folder dinopedia/images 
    - this folder is further structured to hold images for each dinosaur separately
    - TODO a folder media which would allow to keep our other types of files more tidy would be better
  - the database hold only the path to the image.

Docker with docker compose is used to containerize the app; some care is needed for 
- the creation of the volumes
- the creation of the superuser, and
- the migrations
- TODO: add a volume for the database

PgAdmin is used to check that everything in the database are as planned (both for the local development and for the docker)

#### Basic Packages

Pillow is used for the images we install the package

Black is used for formatting.

Pytest is used to verify the functionallity of the APIs. 

Model-bakery  is used to create the instances for the test.

TODO: add a population script

### Admin tasks

#### Model

The model can be found in the image /dinopedia/dinosaurs_models.png

The basic classes are the **Dinosaur**, the **DinoOwner** and the **PetDinosaur**.

The relations and the arguments are clearly depicted in the image.\

Here, we will just denote that there is a ManyToMany relationship between Dinosaur and DinoOwner to account for the liked_dinosaurs.

#### Admin Site

The model is implemented in the admin site. From there the admin can apply the necessary actions.

More specifically, the admin can create:
- the Periods, with start and end years BC, and a description 
  - we do not put a limit to the period names as (as scientists) we might need to add more and more with different age range

- the dinosaur Sizes, with min and max heights, lenghts, widths and weights
  - with the limitation of the following types: tiny, very small, small, medium, large, very large, gigantic

- the Eating Types classification with a description
  - with the limitation: herbivores, omnivores, and carnivores

- the Dinosaur with the above, plus:
  - a list of typical colours (up to four), 
  - a descriptionwhose,
  - and two images.

Additionally, the admin can create, edit, delete:
- the PetDinosaurs, and
- the DinoOwners.
### Roadmap / TODOs

There is one exception in the aove tasks: remove the image from the admin site.

TODO: Also, a good idea is to delete the images folder associated with a dinosaur upon the deletion of the specific dinosaur.

## Second Part

As a developer you’d like to Integrate with the application and have the ability to : 
* Find all the available kinds of dinosaurs
* Search for a particular kind and get their images
* Like your favourite (Optional)
* See your favourites (Optional)

### Technical approach

We use django rest framework (DRF) in conjuction django-filters to filter and order the Dinosaurs (and everything else).

Additionally, the drf-yasg package is implemented to create the API documentation (Swagger and Redoc) dynamically.

### Developers Task

The developer can use the API endpoints to fulfill the tasks.

For the tasks "like and see your favourite" a slightly playful approach is used:
The developer can create a DinoOwner who
- can sequentially own a pet dinosaur (only one) with distinctive features, and
- like any amount of dinosaur kinds.

### API Endpoints

The following main endpoints are provided:

api/
api/dinosaurs/<pk>/images1 [name='dinosaur-related']
admin/
^images/(?P<path>.*)$
^swagger(?P<format>\.json|\.yaml)$ [name='schema-json']
^swagger/$ [name='schema-swagger-ui']
^redoc/$ [name='schema-redoc']

(which needs cleaning)

#### Endpoint api/

This endpoint leads 

`get` api/dinosaurs:

The response provides a list of dinosaurs:
- details for the period, size and eating type. 
- the amount of likes and from which owner 
- the images for the dinosaur, the links of which provide the image when used


Below find and example of a response with one dinosaur:

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
            "likes_count_by": [
                2,
                [
                    [
                        2,
                        "Ash Ketchum"
                    ],
                    [
                        4,
                        "Ash Ketchum7"
                    ]
                ]
            ],
            "image1": "http://127.0.0.1:8000/images/images/Dino%20API/fausto-garcia-menendez-hYKG311mff8-unsplash.jpg",
            "image2": "http://127.0.0.1:8000/images/images/Dino%20API/jon-butterworth-_BJVJ4WcV1M-unsplash.jpg",
            "name": "Dino 2",
            "description": "A description to rule them all",
            "typical_colours": [
                "yellow",
                "orang",
                "blue"
            ],
            "period": {
                "id": 2,
                "name": "first period",
                "start_year": 2500,
                "end_year": 2499,
                "description": "it is the first period"
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
 



#### Filtering

More specifically, the user can filter the dinosaurs according to the following criteria:
- name
- period; name of the period, start year, and end_year
- size; type, height (min and max), weight(min and max)
- eating_type; 'C' for Carnivore, 'H' for Herbivore, 'O' for omnivore.
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


Through the API the user can also update the dinosaur details 
- _Note_: the update of the image which is still a work in progress.

#### POST PUT PATCH

Through the API the user can also update the dinosaur details 
- the update of the image which is still a work in progress.

### YASG - Yet Another Swagger Generator

The libary yasg facilitates the creation of the API Documenation dynamically
The user can browse to the endpoints:
- swagger
- redoc

and get a good idea on how to use the API.

### Testing

The Pytest suite is used and some basic tests have been deployed for the API functionallity
- get
- delete
- post
- patch
- catch the conflict in the insertion of same names

To create instances for the fictional database we use the package model-bakery.

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
