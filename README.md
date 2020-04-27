
# Music Assistant

Music Assistant is an app to search lyrics and save your favorite songs.

### 1. List of Features 
  (Must)
  - [X] User sends a section of some lyrics
  - [X] User receives the song related to that lyrics
  - [X] Result song should have the name and artist
  - [X] User saves can tag a result song as favorite
  - [X] User sees his list of favorite songs
  - [X] (keep session per user)
  - [X] (save all conversations info)
  - [X] Stats show number of people that used the app
  - [ ] Stats show number of chats per day
  - [X] Stats show most popular song      | (search all, which gets searchd more frequently)
  
  (Should) 
  - [ ] Remove  songs from Favorite list
  - [ ] Stats show avg session time       | (till last interaction)

  (Nice)
  - [ ] ..

### 2. Flujo Mensajes:
  - facebook -> /webhook -> View -> fb_webhook -> message_handlers -> (fb_messages <-> MusixMatch ) -> facebook
  - **fb_webhook**: handles inicial connection processing request data
  - **message_handlers**: determine type of Input Message and call a type of response
  - **fb_messages**: build bot response, send musixMatch Api requests and send message back to fb

### 3. Progress TO-DO:
  - [X] handle differences (postback/message)              | message_handlers
  - [X] connect and search some lyrics with musixMatch     | MUSICX-service
  - [X] create models for users and messages
  - [X] create models for songs (attrib: favorites) MODELS
  - [X] add to favorites postback                          | Interaction+process
  - [X] session per user (separate) (use-id)
  - [ ] conversations model (store info stats)             | MODELS
        -  (date+lyrics searched + song + favorited?)
  - [X] show stats on persistent menu


### 4. Tests
  - ./manage.py test bot.tests
  - ./manage.py test bot.tests.test_fb_webhook_helper
  - ./manage.py test bot.tests.test_message_handlers_helper
  - ./manage.py test bot.tests.test_fb_messages_helper

  - ./manage.py test songs.tests