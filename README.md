# GlobalWebIndex Python Challenge - v1 | Exercise: DinosaursAficionado

Create a Python application for Dinosaurs Aficionados which is going to be used to maintain and provide various information about all kinds of Dinosaurs.

## Disclaimer

This Readme is going to be long; the idea is to keep as much information possible from the tasks and blend in my procedure. 
I should mention that, when long parts are included usually I use a wiki page (or some other means) and point to that resource instead of putting everything in a clunky doc. Sorry for the big read.

# TL;DR

How to use: first clone the project, then it depends if you develop local or in docker.

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
  add name, mail and password: use those as credentials to enter the admin site.
- run the server in port 8001 (so it does not conflict with the port run in docker) with: 
  ```
  ./manage.py runserver 8001
  ```
- the address 127.0.0.1:8001 should be running indicating the api endpoints

From there on everytime you want to run the app, just fire the database up and only do the last step (except if there migrations to be made).
## Docker

- browse to the project path
- run
  ```
  docker-compose up --build -d
  ```
- the address 127.0.0.1:8000 should be running indicating the api endpoints
- to enter the admin page, the credentials are admin:admin


# Assignement

## First Part - Admin Tasks

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

<details><summary>1. api/dinosaurs</summary>
<p>

### Technical Approach

#### Basic Tools

- Python 3.8 is used (not 3.10) and Poetry as package manager.
- Django is used to create the model.
- Postgres database to pesist the model.
  - more on the images:
    - the images are held in the file system in the folder dinopedia/media/images 
      - this folder is further structured to hold images for each dinosaur separately
    - the database hold only the path to the image.
- Docker with docker compose is used to containerize the app; some care is needed for 
  - the creation of the volumes,
  - the creation of the superuser, and
  - the migrations.

PgAdmin is used to check that everything in the database are as planned (both for the local development and for the docker)

#### Basic Packages

- Pillow is used for the images we install the package
- Black is used for formatting.
- Pytest is used to verify the functionallity of the APIs. 
- Model-bakery  is used to create the instances for the test.

### Admin tasks

#### Model

The model is shown in the image /dinopedia/dinosaurs_models.png
The basic classes are 
- the **Dinosaur**,
- the **DinoOwner**, and
- the **PetDinosaur**.

The relations and the arguments are clearly depicted in the image.
Here, we will just denote that there is a ManyToMany relationship between Dinosaur and DinoOwner to account for the likes on the dinosaurs (liked_dinosaurs).

_Note_: the folder with the dinosaur images is deleted after the specific dinosaur is deleted; we use _django signals_ for this operation.
#### Admin Site

The model is implemented in the admin site, to which the user can browse from the endpoint admin/.
From there the admin can apply the necessary actions.

More specifically, the admin can create:
- the Periods, with start and end years BC, and a description 
  - we do not put a limit to the period names as (as scientists) we might need to add more and more with different age range

- the dinosaur Sizes, with min and max heights, lenghts, widths and weights
  - with the limitation of the following types: tiny, very small, small, medium, large, very large, gigantic

- the Eating Types classification with a description
  - with the limitation: herbivores, omnivores, and carnivores

- the Dinosaur with the above, plus:
  - a list of typical colours (up to four), 
  - a description,
  - and two images.

Additionally, the admin can create and edit
- the PetDinosaurs, and
- the DinoOwners.

Finally, the admin can delete anything, with the following consequences:
- the deletion of period, size, eating type will not delete the dinosaur, but in this attributes will be set to none,
- upon deletion of a dinosaur, 
  - the pet dinosaur  of this kind will be deleted
  - so the pet owner of this pet dinosaur will no longe have a pet
  - all the likes to this dinosaur will be deleted
- upon deletion of a pet dinosaur
  - the dino owner will no longer have this pet dino
- the deletion of the dino owner has no other effects

### Roadmap / TODOs

There is one exception in the above tasks: remove the image from the admin site.

TODO: add a population script
TODO: add unit tests

</p>
</details>



## Second Part - Developer's Tasks

As a developer you’d like to Integrate with the application and have the ability to : 
* Find all the available kinds of dinosaurs
* Search for a particular kind and get their images
* Like your favourite (Optional)
* See your favourites (Optional)

<details><summary>1. api/dinosaurs</summary>
<p>

### Technical approach

We use django rest framework (DRF) in conjuction django-filters to create A REST API.

The drf-yasg package is implemented to create the API documentation (Swagger and Redoc) dynamically.


