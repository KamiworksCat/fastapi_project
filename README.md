# fastapi_project
Small project build using fastapi with python

API docs is up on http://68.183.177.41:8000/docs

Modules
========

User: email, name, password(hashed before saving), is_administrator and quota
(is_administrator and quota are only adjustable by administrators)

Item: Tied to user via owner_id field, has unique identifier field and title
