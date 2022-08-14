# IntelliPrice.Api
<p align="center">
  <img src="https://user-images.githubusercontent.com/76453820/184288411-d544fb1e-615f-4812-993c-ee37e67857b6.png">
</p>

BaseURL: https://intelli-price.herokuapp.com/

**Get All Products**
----
  Returns list of products for given search term.

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
    `[ {"Title": string,"Price": string,"Shipping":string,"TotalPrice":string,"Seller":string,"url":string} ]`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `[]`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/users/1",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```
