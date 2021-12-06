# 110-1 Database System Final Project

## Team members
- 108590050 李浩銘
- 108590004 謝宗麟
- 108590029 朱欣雨
- 108590049 符芷琪
- 108590056 鄭琳玲
- 108590061 黃聖耀
- 110AEM001 盧佩怡
- 110AEM002 譚永駿

### Note for Team Members
> PLEASE DO NOT ADD ';' TO PYTHON CODE AT THE END OF SENTENCE

Scrum developing procedure:
1. Take a task you are interested in from [Miro](https://miro.com/welcomeonboard/MkF1UFZBb2tJeHM4Nmxtc0lueTZ3b3lJZXQ0TWFWc1lOb25FemFacVB3WVJ3NVlrSWZqTFRuT0xvQ2d6OGYyTHwzMDc0NDU3MzYyMDA0NjQyMjM2?invite_link_id=149965833091)
2. Develop your part on your branch
3. Create a Pull Request(PR) after you finish developing your part
4. Your PR will be reviewed in the Sprint Review
5. Fix your PR if necessary
5. Your PR will be merged into master branch after reviewed
6. Pull and merge master branch into your branch
7. Fix conflict if necessary  
*Pay attention to the compatibility of each function during fixing conflict*

Sprint Review #1: 13 Oct (Wed) at 18:10 @Google Meet  
Sprint Review #2: 29 Oct (Fri) at 13:10 @TB6-327  
Sprint Review #3: 5 Nov (Fri) at 13:10 @TB6-327  
Sprint Review #4: 26 Nov (Fri) at 13:10 @TB6-327  
Sprint Review #5: 3 Dec (Fri) at 13:10 @TB6-327  
Sprint Review #6: 7 Dec (Tue) at 13:10 @TB6-327  
Sprint Review #7: 14 Dec (Tue) at 13:10 @TB6-327  

## Project Objective:
This project requires students to work on a database project in order to exercise the relational DBMS software, SQL, and database design techniques learned and to gain the project experiences. The major focus of the project will be Entity-Relationship modeling, relational database design, SQL, normalization, and Web-based database system development.

## Project Descriptions:
*Design an online e-commerce system, called e-Shop, that allows users to manage, search, and purchase products and query corresponding information. The functionality, information, and constraints which the system shall provide, contain, and satisfy are given as follows (but not limit to):*

### System functionality:
- Shall allow the system to authenticate and authorize the users
  - The system shall have 3 types of users: customers, staffs, and system administrator. Each type of users has different privileges as follows:
    - [ ] The customers can search and purchase products.
    - [ ] The staffs can manage the data of products, such as querying and updating products, processing product ordering.
    - [ ] The administrator can create and manage user accounts.
  - [x] The system shall allow users to login and logout system.
  - [x] The system shall authenticate users with loginid and password.
  - [x] The system should allow a user to register himself/herself as a customer. (optional)
- Shall allow customers to search products, order products, and view the history of his/her orders.
  - [ ] The system shall allow customers to search products.
  - [ ] The system shall have a shopping cart and allow customers to add/remove product items into/from the shopping cart when purchasing products online.
  - [ ] The system shall calculate the total purchase amount of each customer's order when the customer check out their shopping carts. The order transaction is completed when the customers confirm the payment of the purchase after checking out the shopping carts. **Note that the total amount is calculated by computing the subtotal of each purchased product item plus tax and shipping fee. The discounts shall be applied to the orders whenever they are applicable. Refer to discount policy for more details. However, the third-party verification of payment for the purchase is NOT considered in the system and is optional.**
  - [ ] The system shall allow customers to query the history of their orders.
  - [ ] The system should automatically email an order confirmation message to the customers who place an order. (optional)
- Shall allow staffs to manage products and process customer's order requests.
  - [ ] The system shall allow staffs to manage the products, including insert, update, query and delete products.
  - [ ] The system shall allow staffs to process and update the status of customer's orders.
- Shall allow staffs to define various discount policies for the products and/or the orders.
  - [ ] The system shall allow staffs to manage the discount policy, including insert, update, query and delete discount policies.
  - [ ] The system should support three types of discount policies, including shipping, seasonings, and special event discounts. **For each policy, it allows users to specify or define a discount rule. For creating a new discount policy, users requires to specify the type of the discount, description of the discount policy, discount period, and corresponding information, such as the product(s), discount rate, and the total amount of purchase. The system will assign a unique discount code to the policy. Note that the shipping and seasonings discounts are associated with an order while the special event discount is associated with product(s).**
    - [ ] For the shipping type of discount, the discount rule can be a free shipping if the purchase amount is greater than or equal to a certain amount, say $500.  
    - [ ] For the seasonings type of discount, a discount rate, say 0.05%, can be applied to the total amount of the purchase for a specified period (from yyyy:mm:dd to yyyy:mm:dd).
    - [ ] For the special event type of discount, a discount rate, say 0.05% or buy 1 get 1 free, can be applied to specified products for a given period (from yyyy:mm:dd to yyyy:mm:dd). **Note that you can have a unique discount code (representing different kind of discount) assigned to selected products for a given period and then let the shopping cart calculate the discounts for the selected products based on the discount code.**
- Shall allow staffs to generate the corresponding reports or statistics.
  - [ ] The system shall provide the statistic report about the product sales, such as the daily, weekly, monthly sales reports.
  - [ ] The system should provide the report about the best-selling product for each store. (optional)
  - [ ] The system should provide the purchase statistic reports for each product or each store for a given period. (optional)    
- Should allow the system to keep tracking the status of the orders. (optional)
  - [ ] The system shall (automatically) keep tracking the status of an order when the order is submitted (received), processed (processing), delivered (shipping) or completed (closed).
- Additional desired functionality.
  - [ ] Professional user interface. (web or apps)
  - [ ] Support rating and/or writing review comments for the stores. (optional)
  - [ ] Support the functionality of "Customers Who Bought This Product Also Bought". (optional)

### Information to be contained in the System:
- The system shall contain information about each valid users of the system: loginid, name, password, email, address. It is assumed that the information about all staffs and the system administrator are part of the initial state of the database (no interactions are needed to add or delete those users from the system).  The administrator can also be a staff in the system.
- The system shall contain information about each product: productid, name, description, and other attributes, such as product picture, price, the quantity of the product in stock.
- The system shall contain information about each store: storeid, name, address, contact email and phone.
- The system shall contain information about each order: orderid, time, customer, name and price of each purchased item, quantity of each purchased item, total amount of the purchase, current status of the order (received, processing, shipping, closed).
- The loginid, productid, storeid, orderid, and discount code are all unique.
- The sales report can include the date, the store name, the number of orders, the total amount of the sales.

### Business rules and system integrity constraints:
- Three types of discounts, including shipping, seasonings, and special event discounts, can be applied to the same purchase.
- A product cannot be associated with more than one special event type of discount for the same period.
- The periods of special event discount for a given product cannot overlap.
- The quantity of each purchased product must be an integer that is greater than zero.
- The quantity of purchasing for a product must be less than or equal to the current quantity of stock for that product.

### Note:
1. The project should mainly focus on the database design of the system.
2. The above requirements may be incomplete. You are encouraged to explore more detailed requirements about the system by interviewing instructor or surveying (Googling) other similar systems from the Internet.
