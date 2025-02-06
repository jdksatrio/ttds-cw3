# ttds-cw3

1. Run mongodb
docker run -d --name mongodb -p 27017:27017 mongo
NOTE: need to fortify this later

3. Upload the dataset into mongodb (load_json_to_mongo.py) - for dev purpose use lite_for_db.json (truncated version of the original dataset)

4. Run query_from_db.py
NOTE: search_tools.py still so bad