### Developer's Task

The developer can use the API to fulfill the first two tasks in a straiught forward fashion.

For the tasks "like and see your favourite" a slightly "playful" approach is used:
- The developer can create a PetDinosaur which belongs to a type of dinosaur and also has distictive characteristics on its own,
- The developer can create a DinoOwner who
  - can own a pet dinosaur (only one), and
  - like any amount of dinosaur kinds.

#### API Endpoints

When browsing to the parent url, the following endpoints are shown:

- api/
- api/dinosaurs/<pk>/images1 [name='dinosaur-related']
- admin/
- ^images/(?P<path>.*)$
- ^swagger(?P<format>\.json|\.yaml)$ [name='schema-json']
- ^swagger/$ [name='schema-swagger-ui']
- ^redoc/$ [name='schema-redoc']


* The endpoint api/ is what the developer uses, and is further described in the next sections.
* The endpoint api/dinosaurs/<pk>/images1 is used to treat the upload of the first image of the dinosaur via the API.
* The endpoint admin/ is directs to the admin site.

In the following sections the endpoint api/ is described in more detail.

##### TL;DR

In short:
`get` api/dinosaurs: to list the dinosaurs
`post` api/dinosaurs: to  add a dinosaur
`put` api/dinosaurs/<pk>: to  update a dinosaur
`delete` api/dinosaurs/<pk>: to delete a dinosaur
`get` api/petdinosaurs: to list the pet dinosaurs
`post` api/petdinosaurs: to add a pet dinosaur
`put` api/petdinosaurs/<pk>: to update a pet dinosaur
`delete` api/petdinosaurs/<pk>: to delete a pet dinosaur
`get` api/dinoowners: to list the dinosaur owners
`post` api/dinoowners: to add a d dinosaur owner
`put` api/dinoowners/<pk>: to update a dinosaur owner
`delete` api/dinoowners/<pk>: to delete a dinosaur owner

Using the `get` endpoint the user can also filter, order and search.

_Note_ that the following filters are supplied:
- for the literals arguments, e.g. name, 
  - =
  - __icontains=
  - __iexact=
  - __contains=
- for the numerical argumenrs, e.g. start_year or age:
  - =
  - lt
  - gt
  - gte
  - lte
  - in

##### API Documentation

AS mentioned, the libary yasg facilitates the creation of the API Documenation dynamically.
The user can browse to the endpoints:
- swagger/ , or
- redoc/
to get a good idea on how to use the API.

##### Endpoint api/

This endpoint leads to

1. api/dinosaurs
2. api/petdinosaurs
3. api/dinoowners

<details><summary>1. api/dinosaurs</summary>
<p>

###### List dinosaurs

`get` api/dinosaurs:

The response provides a list of dinosaurs, with the following for each one:
- details for the period, size and eating type,
- typical colours, (up to four) 
- the amount of likes and from which owner,
- the images for the dinosaur, the links of which provide the image when used

Example of a response (with one dinosaur):
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
 
Filter can take place according to the following criteria:
- name
- period; name of the period, start year, and end_year
- size; type, height (min and max), weight(min and max)
- eating_type; 'C' for Carnivore, 'H' for Herbivore, 'O' for omnivore.
- description
- TODO: with most likes

To filter add at the end of the endpoint
 ?<field>=<value>

Example:

`get` api/dinosaurs?period__start_year__gte=25000
returns the dinosaurs that live in a period which year starts at and before 25000.

Ordering can take place for the following attributes:
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

Example:

`get` api/dinosaurs?ordering=-period__start_year
returns the dinosaurs in the order of the high to low start year
dinosaurs in the perios that start at 25000, then at 24000 and so on.

Finally, the user can search for a dinosaur with a specific text in the _description_ using the search query word
Example:
`get` api/dinosaurs?seard=A description to rule them all


##### Create and update a dinosaur

The user can add a dinosaur
`post` api/dinosaurs

the period, size and an eating_type could be null or have an existing id

<details><summary>payload for post</summary>
</p>

```json
        {
            "name": "Dino POST",
            "description": "ad description",
            "typical_colours": [colours],
            "period": period_id,
            "size": size_id,
            "eating_type": eating_type_id,
        }
```

</p>
</details>

After the post the user could patch two images for the dinosaur (*work in progress*)

The user may also update a dinosaur provided that he/she know its id
`patch` api/dinosaurs/<pk>

for example for colours with a payload like the folowing



<details><summary>payload for patch</summary>
</p>

