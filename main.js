let products = null;
let categories = null;
let title = null;

// Called once the page has loaded
document.addEventListener("DOMContentLoaded", function (event) {
  loadProducts();
  loadCategories();
});

const DUMMY_PRODUCTS = [
  {
    name: "Sheety",
    shortDescription: "Turn any Google Sheet into an API",
    website: "https://www.sheety.co",
    votes: 100,
    iconUrl: "https://sheety.co/icon.png",
    category: "Web",
    id: 2,
  },
];

const DUMMY_CATEGORIES = [
  {
    name: "Box Score",
    id: 1,
  },
  {
    name: "Play-by-Play",
    id: 2,
  },
  {
    name: "Team Stats",
    id: 3,
  },
];

// Replace this with your Sheety URL
// Make sure NOT to include the sheet name in the URL (just the project name!)
// var projectUrl =
//   "https://api.sheety.co/e1cfbe6d472149b2a7874ea91d598f72/statify";

function loadProducts() {
  this.products = DUMMY_PRODUCTS.sort((a, b) => {
    return a.votes < b.votes;
  });
  showAllProducts();

  //   fetch(projectUrl + "/products")
  //     .then((response) => response.json())
  //     .then((json) => {
  //       this.products = json.products.sort((a, b) => {
  //         return a.votes < b.votes;
  //       });
  //       showAllProducts();
  //     });
}

function loadCategories() {
  this.categories = DUMMY_PRODUCTS.length > 0 ? DUMMY_CATEGORIES : [];
  drawCategories();
  //   fetch(projectUrl + "/categories")
  //     .then((response) => response.json())
  //     .then((json) => {
  //       this.categories = json.categories;
  //       drawCategories();
  //     });
}

function drawProducts(products) {
  const template = Handlebars.compile(
    document.getElementById("products-template").innerHTML
  );
  document.getElementById("products-container").innerHTML = template({
    title: this.title,
    products: products,
  });
}

function drawCategories() {
  const template = Handlebars.compile(
    document.getElementById("menu-template").innerHTML
  );
  console.log("draw ", this.products);
  document.getElementById("menu-container").innerHTML = template(
    this.categories
  );
}

function showAllProducts() {
  this.title = "All Games";
  drawProducts(this.products);
}

function showCategory(category) {
  this.title = category;
  const filteredProducts = this.products.filter((product) => {
    return product.category == category;
  });
  drawProducts(filteredProducts);
}

function upvoteProduct(id) {
  const product = this.products.find((product) => {
    return product.id == id;
  });
  product.votes = product.votes + 1;
  product.hasVoted = true;

  //   let headers = new Headers();
  //   headers.set("content-type", "application/json");
  //   fetch(projectUrl + "/products/" + id, {
  //     method: "PUT",
  //     body: JSON.stringify({ product: product }),
  //     headers: headers,
  //   });

  showAllProducts();
}
