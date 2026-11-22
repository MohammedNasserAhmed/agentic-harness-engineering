
const addButton = document.querySelector("#add-book");
const bookList = document.querySelector("#book-list");

let bookNumber = 1;

addButton.addEventListener("click", () => {
  const item = document.createElement("li");
  item.textContent = `Book #${bookNumber} added to the library`;
  bookList.appendChild(item);
  bookNumber++;
});

