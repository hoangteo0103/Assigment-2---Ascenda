# Hotel Data Integration Project

This project is designed to fetch, merge, and clean data from multiple hotel suppliers. It integrates various sources into a unified format that provides enriched and consistent hotel information.

## 1. Project Structure

The structure of the project is outlined below, providing a clear view of the main components and their organization:

```
├── main.py # Entry point for running the hotel data integration process.
├── README.md # Documentation describing the project setup and usage.
├── requirements.txt # List of dependencies required by the project.
├── runner.sh # Bash script for running the application with predefined arguments.
├── tree.txt # Text representation of the project directory structure.
├── config/ # Configuration files and settings for the project.
│ ├── amenities_config.json # Configuration for mapping and categorizing hotel amenities.
│ ├── config.py # Load amenities_config and supplier_config from json file to use in code.
│ ├── suppliers_config.json # Configuration for hotel data suppliers.
├── src/ # Source code for the project.
│ ├── **init**.py # Makes src a Python package.
│ ├── data_integration/ # Components responsible for data fetching and integration.
│ │ ├── acme_supplier.py # Integration logic specific to the Acme supplier.
│ │ ├── base_supplier.py # Base class for creating supplier-specific integrations.
│ │ ├── data_merger.py # Logic for merging data from different suppliers.
│ │ ├── paperflies_supplier.py # Integration logic for the Paperflies supplier.
│ │ ├── patagonia_supplier.py # Integration logic for the Patagonia supplier.
│ │ ├── supplier_manager.py # Manages fetching and merging of data from suppliers.
│ │ ├── **init**.py # Makes data_integration a Python package.
├ │ ├── parser.py # Contain parsing functions for amenities, images, complex fields.
│ ├── models/ # Data models used in the project.
│ │ ├── hotel.py # Defines the data class for hotel.
│ │ ├── **init**.py # Makes models a Python package.
├── tests/ # Unit tests for the project.
│ ├── test_app.py # Tests for the application logic.
│ ├── test_data_merger.py # Tests for data merging functionalities.
│ ├── **init**.py # Makes tests a Python package.
```

## 2. Config for mapping data from multiple supplier

The project utilizes a configuration-driven approach to handle the differences in data formats and fields provided by various hotel data suppliers. This configuration ensures that the data integration process is flexible and easily adaptable to changes from the suppliers.

### Supplier Configuration

The **suppliers_config.json** file defines the mappings and endpoints for each supplier. This file is crucial as it abstracts the data fetching layer from the data processing layer, allowing the integration logic to remain consistent even when supplier APIs change.

#### Details of the Configuration:

- Endpoints: Each supplier has a unique API endpoint from which data is fetched.
- Field Mappings: Since each supplier may use different field names for the same type of information (e.g., hotel ID, name, or amenities), these mappings ensure that our application can understand which fields to pull from each API response.

### Amenities Configuration

The **amenities_config.json** file provides a structured categorization of amenities into **"general"** and **"room"** categories. This categorization helps in unifying and standardizing the amenities data from different suppliers, which might list them in various formats.

### Data Parsing

#### Simplified Data Parsing with BaseSupplier

The project utilizes a BaseSupplier class to standardize and simplify the data fetching and parsing process for multiple hotel data suppliers. Each specific supplier class inherits from BaseSupplier and needs only to specify a supplier_key. This key is used to fetch the appropriate configuration for endpoints and data field mappings from a centralized JSON configuration file.

##### Implementation of BaseSupplier

###### Core Functionality(data_integration/base_supplier.py):

- Endpoint Configuration: The **supplier_key** unique to each supplier subclass is used to access its specific configuration in the suppliers_config.json. This includes the API endpoint and the necessary field mappings to parse the JSON data correctly.
- Fetching Data: The **fetch()** method in BaseSupplier manages API requests to the supplier’s endpoint. It handles HTTP responses and errors uniformly across different suppliers.
- Generic Parsing Logic: The parse() method, implemented in the BaseSupplier, uses the configurations loaded based on the **supplier_key** to dynamically parse the JSON response into a structured Hotel object. It leverages helper functions like **parse_generic_field()**, **parse_amenities()**, and **parse_images()** to handle specific segments of the data according to the mappings defined in the configuration.

The application employs a modular approach to parse data fetched from different hotel suppliers. Each supplier's data format is mapped using a flexible configuration strategy, ensuring easy adaptation to changes in supplier data structures without modifying the core parsing logic. All the parsing logic is in **utils.py**

#### Key Functions in the Parsing Process:

- **parse(self, dto) -> Hotel**: This method interprets the raw data object (dto) from each supplier according to the mappings defined in suppliers_config.json. It utilizes helper functions to handle specific data segments such as location, amenities, and images.
- **parse_generic_field(data, field_config)**: This function extracts and processes complex nested data structures based on a provided configuration. It allows for detailed nested mappings like those used for the location fields.
- **parse_amenities(amenities)**: Specialized to categorize amenities into 'general' and 'room' based on predefined lists (GENERAL_AMENITIES, ROOM_AMENITIES). This ensures consistent categorization across different suppliers who might have disparate ways of listing amenities.
- **parse_images(image_data, config)**: Handles the parsing of image data, ensuring that images are categorized into 'rooms', 'site', and 'amenities' as per the configurations. This method standardizes the image data structure which can vary significantly between suppliers.

## 3. Merging Strategy for Hotel Data

The project employs a strategic merging approach to consolidate data from multiple hotel suppliers, ensuring that each hotel's record is as comprehensive and accurate as possible. This strategy is designed to handle differences and overlaps in the attributes provided by various sources.

### Overview of Merging Logic

The data merging process is implemented in the data_merger.py module, where multiple entries for the same hotel (identified by hotel ID) from different suppliers are merged into a single entry. The strategy prioritizes completeness and uses the best available information for each attribute.

### Key Aspects of the Merging Process:

- **Name**: Get the longest length string to use as a unique name.
- **Description**: Concatenates descriptions from all sources to provide a comprehensive narrative. This ensures that no descriptive information is lost and that potential guests receive a full understanding of what the hotel offers.
- **Location**: Merges location information by preferring the most complete and detailed entry. If one source provides more detailed geographic coordinates or address information(longer length), that detail is retained in the merged record.
- **Amenities**: Combines amenities listed by all sources, deduplicating them to avoid repetition. This approach ensures that all unique amenities are represented without clutter.
- **Images**: Merges images by ensuring that duplicates (based on the image URL) are removed. This maintains a diverse visual representation of the hotel without redundancy.
- **Booking Conditions**: Consolidates all unique booking conditions provided by different sources to give a complete set of policies.
