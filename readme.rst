LittleLemon API
=====================

Django-based simple API project for the Little Lemon restaurant. 
People with different roles is able to browse, add and edit menu items, 
place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 

User groups
-------------
* Managers
* Delivery members
* Customers (default)

Authentication endpoints 
-------------------------


=====================================================       ===================================== ================ =================================================
  Endpoint                                                      Role                              Method             Purpose 
=====================================================       ===================================== ================ =================================================
/auth/users/                                                      No role required                  POST             Creates a new user with name, email and password 
/auth/users/me/                                               Anyone with a valid user token        GET              Displays only the current user
/auth/token/login/                                            Anyone with a valid username and    POST             Generates access tokens that can be used in 
                                                              password                                             other API calls in this project
/auth/token/logout/                                         Verified users                        POST              Log out endpoint        
/auth/users/activation/                                       unverified users                       POST          Activate an account, with the uidb64 and token
                                                                                                                   provided in the request 
/auth/users/resend_activation/                              unverified users                        POST           Generate an activation link and sends it to the 
                                                                                                                   email address provided in the request 
/auth/users/reset_password/                                 Verified users                          POST           Sends a password recovery link to the email
                                                                                                                   provided in the request 
/auth/users/resest_password_confirm/                        Verified users                          POST           Reset the user password. Requires uidb64, token,
                                                                                                                   and the new_password 
=====================================================       ===================================== ================ =================================================

Menu-items endpoints 
------------------------------


=====================================================       ========================== ========================= =============================================================
  Endpoint                                                      Role                   Method                      Purpose 
=====================================================       ========================== ========================= =============================================================
/api/menu-items                                             Customer, delivery crew    GET                       Lists all menu items. Return a `200 – Ok HTTP` status code
/api/menu-items                                             Customer, delivery crew    POST, PUT, PATCH, DELETE  Denies access and returns 403 – Unauthorized HTTP status code
/api/menu-items/{menuItem}                                  Customer, delivery crew    GET                       Lists single menu item
/api/menu-items/{menuItem}                                  Customer, delivery crew    POST, PUT, PATCH, DELETE  Returns 403 - Unauthorized
/api/menu-items                                             Manager                    GET                       Lists all menu items
/api/menu-items                                             Manager                    POST                      Creates a new menu item and returns 201 - Created
/api/menu-items/{menuItem}                                  Manager                    GET                       Lists single menu item
/api/menu-items/{menuItem}                                  Manager                    PUT, PATCH                Updates single menu item
/api/menu-items/{menuItem}                                  Manager                    DELETE                    Deletes menu item
=====================================================       ========================== ========================= =============================================================

User group Management endpoints
--------------------------------
=====================================================       ========================== ========================= ============================================================================
  Endpoint                                                      Role                   Method                      Purpose 
=====================================================       ========================== ========================= ============================================================================
/api/groups/manager/users                                   Manager                    GET                       Return all managers 
/api/groups/manager/users                                   Manager                    POST                      Assigns the user in the payload to the manager group and returns 201-Created
/api/groups/manager/users/{userId}                          Manager                    DELETE                    Removes this particular user from the manager group and returns 200 – Success if everything is okay.
                                                                                                                 If the user is not found, returns 404 – Not found
/api/groups/delivery-crew/users                             Manager                    GET                       Returns all delivery crew
/api/groups/delivery-crew/users                             Manager                    POST                      Assigns the user in the payload to delivery crew group and returns 201-Created HTTP
/api/groups/delivery-crew/users/{userId}                    Manager                    DELETE                    Removes this user from the manager group and returns 200 – Success if everything is okay.
                                                                                                                 If the user is not found, returns  404 – Not found                                                                                                                 
=====================================================       ========================== ========================= ============================================================================

Cart management endpoints 
--------------------------------
=====================================================       ========================== ========================= ============================================================================
  Endpoint                                                      Role                   Method                      Purpose 
=====================================================       ========================== ========================= ============================================================================
/api/orders                                                 Customer                    GET                       Returns all orders with order items created by this user
/api/orders                                                 Customer                    POST                      Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user.
/api/orders/{orderId}                                       Customer                    GET                       Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.
/api/orders                                                 Manager                     GET                       Returns all orders with order items by all users
/api/orders/{orderId}                                       Customer                    PUT, PATCH                Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1. If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery. If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.
/api/orders/{orderId}                                       Manager                     DELETE                    Deletes this order
/api/orders                                                 Delivery crew               GET                       Returns all orders with order items assigned to the delivery crew
/api/orders/{orderId}                                       Delivery crew               PATCH                     A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.
=====================================================       ========================== ========================= ============================================================================

Features
--------

* Filtering, pagination and sorting capabilites for the /api/menu-items and /api/orders endpoints, powered by rest_framework pagination   
* Throttling ratio (all endpoints):

    * Authenticated users : 10 requests / minute 
    * Guest users: 5 requests / minute


Set up 
------------
First of all, clone the repository

.. code-block:: bash

    $ git clone https://github.com/francisco-oro/LittleLemonAPI.git
    $ cd LittleLemonAPI

Create a virtual environment to install dependencies in and activate it:

.. code-block:: bash

    $ python -m venv venv
    $ source venv/bin/activate

Then install the dependencies:

.. code-block:: bash

    (env)$ pipenv install -r requirements.txt

Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pipenv` has finished downloading the dependencies:

.. code-block:: bash

    (env)$ cd LittleLemon    
    (env)$ python manage.py runserver

Documentation about virtual environments is available at https://docs.python.org/3/library/venv.html

Accounts
------------
* Manager
    * username = jo
    * password = 1

* Delivery Crew
    * username = yassen
    * password = table2016

* Customer 1 
    * username = youssef 
    * password = table2016
* Customer 2
    * username = ayat 
    * password = table2016
    
License
-------

This project is licensed under the
`BSD 3-Clause license <https://choosealicense.com/licenses/bsd-3-clause/>`_.
