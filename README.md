# tencowry_crud_categories
Create CRUD endpoints to handle categories

## CRUD REST API endpoints
* C - create categories and sub categories
`/categories` - `POST` - create a new category
`/categories/<category_id>/sub` - `POST` - Create a new sub category for an existing category

* R - read/get categories and sub categories
`/categories`- `GET` - get all categories and their sub categories
`/categories/<category_id>` - `GET` - get a category and its sub categories

* U - update categories and sub categories
`/categories/<category_id>` - `PUT` - update a category
`/categories/<category_id>/sub/<subcategory_id>` - `PUT` - update a sub category

* D - delete categories and sub categories
`/categories/<category_id>` - `DELETE` - delete a category
`/categories/<category_id>/sub/<subcategory_id>` - `DELETE` - delete a sub category