# pawsitive_training
An online shop and lesson hub for pet training. 

Source code can be found [here](https://github.com/pac-dan/pawsitive_training)

The live project can be viewed [here](https://pawsitive-training-37efa34a3204.herokuapp.com/)

## Purpose of Project 
The aim of the project is to help pet owners train their pets while providing a one-stop shop for pet training products. The website combines an online store—with carefully selected pet care products—and a subscription service that grants access to exclusive training video lessons.

ADD RESPONSIVE SCREENSHOT HERE

---

## Links to content

[**Purpose of Project**](#purpose-of-project)

[**ECommerce Business Model**](#ecommerce-business-model)

[**Web Marketing**](#web-marketing)

[**Features**](#Features)

[**User Experience**](#User-Experience)
- [Design](#design)
    - [Fonts](#fonts)
    - [Colour](#colour)
    - [Wireframes](#wireframes)

[**Development Process**](#Development-Process)
- [Project Planning](#project-planning-and-documentation-in-github)
- [Search Engine Optimization](#search-engine-optimization)
- [Data Model](#data-model)

[**Testing**](#Testing)
- [Manual Testing](#manual-testing)
    - [Feature Testing](#feature-testing)
    - [Responsiveness](#responsiveness)
    - [Lighthouse](#lighthouse)
    - [Code Validation](#code-validation)
        - [Python](#python-code)
        - [JavaScript](#javascript-code)
        - [HTML](#html-validation)
        - [CSS](#css-validation)
    - [User Stories](#user-stories)
- [Automated Testing](#automated-testing)
    - [Django testing](#testing-django-views-models-and-forms)

[**Bugs**](#Bugs)

[**Libraries and Programs Used**](#libraries-and-programs-used)

[**Deployment**](#Deployment)
- [Deploying the app on Heroku](#deploying-the-app-on-heroku)
- [Making a local clone](#making-a-local-clone)
- [Running the app in your local environment](#running-the-app-in-your-local-environment)

[**Credits**](#Credits)

[**Acknowledgements**](#acknowledgements)

---

## ECommerce Business Model
This project follows a B2C model aimed at selling pet training products directly to consumers.
The site offers both tangible products—such as training aids, accessories, and nutritional supplements—and a digital service in the form of subscription-based video lessons.
The online store is designed to streamline the purchase process by minimizing friction and allowing users to quickly add items to their basket and check out.



## Web Marketing

---

## Features
The following pages are visible to all users, logged in or not.

<details>
<summary>Welcome Page (Landing Page)</summary>

- The landing page offers two primary actions:
    - Shop for pet training products
    - Subscribe to pet training lessons
- The page, like all others, features a header with the following elements (from left to right):
    - A clickable site icon that returns users to the homepage.
    - A search bar and button allowing users to search products by keyword.
    - A display showing the logged-in user's name (empty if the user is anonymous).
    - A staff dropdown menu (visible only to staff) with options to:
        - Add a Product
        - View the Product List
        - View the Order List
    - An account dropdown menu for users not logged in, offering:
        - Register
        - Login
    - A basket link that takes the user directly to the View Basket page.
- The page footer, common to all pages, features a call-to-action encouraging users to "Stay in Touch!", a link to the site's Facebook promotional page, and an invitation to subscribe to the mailing list (integrated with MailChimp).

![Welcome Page]()

</details>

<details>
<summary>Product Display Page</summary>

- This page displays pet training products in a tiled layout, which can be filtered by one of the category filters at the top or by a keyword search from the navbar.
- If there are any current special offers, they are showcased in a rotating banner (using a Bootstrap Carousel).
- Each product tile is clickable and links to its respective Product Detail Page.

![Product Display]()

</details>

<details>
<summary>Product Detail Page</summary>

![Product Detail]()

- This page provides detailed information about a product:
    - A clear image of the product.
    - The full name and description of the product.
    - Pricing details, the product category, and current stock levels.
    - A range-bound quantity input.
    - A primary “Add To Basket” button, which adds the specified quantity to the user's basket.
    - Additional buttons below the main content that link to:
        - Return to the shop
        - Edit the product (visible only to staff)
        - View the basket

</details>

<details>
<summary>Basket Page</summary>

- The Basket page lists all items added to the basket.
- Users can adjust the quantity of each product (using a range-bound input) or remove items entirely (using a trash icon button).
- The page includes buttons to return to the All Products page or to clear the entire basket.
- A summary table displays the subtotal, any delivery charges, and the grand total.
- A large blue checkout button directs the user to the Checkout Page.

![Basket]()

</details>

<details>
<summary>Checkout Page</summary>

![Checkout]()

- The Checkout page is divided into three main sections:
    - A form for entering the user's delivery details, which includes a checkbox to save data for future purchases.
    - A Stripe Payment element for secure payment entry.
    - A concise summary of the basket contents, including product names, quantities, and total costs, along with delivery and grand totals.
- Two buttons allow the user to either:
    - Return to the View Basket page.
    - Cancel the purchase (redirecting back to the Product Display page).

</details>

<details>
<summary>Checkout Success Page</summary>

![Checkout Success]()

- The Checkout Success page displays a “Payment Successful” message.
- It summarizes the order and delivery details.
- A call-to-action invites users to browse the training video lessons section of the site.

</details>

<details>
<summary>Video Lessons Page</summary>

![Video Lessons]()

- This page features a left-hand panel that displays a motivational message (“Practice Makes Perfect”) for subscribed users or a Subscribe link for non-subscribers.
- The main section lists the available training video lessons, organized by course.
- The first two lessons in each course are available for free, while additional lessons require a subscription (indicated by a padlock icon on non-accessible lessons).

</details>

<details>
<summary>Video Player Page</summary>

![Video Player]()

- The Video Player page is centered around the video element that plays the training lesson.
- Navigation buttons for “Previous,” “Next,” and “All Lessons” allow sequential or direct access to lessons.
- Thumbnails for the remaining lessons are displayed for quick navigation.

</details>

<details>
<summary>Login Page</summary>

![Login Page]()

- The Login page provides a standard authentication form.
- It includes options for social login (Google and Facebook) and matches the site's overall styling.

</details>

<details>
<summary>Register Page</summary>

![Register Page]()

- The Register page allows new users to sign up with email, username, and password (with confirmation).
- All fields are required, and the form is styled consistently with the rest of the site.

</details>

---

The following pages are available only to logged-in users:

<details>
<summary>Choose Subscription Page</summary>

![Choose Subscription]()

- This page presents a straightforward choice between different subscription durations (e.g., 1 month, 3 months, or yearly).
- Each option links directly to the Stripe subscription checkout page.

</details>

<details>
<summary>Subscription Success Page</summary>

![Subscription Success]()

- The Subscription Success page displays a confirmation message after a successful subscription purchase.
- It provides links to access premium video lessons and to manage subscription details through Stripe.

</details>

---

The following pages are accessible only to staff:

<details>
<summary>Add/Edit Product Pages</summary>

![Add/Edit Product]()

- These pages allow staff to add new pet training products or edit existing ones.
- The forms include preview functionality for product images and any associated media.

</details>

<details>
<summary>Product List Page</summary>

![Product List]()

- The Product List page displays all products in a sortable table.
- Table headers allow sorting by product name, category, price, or stock levels.
- Each row includes a delete option and links to the Edit Product page.

</details>

<details>
<summary>Order Detail Page</summary>

![Order Detail]()

- The Order Detail page shows comprehensive information about a particular order, including delivery details and order line items.
- It includes options for staff to mark an order as fulfilled and navigate back to the Order List page.

</details>


---
## Future Features

- It would be useful for staff to track the volume of sales for different pet training products over various timeframes. A dashboard, potentially built using Plotly, could display sales by product and period, providing valuable insights for inventory and marketing decisions.
- An added benefit for subscribers would be the ability to share videos of their pet training progress, with features to like and comment on each other’s posts. This community engagement tool would require moderation to ensure that feedback remains constructive and supportive.
- Another future feature under consideration is an embedded video-calling functionality. This would allow subscribers to connect with one another or even with professional pet trainers for live training sessions, tips, and advice. Unfortunately, due to time constraints, this feature was not implemented in the current version of the project.


---
[Return to top](#)
# User Experience

## Design

### Fonts 

The Roboto font is used throughout the project. Its a sleek simple style.

---


### Colour
The following colour palette was used in the project:

- **Deep Teal:** Conveys trust and reliability, used predominantly for headers and call-to-action elements.
- **Vibrant Orange:** Highlights special offers and key promotional elements, adding energy and drawing attention.
- **Soft Grey:** Provides a neutral backdrop for content areas, ensuring a clean and modern look.
- **Crisp White:** Used for contrast, helping text and images stand out.

These primary colours are derived from the project's hero image, which features a friendly pet in a dynamic training environment. The vibrant orange emphasizes special promotions, while deep teal and soft grey create an inviting, professional atmosphere throughout the site.

---


### Wireframes
#### _Product Display page_

![products_display wireframe]()

#### _Product Detail page_
![products_detail wireframe]()

#### _Basket page_
![checkout_page wireframe]()

#### _Checkout page_
![checkout_page wireframe]()

#### _Lessons page_
![checkout_page wireframe]()

[Return to top](#)

# Development Process

## Project Planning and Documentation in GitHub

For this project, GitHub Issues were used to document the development tasks and track progress through clearly defined user stories and epics. We created two issue templates—one for User Epics and one for User Stories—to ensure that all requirements were captured and prioritized. Various labels were employed to quickly identify issue types, including Bugs, User Epics, User Stories, and Style. We also used MoSCoW prioritisation with labels such as must-have, should-have, and could-have to focus on the most critical features first.

To break the project into manageable sprints, GitHub Projects was used to create a Kanban board where issues were moved from 'Todo' to 'In Progress' to 'Done' as they were completed. Below are the primary epics and their associated user stories:

### Epic 1: Dog Training Video Content
- **Story 1:** As a dog owner, I want to view a library of free training videos so I can quickly learn tips.
- **Story 2:** As a registered user, I want access to full-length training classes so I can learn in-depth techniques.
- **Story 3:** As a user, I want to bookmark my favorite videos so I can easily revisit them.

### Epic 2: Online Store
- **Story 1:** As a dog owner, I want to browse a store featuring treats, training gear, and accessories so I can purchase quality products.
- **Story 2:** As a shopper, I want to filter products by category (e.g., treats, toys, training aids) to quickly find what I need.
- **Story 3:** As a shopper, I want to view detailed product pages with images and descriptions so I can make informed purchasing decisions.
- **Story 4:** As a shopper, I want to add items to my basket and review them before checkout.
- **Story 5:** As a shopper, I want to securely complete purchases using an integrated Stripe payment system so my transactions are safe.
- **Story 6:** As a shopper, I want the option to save my shipping details for future orders to streamline repeat purchases.

### Epic 3: User Account & Authentication
- **Story 1:** As a visitor, I want to register for an account so I can access premium features.
- **Story 2:** As a registered user, I want to log in and manage my profile so my personal data and preferences are maintained.
- **Story 3:** As a user, I want to view my order history and class registrations for easy reference.

### Epic 4: User Experience & Navigation
- **Story 1:** As a user, I want a responsive website design so I can easily navigate on any device.
- **Story 2:** As a user, I want a clear navigation menu linking to training videos, classes, the store, and my account so I can quickly find what I need.
- **Story 3:** As a user, I want a search function to quickly locate videos and products that match my interests.
- **Story 4:** As a user, I want clear feedback on my actions (e.g., adding items to the basket) so I know that the system has responded.

### Epic 5: Marketing & SEO
- **Story 1:** As the site owner, I want to implement SEO best practices (meta tags, sitemap, robots.txt) so my site is easily discoverable.
- **Story 2:** As the site owner, I want to integrate a newsletter signup and social media links so I can engage my audience and boost brand presence.

### Epic 6: Admin & Content Management
- **Story 1:** As an admin, I want a backend interface to add or edit training videos, classes, and products so content is updated easily.
- **Story 2:** As an admin, I want to view a dashboard of orders and class registrations so I can monitor business performance.
- **Story 3:** As an admin, I want to receive alerts for low stock levels so I can replenish store inventory promptly.

This structured planning using GitHub Issues and Projects allowed us to clearly define the scope and priority of features, ensuring an organized development process from initial design through to final deployment.

## Search Engine Optimization
A set of long- and short-tail keywords was developed to target pet owners and training enthusiasts. The initial set was generated through brainstorming and by examining related searches on Google. This list was then refined to a smaller, more targeted set of keywords, which were each trialed on [wordtracker.com](https://wordtracker.com). The final list of terms, ordered by estimated search volume, is shown below:

| Term                      | Short/Long-tail | Volume  | Competition |
|---------------------------|-----------------|---------|-------------|
| Pet Training              | Short           | 180000  | 50.12       |
| Dog Training              | Short           | 90000   | 42.78       |
| Cat Training              | Short           | 30000   | 35.00       |
| Online pet training       | Long            | 22000   | 28.45       |
| Pet training tips         | Long            | 15000   | 30.25       |
| Dog obedience classes     | Long            | 12000   | 25.60       |
| Puppy training            | Short           | 11000   | 20.75       |
| Pet behavior advice       | Long            | 8000    | 18.30       |
| How to train your pet     | Long            | 6000    | 15.20       |
| Pet training shop         | Short           | 5000    | 22.10       |
| Affordable pet training   | Long            | 3000    | 10.50       |

After completing this research, I updated the project's templates as follows:

- **`<title>` tag in base.html:**  
  Set to *"Everything a pet owner needs – Pawsitive Training"*. This places a high-volume, short-tail keyword in one of the most important SEO locations while also including the site name.

- **`<meta>` description tag in base.html:**  
  Updated to:  
  *"Pets are more than just animals—they’re family. Join us at Pawsitive Training, where you can learn effective pet training techniques through our online pet training lessons. Discover a wide range of pet care products in our online shop."*  
  This description integrates several of the chosen keywords while keeping the description concise.

- **`<meta>` keywords in base.html:**  
  The following terms were added: pet training, dog training, cat training, pet training shop, online pet training.

- **Heading elements:**  
  - On the landing page (welcome.html), the `<h1>` element text was changed to *"For Pet Owners, by Pet Owners"* (shortened to *"For Pet Owners"* on smaller screens).  
  - On the product detail page, the product name appears as the content of the `<h2>` tag to reinforce keyword relevance.

- **`<img>` tag alt attributes:**  
  On the product display page, alt tags are set to *"Image of {{ product.name }}"* to help ensure that the product names are indexed by search engines.

- **Image filenames:**  
  Product image filenames were renamed to descriptively reflect the product, while training video lesson images are titled based on the pet training topics they cover.

- **Emphasized text:**  
  On the Checkout Success page, the words *"pet training lessons"* are wrapped in `<strong>` tags to highlight key services.


## Data Model
### Products App
![Entity-relationship diagram for models]()

### Checkout App
![Entity-relationship diagram for models]()

### Video_lessons App
![Entity-relationship diagram for models]()


---

## Data Validation

The following decimal fields, representing currency amounts, are protected by Django's `MinValueValidator`, ensuring that prices cannot be set below 0:

- `training.models.Subscription.price`
- `products.models.Product.price`

Additionally, the JavaScript in [basket/static/js/quantity_buttons.js](https://github.com/pac-dan/pawsitive_training/blob/main/basket/static/js/quantity_buttons.js) monitors the quantity input on the basket page. It disables the decrement button if the quantity is less than or equal to 1 and the increment button if the quantity is 10 or more. This script also prevents users from entering out-of-range values manually. This functionality was adapted from the Boutique Ado project.

---
---

# Testing
- Manual testing
- Validator testing
- User story testing
- Automated testing

---

## Manual Testing

### Feature Testing
Manual testing of the site’s features was carried out on a 1920 x 1080 desktop screen, a Samsung tablet, and an iPhone 12 Pro to ensure optimal functionality across devices.

<details>
<summary>Basket App</summary>

| Page                      | Feature                                              | Action                                                         | Effect                                                                 |
|---------------------------|------------------------------------------------------|----------------------------------------------------------------|------------------------------------------------------------------------|
| /basket/view_basket/      | All items appear in list                             | Add an item to the basket from the product detail page         | The added item appears in the basket table                           |
| /basket/view_basket/      | Correct item quantities                             | Add multiple items from the product detail page                | The correct number of items appears in the basket                      |
| /basket/view_basket/      | Increment button increases quantity                 | Click the increment button                                     | Quantity increases by 1                                                |
| /basket/view_basket/      | Decrement button decreases quantity                 | Click the decrement button                                     | Quantity decreases by 1                                                |
| /basket/view_basket/      | Minimum quantity enforced                            | Decrement quantity down to 1                                   | The decrement button becomes inactive at 1                           |
| /basket/view_basket/      | Maximum quantity enforced                            | Increment quantity up to 10                                    | The increment button becomes inactive at 10                          |
| /basket/view_basket/      | Smooth quantity changes without immediate reload     | Click increment and decrement buttons quickly                  | Buttons work responsively, with a brief delay before the page reloads   |
| /basket/view_basket/      | Confirmation message after quantity change           | Change quantity and wait a moment                              | Page reloads with a confirmation message showing the updated quantity  |
| /basket/view_basket/      | Removal of items from basket                         | Click the trash icon on an item                                | The item is removed from the basket                                  |
| /basket/view_basket/      | Display message when basket is empty                 | Navigate to the basket page without any items                  | A message indicates that the basket is empty                           |
| /basket/view_basket/      | Navigation back to shop                              | Click the shop link                                            | User is redirected to the products page                                |
| /basket/view_basket/      | Clear basket functionality                           | Click the 'clear all' link                                     | The basket is emptied and the user is redirected to the products page  |
| /basket/view_basket/      | Correct subtotal calculation                         | Add two products to the basket                                 | The subtotal equals the sum of the product prices                      |
| /basket/view_basket/      | Delivery charge conditions                           | Add a product and verify the appropriate delivery charge         | No delivery charge appears for training products; a standard charge applies for other items|
| /basket/view_basket/      | Consistent product pricing                           | Compare product price on product detail with that in the basket   | Prices match across pages                                              |
| /basket/view_basket/      | Checkout button functionality                        | Click the checkout button                                      | User is redirected to the Checkout page                                |
| /basket/view_basket/      | Direct input validation                              | Try entering an out-of-range quantity manually                   | The input value is automatically corrected to fall within the allowed range |
</details>

<details>
<summary>Products App</summary>

| Page              | Feature                                          | Action                                             | Effect                                                                                 |
|-------------------|--------------------------------------------------|----------------------------------------------------|----------------------------------------------------------------------------------------|
| /products/        | Product filtering by category                    | Click on a category link                           | Only products within the selected category are displayed                              |
| /products/        | Keyword search functionality                     | Enter a valid keyword in the search field          | Only matching products are shown, based on the search term                               |
| /products/        | Handling of invalid search queries               | Enter text that yields no matches                  | A 'no results' message is displayed                                                     |
| /products/        | Navigation to product detail page                | Click on a product card                            | User is redirected to the corresponding Product Detail page                             |
| /products/        | Out-of-stock indicator                           | Set a product's stock to 0 in the admin panel       | The product is greyed out and displays an out-of-stock badge                             |
| /product_detail/ | Product image, name, and full description display  | Navigate to a product detail page                  | The page displays a clear product image, full name, and detailed description             |
| /product_detail/ | Price and category display                       | Navigate to a product detail page                  | The correct price and category are displayed                                              |
| /product_detail/ | Out-of-stock handling on detail page             | View a product with 0 stock                         | A greyed-out banner appears and the add-to-basket option is hidden                         |
| /product_detail/ | Navigation back to shop                          | Click the "Back to Shop" button                    | User is redirected back to the Product Display page                                         |
| /product_detail/ | Incrementing basket quantity                     | Set a quantity and click the "Add to Basket" button  | The basket quantity is updated by the specified amount                                    |
| /product_detail/ | Navigation to basket                             | Click the "View Basket" button                     | User is taken to the Basket page                                                            |
| /product_detail/ | Audio clip playback (if available)               | Navigate to a product with an audio clip           | An audio player appears and the clip plays as expected                                  |
| /product_detail/ | Display of associated products                   | View a product with related items                   | Related products are displayed, complete with image, name, and price                         |
| /product_detail/ | Quick add option for associated products         | Click the quick add button on an associated product  | The product is added to the basket without navigating away                                  |
| /product_detail/ | Staff-only options                               | Log in as a staff member and view the product detail page | Staff-specific options are displayed (e.g., stock level display), while editing is managed via Django Admin |
</details>

<details>
<summary>Checkout App</summary>

| Page                           | Feature                                          | Action                                             | Effect                                                                               |
|--------------------------------|--------------------------------------------------|----------------------------------------------------|--------------------------------------------------------------------------------------|
| /checkout/                     | Pre-filled delivery details                      | If a UserOrderProfile exists, details auto-fill     | Delivery form is populated with stored user details                                 |
| /checkout/                     | Stripe payment integration                       | Proceed to checkout from the basket                | The Stripe payment form is displayed for secure transactions                          |
| /checkout/                     | Order summary display                            | Add items to basket and go to checkout             | An order summary displays item details, delivery charge, and total cost                |
| /checkout/                     | Navigation back to basket                        | Click the "View Basket" button                     | User is redirected to the Basket page                                                 |
| /checkout/                     | Order cancellation                                | Click the "Cancel Purchase" button                 | User is redirected back to the Product Display page, and the purchase is cancelled      |
| /checkout/                     | Stripe error handling                             | Enter invalid card details                         | Specific error messages appear beneath each input field                               |
| /checkout/                     | Disabling interactions during payment processing  | Click "Pay Now" with valid details                 | Interactive elements are temporarily disabled during the payment process              |
| /checkout/checkout_succeeded/  | Display of delivery details                      | Successfully complete a payment                    | Delivery details are summarized in a table on the success page                         |
| /checkout/checkout_succeeded/  | Order summary display                            | Successfully complete a payment                    | An order summary (including line items, delivery charge, and total) is displayed          |
| /checkout/checkout_succeeded/  | Navigation to video lessons                      | Click the "Video Lessons" button                   | User is redirected to the All Lessons page                                             |
| /checkout/staff_order_list/    | Comprehensive order listing                      | Navigate to the Staff Order List page              | Orders are listed in order based on payment and fulfillment status                       |
| /checkout/staff_order_detail/  | Detailed order information                       | Click an order in the list                         | The Order Detail page displays complete delivery and order line information              |
| /checkout/staff_order_detail/  | Order fulfillment update                         | Click "Mark as Fulfilled" (if applicable)          | Order is marked as fulfilled; note that this action is managed only in Django Admin      |
</details>

<details>
<summary>Welcome App and Navbar</summary>

| Page | Feature                                            | Action                                               | Effect                                                                  |
|------|----------------------------------------------------|------------------------------------------------------|-------------------------------------------------------------------------|
| /    | Hero image and title display                       | Navigate to the landing page                         | The hero image and title appear as designed                              |
| /    | Shop button navigation                             | Click the "Shop" button                              | User is redirected to the Products page                                 |
| /    | Subscribe button navigation                        | Click the "Subscribe" button                         | User is redirected to the Video Lessons page                             |
| /    | Logo functionality                                 | Click the logo                                       | The page reloads                                                         |
| /    | Search functionality                               | Enter text in the search bar and submit              | User is directed to the Products page with filtered results              |
| /    | Login status indicator                             | Log in as a user                                     | Navbar displays "logged in as {username}"                               |
| /    | Account dropdown options                           | Click the account dropdown                           | Login and Register links are displayed                                   |
| /    | Staff navigation                                   | Log in as a staff member                             | A staff dropdown appears with links to product stock levels and order management (accessible via Django Admin) |
| /    | Basket icon display                                | Add an item to the basket                            | Basket icon updates with current item count and total cost               |
</details>

<details>
<summary>Stock App</summary>

| Page                       | Feature                                          | Action                                             | Effect                                                                                   |
|----------------------------|--------------------------------------------------|----------------------------------------------------|------------------------------------------------------------------------------------------|
| /stock/                    | Product stock level display (staff only)         | Navigate to the stock management page (via Django Admin) | Staff can view current stock levels for products; adding or editing products is managed exclusively through Django Admin |
</details>

<details>
<summary>Video Lessons App</summary>

| Page                                  | Feature                                               | Action                                                    | Effect                                                                        |
|---------------------------------------|-------------------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------------------|
| /video_lessons/all_lessons/           | Display of all available lessons                       | Navigate to the All Lessons page                          | Lessons are displayed, categorized by course                                  |
| /video_lessons/all_lessons/           | Access control for lessons                             | Non-subscribers see only the first two lessons clickable   | Only the first two lessons are accessible; additional lessons are locked       |
| /video_lessons/all_lessons/           | Subscribe link visibility                              | View the lessons page as a non-subscriber                  | A subscribe link appears in the left panel, directing users to the subscription page |
| /video_lessons/video_player/          | Video playback functionality                           | Click on a lesson thumbnail                                | The video plays in the video player                                           |
| /video_lessons/video_player/          | Navigation controls                                    | Use the Previous/Next buttons                              | The appropriate lesson loads; navigation buttons disable at first/last lesson    |
| /video_lessons/subscription_success/   | Subscription confirmation                              | Complete a subscription process                          | A confirmation message is shown with links to premium content and account management |
</details>

---

### Responsiveness

All pages on the live site were tested using the default device presets in Chrome DevTools—covering desktop, tablet, and mobile views. Public-facing pages (such as the Welcome, Product Display, Product Detail, Basket, and Checkout pages) have been optimized for both portrait and landscape orientations to ensure a seamless user experience across all devices.

For staff-related sections (like the Product List and Order Detail pages, which are accessed via Django Admin), these pages display a large amount of tabular data. They are best viewed in landscape mode on smaller devices. A note is displayed on these pages when accessed from small screens in portrait mode to inform users of this limitation. While non-essential columns are hidden on medium-sized screens to improve readability, a minimum set of columns remains visible to ensure the pages remain functional. Given that these pages are intended for staff use rather than end consumers, this compromise is acceptable.

### Lighthouse


<details>
<summary>Lighthouse results by page</summary>

- Welcome Page

![welcome_page_lighthouse]()

- Product Display Page

![product display lighthouse]()

- Product Detail Page

![product detail lighthouse]()

- Basket Page

![basket lighthouse]()

- Checkout Page

![checkout lighthouse]()

- Checkout Success Page

![checkout success lighthouse]()

- All Video Lessons Page

![video lessons lighthouse]()

- Video Player Page

![video player lighthouse]()

- Subscription Success Page

![subscription success lighthouse]()

- Product List Page

![product list lighthouse]()

- Order List Page

![order list lighthouse]()

- Order Detail Page

![order detail lighthouse]()

- Login Page

![signin lighthouse]()

- Register Page 

![register lighthouse]()

</details>

---

### Code Validation

#### Python code : 

#### JavaScript code :

#### HTML Validation :

#### CSS Validation :

---
## Stripe Webhook Testing


### Stripe Payment Flow

For a more robust payment process, the application is designed to record orders and subscriptions in the database *before* initiating the Stripe payment process. A `payment_confirmed` flag is set to false by default when an order is created. This ensures that every purchase—whether for pet training products or training video subscriptions—is recorded before any network communication with Stripe begins.

The order's unique identifier is sent to Stripe as metadata, which allows the order to be accurately retrieved later without having to reconstruct it from the basket contents. When the Stripe payment process completes successfully (via the confirmPayment method called in `stripe_payments.js`), the front-end sends a POST request back to the server to update the corresponding order, setting the `payment_confirmed` flag to true.

If the payment process fails or the POST request encounters an error, the Stripe webhook event (`stripe.payment_intent.succeeded`) is used as a fallback. The webhook handler checks for the corresponding order in the database and, if found, ensures the `payment_confirmed` flag is updated. If no matching order is found, the handler can reconstruct the order using the basket information included in the metadata, serving as an insurance policy.

This approach offers the added advantage that any orders whose payments are not processed remain in the system, allowing staff and users to review or follow up on these transactions later (although this follow-up functionality is not implemented in the current version of the project).

### Webhook Tests

The pawsitive_training project listens for several key Stripe webhook events to ensure that all payment transactions—both for product orders and training lesson subscriptions—are accurately recorded. Our payment flow is designed to create orders in the database before the Stripe payment process begins, with a `payment_confirmed` flag set to false. Essential metadata (such as an order number) is sent to Stripe so that, upon successful payment, the webhook events can update the corresponding record in our database. Manual tests were conducted by forwarding webhook events to a local listener on port 8000. (Note: the webhook for the deployed Heroku app was temporarily disabled during testing since both environments share the same database.)

- **stripe.payment_intent.succeeded:**  
  The webhook handler retrieves the order number from the event metadata and confirms that the corresponding order exists. If it does, the handler updates the order record, setting `payment_confirmed` to true. This was tested by temporarily disabling the view that normally sets this flag, then verifying via the admin panel that after a successful payment, the order’s `payment_confirmed` flag was correctly updated.

- **stripe.payment_intent.payment_failed:**  
  This handler simply acknowledges the event by returning an HTTP 200 response to Stripe, confirming receipt of the event even though no changes are made to the order.

- **stripe.checkout.session.completed:**  
  This webhook is critical for our subscription service. When a user subscribes to access full-length pet training video lessons, the handler checks the corresponding subscription record (e.g., in a UserOrderProfile or similar model) and ensures that the `subscriber` flag is set to true. It also verifies that `stripe_customer_id` and `stripe_subscription_id` are populated correctly based on the metadata. Tests confirmed that when webhook forwarding is enabled, these fields are updated as expected after a successful subscription payment.

- **stripe.invoice_paid:**  
  This event triggers the handler to update the subscription status for a user. Upon receiving this event, the handler sets the `subscription_paid` flag to true, activating full access to premium training video content. Tests confirmed that the flag was correctly updated in the database when this webhook was received.

- **stripe.invoice.payment_failed:**  
  In the event that an invoice payment fails, the handler updates the subscription record by setting the `subscription_paid` flag to false, thereby revoking access to premium content. Although this webhook is more challenging to test (requiring a test card with a short expiration date), initial tests in Stripe’s test environment indicate that the handler behaves as expected.

Through these webhook handlers, the pawsitive_training project ensures that any changes in payment status reported by Stripe are accurately and reliably reflected in our order and subscription records.


---


## Automated Testing

### Testing django views, models and forms.


[Return to top](#)

---
---

# Bugs
    
## Remaining Bugs


[Return to top](#)

---
---

# Libraries and Programs Used

---
---

# Deployment

## Using an AWS S3 Bucket for Static and Media Storage

The pawsitive_training project stores all of its static and media files—such as images (for products and training content) and any audio clips uploaded by staff—in an AWS S3 bucket. Using S3 ensures that these files are persistently stored and can be efficiently delivered to users regardless of dyno restarts or new deployments. Detailed instructions on setting up and configuring an S3 bucket can be found [here](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3).

On the Django side, the following configuration in your `settings.py` is necessary to integrate with S3:

python
AWS_STORAGE_BUCKET_NAME = 'daaansawsbucket'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Static and Media files settings
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATICFILES_LOCATION = 'static'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
MEDIAFILES_LOCATION = 'media'

# Override static and media URLs in production
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'


## Deploying the App on Heroku

1. **Log into Heroku:**  
   Navigate to the Heroku Dashboard and click on the **New** button.

2. **Create a New App:**  
   - Choose a unique app name (e.g., `pawsitive-app`) and select the region closest to you.

3. **Set Up a Database:**  
   - Go to the **Resources** tab.
   - Click the **Find more add-ons** button.
   - Search for and select **Heroku Postgres**; then click **Install Heroku Postgres**.
   - Choose a plan (the default Mini plan at $5.00/month is sufficient for most cases) and link it to your app.
   - Return to the **Resources** tab, click the Heroku Postgres icon, then open the **Settings** tab and click on **Database Credentials**.
   - Copy the provided URI and paste it into your `env.py` file under the key `DATABASE_URL`. This ensures you use the same database for both development and production.

4. **Configure Environment Variables:**  
   - In the **Settings** tab on the Dashboard, click **Reveal Config Vars**.
   - Your database URL should be auto-populated. Add your Django secret key and set the `PORT` variable to `8000`.

5. **Add a Procfile:**  
   - In your local repository, create a file named `Procfile` in the root directory.
   - Add the following line:
     ```
     web: gunicorn pawsitive.wsgi
     ```

6. **Update Django Settings:**  
   - Add your Heroku project URL to the `ALLOWED_HOSTS` list in your `settings.py`.

7. **Set Up Social Authentication:**  
   - Create two social apps for Facebook and Google sign-in.
   - Add the respective API keys and secrets to your database.
   - Update the application details and callback URLs on the Google and Facebook OAuth dashboards.

8. **Configure Stripe (for payments, if applicable):**  
   - Open a Stripe account and add your `STRIPE_PRIVATE_KEY` and `STRIPE_SECRET` to the Heroku config vars.
   - Set up a webhook to target your designated endpoint, and copy the `STRIPE_WEBHOOK_SECRET` to the config vars.
   - (Optional) Create three products in the Stripe Developer console to match the subscription durations offered in Pawsitive, and link their API keys to the corresponding subscription instances in the database.

9. **Prepare for Deployment:**  
   - Set `DEBUG` to `False` in your settings.
   - Commit your changes and push them to GitHub.

10. **Configure Heroku Buildpacks and Deployment:**  
    - In Heroku, navigate to the **Settings** tab and scroll to the **Buildpacks** section.
    - Click **Add Buildpack**, select the Python buildpack, and save the changes.
    - Go to the **Deploy** tab, select the GitHub icon under **Deployment Method** to connect your GitHub repository.
    - Enter your repository name (e.g., `yourusername/pawsitive`), click **Search**, and then click **Connect** when your repo appears.
    - Under **Manual deploy**, click **Deploy Branch**.  
      You should see a confirmation message such as "Your app was successfully deployed." Click **View** to open the app in your browser.


## Making a local clone

1. Open a terminal or command prompt on your local machine.
2. Navigate to the directory where you want to clone the project.
3. Enter the following command: 'git clone https://github.com/pac-dan/pawsitive.git'


## Running the app in your local environment

1. Create a virtual enviroment in the new project folder using the command `python3 -m venv venv`
2. Activate the virtual environment : `source venv/bin/activate`
3. Install the project requirements : `pip3 install -r requirements.txt`
4. Create an env.py file containing the following variables (see env.example.py in the root directory of the project for a complete list of variables necessary to run the app) :
    - AWS_ACCESS_KEY_ID : Used to access S3 bucket for static and media files
    - AWS_SECRET_ACCESS_KEY : As above
    - BASE_URL : The root URL for the dev project, usually `http://localhost:8000/`
    - DATBASE_URL : This is the url generated by Heroku - see [Deploying the app](#deploying-the-app-on-heroku)
    - DEBUG : Set to True for development work locally
    - EMAIL_APP_PASSWORD : The email password for your email account
    - EMAIL_APP_USER : A personal or ephemeral email account you can use to test your email functionality.
    - PORT : Default Django port is 8000.
    - SECRET_KEY : This is the Django secret key.
    - STRIPE_PRIVATE_KEY : Stripe private key credential
    - STRIPE_PUBLIC_KEY : Stripe public key credential
    - STRIPE_WEBHOOK_SECRET : Stripe webhook signing secret


[Return to top](#)

---
---

# Credits


# Acknowledgements


[Return to top](#)