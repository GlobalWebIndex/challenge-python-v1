# Dinosaur and Image Services API Documentation


## How to run the application


at Dinopedia directory level docker-compose up --build


## Services URLs
- **Dinosaur Service:** [http://localhost:8001](http://localhost:8001)
- **Image Service:** [http://localhost:8002](http://localhost:8002)
- **User Service:** [http://localhost:8003](http://localhost:8003)

## Predefined Tokens for Access
- `token=123`  // dev access
- `token=456`  // admin access

## Dinosaur Service

### Create Dinosaur
```sh
curl -X POST "http://localhost:8001/dinosaurs?token=456" \
-H "Content-Type: application/json" \
-d '{
  "name": "Tyrannosaurus Rex",
  "eating_classification": "carnivores",
  "typical_color": "green",
  "period": "cretaceous",
  "average_size": "large",
  "images": []
}'

### Get All Dinosaurs
curl -X GET "http://localhost:8001/dinosaurs?token=123"

### Get All Dinosaurs with filter search
curl -X GET "http://localhost:8001/dinosaurs?name=Tyrannosaurus&include_images=true&token=123"

### Delete a Dinosaur
curl -X DELETE "http://localhost:8001/dinosaurs/1?token=456"

## Image service
### upload an image
curl -X POST "http://localhost:8002/images?dinosaur_id=1&token=456" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@yourfile.jpg"

### Delete image by id 
curl -X DELETE "http://localhost:8002/images/1?token=456" -H "accept: application/json"

### Delete all images for dinosaur
curl -X DELETE "http://localhost:8002/images?dinosaur_id=1&token=456" -H "accept: application/json"



### could improve further:
better caching with a redis service
complete token authorization for users
docker-compose for dev, staging environments etc
package structure for app .py files


