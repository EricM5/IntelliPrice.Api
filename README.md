# IntelliPrice.Api
<p align="center">
  <img src="https://user-images.githubusercontent.com/76453820/184288411-d544fb1e-615f-4812-993c-ee37e67857b6.png">
</p>

BaseURL: https://intelli-price.herokuapp.com/

**Get All Products**
----
  Returns 60+ products from Google Shopping for given search term, specified in parameter. Returns list of products in ascending order by total price with shipping cost factored in.

* **URL**

  /getall/{searchterm}

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `searchterm=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```json
    [
      {
        "Title": "string",
        "Price": "string",
        "Shipping": "string",
        "TotalPrice": "string",
        "Seller": "string",
        "url": "https:/producturlfoundhere.com"
      },
      {
        "Title": "string",
        "Price": "string",
        "Shipping": "string",
        "TotalPrice": "string",
        "Seller": "string",
        "url": "https:/producturlfoundhere.com"
      },
    ]
    ```
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
    ```
    []
    ```

* **Sample Call:**

  ```python
    import requests

    querysearchterm = "San Jose Sharks Jersey"
    response = requests.get("https://intelli-price.herokuapp.com/getall/" + querysearchterm)

    print(response)

    listofproducts = response.json()

    lowestpricedproduct = listofproducts[0]
    highestpricedproduct = listofproducts[-1]
  ```
