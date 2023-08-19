# real-estate-management
The "Real Estate Management" module is developed to manage real estate properties within the Odoo platform. This module allows users to create, manage, and track real estate properties, their details, offers, and status.

## Features

- Create, edit, and view real estate property listings.
- Track property details such as title, description, and price.
- Manage property offers and keep track of the best offer.
- Define property types and assign them to properties.
- Manage property tags for better categorization.
- Monitor the status of properties through different stages (e.g., New, Offer Received, Sold, etc.).
- Assign salespersons and buyers to properties.
- Handle property cancellation and sale actions with appropriate constraints.

## Version

The current version of the module is 1.0.

## Environment

- Odoo version: 16.0
- Python version: 3.10
- Operating System: Ubuntu 64-bit

## Installation and Setup

1. Firstly I Cloned the repository to my local machine through following command:

git clone https://github.com/annshah0/real-estate-management

2. Then I installed the required Python packages:

pip install -r requirements.txt

3. I set up my Odoo development environment through provided guidance

4. Added the "Real Estate Management" module to my Odoo addons path.

5. Updated the Odoo addons list to include the new module.

6. Run the Odoo server using the following command:

odoo-bin -c /home/quratulain/programming/env/realestate_management/config/real_estate.conf 

7. Accessed the Odoo web interface and navigated to the "Real Estate Management" module.

## Configuration

- Configured user groups and access rights to control user access to the module's features.

## Usage

- Created and managed real estate properties through the provided interface.
- Utilized different views (list view, form view) to interact with property data.
- Managed property offers and track the best offer for each property.
- Monitored the status of properties and update them as they progress through different stages.
