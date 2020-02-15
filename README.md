# fastapi_project
Small project build using fastapi with python

API docs is up on the server url with the prefix of docs.

Modules
========

User: email, name, password(hashed before saving), is_administrator and quota
(is_administrator and quota are only adjustable by administrators)

Item: Tied to user via owner_id field, has unique identifier field and title