```json

{
  "typical_colours": ["white"],
}

```

</p>
</details>

- note: the update of the image which is still a work in progress.


_Note_: `put` can also be used ti update the dinosaur but `patch` is to be prefered in general.

</p>
</details>

##### Delete a dinosaur

Check if we can do that in case a petdinosaur relates to it 

`delete` api/dinosaurs/<pk>

<details><summary>2. api/petdinosaurs</summary>
<p>

##### List petdinosaurs

`get` api/petdinosaurs:

The response provides a list of pet dinosaurs with:
- theid specifics; pet name, age, height, weight, width, colour, diet, and description,
- details of their dinosaur type they are, so we can have a comparison of their specific appeareance comparing to their kind. 
- details of their owner. 

Filtering an take place according to the following criteria:
- pet_name
- dino_type__name
- dino_type__period__name
- dino_type__period__start_year
- dino_type__period__end_year
- dino_type__size__size
- age
- height
- weight
- diet
- pet_description

Example:

`get` api/petdinosaurs?dino_type __period__start_year__gte=25000
returns the pet dinosaurs whose species lived in a period which year starts at and before 25000.


Ordering can take place according for the following attributes:
- dino_type__name
- pet_name
- height
- weight
- age

Example:

`get` api/petdinosaurs?ordering=-height
returns the petdinosaurs in the order of the high to short pet dinosaur.

Finally, search for a specific text in the _description_ using the search query word.

Example:

`get` api/petdinosaurs?search=A description to rule them all

##### Create and update a pet dinosaur

The user can add a pet dinosaur
`post` api/petdinosaurs

all arguments must be provided.

<details><summary>payload for post</summary>
</p>

```json
  {
      "dino_type": dinosaur_id,
      "pet_name": "WaterMelon2",
      "age": 1,
      "height": 0.001,
      "length": 0.001,
      "width": 0.001,
      "weight": 0.001,
      "colour": "a colour",
      "diet": "water",
      "pet_description": "this is a dino who drinks only water",
  }
```

</p>
</details>


The user may also update a pet dinosaur provided that he/she know its id
`patch` api/petdinosaurs/<pk>

for example for colours with a payload like the folowing

<details><summary>payload for post</summary>
</p>

```json
  {
      "colour": "another colour",
  }
```

</p>
</details>


<details><summary>3. api/dinoowner</summary>
<p>

##### Delete a pet dinosaur

TODO check if this is possible in case an owner depend on ti

`delete` api/petdinosaurs/<pk>

##### List Dino Owners

`get` api/dinoowner:

The response provides a list of dinosaur owners:
- nickname
- their pet dinosaur
- the kind of dinosaurs they like

Filtering an take place according to the following criteria:
- nickname
- petDino__pet_name
- petDino__age
- petDino__height
- petDino__length
- petDino__colour
- petDino__diet
- petDino__dino_type__name
- petDino__dino_type__period__name
- number_liked_dinosaurs


Example:

`get` api/dinoowners?petDino__dino_type__period__name=first period
returns the pet dinosaurs whose species lived in a period with name "first period".


Ordering can take place according for the following attributes:
- nickname
- petDino__pet_name

Example:

`get` api/petdinosaurs?ordering=nickname
returns the owners with alphabetical order.


##### Create and update a dinosaur owner

The user can add a pet dinosaur
`post` api/dinoowners

only the nickname argument must be provided.
The owner can have only one dinosaur but he can like as many types of dinosaurs he/she wants.

<details><summary>payload for post</summary>
</p>

```json
{
  "nickname": "Cool Owner",
  "petDino": petDinosaur_id,
  "liked_dinosaurs": [dinosaur_id1, dinosaur_id2, ...]
}
```

</p>
</details>


The user may also update the characteristics of an owner with the id
`patch` api/dinoowners/<pk>

for example for nickname with a payload like the folowing

<details><summary>payload for post</summary>
</p>

```json
  {
      "nickname": "Awesome Owner",
  }
```

</p>
</details>


##### Delete an owner

`delete` api/dinoowners/<pk>



#### Unit Tests

Disclaimer: only the API has passed through unit tests; 
the model is tested in more practical fashion in the admin site.

The Pytest suite is used to create the following tests for the API functionallity:
- get
- delete
- post
- patch
- catch the conflict in the insertion of same names

To create instances for the fictional database we use the package model-bakery.

##### Roadmap - TODOS

- add tests for more conflicts,
- add tests for filtering and ordering.

</p>
</details>
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
