# DinosaursAficionado


Due to time reasons the following are not fully implemented:
- Favorites functionality is not fully implemented. You can only add and view favorites, you can't remove though.
- When uploading images there should be a max file size limit(e.g 5MB) and after image is uploaded it could be processed to reduce size.


## Features
- You can add dinosaurs either from http://127.0.0.1:8000/admin or if you add a user with permissions ("can_edit", "User can create/edit/delete dinosaurs") then this user has the option to add dinosaurs.
- As a regular user, you can view all dinosaurs, search by name, add to favorites and view them.


## Docker
```sh
cd challenge-python-v1
docker-compose up --build
```

Then navigate to http://127.0.0.1:8000

## Data
Some data are included in 'data.sql' file. 
Can be loaded with 
```sh
cat data.sql | docker exec -i dinopediaproject_db_1 psql -U postgres
```

Three users exists if 'data.sql' is imported.
- Super user: alex Password: pass
- Admin user: admin Password: strong-pass
- Developer user: developer Password: strong-pass
