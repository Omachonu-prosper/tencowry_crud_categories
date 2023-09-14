# tencowry_crud_categories
Create CRUD endpoints to handle categories

## CRUD REST API endpoints
* `/` - `GET` - The index page

* C - create categories and sub categories
`/categories` - `POST` - create a new category
`/categories/<category_name>/sub` - `POST` - Create a new sub category for an existing category

* R - read/get categories and sub categories
`/categories`- `GET` - get all categories and their sub categories
`/categories/<category_name>` - `GET` - get a category and its sub categories

* D - delete categories and sub categories
`/categories/<category_name>` - `DELETE` - delete a category
`/categories/<category_name>/sub/` - `DELETE` - delete a sub category

## API Docs
Api docs for the api, its endpoints and payloads can be found [here](https://docs.google.com/document/d/1qKwQerWQ2OL6pUik_uGk0eAgER0v1V3DtqmWp7ST2DQ/edit?usp=sharing)